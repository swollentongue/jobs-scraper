import requests
from bs4 import BeautifulSoup

baseurl = 'http://www.indeed.com/jobs'
payload = {'q': 'data', 'l': 'Oakland, CA', 'fromage': 1}

r = requests.get(baseurl, params=payload)
r.test
r.text
rbs = bs(r, 'lxml')
soup = BeautifulSoup(r, 'lxml')
r.text
soup = BeautifulSoup(r, 'lxml')
soup = BeautifulSoup(r.html, 'lxml')
soup = BeautifulSoup(r.text, 'lxml')
soup.find('body')
results = soup.find(id='resultsCol')
results
results.findAll('div', {'class': '  row  result'}
)
job_posts = results.findAll('div', {'class': '  row  result'}
)
job_posts[0]
first_job = job_posts[0]
first_job
first_job.title
first_job.h1
first_job.find(class='title')
first_job.find({'class':'title')

})
first_job.find({'class':'title'})
first_job.find({'class':'title'}).text
first_job.find({'class':'jobtitle'}).text
first_job.find({'class':'jobtitle'})
first_job.h2
first_job.find(h2, {'class':'jobtitle'})
first_job.find('h2', {'class':'jobtitle'})
first_job.find('h2', {'class':'jobtitle'}).test
first_job.find('h2', {'class':'jobtitle'}).text
first_job.find('h2', {'class':'jobtitle'}).text.strip()
first_job.find('span', {'class':'company'}).text.strip()
first_job.find('h2', {'class':'jobtitle'}).a
first_job.find('h2', {'class':'jobtitle'}).a.url
first_job.find('h2', {'class':'jobtitle'}).a.text
first_job.find('h2', {'class':'jobtitle'}).a.get('href')
first_job.find('h2', {'class':'jobtitle'}).a.href
first_job.find('h2', {'class':'jobtitle'}).a.get('href')
def parse_jobpost(posting):
    '''Expects a bs4 object, returns dictionary respresntation of listing'''
    res = {}
    title = posting.find('h2', {'class': 'jobtitle'})
    res['title'] = title.text
    res['url'] = title.a.get('href')
    res['snippet'] = posting.find('span', {'class': 'summary'}).text
    res['company'] = posting.find('span', {'class': 'company'}).text
    return res
parse_jobpost(first_job)
def parse_jobpost(posting):
    '''Expects a bs4 object, returns dictionary respresntation of listing'''
    res = {}
    title = posting.find('h2', {'class': 'jobtitle'}).strip()
    res['title'] = title.text
    res['url'] = title.a.get('href')
    res['snippet'] = posting.find('span', {'class': 'summary'}).text.strip()
    res['company'] = posting.find('span', {'class': 'company'}).text.strip()
    return res
parse_jobpost(first_job)
def parse_jobpost(posting):
    '''Expects a bs4 object, returns dictionary respresntation of listing'''
    res = {}
    title = posting.find('h2', {'class': 'jobtitle'})
    res['title'] = title.text.strip()
    res['url'] = title.a.get('href')
    res['snippet'] = posting.find('span', {'class': 'summary'}).text.strip()
    res['company'] = posting.find('span', {'class': 'company'}).text.strip()
    return res
parse_jobpost(first_job)
def parse_jobpost(posting):
    '''Expects a bs4 object, returns dictionary respresntation of listing'''
    res = {}
    title = posting.find('h2', {'class': 'jobtitle'})
    res['title'] = title.text.strip()
    res['url'] = 'http://www.indeed.com' + title.a.get('href')
    res['snippet'] = posting.find('span', {'class': 'summary'}).text.strip()
    res['company'] = posting.find('span', {'class': 'company'}).text.strip()
    return res
parse_jobpost(first_job)
for job in job_posts:
    print(parse_jobpost(job))
for job in job_posts:
    parsed = parse_jobpost(job)
    if re.search(r'data analyst', parsed['title'], re.I):
        print parsed['title']
import re
for job in job_posts:
    parsed = parse_jobpost(job)
    if re.search(r'data analyst', parsed['title'], re.I):
        print parsed['title']
%history
%history > indeed_parser.py
pwd
%history indeed_parser.py
%history -f indeed_parser.py
