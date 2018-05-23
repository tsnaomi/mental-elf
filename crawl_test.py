import requests
import argparse
from bs4 import BeautifulSoup

def crawl(url, disorder):
	base = 'https://www.mayoclinic.org'
	response = requests.get(url)
	data = response.text
        disorder = disorder.lower()
 
	# Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
	soup = BeautifulSoup(data, 'lxml')
	 
	# Extracting all the <a> tags into a list.
	tags = soup.find_all('a')
	 
	# Extracting URLs from the attribute href in the <a> tags.
	for tag in tags:
		tag = tag.get('href')
		if tag != None:
			if disorder in tag :
				return tag
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
	print(crawl(base_url, dis))
