// udp_sender
package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
)

func main() {

	if len(os.Args) < 3 {
		fmt.Printf("Usage: %s ip port\n", os.Args[0])
		os.Exit(1)
	}

	conn, err := net.Dial("udp", os.Args[1]+":"+os.Args[2])
	if err != nil {
		fmt.Println("net.Dial err:", err)
		return
	}
	defer conn.Close()

	go func() {
		n2z := [...]int{1, 10, 100, 1000, 10000}
		str := make([]byte, 1024)
		out_str := make([]byte, 10240)
		offset := 0
		for {

			n, err := os.Stdin.Read(str) //从键盘读取内容， 放在str
			if err != nil {
				fmt.Println("os.Stdin. err1 = ", err)
				return
			}
			/*
				var n int
				fmt.Scanf("%d", &n)

				if n <= 0 {
					fmt.Println("Input a number")
					continue
				}
				fmt.Println("send ", n)
				str := strconv.Itoa(n)
				n = len(str)
			*/
			switch str[0] {
			case '\r', '\n':
				continue
			}

			n_str := strings.Replace(string(str[:n]), "\r", "", -1)
			n_str = strings.Replace(n_str, "\n", "", -1)
			n_str = strings.Replace(n_str, " ", "", -1)
			n_str = strings.Replace(n_str, "\t", "", -1)

			num, err := strconv.Atoi(n_str)
			if err != nil {
				fmt.Println("Input error ", err)
				fmt.Println("Please input a number")
				continue
			}
			fmt.Println("send ", num)
			n = len(n_str)

			offset = 0
			//str = []byte(n_str)
			for si := n; si > 0; si-- {
				//fmt.Println("si=", si)
				//fmt.Println("str[n-si]=", str[n-si])
				//fmt.Println("int str[n-si]=", int(str[n-si]))
				if int(n_str[n-si]-0x30) >= 10 {
					fmt.Println("error ", n_str[n-si])
					break
				}
				for i := 0; i < int(n_str[n-si]-0x30); i++ {

					for j := 0; j < n2z[si-1]; j++ {
						out_str[offset] = byte(i + 0x31)
						offset++
						//fmt.Printf("%d ", offset)
					}
				}
			}
			//fmt.Println(string(out_str[:offset]))
			conn.Write(out_str[:offset]) // 给服务器发送
		}
	}()

	buf := make([]byte, 10240)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Println("conn.Read err:", err)
			return
		}
		fmt.Println("recv ", n, ": ", string(buf[:n]))
	}
}
