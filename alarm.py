import psutil
import os
import sys

#def get_ip():
#    vm_ip = str(psutil.net_if_addrs()['eth0'][0]).split(",")[1].split("'")[1]
#    os.environ['vm_ip'] = vm_ip

def monitor(high_limit):
    flag1 = 0
    flag2 = 0
    while(1):
        cpu_util = psutil.cpu_percent(interval=1)
        if int(cpu_util) >= int(high_limit) :
	    if flag1 == 0:
	        os.system('echo alarm > /home/user/test.txt')
	        flag1 = 1
	    else:
	        flag2 = 0
        else:
	    if flag2 == 0:
	        os.system('echo ok > /home/user/test.txt')
	        flag2 = 1
	    else:
	        flag1 = 0
	    continue

if __name__ == '__main__':
    high_limit = sys.argv[1]
    #get_ip()
    monitor(high_limit)
