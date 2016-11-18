from __future__ import print_function
import sys
import libvirt
import os
import ast
import json
import time
import subprocess
import base64
import curses
from texttable import Texttable
########### connect to KVM ############
def connect():
    connect = libvirt.open('qemu:///system')
    if connect == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    else:
	return connect

########## get active vm's domain ID #########
def get_active_domainIDs(connect):
    domainIDs = connect.listDomainsID()
    if domainIDs == None:
        print('Failed to get a list of domain IDs', file=sys.stderr)
    
    return domainIDs if len(domainIDs) != 0 else null


########## get active vm name ###########
def get_active_domain_name(connect,domainID):
    dom = connect.lookupByID(domainID)
    return dom.name()

########## get active vm MAX memory ############
def get_active_domain_max_mem(connect,domainID):
    dom = connect.lookupByID(domainID)
    mem = int(dom.info()[1])/1024
    return mem

########## get active vm current cpu ############
def get_current_cpu_count(domainID):
    proc = subprocess.Popen(['virsh', 'dominfo', ' %s'%(domainID)], stdout=subprocess.PIPE)
    tmp = proc.stdout.readlines()
    tmp[5] = "".join(tmp[5].split())
    current_cpu = tmp[5].strip('CPU(s):')[0]
    return current_cpu


########## get active vm current memory ############
def get_current_memory_size(domainID):
    proc = subprocess.Popen(['virsh', 'dominfo', ' %s'%(domainID)], stdout=subprocess.PIPE)
    tmp = proc.stdout.readlines()
    tmp[8] = "".join(tmp[8].split())
    size = tmp[8].split(':')[1].split('KiB')[0]
    current_memory_size = int(size)/1024
    #print(current_memory_size)
    return current_memory_size


########## get active vm MAX CPU ############
def get_active_domain_max_cpu(connect,domain_name):
    dom = connect.lookupByName(domain_name)
    max_cpu = dom.maxVcpus()
    return max_cpu

######### get active vm network ip ############
def get_active_domain_ip(domainID):
    os.environ['domainID'] = str(domainID)
    interfaces =  os.popen('virsh qemu-agent-command $domainID \'{"execute":"guest-network-get-interfaces"}\'').read()
    data = json.loads(interfaces)['return'] #####type list##########
    tmp_ip={}
    for i in (1,(len(data)-1)):
        data_ip = data[i]######type dict####
	tmp_ip[str(data_ip.values()[1])] = str(data_ip.values()[0][0].values()[1])
    ip = str(tmp_ip)
    ip = ip.replace('\'','')
    ip = ip.replace('{','')
    ip = ip.replace('}','')
    ip = ip.replace(',','')
    return ip            #########type dict#############



########## disconnect KVM ##############
def disconnect(connect):
    connect.close()
    exit(0)


########## Open Vm Alarm File ###########
def open_vm_alarm_file(domainID):
    #handles = {}
    #for domainID in domainIDs:
    os.environ['domainID'] = str(domainID)
    handle = os.popen('virsh qemu-agent-command $domainID \'{"execute":"guest-file-open", "arguments":{"path":"/home/user/test.txt","mode":"r"}}\'').read()    
    handles = ast.literal_eval(handle.rstrip()).get('return')
    #handles[domainID] = handle_value   #dict handles{domainID : handle}
    return handles

######### Read Vm Alarm File And Record To Dict ###########
def read_vm_alam_file(domainID,handles):
    #vm_alarm = {}
    #for domainID, handle_value in handles.iteritems():
    read_command = {"execute":"guest-file-read", "arguments":{"handle":handles}}
    read_command_json_fomat = json.dumps(read_command)
    os.environ['handle_value'] = str(handles)
    os.environ['read_command'] = read_command_json_fomat
    os.environ['domainID'] = str(domainID)
    read_command_json_format = os.popen('virsh qemu-agent-command $domainID $read_command').read()
    file_content = json.loads(read_command_json_format.rstrip())
    data = file_content["return"]["buf-b64"]
        #vm_alarm[domainID] = data   #dict vm_alarm{domainID : status}
    return data

######### Close Vm Alarm File ###########
def close_vm_alarm_file(domainID,handles):
    #for domainID, handle_value in handles.iteritems():
    close_command = {"execute":"guest-file-close", "arguments":{"handle":handles}}
    close_command_json_fomat = json.dumps(close_command)
    os.environ['close_command'] = close_command_json_fomat
    os.environ['domainID'] = str(domainID)
    a = os.popen('virsh qemu-agent-command $domainID $close_command').read()

def check_vm_alarm(vm_alarm):
    for domainID, data in vm_alarm.iteritems():
	#print domain
	#return data
        if data == "YWxhcm0K":
	#    print('alarm')
            return  

def get_vm_vcpu_count(domainID):
    os.environ['domainID'] = str(domainID)
    cpu =  os.popen('virsh qemu-agent-command $domainID \'{"execute":"guest-get-vcpus"}\'').read()
    cpu_online = 0
    cpu_return_data = json.loads(cpu.rstrip())
    dict_tmp = cpu_return_data["return"]
    for i in  range(0,len(dict_tmp),1):
        dict_tmp = cpu_return_data["return"][i]
        if dict_tmp["online"]:
            cpu_online = cpu_online +1
    return str(cpu_online)

def get_vm_cpu_usage(domainID):
    hand = open_vm_alarm_file(domainID)
    text = read_vm_alam_file(domainID,hand)
    data = base64.b64decode(text)
    close_vm_alarm_file(domainID,hand)
    return data.split('\n')[0]

def get_vm_mem_usage(domainID):
    hand = open_vm_alarm_file(domainID)
    text = read_vm_alam_file(domainID,hand)
    data = base64.b64decode(text)
    close_vm_alarm_file(domainID,hand)
    return data.split('\n')[2]

def get_vm_cpu_alarm(domainID):
    hand = open_vm_alarm_file(domainID)
    text = read_vm_alam_file(domainID,hand)
    data = base64.b64decode(text)
    close_vm_alarm_file(domainID,hand)
    result = data.split('\n')[1]
    return result

def get_vm_memory_alarm(domainID):
    hand = open_vm_alarm_file(domainID)
    text = read_vm_alam_file(domainID,hand)
    data = base64.b64decode(text)
    close_vm_alarm_file(domainID,hand)
    return data.split('\n')[3]

def get_vm_disk_total(domainID):
    hand = open_vm_alarm_file(domainID)
    text = read_vm_alam_file(domainID,hand)
    data = base64.b64decode(text)
    close_vm_alarm_file(domainID,hand)
    return data.split('\n')[4]

def get_vm_disk_usage(domainID):
    hand = open_vm_alarm_file(domainID)
    text = read_vm_alam_file(domainID,hand)
    data = base64.b64decode(text)
    close_vm_alarm_file(domainID,hand)
    return data.split('\n')[5]

def control_vm_cpu(domainID,domain_max_cpu,domain_online_cpu):
    result = get_vm_cpu_alarm(domainID)
    max_cpu = int(domain_max_cpu)
    online_cpu = int(domain_online_cpu)
    if result == 'HIGH':
        if online_cpu == max_cpu:
	    return
	else:
	    online_cpu = online_cpu + 1
	    set = subprocess.Popen(['virsh', 'setvcpus', ' %s'%(domainID), '%s'%(online_cpu),'--guest'], stdout=subprocess.PIPE)
	    return
    elif result == 'LOW':
	if online_cpu == 1:
	    return
	else:
	    online_cpu = online_cpu - 1
	    set = subprocess.Popen(['virsh', 'setvcpus', ' %s'%(domainID), '%s'%(online_cpu),'--guest'], stdout=subprocess.PIPE)
	    return	
    else:
	return
	 
if __name__ == '__main__':
    conn = connect()
    while(1):
	#time.sleep(1)
	domainIDs = get_active_domainIDs(conn)
        #t = PrettyTable(['VM Name', 'Current CPU','Max CPU','IP'])
	t = Texttable()
	t.set_cols_align(['c','c','c','c','c','c','c','c','c','c','c'])
	t.set_cols_valign(['m','m','m','m','m','m','m','m','m','m','m'])
	t.set_cols_width([20,13,10,10,15,15,22,15,15,10,10])
        for domainID in domainIDs:
	    domain_name = get_active_domain_name(conn,domainID)
	    domain_memory = get_current_memory_size(domainID)
	    domain_max_mem = get_active_domain_max_mem(conn,domainID)
	    domain_max_cpu = get_active_domain_max_cpu(conn,domain_name)
            domain_current_cpu = get_current_cpu_count(domainID)
	    domain_ip = get_active_domain_ip(domainID)
	    domain_online_cpu = get_vm_vcpu_count(domainID)
	    domain_cpu_usage = get_vm_cpu_usage(domainID)
	    domain_mem_usage = get_vm_mem_usage(domainID)
	    domain_disk_total = get_vm_disk_total(domainID)
	    domain_disk_usage = get_vm_disk_usage(domainID)
	    t.add_rows([['VM Name', 'Current CPU','Online CPU','Max CPU','Current Memory','Max Memory','Interface:IP','CPU Usage','Memory Usage','Disk Space','Disk Usage'], [domain_name, domain_current_cpu,domain_online_cpu,domain_max_cpu,str(domain_memory)+' MB',str(domain_max_mem)+' MB',domain_ip,domain_cpu_usage,domain_mem_usage,domain_disk_total,domain_disk_usage]])
		####################################################################
	#handles = open_vm_alarm_file(domainIDs)
	#w = curses.initscr()
	#w.addstr(t.draw())
	#w.refresh()
	#control_vm_cpu(domainID,domain_max_cpu,domain_online_cpu)
	time.sleep(1)
	print (t.draw())
        #sys.stdout.write('%s\r'%str(t.draw()))
	#sys.stdout.flush()
	#time.sleep(1)

	#vm_alarm = read_vm_alam_file(handles)
	#print (vm_alarm)
	#check_vm_alarm(vm_alarm)
	#if data == "YWxhcm0K":
	    
	#print (data) 
	#get_vm_vcpu_count(vm_alarm)
	#close_vm_alarm_file(handles)
	disconnect(conn)
