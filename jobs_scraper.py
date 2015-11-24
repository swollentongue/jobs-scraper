'''
Author: swollentongue (at) gmail.com
Date: Dec, 2015

Simple water and wastewater laboratory jobs scraper.

TODO:
* create functionality for saving/ignoring seen jobs -- done somewhat
* refactor scrapers into their own subclasses
* Add Government Jobs and Indeed scrapers
* Add more robust decision logic for which jobs to choose
    (perhaps using the posted job description)

'''

import random
import time
import io
import os
import re
import requests
import sys
from bs4 import BeautifulSoup
from craigslist import CraigslistJobs
from indeed import IndeedClient


class JobsScraper(object):
    def __init__(self, search_terms, matching_terms):
        self.matching_terms = set(matching_terms)
        self.search_terms = search_terms
        home_dir = os.path.expanduser("~")
        self.settings_dir = os.path.join(home_dir, '.jobs-scraper')

        # Create the default settings directory on init
        try: 
            os.makedirs(self.settings_dir)
        except OSError:
            if not os.path.isdir(self.settings_dir):
                raise

    def scrape_jobs(self, indeed_api_key, ip_address):
        job_list = []
        job_list += self.scrape_cl()
        job_list += self.scrape_cwea()
        job_list += self.scrape_indeed(indeed_api_key, ip_address)
        return job_list

    def load_titles(self, tfile):
        title_filename = os.path.join(self.settings_dir, tfile)
        try:
            with io.open(title_filename, 'r', encoding='utf-8') as fr:
                return set([line.strip() for line in fr])
        except IOError:
            return set()

    def save_titles(self, tfile, titles):
        sdir = self.settings_dir
        title_filename = os.path.join(sdir, tfile)

        with io.open(title_filename, 'w') as fw:
            for title in titles:
                fw.write(unicode(title) + '\n')

    def get_ngrams(self, text, ngram_range=(1, 3)):
        '''
        Takes a list of words and returns a list of ngrams
        within the ngram range.
        '''
        total_ngrams = []
        for ngram_length in range(*ngram_range):
            ngrams = zip(*[text[i:] for i in range(ngram_length)])
            ngram_strings = [" ".join(i) for i in ngrams]
            total_ngrams += ngram_strings
        return total_ngrams

    def filter_title(self, title):
        title = re.sub(r'[\W_-]', ' ', title)
        tokens = title.strip().lower().split()
        ngrams = self.get_ngrams(tokens)
        for ngram in ngrams:
            if ngram in self.matching_terms:
                return True
        return False

    def scrape_cl(self, places=None):
        '''
        Scrapes multiple CL sites for a list of jobs
        Requires python-craigslist -- CraigslistJobs class
        '''
        if not places:
            places = ['sfbay', 'sacramento', 'slo', 'mendocino', 'humboldt', 'eugene', 'portland', 'seattle', 'spokane', 'bellingham', 'boise',  'monterey', 'austin', 'minneapolis', 'raleigh', 'chicago']

        cl_matched_jobs = []
        seen_titles = set()

        for place, term in [(place, term)
                            for place in places
                            for term in self.search_terms]:
            time.sleep(random.randrange(1, 10))  # throttle requests

            sys.stderr.write('Searching {} Craigslist for {}...'.format(place, term))
            cl_jobsearch = CraigslistJobs(site=place,
                                          filters={'query': term,
                                                   'posted_today': '1'})
            cl_jobs_generator = cl_jobsearch.get_results(sort_by='newest')
            cl_jobs = [i for i in cl_jobs_generator]
            sys.stderr.write('\t*Found {} items\n'.format(str(len(cl_jobs))))

            for job in cl_jobs:
                job_title = job['name'].encode('utf-8')
                # check for seen titles
                if job_title not in seen_titles:
                    if self.filter_title(job_title):
                        job_info = [job_title, job['where'], job['url']]
                        cl_matched_jobs.append(job_info)
                    seen_titles.add(job_title)

        return cl_matched_jobs

    def scrape_cwea(self):
        '''
        scrapes the cwea website for jobs
        TODO : save and check against seen titles
        '''
        matched_jobs = []

        base_url = 'http://cwea.org'
        cwea_jobpage = requests.get(base_url + '/e-bulletin/jobs.cfm').text
        cwea_soup = BeautifulSoup(cwea_jobpage, 'html.parser')
        seen_jobs = self.load_titles('cwea_jobs')
        jobs = cwea_soup.find_all('td', {"class": "body_text_med"})
        id_re = re.compile(r'([0-9]+)$')

        for job in jobs:
            try:
                link = job.find('a')
                full_title = link.text.encode('utf-8')
                job_id = id_re.search(link.get('href')).group(1)

                if job_id not in seen_jobs:
                    seen_jobs.add(job_id)
                    if self.filter_title(full_title.rstrip().split('\n')[0]):
                        title = full_title.rstrip().replace('\n', ' ')
                        where = job.find('b').text.lstrip('(')
                        link_url = base_url + link.get('href')
                        # should probably make this a dict to standardize things
                        matched_jobs.append([title, where, link_url])
            except AttributeError:
                pass

        self.save_titles('cwea_jobs', seen_jobs)
        return matched_jobs

    def scrape_indeed(self, api_key, ip_address, places=None):
        indeed_client = IndeedClient(api_key)
        indeed_matched_jobs = []
        seen_jobs = self.load_titles('indeed_jobs')

        if not places:
            places = ['oakland, ca', 'sacramento, ca', '' 'eugene, or', 'seattle, wa', 'boise, id', 'san luis obispo, ca', 'austin, tx', 'minneapolis, mn', 'chicago, il']

        for place, term in [(place, term)
                            for place in places 
                            for term in self.search_terms]:
            sys.stderr.write('Searching {} Indeed for {}... '.format(place, term))
            # time.sleep(random.randrange(1, 3))  # throttle requests
            params = {
                'q': term,
                'l': place,
                'userip': ip_address,
                'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
                'limit': 25 }
            search_response = indeed_client.search(**params)
            job_results = search_response['results']
            sys.stderr.write('returned {} items\n'.format(len(job_results)))

            for job in job_results:
                job_id = job['jobkey']
                if job_id not in seen_jobs:
                    seen_jobs.add(job_id)
                    job_title = job['jobtitle']
                    if self.filter_title(job_title):
                        indeed_matched_jobs.append([
                            job_title, job['formattedLocationFull'], job['url'], job['snippet']])

        self.save_titles('indeed_jobs', seen_jobs)
        return indeed_matched_jobs


if __name__ == '__main__':
    js = JobsScraper(['water', 'wastewater'],
                     ['environmental', 'environment', 'laboratory',
                      'lab', 'biotech', 'bio tech', 'bio-tech',
                       'chemist'])
    jobs = js.scrape_jobs()
    for job in jobs:
        print ' | '.join(job)