'''
Author: swollentongue (at) gmail.com
Date: Dec, 2015

Simple water and wastewater laboratory jobs scraper. 

TODO:
* Add Government Jobs and Indeed scrapers
* generalize scraper into it's own class (or at least modularize the the scrapers into their own classes)
* Add more robust decision logic for which jobs to choose (perhaps using the posted job description)

'''

import random
import time
import os
import re
import smtplib
import requests
from bs4 import BeautifulSoup
from craigslist import CraigslistJobs
from urlparse import urljoin
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

def scrape_cljobs(search_terms, places=['sfbay', 'eugene', 'seattle', 'boise', 'slo', 'monterey']):
    '''
    Scrapes multiple CL sites for a list of jobs
    
    Requires python-craigslist
    
    TODO: modularize within a scrape object
    '''
    cl_matched_jobs = []
    seen_titles = set()
    
    for place, term in [(place, term) for place in places for term in search_terms]:
        time.sleep(random.randrange(1,10)) # throttle requests

        cl_jobsearch = CraigslistJobs(site=place, filters={'query':term, 'posted_today':'1'})
        cl_jobs_generator = cl_jobsearch.get_results(sort_by='newest')
        cl_jobs = [i for i in cl_jobs_generator]

        for job in cl_jobs:
            job_title = job['name'].encode('utf-8')
            if job_title not in seen_titles: # check for seen titles
                if filter_title(job_title):
                    job_info = [job_title, job['where'], job['url']]
                    cl_matched_jobs.append(job_info)
                seen_titles.add(job_title) 
            
    return cl_matched_jobs

def scrape_cwea():
    '''
    scraper for the cwea website
    
    TODO : save and check against seen titles
           modularize within scraper object
    '''
    cwea_jobs = []
    matched_jobs = []
    
    base_url = 'http://cwea.org'
    cwea_jobpage = requests.get(urljoin(base_url, '/e-bulletin/jobs.cfm')).text
    cwea_soup = BeautifulSoup(cwea_jobpage, 'html.parser')
    jobs = cwea_soup.find_all('td', {"class":"body_text_med"})

    print cwea_jobpage
    
    for job in jobs:
        try:
            link = job.find('a')
            full_title = link.text
            if filter_title(full_title.rstrip().split('\n')[0]):
                title = full_title.rstrip().replace('\n', ' ')
                link = urljoin(base_url, link.get('href'))
                print link
                where = job.find('b').text.lstrip('(')
                matched_jobs.append([title, where, link]) # should probably make this a dict to standardize things
        except AttributeError:
            pass
    return matched_jobs

def get_ngrams(text, ngram_range=(1, 3)):
    '''
    Takes a list of words and returns a list of ngrams within the ngram range.
    '''
    total_ngrams = []
    for ngram_length in range(*ngram_range):
        ngrams = zip(*[text[i:] for i in range(ngram_length)])
        ngram_strings = [" ".join(i) for i in ngrams]
        total_ngrams += ngram_strings
    return total_ngrams
    
def filter_title(title):
    title = re.sub(r'[\W_-]', ' ', title)
    tokens = title.strip().lower().split()
    ngrams = get_ngrams(tokens)
    for ngram in ngrams:
        if ngram in job_kws:
            return True
    return False

def mail(to, subject, text, attach=None):
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    if attach:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
               'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()

def save_settings(filename, path):

def load_settings(filename, path):

if __name__ == '__main__':
    # variables that need to be off-loaded to a settings.json file
    gmail_user = "EMAIL_ADDRESS"
    gmail_pwd = "PASSWORD"
    
    # Local variables
    job_list = []
    job_kws = ('environmental', 'environment', 'laboratory', 'lab', 'biotech', 'bio tech', 'bio-tech', 'chemist')
    
    # Run scrapers
    # job_list += scrape_cljobs(['water', 'wastewater'], ['sfbay'])
    job_list += scrape_cwea()

    # Compose and Email list of matched jobs
    email_msg = ''
    for job in job_list:
        email_msg += "{}\n({})\n{}\n\n".format(*job)
    # mail('EMAIL ADDRESS', 'test email', email_msg)
    print email_msg