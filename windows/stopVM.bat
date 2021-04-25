@ECHO OFF&CD /D "%~DP0"&NET SESSION>NUL 2>&1||(powershell -windowstyle hidden -noprofile "Start-Process '%~dpnx0' -Verb RunAs" 2>NUL&&EXIT)
net stop "VMware DHCP Service"
net stop "VMware NAT Service"
net stop "VMwareHostd"
net stop "VMAuthdService"
net stop "VMUSBArbService"
