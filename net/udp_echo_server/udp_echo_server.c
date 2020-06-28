#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>


#define STRSIZE		40

struct msg_st{
	char data[1024];
};

int main(int argc, char *argv[])
{
	int sd;
	struct msg_st rbuf;
	struct sockaddr_in laddr,raddr;
	socklen_t raddr_len;
	char ipstr[STRSIZE];
	ssize_t recv_len = 0;

	unsigned short lport = 1025;
	if (argc > 1){
		int p = atoi(argv[1]);
		
		if (p > 65535 || p == 0){
			printf("local port set error\n");
			exit(1);
		}
		lport = p;
	}
	
	sd = socket(AF_INET,SOCK_DGRAM,0/*IPPROTO_UDP*/);
	if(sd < 0)
	{
		perror("socket()");
		exit(1);
	}

	laddr.sin_family = AF_INET;
	laddr.sin_port = htons(lport);
	inet_pton(AF_INET,"0.0.0.0",&laddr.sin_addr);
	// addr.sin_addr.s_addr = INADDR_ANY; 
	if(bind(sd,(void *)&laddr,sizeof(laddr)) < 0)
	{
		perror("bind()");
		exit(1);
	}

	printf("bind at 0.0.0.0:%u\n", lport);
	raddr_len = sizeof(raddr);

	while(1)
	{
		recv_len = recvfrom(sd,&rbuf,sizeof(rbuf),0,(void *)&raddr,&raddr_len);
		if(recv_len < 0){
			perror("recvfrom()");
			exit(1);
		}
		rbuf.data[recv_len] = 0;
		inet_ntop(AF_INET,&raddr.sin_addr,ipstr,STRSIZE);
		printf("--MESSAGE FROME:%s:%d--\n",ipstr,ntohs(raddr.sin_port));
		printf("recv len: %d, recv data : %s\n",recv_len, rbuf.data);

		if(sendto(sd, &rbuf, recv_len, 0, (void *)&raddr, raddr_len) < 0){
			perror("sendto()");
			exit(1);
		}
	}

	close(sd);

	exit(0);
}

