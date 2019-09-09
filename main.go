package main

import (
	"fmt"
	"github.com/tatsushid/go-fastping"
	"net"
	"os"
	"time"
)

var (
	threeSeconds = 3000000000
)

func main() {
	ping("Gordon's phone", "192.168.1.216")
	ping("Dad's phone", "192.168.1.214")
	ping("Mum's phone", "192.168.1.30")
	ping("Vicki's phone", "192.168.1.202")
	ping("Titi's phone", "192.168.1.50")
}

func ping(name string, host string) {
	pingPing := fastping.NewPinger()
	pingPing.MaxRTT = time.Duration(threeSeconds)

	ra, err := net.ResolveIPAddr("ip4:icmp", host)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	pingPing.AddIPAddr(ra)
	pingPing.OnRecv = func(addr *net.IPAddr, duration time.Duration) {
		fmt.Println(name, "is active")
	}

	pingPing.OnIdle = func() {
	}
	err = pingPing.Run()
	if err != nil {
		fmt.Println(err)
		os.Exit(2)
	}
}
