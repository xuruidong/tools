#!/bin/bash

ARCHIVE=`awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }' $0`
echo $ARCHIVE
tail -n+$ARCHIVE $0 | tar xvf -C /usr/local/src
#mv lnmp0.7 /root/lnmp
cd /usr/local/src/httpd
./install.sh   
ret=$? 
exit $ret
__ARCHIVE_BELOW__
