import psutil
import time
import sys
import os
import subprocess
from threading import Thread

class cpuInfo:
    def __init__(self, status = 'N/A'):
        self.status = status
        self.preStatus = 'N/A'
        #self.count = count

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.preStatus = self.status
        self.status = status

class memInfo:
    def __init__(self, status = 'N/A'):
        self.status = status
        self.preStatus = 'N/A'
        #self.count = count

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.preStatus = self.status
        self.status = status


def get_logic_cpu_count():
    proc = subprocess.Popen(['lscpu'], stdout=subprocess.PIPE) 
    tmp = proc.stdout.readlines()
    tmp[4] = "".join(tmp[4].split())
    tmp = tmp[4].split('list:')[1]
    #print(tmp)
    if tmp.find('-')==1:
        #print(tmp.split('-')[1])
        tmp = int(tmp.split('-')[1])-int(tmp.split('-')[0])+1
        return tmp
    else:
        return len(tmp.split(','))

def cpu_per():
    cpu = psutil.cpu_percent(interval=1,percpu=True)
    return cpu[0]

#def write_result(cpu_status,mem_status,file_name,cpuInfo,memInfo):
def write_result(cpu_status,mem_status,file_name,cpuInfo,memInfo,cpu_per):
    #cpu = cpu_per()
    cpu = cpu_per
    #cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/')
    disk_total = round(disk.total/1073741824.0,1)
    write_cpu_status = cpuInfo.getStatus()
    write_mem_status = memInfo.getStatus()
    f = open(file_name,'w')
    result = [str(cpu)+'%',write_cpu_status,str(mem)+'%',write_mem_status,str(disk_total)+'GB',str(disk.percent)+'%']
    f.write(str(result))
    f.close

def cd_status(cpuInfo):
    tmp_status = cpuInfo.getStatus()
    cpuInfo.setStatus('CD')
    time.sleep(4)
    #print('CD end')
    cpuInfo.setStatus(tmp_status)
    #cpuInfo.setStatus('ok')

def get_cpu_status(file_name):
    f=open(file_name,'r')
    cpu_status = f.readlines()[0].split()[1].split('\'')[1]
    f.close()
    return cpu_status

if __name__ == '__main__':
    #filename = sys.argv[1]
    #filename1 = sys.argv[2]
    time_count = 4
    cpu_status = 'N/A'
    mem_status = 'N/A'
    file_name = '/home/user/test1.txt'
    alarm_count = 0
    ok_count = 0
    c_alarm_count = 0
    c_ok_count = 0
    c_low_count = 0
    status = 0
    ti=1
    tmp_swap = psutil.swap_memory().sout
    tmp_cpu_count = get_logic_cpu_count()
    load = os.getloadavg()[0]
    cpuInfo = cpuInfo()
    memInfo = memInfo()
    #memory_montor(filename,filename1)
    while(1):
        cpu = cpu_per()
        swap = psutil.swap_memory()
        #cpu = psutil.cpu_percent(interval=0.5)
        #write_result(cpu_status,mem_status,file_name)
        #pre_cpu_status = get_cpu_status(file_name)
        cpu_count = get_logic_cpu_count()
        now_swap = psutil.swap_memory().sout
        #if (cpuInfo.getStatus()) == 'CD':
        #    status = 1
        #elif (cpu_count) != tmp_cpu_count:
        #    tmp_cpu_count = cpu_count
            #print('CD start')
            #cpu_status = 'CD'
        #    th = Thread(target=cd_status,name ='thread-',args=(cpuInfo,))
        #    th.start()
        #else:
        if (cpu) >= (80):
            c_alarm_count = c_alarm_count + 1
            c_low_count = 0
        elif (cpu) <= (20):
            c_low_count = c_low_count + 1
            c_alarm_count = 0
        else:
            c_ok_count = c_ok_count + 1
        if (c_alarm_count) >= (time_count):
            #cpu_status = 'HIGH'
            cpuInfo.setStatus('HIGH')
            cpu_status =  cpuInfo.getStatus()
            #write_result(cpu_status,mem_status,file_name)
            c_low_count = 0
            c_ok_count = 0
            c_alarm_count = 0
        elif (c_low_count) >= (time_count):
            #cpu_status = 'LOW'
            cpuInfo.setStatus('LOW')
            cpu_status =  cpuInfo.getStatus()
            #write_result(cpu_status,mem_status,file_name)
            c_alarm_count = 0
            c_ok_count = 0
            c_low_count = 0
        elif(c_ok_count) >=(time_count):
            cpu_status = 'OK'
            mem_status = 'NULL'
            #write_result(cpu_status,mem_status,file_name)
            c_alarm_count = 0
            c_low_count = 0
            c_ok_count = 0

        mem = psutil.virtual_memory()
        if (now_swap-tmp_swap) > (0):
            memInfo.setStatus('HIGH')
            tmp_swap = now_swap
        elif (mem.percent) <= (30):
            memInfo.setStatus('LOW')
        else:
            memInfo.setStatus('OK')
        #mem_status = cpu_status
        write_result(cpu_status,mem_status,file_name,cpuInfo,memInfo,cpu)
        #print('H',str(c_alarm_count)+' L',(c_low_count))
        #print('now:'+str(cpu_count),'pre:'+str(tmp_cpu_count))
        #ff = open('/home/user/cpu_count/cpu.csv','a')
        print(ti)
        ti=ti+1
        #fd=open('/home/user/memort_test/con_memused.csv','a')      
        #ff = open('/home/user/memort_test/con_swap.csv','a')
        fa=open('/home/user/memort_test/con_ava.csv','a')      
        #ff.write(str(swap.used/1048576)+',')
        #fd.write(str(mem.used/1048576)+',')
        fa.write(str(mem.available/1048576)+',')
        #ff.close()
        #fd.close()
        fa.close()
        #fl=open('/home/user/memort_test/con_load.csv','a')
        #fl.write(str(load)+',')
        #fl.close()
        #print(open('/home/user/test1.txt','r').readlines())
