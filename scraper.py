import requests
import argparse
import string
import json
from bs4 import BeautifulSoup

"""
This is a web scraper that is built to scrape basic information from a Mayo Clinic page
To use the scraper, run 'python scraper.py --url {Mayo Clinic Disorder URL}'
"""

def main(args):
  base_url = "https://www.mayoclinic.org"
  data = {}
  data["Id"] = {}
  data["Condition"] = {}
  data["Overview"] = {}
  data["Symptoms"] = {}
  data["Causes"] = {}
  data["Diagnosis"] = {} 
  data["Treatments"] = {}

  overview_page = requests.get(base_url + args.overview_url)
  overview_soup = BeautifulSoup(overview_page.content, 'html.parser')
  assert overview_page.status_code == 200
  symptoms_url = overview_soup.findAll("a", {"class": "fwd"})[0]['href']
  symptoms_page = requests.get(base_url + symptoms_url)
  symptoms_soup = BeautifulSoup(symptoms_page.content, 'html.parser')
  assert symptoms_page.status_code == 200


  data["Id"]["N"] = args.id
  title = overview_soup.find('title').text
  data["Condition"]["S"] = "".join([x + " " for x in title.split("-")[0].split()])

  h2 = overview_soup.article.find_all('h2')

  data["Overview"]["S"] = h2[0].nextSibling.text

  ul = h2[1].nextSibling.nextSibling.nextSibling
  if ul.name != 'ul':
    data["Symptoms"]["S"] = h2[1].nextSibling.text
  else:
    symptoms = [li for li in ul]
    symptoms = [x.strong.text.strip(string.punctuation) if x.strong is not None else
        x.text.strip(string.punctuation) for x in symptoms[1::2]]
    data["Symptoms"]["S"] = "".join([x + ", " for x in symptoms])[:-2]

  ul = h2[2].nextSibling.nextSibling.nextSibling
  if ul.name != 'ul':
    data["Causes"]["S"] = h2[2].nextSibling.text
  else:
    causes = [li for li in ul]
    causes = [x.strong.text.strip(string.punctuation) if x.strong is not None else
        x.text.strip(string.punctuation) for x in causes[1::2]]
    data["Causes"]["S"] = "".join([x + ", " for x in causes])[:-2]

  ul = symptoms_soup.article.find_all('ul')
  diagnosis = [li for li in ul[0]]
  diagnosis = [x.strong.text.strip(string.punctuation) if x.strong is not None else
      x.text.strip(string.punctuation) for x in diagnosis[1::2]]
  treatment = [li for li in ul[1]]
  treatment = [x.strong.text.strip(string.punctuation) if x.strong is not None else
      x.text.strip(string.punctuation) for x in treatment[1::2]]
  data["Diagnosis"]["S"] = "".join([x + ", " for x in diagnosis])[:-2]
  data["Treatments"]["S"] = "".join([x + ", " for x in treatment])[:-2]

  with open(args.output_file, "w") as f:
    json.dump(data, f)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--id', type=str,
                      required=True,
                      help='Id to use in table. Required')
  parser.add_argument('--overview_url', type=str,
                      required=True,
                      help='Mayo Clinic Overview URL to scrap data from. Required')
  parser.add_argument('--output_file', type=str,
                      required=True,
                      help='File to output json to. Required')
  args = parser.parse_args()
  main(args)
