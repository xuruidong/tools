#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <errno.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

#define SERVERPORT	9995
#define BUFSIZE		10240
#define STRSIZE		40

static void server_job(int sd)
{
	char buf[BUFSIZE];
	int len;
	size_t ret = 0;

	while(1) {
		ret = recv(sd, buf, STRSIZE, 0);
		if(ret < 0) {
			perror("recv");
			continue;
		}
		else if(ret == 0) {
			printf("recv ret==0\n");
			break;
		}
		printf("recv %s\n", buf);
		if(strncmp(buf, "quit", 4) == 0) {
			break;
		}
		len = sprintf(buf, "%lld\r\n",(long long)time(NULL));

		if(send(sd,buf,len,0) < 0)
		{
			perror("send()");
			exit(1);
		}
	}

	return ;
}

int main()
{
	int sd,newsd;	
	struct sockaddr_in laddr,raddr;
	socklen_t raddr_len;
	char ipstr[STRSIZE];

	sd = socket(AF_INET,SOCK_STREAM,0/*IPPROTO_TCP,IPPROTO_SCTP*/);
	if(sd < 0)
	{
		perror("socket()");
		exit(1);
	}


	int val = 1;
	if(setsockopt(sd,SOL_SOCKET,SO_REUSEADDR,&val,sizeof(val)) < 0)
	{
		perror("setsockopt()");
		exit(1);
	}


	laddr.sin_family = AF_INET;
	laddr.sin_port = htons(SERVERPORT);
	inet_pton(AF_INET,"0.0.0.0",&laddr.sin_addr.s_addr);
	
	if(bind(sd,(void *)&laddr,sizeof(laddr)) < 0)
	{
		perror("bind()");
		exit(1);
	}

	if(listen(sd,100) < 0)
	{
		perror("listen()");
		exit(1);
	}

	raddr_len = sizeof(raddr);

	while(1)
	{
		newsd = accept(sd,(void *)&raddr,&raddr_len);
		if(newsd < 0)
		{
			if(errno == EINTR)
				continue;
			perror("accept()");
			exit(1);
		}
		inet_ntop(AF_INET,&raddr.sin_addr,ipstr,STRSIZE);
		printf("Client:%s:%d\n",ipstr,ntohs(raddr.sin_port));
		server_job(newsd);
		close(newsd);
	}

	close(sd);

	exit(0);
}


