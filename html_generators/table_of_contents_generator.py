import requests
import os
import io
import re

chapter_count=45
section_counts=[6, 7, 6, 7, 8, 8, 7, 6, 5, 7, 6, 6, 6, 7, 9, 6, 6, 5, 6, 6, 7, 6, 9, 6, 6, 6, 5, 5, 8, 7, 5, 7, 6, 7, 7, 7, 5, 8, 7, 8, 7, 8, 6, 7, 8]
chapters=[]
for chapter_number in range(1,chapter_count+1):
	print('parsing chapter',chapter_number)
	html=requests.get('https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/hillis2e_ch'+('0'+str(chapter_number))[-2:]+'_1.html').content.decode('utf-8')
	chapter_title=re.match(r'.*?<h2 class="section-title"><span data-type="title" data-title-for="hillis2e-ch\d+-section-1">(.*?)</span></h2>',html,16).group(1)
	concepts=[]
	for concept_id in range(2,section_counts[chapter_number-1]+1):
		print('\t',str(chapter_number)+'.'+str(concept_id-1))
		html=requests.get('https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/hillis2e_ch'+('0'+str(chapter_number))[-2:]+'_'+str(concept_id)+'.html').content.decode('utf-8')
		concept_title=re.match(r'.*?<h2 class="section-title"><span data-type="title".*?>(?:Concept \d+\.\d+: )?(.*?)</span>',html,16).group(1)
		if concept_title=='Summary':
			concepts.append({
				'concept_title':'',
				'bold':'Chapter Summary',
				'concept_id':str(concept_id)
			})
		else:
			concepts.append({
				'concept_title':concept_title,
				'bold':'Concept '+str(chapter_number)+'.'+str(concept_id-1)+':',
				'concept_id':str(concept_id)
			})
	chapters.append({
		'chapter_number':str(chapter_number),
		'chapter_id':('0'+str(chapter_number))[-2:],
		'chapter_title':chapter_title,
		'concepts':concepts
	})
#loading template

file=open('./index.template','r',encoding='utf-8')
template=file.read()
file.close()
def templateFill(text,replace):
	while(text.find('%')!=-1):
		token=text[text.find('%')+1:text.find('%',text.find('%')+1)]
		text=text[:text.find('%')]+'%'+text[text.find('%',text.find('%')+1)+1:]
		if token not in replace:
			print('error token:',token)
			break
		if type(replace[token])==type([]):
			for i in replace[token]:
				text=text[:text.find('%')]+templateFill(text[text.find('{')+1:text.find('}%'+token+'%')],replace|i)+text[text.find('%'):]
			text=text[:text.find('%')]+text[text.find('}%'+token+'%')+len('}%'+token+'%'):]
			continue
		text=text[:text.find('%')]+replace[token]+text[text.find('%')+1:]
	return text

#filling template and writing file
file=open(os.path.dirname(os.path.dirname(__file__)).replace('\\','/')+'/index.html','w',encoding='utf-8')
file.write(templateFill(template,replace={'chapters':chapters}))
file.close()

'''
%chapters%
# %chapter_id%
# %chapter_number%
# %chapter_title%
# %concepts%
# %concept_id%
# %concept_number%
# %concept_title%
'''
