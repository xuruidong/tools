#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <unistd.h>


int main(int argc,char **argv)
{
	int map[] = {1, 10, 100, 1000, 10000};
	int sd;
	char *sbuf = NULL;
	struct sockaddr_in raddr;

	if(argc < 4)
	{
		fprintf(stderr,"Usage: %s ip port data_size\n", argv[0]);
		exit(1);
	}

	sd = socket(AF_INET,SOCK_DGRAM,0);
    if(sd < 0)
    {
        perror("socket()");
        exit(1);
    }

    int size = atoi(argv[3]);
    sbuf = (char *)malloc(size+1);
	memset(sbuf,'\0',size+1);

	if(size>=100000){
		printf("big size\n");
		exit(0);
	}

	const char *p = argv[3];
	size_t slen = strlen(argv[3]);
	size_t si = slen;
	int i=0, j=0;
	int offset = 0;
	for(;si>0; si--){
		
		for(i=0; i<p[slen-si] - 0x30; i++){
			for(j=0; j<map[si-1]; j++){
				sbuf[offset++] = i+0x31;
			}
		}

	}
	printf("%s\n", sbuf);
	

	printf("size=%d, %s\n", size, sbuf);
	raddr.sin_family = AF_INET;
	raddr.sin_port = htons(atoi(argv[2]));
	inet_pton(AF_INET,argv[1],&raddr.sin_addr);

    if(sendto(sd,sbuf, size,0,(void *)&raddr,sizeof(raddr)) < 0)
	{
		perror("sendto()");
		exit(1);
	}

	puts("ok!");

	free(sbuf);
    close(sd);

    exit(0);
}




