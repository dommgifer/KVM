import psutil
import time
import sys
import os

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close() 



def memory_montor(filename,filename1):
    flag1 = 0
    flag2 = 0
    tmp = psutil.swap_memory().sout
    alarm_count = 0
    ok_count = 0
    c_alarm_count = 0
    c_ok_count = 0
    c_low_count = 0
    status = 0
    file_name = '/home/user/test.txt'
    while(1):
	time.sleep(1)
	cpu = psutil.cpu_percent(interval=1)
	mem = psutil.virtual_memory()
	swap = psutil.swap_memory()
	disk = psutil.disk_usage('/')
	disk_total = round(disk.total/1073741824.0,1)
        swap_out = psutil.swap_memory().sout
	mem_used = mem.used/1048576
	swap_used = swap.used/1048576
        #result = open(filename,'a')
        #result1 = open(filename1,'a')
        #result.write(str(mem.percent))
        #result.write(',')
        #result1.write(str(swap_used))
        #result1.write(',')
	#f = open("test.txt","w")
	text = str(cpu)+'%'+'\n'
	replace_line(file_name,0,text)
	#f.write(str(cpu)+'%' + "\n")
	print('H '+ str(c_alarm_count))
	print('L '+ str(c_low_count))	
	if (cpu) >= (80):
	    print('CCCC')
	    c_alarm_count = c_alarm_count + 1
 	    #c_low_count = 0
            #c_ok_count = 0

	    #print('H '+ str(c_alarm_count))
	    #if(status) == (0):
	    #    f.write('N/A'+"\n")
	    #if (c_alarm_count) >= (10):
            #    f.write('HIGH'+"\n")
		#status = 1
	elif (cpu) <= (20):
	    c_low_count = c_low_count + 1
	    #c_alarm_count = 0
            #c_ok_count = 0
	    #print('L '+ str(c_low_count))
	    #if(status) == (0):
               # f.write('N/A'+"\n")
	    #if (c_low_count) >= (10):
             #   f.write('LOW'+"\n")
	#	status = 1
	else:
	    c_ok_count = c_ok_count + 1
	    #c_alarm_count = 0
            #c_low_count = 0
	    #if (c_ok_count) >= (10):
	     #   f.write('ok'+"\n")
	#	status = 1
        if (c_alarm_count) >= (10):
	    text = 'HIGH'+'\n'
	    replace_line(file_name,1,text)
	    #f.write('HIGH'+"\n")
	    c_low_count = 0
	    c_ok_count = 0
	    c_alarm_count = 0
	    status = 1
	elif (c_low_count) >= (10):
	    text = 'LOW'+'\n'
	    replace_line(file_name,1,text)
	    #f.write('LOW'+"\n")
	    c_alarm_count = 0
	    c_ok_count = 0
	    c_low_count = 0
	    status = 1
	elif(c_ok_count) >=(10):
 	    text = 'ok'+'\n'
	    replace_line(file_name,1,text)
	    #f.write('ok'+"\n")
 	    c_alarm_count = 0
	    c_low_count = 0
	    c_ok_count = 0
	    status = 1
	elif(status) == 0:
	    text = 'N/A'+'\n'
	    replace_line(file_name,1,text)
	    #f.write('N/A'+"\n")
	"""
	if (cpu) >= (80):
	    f.write('HIGH'+"\n")
	elif (cpu) <= (20):
	    f.write('LOW'+"\n")
	else:
	    f.write('ok'+"\n")
        """
	
	text = str(mem.percent)+'%'+'\n'
	replace_line(file_name,2,text)
	#f.write(str(mem.percent)+'%' + "\n")
	#print (mem.percent)
	#print (swap_out)
#	print (alarm_count)
	#print (ok_count)
	if (alarm_count) >= (5) :
	    text = 'HIGH'+'\n'
	    replace_line(file_name,3,text)
            #f.write('alarm'+"\n")
	else:	
	    text = 'ok'+'\n'
	    replace_line(file_name,3,text)
	    #f.write('ok'+"\n")
        #elif(ok_count) >= (5):
            #f.write('ok'+"\n")
	
	text = str(disk_total)+'GB'+'\n'
	replace_line(file_name,4,text)
	text = str(disk.percent)+'%' + '\n'
	replace_line(file_name,5,text)
	#f.write(str(disk_total)+'GB' + "\n")
	#f.write(str(disk.percent)+'%' + "\n")
	if (swap_out-tmp) > 0 :
            alarm_count = alarm_count + 1
	    tmp = swap_out
	    #ok_count = 0
	else:
	    #ok_count = ok_count +1 
	    alarm_count = 0
	#time.sleep(1)

if __name__ == '__main__':
    filename = sys.argv[1]
    filename1 = sys.argv[2]
    memory_montor(filename,filename1)
