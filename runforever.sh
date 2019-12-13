#!/bin/bash
#2019-10-29:	v1.0.2
#2019-11-08:	v1.0.3

if [ $# -lt 1 ] ; then 
	echo "USAGE: $0 command line" 
	echo " e.g.: $0 python abc.py" 
	exit 1; 
fi 
#echo $#
#echo $$
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

filename=`basename $0`

function watch()
{
	while true; do
		#echo $*
		server=`ps -ef | grep "$*" | grep -v grep | grep -v "$filename"`
		if [ ! "$server" ]; then
			#如果不存在就重新启动
			#nohup ./  .. >/dev/null 2>&1 &
			#echo "start"
	        logger -p local3.info "runforever start $*"
	        #echo "start $*"
			setsid $* >/dev/null 2>&1 </dev/null &
	        sleep 1
		fi
		#每次循环沉睡10s
		sleep 1
	done
}

watch $* >/dev/null 2>&1 </dev/null &
#watch $* 