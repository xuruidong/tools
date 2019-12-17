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

