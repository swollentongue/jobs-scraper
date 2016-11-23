import re
import time
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from craigslist import CraigslistJobs


gmail_user = "EMAIL_ADDRESS"
gmail_pwd = "PASSWORD"
email_announce = [] # add who you want to recieve updates
job_list = []
job_kws = ('environmental', 'environment', 'laboratory', 'lab', 'biotech', 'bio tech', 'bio-tech')

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
    msg['CC'] = gmail_user
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
    # probably should generalize this to take a list of sites and search queries
    cl_water = CraigslistJobs(site='sfbay', filters={'query':'water', 'posted_today':'1'})
    cl_waterjobs_generator = cl_water.get_results(sort_by='newest')
    cl_waterjobs = [i for i in cl_waterjobs_generator]

    for job in cl_waterjobs:
        if filter_title(job['name']):
            job_info = [job['name'], job['where'], job['url']]
            job_list.append(job_info)

    email_msg = ''
    for job in job_list:
        email_msg += "{}\n({})\n{}\n\n".format(*job)

    for email in email_announce:
        mail(email, 'Water Jobs for {}'.format(time.strftime("%x")), email_msg)