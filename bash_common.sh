#!/bin/bash

function config_load()
{
	CONFIG_FILE=$1
	if [ -e $CONFIG_FILE ]; then
		while read line;
		do
		    eval "$line"
		    if [ $? != 0 ];then
		    	echo "read configure error"
		    	return 1
		    fi
		done < $CONFIG_FILE
	else
		echo "$CONFIG_FILE is not exist"
		return 2
	fi
}

# from https://blog.csdn.net/Maestro_T/article/details/108379780
# 255.255.0.0  -> 16
mask2cidr ()
{
    # Assumes there's no "255." after a non-255 byte in the mask
    local x=${1##*255.}
    set -- 0^^^128^192^224^240^248^252^254^ $(( (${#1} - ${#x})*2 )) ${x%%.*}
    x=${1%%$3*}
    echo $(( $2 + (${#x}/4) ))
}
# 16 -> 255.255.0.0
cidr2mask ()
{
    # Number of args to shift, 255..255, first non-255 byte, zeroes
    set -- $(( 5 - ($1 / 8) )) 255 255 255 255 $(( (255 << (8 - ($1 % 8))) & 255 )) 0 0 0
    [ $1 -gt 1 ] && shift $1 || shift
    echo ${1-0}.${2-0}.${3-0}.${4-0}
}
