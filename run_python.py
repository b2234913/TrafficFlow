import os
for i in range(0,6):
    filename = 'nohup python get_info.py ' + str(5*i+1) + ' ' + str(5*(i+1)) + ' &'
    print filename
    os.system(filename)
