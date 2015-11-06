'''
Author: swollentongue (at) gmail.com
Date Dec, 2015

Simple water and wastewater laboratory jobs scraper. 

TODO:
* Add CWEA, Government Jobs and Indeed scrapers
* generalize scraper into it's own class (or at least modularize the the scrapers into their own classes)
* Add more robust decision logic for which jobs to choose (perhaps using the posted job description)

'''

import random
import time
import os
import re
import smtplib
from craigslist import CraigslistJobs
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

def scrape_cljobs(search_terms, places=['sfbay', 'eugene', 'seattle', 'boise', 'slo', 'monterey']):
    for place, term in [(place, term) for place in places for term in search_terms]:
        time.sleep(random.randrange(1,10)) # throttle requests
        print 'Searching: {} for {}'.format(place, term)
        cl_jobsearch = CraigslistJobs(site=place, filters={'query':term, 'posted_today':'1'})
        cl_jobs_generator = cl_jobsearch.get_results(sort_by='newest')
        cl_jobs = [i for i in cl_jobs_generator]
        print 'number of results: {}'.format(str(len(cl_jobs)))
        for job in cl_jobs:
            job_title = job['name'].encode('utf-8')
            print 'checking: {}'.format(job_title)
            if filter_title(job_title):
                job_info = [job_title, job['where'], job['url']]
                job_list.append(job_info)
            seen_titles.add("{} {}".format(job_title, job['url']))

def scrape_cwea():
    
    
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
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

if __name__ == '__main__':
    gmail_user = "EMAIL_ADDRESS"
    gmail_pwd = "PASSWORD"
    job_list = []
    seen_titles = set()
    job_kws = ('environmental', 'environment', 'laboratory', 'lab', 'biotech', 'bio tech', 'bio-tech')
    # scrape_cljobs(['water', 'wastewater'])
    scrape_cwea()

    email_msg = ''
    for job in job_list:
        email_msg += "{}\n({})\n{}\n\n".format(*job)
    # mail('swollentongue@gmail.com, cmgenualdi@gmail.com', 'test email', email_msg)
    print email_msg