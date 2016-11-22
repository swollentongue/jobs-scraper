import re
import requests
from bs4 import BeautifulSoup

def build_regex_from_list(filter_list):
    '''Takes list of strings, returns an inclusive regex object from a list of strings'''
    regex_string = '|'.join(filter_list)
    return re.compile(regex_string, re.I)

def parse_jobs(filter, locs=['Oakland, CA'], num_pages=5, title_only=True):
    '''Scrapes indeed, yields dictionary respresentations of listings'''
    baseurl = 'http://www.indeed.com/jobs'

    for search_term, filter_items in filter.items():
        regex_filter = build_regex_from_list(filter_items)
        payload = {'as_ttl': search_term, 'l': 'Oakland, CA', 'fromage': 1, 'limit': 50, 'psf': 'advsrch'}
        r = requests.get(baseurl, params=payload)
        soup = BeautifulSoup(r.text, 'lxml')
        job_posts = soup.find(id='resultsCol').findAll('div', {'class': '  row  result'})

        for posting in job_posts:
            title = posting.find('h2', {'class': 'jobtitle'})
            if regex_filter.search(title.text):
                res =  {}
                res['title'] = title.text.strip()
                res['url'] = 'http://www.indeed.com' + title.a.get('href')
                res['snippet'] = posting.find('span', {'class': 'summary'}).text.strip()
                res['company'] = posting.find('span', {'class': 'company'}).text.strip()
                yield res

if __name__ == '__main__':
    for job in parse_jobs({'data': ['data analyst', 'data engineer', 'data quality']}):
        print '\n'.join([job['title'], job['company'], job['url']]) + '\n'
