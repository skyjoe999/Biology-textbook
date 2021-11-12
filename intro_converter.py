import requests
import os
import io
from PIL import Image
import re
chapter_count=45
for c in range(1,chapter_count+1):
	print('\tconverting chapter #'+str(c))
	html=requests.get('https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/hillis2e_ch'+('0'+str(c))[-2:]+'_1.html').content.decode('utf-8')

	#links cleanup
	while 1:
		match=re.match(r'.*?(<span data-type="link" data-PNlinktype="ConceptLink" data-href="(hillis2e_ch(\d+)_(\d+)\.html)">(.*?)</span>)',html,16)
		if match == None:
			break
		if match.group(4)=='1':
			print('replaced a link to intro #'+match.group(3).lstrip('0'))
			html=html[:match.start(1)]+'<a class="concept_link" target="_blank" href="../../ch'+match.group(3).lstrip('0')+'/intro/intro.html">'+match.group(5)+'</a>'+html[match.end(1):]
		else:
			print('replaced a link to section '+match.group(3).lstrip('0')+'.'+str(int(match.group(4))-1))
			html=html[:match.start(1)]+'<a class="concept_link" target="_blank" href="https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/'+match.group(2)+'">'+match.group(5)+'</a>'+html[match.end(1):]
	while 1:
		match=re.match(r'.*?(<span data-type="termref" data-term=".*?">(.*?)</span>)',html,16)
		if match == None:
			break
		print('replaced a "termref" defining '+match.group(2))
		html=html[:match.start(1)]+'<a class="term_definition" target="_blank" href="https://www.google.com/search?q='+match.group(2)+'">'+match.group(2)+'</a>'+html[match.end(1):]
	while 1:
		match=re.match(r'.*?(<span data-type="link" data-PNlinktype="FigureLink".*?data-href="(asset/img_ch(\d+)/c13_fig(\d+).jpg)">(.*?)</span></span>)',html,16)
		if match == None:
			break
		print('replaced a link to figure '+match.group(3).lstrip('0')+'.'+match.group(4).lstrip('0'))
		html=html[:match.start(1)]+'<a class="figure_link" target="_blank" href="https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/'+match.group(2)+'">'+match.group(5)+'</a>'+html[match.end(1):]
	while 1:
		match=re.match(r'.*?(<span data-PNtype="nowrap">(.*?)</span>)',html,16)
		if match == None:
			break
		print('replaced a "nowrap" span')
		html=html[:match.start(1)]+'<span class="no_wrap">'+match.group(2)+'</span>'+html[match.end(1):]
	while 1:
		match=re.match(r'.*?(<div data-block_type="blockquote" (id=".*?")><p>(.*?)</p></div>)',html,16)
		if match == None:
			break
		print('replaced a "blockquote" div')
		html=html[:match.start(1)]+'<p '+match.group(2)+' class="blockquote">'+match.group(3)+'</p>'+html[match.end(1):]

	#item parsing
	title=re.match(r'.*?<h2 class="section-title"><span data-type="title" data-title-for="hillis2e-ch\d+-section-1">(.*?)</span></h2>',html,16).group(1)
	sections=re.match(r'.*?<h3 data-type="title" data-for_type="box" data-title-for="hillis2e-ch\d+-box-1">Key Concepts</h3>(.*?)</div>',html,16).group(1)
	sections=list(map((lambda a: (a.group(1),a.group(2),str(int(a.group(1))+1))),list(map((lambda a:re.match(r'<p id="hillis2e-ch\d+-p-\d+"><strong>\d+\.(.*?)</strong>(.*?)</p>',a,16)),sections.split('\n')[1:-1]))))
	img=(lambda a: (a.group(1),a.group(2)))(re.match(r'.*?<img id=".*?".*?src="(asset/img_ch\d+/(.*?))"',html,16))
	imgCap=re.match(r'.*?<div data-type="figure_text"><span data-type="caption">(.*?)</span></div>',html,16).group(1)
	paragraphs=re.match(r'.*?Key Concepts</h3>.*?</div>.*?(?=<p)(.*?)<div',html,16).group(1)
	paragraphs=list(map((lambda a:(lambda a: [a.group(3),a.group(2),int(a.group(1))])(re.match(r'<p id="hillis2e-ch\d+-p-(\d+)"(.*?)>(.*?)</p>',a,16))),paragraphs.strip().split('\n')))
	paragraphs[0][0]='<span class="first_letter">'+paragraphs[0][0][0]+'</span>'+paragraphs[0][0][1:]
	paragraphs.sort(key=(lambda a:a[2]))
	question=[False]
	if re.match(r'.*?<div data-type="box"\ data-block_type="question"\ id="hillis2e-ch\d+-box-\d+">',html,16)!=None:
		question=[True,re.match(r'.*?<h3>Question.*?<p id="hillis2e-ch\d+-p-\d+">(.*?)</p>',html,16).group(1),sections[-1][0],str(int(sections[-1][0])+1)]

	#loading template
	file=open('./intro.template','r',encoding='utf-8')
	template=file.read()
	file.close()
	def templateFill(text,replace):
		while(text.find('%')!=-1):
			token=text[text.find('%')+1:text.find('%',text.find('%')+1)]
			text=text[:text.find('%')]+'%'+text[text.find('%',text.find('%')+1)+1:]
			if token.startswith('if '):
				token=token[3:]
				if token not in replace:
					print('error if token:',token)
					break
				if replace[token][0]:
					tempRep=replace.copy()
					for n,v in enumerate(replace[token][1:]):
						tempRep[str(n)]=v
					text=text[:text.find('%')]+templateFill(text[text.find('{')+1:text.find('}')],tempRep)+text[text.find('}')+1:]
				else:
					text=text[:text.find('%')]+text[text.find('}')+1:]
				continue
			if token not in replace:
				print('error token:',token)
				break
			if type(replace[token])==type([]):
				for i in replace[token]:
					tempRep=replace.copy()
					for n,v in enumerate(i):
						tempRep[str(n)]=v
					text=text[:text.find('%')]+templateFill(text[text.find('{')+1:text.find('}')],tempRep)+text[text.find('%'):]
				text=text[:text.find('%')]+text[text.find('}')+1:]
				continue
			text=text[:text.find('%')]+replace[token]+text[text.find('%')+1:]
		return text

	#filling template and writing file
	os.makedirs(os.path.dirname(os.path.dirname(__file__)).replace('\\','/')+'/chapters/ch'+str(c)+'/intro', exist_ok=True)
	file=open(os.path.dirname(os.path.dirname(__file__)).replace('\\','/')+'/chapters/ch'+str(c)+'/intro/intro.html','w',encoding='utf-8')
	file.write(
		templateFill(template,
			replace={
				'c':str(c),
				'c0':('0'+str(c))[-2:],
				'title':title,
				'imgCap':imgCap,
				'img1': img[1],
				'sections':sections,
				'paragraphs':paragraphs,
				'question': question
			}
		)
	)
	file.close()

	#getting the intro image
	ir=requests.get('https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/'+img[0], stream = True)
	ir.raw.decode_content = True
	im=Image.open(io.BytesIO(ir.content))
	im.save(os.path.dirname(os.path.dirname(__file__)).replace('\\','/')+'/chapters/ch'+str(c)+'/intro/'+img[1])
	im.close()
'''
'''
2✔ 6✔ 10✔ 13✔ 16✔ 32✔ 36✔ 38 39✔
'''
