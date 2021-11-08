import requests
chapter_count=[]
chapter_count=[6, 7, 6, 7, 8, 8, 7, 6, 5, 7, 6, 6, 6, 7, 9, 6, 6, 5, 6, 6, 7, 6, 9, 6, 6, 6, 5, 5, 8, 7, 5, 7, 6, 7, 7, 7, 5, 8, 7, 8, 7, 8, 6, 7, 8]
c=1
while 0:
	s=1
	print('\nch'+('0'+str(c))[-2:]+': ',end='')
	while 1:
		r=requests.head('https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/hillis2e_ch'+('0'+str(c))[-2:]+'_'+str(s)+'.html')
		if r.status_code==404:
			break
		# print(str(r.status_code)[0],end='')
		print(s,end='')
		s+=1
	if s==1:
		break
	chapter_count+=[s-1]
	c+=1
print()
# print(chapter_count)
print('''
<!DOCTYPE html>
<html lang="en" dir="ltr">
	<head>
		<meta charset="utf-8">
		<title>Bio Table of Contents</title>
		<style>
			body {font-family: Arial; background-color:#2C313C;}
			body table tr td a {text-decoration-line: none; font-size: xx-large; font-weight: 800;}
			body table tr td table tr td a {margin: 3px; padding: 0px 40px; font-size: x-large;border-radius: 25px; background: #98C379;}
			a{color: white;}
		</style>
	</head>
	<body>
		<p>
			<div style="color: white; font-weight: 800; font-size: xxx-large;">Principles of Life</div>
			<div style="color: white; font-weight: 800; font-size: x-large; padding-left: 20px;">2nd Edition</div>
			<hr>
		</p>
		<table>''')
for c,s in enumerate(chapter_count[:]):

	print('\t'*3+'<tr><td><a target="_blank" href="https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/hillis2e_ch'+('0'+str(c+1))[-2:]+'_1.html">Chapter '+str(c+1)+'</a><table><tr>')
	for i in range(1,s):
		print('\t'*4+'<td><a target="_blank" href="https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/hillis2e_ch'+('0'+str(c+1))[-2:]+'_'+str(i+1)+'.html">'+str(c+1)+'.'+str(i)+'</a></td>')
	print('\t'*3+'</tr></table></td></tr>')


print('''		</table>
	<div style="margin-top: 100px;"></div>
	</body>
</html>''')
