'''
Author: swollentongue (at) gmail.com
Date: Dec, 2015

Simple water and wastewater laboratory jobs scraper.

TODO:
* Add Government Jobs and Indeed scrapers
* generalize scraper into it's own class (or at least modularize
    the scrapers into their own classes)
* Add more robust decision logic for which jobs to choose
    (perhaps using the posted job description)

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


class JobsScraper(object):
    def __init__(self):

class CLJobsScraper(JobsScraper):
    def __init__(self):
        super(CLJobsScraper, self).__init__()

class CWEAJobsScraper(JobsScraper):
    def __init__(self):
        super(CWEAJobsScraper, self).__init__()

class IndeedJobsScraper(JobsScraper):
    def __init__(self):
        super(IndeedJobsScraper, self).__init__()