from bs4 import BeautifulSoup
import re
import sys
import requests
import os

try:
  os.remove('links.txt')
except OSError:
  pass

page_size = 25
current_page = 0
total_results = 9999

def get_url(page_size=25, current_page=0):
  url = 'http://api.indeed.com/ads/apisearch?publisher=3466392261750798'
  url = url + '&v=2' #version
  url = url + '&q=developer' #query
  url = url + '&st=jobsite' #only jobs site
  url = url + '&limit=' + str(page_size) #limit
  url = url + '&start=' + str(current_page * page_size) #start
  # url = url + '&co=ca'  #country
  return url

def download_pages(url):
  r = requests.get(get_url(page_size, current_page))  
  soups = BeautifulSoup(r.content, "html.parser")
  global total_results
  if total_results == 9999:
    total_results = int(soups.totalresults.string)

  target = open('links.txt', 'a')
  for result in soups.find_all('result'):
    target.write(result.url.string)
    target.write('\n')
  target.close()


while total_results > 0:
  download_pages(get_url(page_size, current_page))
  global total_results
  total_results -= page_size
  current_page += 1
  print '{} jobs'.format(total_results)


try:
  os.remove('jobs_descriptions.txt')
except OSError:
  pass

count = 0
file = open('links.txt', "r")
for line in file:
  print 'processing {}'.format(str(count))
  count += 1
  r = requests.get(line)
  soups = BeautifulSoup(r.content, "html.parser")
  f = open('jobs_descriptions.txt', 'a')
  for tags in soups.find_all('span'):
    str1='summary'
    str2=tags.get('class')
    if str2 and str1 in str2:
      for string in tags.strings:
        f.write(string.encode('utf-8'))
  f.write('\n')
  f.close()
      