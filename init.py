from __future__ import print_function
import subprocess
import base64
import libvirt
import os
import ast
import json
from texttable import Texttable

########### connect to KVM ############
def connect():
    connect = libvirt.open('qemu:///system')
    if connect == None:
        print('Failed to open connection to qemu://sysyem')
        exit(1)
    else:
        return connect

def check_numa_node(connect):
    nodeinfo = connect.getInfo()
    #print('Number of NUMA nodes: '+str(nodeinfo[4]))
    return str(nodeinfo[4])

def get_numa_node_memory(conn):
    nodeinfo = conn.getInfo()
    numnodes = nodeinfo[4]
    memlist = conn.getCellsFreeMemory(0, numnodes)
    cell = 0
    for cellfreemem in memlist:
        print('Node '+str(cell)+': '+str(cellfreemem)+' bytes free memory')
        cell += 1
    return

def list_all_domain(connect):
    t = Texttable()
    t.set_cols_align(['l','c'])
    t.set_cols_valign(['m','m'])
    t.set_cols_width([25,13])
    domainIDs = connect.listDomainsID()
    domainNames = conn.listDefinedDomains()
    if domainIDs == None:
        print('Failed to get a list of domain IDs', file=sys.stderr)
    for domainID in domainIDs:
        dom = connect.lookupByID(domainID)
        domain = conn.lookupByID(domainID)
        t.add_rows([['VM Name','Status'],[str(dom.name()),'Running']])
    if len(domainNames) == 0:
        print('  None')
    else:
        for domainName in domainNames:
            t.add_rows([['VM Name','Status'],[domainName,'Power Off']])
    print(t.draw())

def rawInputTest():
    x = raw_input(" ")
    return x


def boot_domain_InputTest():
    x = raw_input("Input boot domain Name:")
    return x

def set_vm_option():
    x = raw_input("Set VM option : ['Compute type',CPU High usage, CPU Low usage, CPU status continue time, Cool Down, Memory Low usage]  Example: ['CPU',80,20,5,5,30]")
    #x =eval(x)
    return x

def boot_domain(option,domainName):
    option = option

def open_vm_info_file_write(domainID):
    os.environ['domainID'] = str(domainID)
    handle = os.popen('virsh qemu-agent-command $domainID \'{"execute":"guest-file-open", "arguments":{"path":"/home/user/info.txt","mode":"w+"}}\'').read()
    handles = ast.literal_eval(handle.rstrip()).get('return')
    #handles[domainID] = handle_value   #dict handles{domainID : handle}
    return handles

def write_vm_info_file(domainID,option,handles):
    encoded = base64.b64encode(option)
    read_command = {"execute":"guest-file-write", "arguments":{"handle":handles,"buf-b64":encoded}}
    read_command_json_fomat = json.dumps(read_command)
    os.environ['handle_value'] = str(handles)
    os.environ['read_command'] = read_command_json_fomat
    os.environ['domainID'] = str(domainID)
    a = os.popen('virsh qemu-agent-command $domainID $read_command').read()

def close_vm_info_file(domainID,handles):
    #for domainID, handle_value in handles.iteritems():
    close_command = {"execute":"guest-file-close", "arguments":{"handle":handles}}
    close_command_json_fomat = json.dumps(close_command)
    os.environ['close_command'] = close_command_json_fomat
    os.environ['domainID'] = str(domainID)
    a = os.popen('virsh qemu-agent-command $domainID $close_command').read()


def disconnect(connect):
    connect.close()
    exit(0)

if __name__ == '__main__':
    conn = connect()
    print("Chose Your active: (1) List All Domain (2) Boot Domain:")
    #print('type,high,low,continu,cd,mem_low')
    #boot_dom = boot_domain_InputTest()
    chose = rawInputTest()
    if (chose) == '1':
         list_all_domain(conn)
    elif chose == '2':
        domainID = boot_domain_InputTest()
        option = set_vm_option()
        handles = open_vm_info_file_write(domainID)
        write_vm_info_file(domainID,option,handles)
        close_vm_info_file(domainID,handles)
    #print(chose)
    #if chose == 1:
    #   list_all_domain(conn)
    #elif chose == 2:
        
    #check_numa_node(conn)
    #get_numa_node_memory(conn)
    #active_domain_ids = get_active_domainIDs(conn)
    #get_active_domain_name(conn,active_domain_ids)
    #list_inactive_domain(conn)
    #list_all_domain(conn)
    disconnect(conn)
