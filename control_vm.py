from __future__ import print_function
import sys
import libvirt
import os
import ast
import json

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

########## disconnect KVM ##############
def disconnect(connect):
    connect.close()
    exit(0)


########## Open Vm Alarm File ###########
def open_vm_alarm_file(domainIDs):
    handles = {}
    for domainID in domainIDs:
        os.environ['domainID'] = str(domainID)
        handle = os.popen('virsh qemu-agent-command $domainID \'{"execute":"guest-file-open", "arguments":{"path":"/home/user/test.txt","mode":"r"}}\'').read()    
        handle_value = ast.literal_eval(handle.rstrip()).get('return')
        handles[domainID] = handle_value   #dict handles{domainID : handle}
    return handles

######### Read Vm Alarm File And Record To Dict ###########
def read_vm_alam_file(handles):
    vm_alarm = {}
    for domainID, handle_value in handles.iteritems():
        read_command = {"execute":"guest-file-read", "arguments":{"handle":handle_value}}
        read_command_json_fomat = json.dumps(read_command)
        os.environ['handle_value'] = str(handle_value)
        os.environ['read_command'] = read_command_json_fomat
        os.environ['domainID'] = str(domainID)
        read_command_json_format = os.popen('virsh qemu-agent-command $domainID $read_command').read()
        file_content = json.loads(read_command_json_format.rstrip())
        data = file_content["return"]["buf-b64"]
        vm_alarm[domainID] = data   #dict vm_alarm{domainID : status}
    return vm_alarm

######### Close Vm Alarm File ###########
def close_vm_alarm_file(handles):
    for domainID, handle_value in handles.iteritems():
        close_command = {"execute":"guest-file-close", "arguments":{"handle":handle_value}}
        close_command_json_fomat = json.dumps(close_command)
        os.environ['close_command'] = close_command_json_fomat
        os.environ['domainID'] = str(domainID)
        os.system('virsh qemu-agent-command $domainID $close_command')

def check_vm_alarm(vm_alarm):
    for domainID, data in vm_alarm.iteritems():
        if data == "YWxhcm0K":
            return


def get_vm_vcpu_count(vm_alarm):
    for domainID, data in vm_alarm.iteritems():
        os.environ['domainID'] = str(domainID)
        cpu =  os.popen('virsh qemu-agent-command $domainID \'{"execute":"guest-get-vcpus"}\'').read()
        cpu_online = 0
        cpu_return_data = json.loads(cpu.rstrip())
        dict_tmp = cpu_return_data["return"]
        for i in  range(0,len(dict_tmp),1):
            dict_tmp = cpu_return_data["return"][i]
            if dict_tmp["online"]:
                cpu_online = cpu_online +1
        vm_alarm[domainID] = cpu_online #dict vm_alarm{domainID : vcpu_count}
    return vm_alarm

if __name__ == '__main__':
    conn = connect()
    domainIDs = get_active_domainIDs(conn)
    handles = open_vm_alarm_file(domainIDs)
    vm_alarm = read_vm_alam_file(handles)
    get_vm_vcpu_count(vm_alarm)
    close_vm_alarm_file(handles)
    disconnect(conn)
