from gmailer import Gmailer

if __name__ == '__main__':
    e = Gmailer('.jobs-scraper')
    e.send_email('swollentongue@gmail.com', 'testing', 'test message')