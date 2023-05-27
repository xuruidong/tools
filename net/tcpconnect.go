// tcpecho
package main

import (
    "fmt"
    "net"
    "os"
    "time"
    "strconv"
)

func handleConn(ip string, port string) {
	conn, err := net.Dial("tcp", ip + ":" + port)
    if err != nil {
        fmt.Println("err : ", err)
        return
    }
    defer conn.Close() // 关闭TCP连接
    for {
        buf := [512]byte{}
        n, err := conn.Read(buf[:])
        if err != nil {
            fmt.Println("recv failed, err:", err)
            return
        }
        fmt.Println(string(buf[:n]))
    }
}
// TCP 客户端
func main() {
	if len(os.Args) < 4 {
		fmt.Println("Usage:<command> <ip> <port> <connection-number>")
		return
	}
	ip := os.Args[1]
	port := os.Args[2]
	conn_str := os.Args[3]
	conn_num, err := strconv.Atoi(conn_str)
	if err != nil {
		fmt.Println("invalid paramter: connection-number, ", err)
		return
	}
	
    for i := 0; i <= conn_num; i++ {
    	go handleConn(ip, port)
    	fmt.Println("connect ", i)
    }
    time.Sleep(60 * time.Second) 
}
