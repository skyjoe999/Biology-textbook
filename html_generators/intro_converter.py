from bs4 import BeautifulSoup
import requests
import os
import io
from PIL import Image
def templateFill(text,replace):
	while(text.find('%')!=-1):
		token=text[text.find('%')+1:text.find('%',text.find('%')+1)]
		text=text[:text.find('%')]+'%'+text[text.find('%',text.find('%')+1)+1:]
		if token not in replace:
			print('error token:',token,text)
			break
		if type(replace[token])==type([]):
			for i in replace[token]:
				text=text[:text.find('%')]+templateFill(text[text.find('{')+1:text.find('}%'+token+'%')],replace|i)+text[text.find('%'):]
			text=text[:text.find('%')]+text[text.find('}%'+token+'%')+len('}%'+token+'%'):]
		elif type(replace[token])==type(True):
			if replace[token]:
				text=text[:text.find('%')]+templateFill(text[text.find('{')+1:text.find('}%'+token+'%')],replace)+text[text.find('%'):]
			text=text[:text.find('%')]+text[text.find('}%'+token+'%')+len('}%'+token+'%'):]
		elif type(replace[token])==type(''):
			text=text[:text.find('%')]+replace[token]+text[text.find('%')+1:]
		elif type(replace[token])==type({}):
			text=text[:text.find('%')]+templateFill(text[text.find('{')+1:text.find('}%'+token+'%')],replace|replace[token])+text[text.find('}%'+token+'%')+len('}%'+token+'%'):]
		else:
			print('error type:',token,'is type',type(replace[token]))
	return text

chapter_count=45
for c in range(1,chapter_count+1):
	print('\tconverting chapter #'+str(c))
	html=requests.get('https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/hillis2e_ch'+('0'+str(c))[-2:]+'_1.html').content.decode('utf-8')
	soup=BeautifulSoup(html,'html.parser')

	for i in soup.find_all(attrs={'data-pnlinktype':'ConceptLink'}):
		print('replaceing concept link:',i.get('data-href'),i.text)
		n=soup.new_tag('a',attrs={'class':'concept_link','target':'_blank'},href=
			('../../ch'+i.get('data-href')[i.get('data-href').rfind('ch')+2:i.get('data-href').rfind('_')].strip('0')+'/intro/intro.html'
				if i.get('data-href')[i.get('data-href').rfind('_')+1:i.get('data-href').rfind('.')]=='1' else
			'https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/'+i.get('data-href'))
		)
		n.string=i.text
		i.replace_with(n)
	for i in soup.find_all(attrs={'data-type':'termref'}):
		print('replaceing termref:',i.get('data-term'),i.text)
		n=soup.new_tag('a',attrs={'class':'term_definition','target':'_blank'},href='https://www.google.com/search?q='+i.text)
		n.string=i.text
		i.replace_with(n)
	for i in soup.find_all(attrs={'data-pnlinktype':'FigureLink'}):
		print('replaceing figure link:',i.get('data-href'),i.text)
		n=soup.new_tag('a',attrs={'class':'figure_link','target':'_blank'},href=
			'https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/'+i.get('data-href'))
		n.string=i.text
		i.replace_with(n)
	for i in soup.find_all(attrs={'data-block_type':'blockquote'}):
		print('replaceing blockquote')
		i.p.attrs={'class':'blockquote','id':i.get('id')}
		i.replace_with(i.p)
	for i in soup.find_all(attrs={'data-pntype':'nowrap'}):
		print('replacing nowrap:',i.text)
		i.attrs={'class':'no_wrap'}


	intro_info={
		'c': str(c),
		'c0': ('0'+str(c))[-2:],
		'chapter_title': soup.find(class_='section-title').span.text,
		'key_concepts': [
			{
				'concept_id': a.get('id').split('-')[-1],
				'concept_number': a.strong.text,
				'concept_title': a.text[a.text.find(' ')+1:]
			} for a in soup.find(attrs={'data-block_type':'concepts'}).find_all('p')
		],
		'img_src': soup.find(attrs={'data-block_type':'fig_chapter_opener'}).img.get('src'),
		'img_title': soup.find(attrs={'data-block_type':'fig_chapter_opener'}).img.get('src').split('/')[-1],
		'img_caption': soup.find(attrs={'data-type':'figure_text'}).span.decode_contents(),
		'paragraphs': [
			{
				'paragraph_text': ('<span class="first_letter">'+a.decode_contents()[0]+'</span>'+a.decode_contents()[1:]) if n==0 else a.decode_contents(),
				'paragraph_class': ' class="'+a.get('class')+'"' if a.get('class')!=None else '',
				'id': a.get('id').split('-')[-1]
			} for n,a in enumerate(soup.div.div.find_all('p',recursive=False))
		],
		'do_question': soup.find(attrs={'data-block_type':'question'})!=None
	}
	intro_info['question']={
		'question_text': soup.find(attrs={'data-block_type':'question'}).div.div.p.decode_contents(),
		'question_concept_number': intro_info['key_concepts'][-1]['concept_number'],
		'question_concept_id': intro_info['key_concepts'][-1]['concept_id']
	} if intro_info['do_question'] else {}
	intro_info['paragraphs'].sort(key = (lambda a:int(a['id'])))

	file=open('./intro.template','r',encoding='utf-8')
	template=file.read()
	file.close()

	os.makedirs(os.path.dirname(os.path.dirname(__file__)).replace('\\','/')+'/chapters/ch'+str(c)+'/intro', exist_ok=True)
	file=open(os.path.dirname(os.path.dirname(__file__)).replace('\\','/')+'/chapters/ch'+str(c)+'/intro/intro.html','w',encoding='utf-8')
	file.write(
		templateFill(template,
			replace=intro_info
		)
	)
	file.close()
	# #getting the intro image
	# ir=requests.get('https://www.macmillanhighered.com/BrainHoney/Resource/6716/digital_first_content/trunk/test/hillis2e/'+img[0], stream = True)
	# ir.raw.decode_content = True
	# im=Image.open(io.BytesIO(ir.content))
	# im.save(os.path.dirname(os.path.dirname(__file__)).replace('\\','/')+'/chapters/ch'+str(c)+'/intro/'+img[1])
	# im.close()
'''
2✔ 6✔ 10✔ 13✔ 16✔ 32✔ 36✔ 38 39✔
16:13.6
22:22.18
'''
