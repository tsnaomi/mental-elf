from __future__ import print_function
import requests
import argparse
from bs4 import BeautifulSoup
import argparse

def main(args):
  page = requests.get(args.url)
  assert page.status_code == 200
  soup = BeautifulSoup(page.content, 'html.parser')
  print("Overview:", end=' ')
  print(soup.article.find_all('h2')[0].nextSibling.text)
  print("Symptoms:", end=' ')
  print(soup.article.find_all('h2')[1].nextSibling.text)
  print("Causes:", end=' ')
  print(soup.article.find_all('h2')[2].nextSibling.text)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--url', type=str,
                      required=True,
                      help='Mayo Clinic URL to scrap data from. Required')
  args = parser.parse_args()
  main(args)
