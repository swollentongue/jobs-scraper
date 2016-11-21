import re
import requests
from bs4 import BeautifulSoup



def parse_jobpost(filter, locs=['Oakland, CA'], num_pages=5, ):
    '''Scrapes indeed, yields dictionary respresentations of listings'''
    baseurl = 'http://www.indeed.com/jobs'
    for search_term in filter.keys()
    for i+1 in in range(num_pages):


        res = {}
        title = posting.find('h2', {'class': 'jobtitle'})
        res['title'] = title.text.strip()
        res['url'] = 'http://www.indeed.com' + title.a.get('href')
        res['snippet'] = posting.find('span', {'class': 'summary'}).text.strip()
        res['company'] = posting.find('span', {'class': 'company'}).text.strip()
        yield res

if __name__ == '__main__':
    r = requests.get(baseurl, params=payload)
    soup = BeautifulSoup(r.text, 'lxml')
    job_posts = soup.find(id='resultsCol').findAll('div', {'class': '  row  result'}
)

    for job in job_posts:
        parsed = parse_jobpost(job)
        if re.search(r'data analyst', parsed['title'], re.I):
            print parsed['title'], parsed['company']