import requests
# output
# chapter_count=45
# section_counts=[6, 7, 6, 7, 8, 8, 7, 6, 5, 7, 6, 6, 6, 7, 9, 6, 6, 5, 6, 6, 7, 6, 9, 6, 6, 6, 5, 5, 8, 7, 5, 7, 6, 7, 7, 7, 5, 8, 7, 8, 7, 8, 6, 7, 8]

# WARNING: Takes a while to run, just use results above
quit()
section_counts=[]
c=1
while 1:
	s=1
	print('\nch'+('0'+str(c))[-2:]+': ',end='')
	while 1:
		r=requests.head('https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/hillis2e_ch'+('0'+str(c))[-2:]+'_'+str(s)+'.html')
		if r.status_code==404:
			break
		# print(str(r.status_code)[0],end='')
		print(s,end=' ')
		s+=1
	if s==1:
		break
	section_counts+=[s-1]
	c+=1
chapter_count=len(section_counts)
