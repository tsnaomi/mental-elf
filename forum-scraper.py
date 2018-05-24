import requests, argparse, lxml, pdb, re
from bs4 import BeautifulSoup

urls_dict = dict()

names = ['selective mutism', 'O.C.D.','S.A.D.','depression', 'P. T. S. D.','panic attacks','body dismorphia','bulimia','multiple personality disorder','post-partum depression']
urls = ['https://www.depressionforums.org/forums/topic/15718-selective-mutism/','https://www.depressionforums.org/forums/topic/72578-what-type-of-ocd-do-you-have/','https://www.depressionforums.org/forums/topic/126593-seasonal-affective-disorder-sad/','https://www.depressionforums.org/forums/topic/5812-dysthymic-disorder-chronic-depression/','https://www.depressionforums.org/forums/topic/113459-p-t-s-d-post-traumatic-stress-disorder-its-not-just-veterans/','https://www.depressionforums.org/forums/topic/95459-panic-anxiety-attacks/','https://www.depressionforums.org/forums/topic/28775-body-dysmorphic-disorder/','https://www.depressionforums.org/forums/topic/11725-binge-eating/','https://www.depressionforums.org/forums/topic/4759-dissociative-identity-disorder-did/?page=3','https://www.depressionforums.org/forums/topic/7367-post-partum-depression-ppd/']

def main(url,condition):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'lxml')
	matches = soup.find_all('div', class_='cPost_contentWrap ipsPad')
	texts = []
	for match in matches:
		text = match.find_all('p')[1:]
		texts.append(text)
	paragraphs = []
	for t in texts:
		# trying to cut out mention
		new_t = ''.join([a.get_text() for a in t])
		new_t = new_t.replace(r'[\r\n\t]+','')
		paragraphs.append(new_t)
	d = dict()
	d[condition]=paragraphs
	return (d)

def process_all ():
	global urls_dict
	fulld = dict()
	for i in range(len(names)):
		fulld.update(main(urls[i],names[i]))
		print 'done with one'


	return (fulld)

process_all()
