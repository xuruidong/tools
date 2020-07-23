// tcpecho
package main

import (
	"fmt"
	"io"
	"net"
	"os"
)

const BUFF_SIZE = 1024

var buff = make([]byte, BUFF_SIZE)

// 接受一个TCPConn处理内容
func handleConn(tcpConn *net.TCPConn) {
	if tcpConn == nil {
		return
	}
	defer tcpConn.Close()
	for {
		n, err := tcpConn.Read(buff)
		if err == io.EOF {
			fmt.Printf("The RemoteAddr:%s is closed!\n", tcpConn.RemoteAddr().String())
			return
		}
		n2 := handleError(err)
		if n2 != 0 {
			return
		}
		if string(buff[:n]) == "exit" {
			fmt.Printf("The client:%s has exited\n", tcpConn.RemoteAddr().String())
		}
		if n > 0 {
			fmt.Printf("Read:%s", string(buff[:n]))
		}
		n, err = tcpConn.Write(buff[:n])
	}
}

// 错误处理
func handleError(err error) int {
	if err == nil {
		return 0
	}
	fmt.Printf("error:%s\n", err.Error())
	return 1
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage:<command> <port>")
		return
	}
	port := os.Args[1]
	tcpAddr, err := net.ResolveTCPAddr("tcp4", "0.0.0.0:"+port)
	handleError(err)
	tcpListener, err := net.ListenTCP("tcp4", tcpAddr) //监听
	handleError(err)
	defer tcpListener.Close()
	for {
		tcpConn, err := tcpListener.AcceptTCP()
		fmt.Printf("The client:%s has connected!\n", tcpConn.RemoteAddr().String())
		handleError(err)

		go handleConn(tcpConn) //起一个goroutine处理
	}
}
