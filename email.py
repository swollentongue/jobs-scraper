import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

class Email(object):
    '''
    Simple email class.

    requires gmail credentials on init and will send emails using the
    send_email() method.
    '''
    def __init__(self, email_address, password):
        self.user = email_address
        self.pwd = password

        def send_email(to, subject, text, attach=None):
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
