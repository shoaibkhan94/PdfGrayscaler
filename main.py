import subprocess
import pypdftk
import shlex
from os import listdir
from os.path import isfile, join
from  os import  chdir
from os import getcwd
from natsort import natsorted, ns

f = raw_input("Enter the file name : ")
test = f
cwd = getcwd()
subprocess.call('mkdir temp', shell=True)
temp_dir = cwd + '/temp'
page_paths=[]
page_paths = pypdftk.split(f, 'temp')
#print(page_paths)
s = raw_input("Enter the page nos. to be printed in grayscale separated by spaces : ")
pageslist = map(int, s.split(' '))
#print(pageslist, type(pageslist))
onlyfiles = [f for f in listdir('temp/') if isfile(join('temp/', f))]
#print(onlyfiles)
mergelist = []
for file in onlyfiles:
    if file.startswith('page_') :
        pg = file.split('_')[1]
        #print(pg, type(pg), int(pg[:2]) < 10, pg[:2])
        if int(pg[:2]) < 10 :
            c = 'mv -f '+file+' page_'+(pg[1])+'.pdf'
            #print(c)
            subprocess.call(c, shell=True, cwd=temp_dir)
for i in range(len(pageslist)):
    print(pageslist[i])
    comm = 'gs -sOutputFile=op_'+str(pageslist[i])+'.pdf -sDEVICE=pdfwrite -sColorConversionStrategy=Gray -dProcessColorModel=/DeviceGray -dAutoRotatePages=/None -dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH page_'+str(pageslist[i])+'.pdf'
    subprocess.call(shlex.split(comm), cwd=temp_dir)

onlyfiles = [f for f in listdir('temp/') if isfile(join('temp/', f))]
#print(onlyfiles)
for file in onlyfiles:
    if file.startswith('op_') :
        pg = file.split('_')[1]
        c2 = 'mv -f op_'+pg+' page_'+pg
        #print(c2)
        subprocess.call(c2, shell=True, cwd=temp_dir)

onlyfiles = [f for f in listdir('temp/') if isfile(join('temp/', f))]
for file in onlyfiles:
    if file.startswith('page_'):
        mergelist.append(file)

#print(mergelist)
sortedlist = natsorted(mergelist, key=lambda y: y.lower())
#print(sortedlist)
#print(test)
chdir(temp_dir)
#print(test)
pypdftk.concat(sortedlist, test)
copy_comm = 'cp '+temp_dir+'/'+test+' '+cwd+'/'+'new.pdf'
#print(copy_comm)
subprocess.call(copy_comm, shell=True, cwd=temp_dir)
flatten_comm = 'pdftk new.pdf output output.pdf flatten'
subprocess.call(flatten_comm, shell=True, cwd=cwd)
subprocess.call('rm -f new.pdf', shell=True, cwd=cwd)
rm_comm = 'rm -rf temp/'
subprocess.call(rm_comm, shell=True, cwd=cwd)
