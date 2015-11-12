from jobs_scraper import JobsScraper
from gmailer import Gmailer

email_msg = ''
email_address = 'email@email.com'

js = JobsScraper(['water', 'wastewater'],
                 ['environmental', 'environment', 'laboratory',
                  'lab', 'biotech', 'bio tech', 'bio-tech',
                  'chemist'])
e = Gmailer('.jobs-scraper')

job_list = js.scrape_jobs()
# for job in jobs:
#     print ' | '.join(job)
for job in job_list:
    email_msg += "{}\n({})\n{}\n\n".format(*job)

e.send_email(email_address, 'Water Jobs for Today', email_msg)
print email_msg
