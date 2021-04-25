@ECHO OFF&CD /D "%~DP0"&NET SESSION>NUL 2>&1||(powershell -windowstyle hidden -noprofile "Start-Process '%~dpnx0' -Verb RunAs" 2>NUL&&EXIT)

net start "VMware DHCP Service"
net start "VMware NAT Service"
net start "VMAuthdService"
net start "VMUSBArbService"
net start "VMwareHostd"
