from bs4 import BeautifulSoup
import requests
import os

BASE_URL = 'https://www.indeed.com'

page_size = 50
current_page = 0

num_resumes = 1500

def get_url(current_page, page_size):
  url = BASE_URL + '/resumes'
  url = url + '?q=developer' #query
  url = url + '&co=US' #location
  url = url + '&start=' + str(current_page * page_size) #start
  return url

try:
  os.remove('resumes.txt')
except OSError:
  pass

count = 0
target = open('resumes.txt', 'a')
while num_resumes > 0:
  url = get_url(page_size, current_page)
  r = requests.get(url)
  soap = BeautifulSoup(r.content, "html.parser")

  for link in soap.find_all("a", "app_link"):
    resume_url = BASE_URL + link['href']
    r2 = requests.get(resume_url)
    soap2 = BeautifulSoup(r2.content, "html.parser")  
    try:
      for string in soap2.find(id="res_summary").strings:
        target.write(string.encode('UTF-8'))
        target.write('\n')
    except Exception:
      pass
    try:    
      for p in soap2.find_all('p', "work_description"):
        for string in p.strings:
          target.write(string.encode('UTF-8'))        
          target.write('\n')
    except Exception:
      pass
    print 'processing {}'.format(count)
    count += 1
    
  current_page += 1
  target.write('\n')
  global num_resumes
  num_resumes -= page_size
  print '{} resumes'.format(num_resumes)

target.close()
