import requests
import argparse
from bs4 import BeautifulSoup

def scrape(url):
	page = requests.get(url)
	assert page.status_code == 200
	soup = BeautifulSoup(page.content, 'html.parser')
	print("Overview: " + soup.article.find_all('h2')[0].nextSibling.text)
	print("Symptoms: " + soup.article.find_all('h2')[1].nextSibling.text)
	print("Causes: " + soup.article.find_all('h2')[2].nextSibling.text)

def crawl(url, disorder):
	base = 'https://www.mayoclinic.org'
	response = requests.get(url)
	data = response.text
 
	# Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
	soup = BeautifulSoup(data, 'lxml')
	 
	# Extracting all the <a> tags into a list.
	tags = soup.find_all('a')
	 
	# Extracting URLs from the attribute href in the <a> tags.
	for tag in tags:
		tag = tag.get('href')
		if tag != None:
			if disorder in tag :
				print(base+tag)
				return base+tag
	return ''

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--disorder', nargs='*', type= str, default = ['bipolar','disorder'])
	args = parser.parse_args()
	dis = args.disorder
	if len(dis) > 1:
		dis = '-'.join(dis) # converts list to string
	else:
		dis = dis[0] # get string from list of size one
	letter = dis[0].upper()
	base_url = 'https://www.mayoclinic.org/diseases-conditions/index?letter=' + letter
	dis_url = crawl(base_url, dis)
	if dis_url != '':
		scrape(dis_url)
	else: print('disorder not found')
