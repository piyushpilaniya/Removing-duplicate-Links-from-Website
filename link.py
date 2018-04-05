#import the libraries
import urllib
import lxml.html
import sys
import os 
 
#taking command line arguement
argument = sys.argv[1]

#finding the complete path of the html
dir_path = os.path.dirname(os.path.realpath(argument))

new_path = "file://"+dir_path+"/"+argument            #modifying the path by adding file:// in front and name of html file at end

connection = urllib.urlopen(new_path)                 #opening the url 
                              
dom =  lxml.html.fromstring(connection.read())        #lxml allow us to process html with python
 
hl = list()                           #list to store distinct links
record = list()                       #list which stores the index of hl list of the elements which have duplicates
total = list()                        #list to store all the links available in the website
duplindex = list()                    #list which stores the index of total list of the elements which are duplicates
found=0
 
lo=0




#here I am updating the "hl", "total","duplindex" and "record" list
for link in dom.xpath('//a/@href'): 
	if len(hl)>0:
		match=0
		total.append(link)
		for st in hl:
			if st in link:
				found=found+1
				match=match+1
				ind = hl.index(st)
				record.append(ind)
				duplindex.append(lo)
				break
				
		if match==0:
			hl.append(link)
		lo=lo+1	
	else:
		hl.append(link)
		total.append(link)
		lo=lo+1
print "Found",found,"duplicates:"	#printing number of duplicates	


i=1
duplicatelist = list()     #list to store the duplicate links

for al in record:
	#print i,hl[al]
	duplicatelist.append(hl[al])
	i=i+1



text = list()                           #list which stores text description of all the links.
for pink in dom.xpath('//a'):
	text.append(pink.text_content())


textlist = list()                        #list which stores the text description of only duplicate links.

i=1
#appending to textlist to store description of duplicate links
for zx in duplindex:
	#print i,text[zx]
	textlist.append(text[zx])
	i=i+1 		

le = len(duplindex)

print 

datafile = file(argument)       #opening the html file
linee=1
linenu=list()			#list which store line number of all the duplicate links
pp=0

#updating the list "linenu" to store line numbers of duplicate links
for line in datafile:
	if pp==le:
		break
	if textlist[pp] in line:
		pp=pp+1
		linenu.append(linee)
	linee=linee+1



#printing all the information of duplicate links
for ppp in range(1,le+1):
	print ppp,".",duplicatelist[ppp-1],"\"",textlist[ppp-1],"\"" " at line " ,linenu[ppp-1]



print
print "Select hyperlinks that you want to keep."
print "Enter A to keep all, OR"
print "Enter F to keep the first one in a set of duplicates, OR"
print "Enter the serial numbers (separated by commas) of the links to keep."






#taking input from user by giving option of which duplicate link to keep
name = raw_input("\nYour Selection:")
donothing=0

#case when user enters "A"-> I won't remove any link
if name=='A':
	donothing=1
#case when user enters "F"-> Only the first link will be kept other will be removed
elif name=='F':
	notline = list()   #list contianing the line numbers which will not be displayed in output file
	ch=1
	for xx in linenu:
		if ch in range(1,2):
			ch=ch+1
			continue
		notline.append(xx)	
		ch=ch+1
	#print notline
#here user will enter the numbers which he want to keep, others links will be removed
else:
	mylist = [int(x) for x in name.split(',')]        #list which contains position of duplicate link which we want to keep
	notline = list()   #list contianing the line numbers which will not be displayed in output file
	ch=1
	for xx in linenu:
		if ch in mylist:
			ch=ch+1
			continue
		notline.append(xx)	
		ch=ch+1

#modifying the name of the output file
output = argument+".dedup"

#opening html file
datafile = file(argument)
fp=open(output,"w+")

#if user enters option other than "A"
if donothing==0:
	imline=1
	fp=open(output, "a+")
	for line in datafile:	
		
		if imline in notline:
		#	print "hello"
			imline=imline+1
			continue
		fp.write("%s"%line)			#writing the data to desired file (leaving all the links which are not desired
		#print "hi"
		imline=imline+1	
	print "Removed",len(notline),"hyperlinks. Output file written to",output
else:                            #if user enters "A"
	#print "hi"
	fpn=open(output,"a+")
	for line in datafile:
		fpn.write("%s"%line)			#copying complete data to the output file
	print "Remove 0 hyperlinks. Output file written to",output



