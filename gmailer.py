import os
import sys
import json
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders


class Gmailer(object):
    '''
    Simple class that uses gmail to send emails.

    requires settings directory on init and will send emails using the
    send_email() method.
    '''

    def __init__(self, settings_dir):
        self.user, self.pwd = self.process_settings(settings_dir)

    def process_settings(self, sdir):
        '''
        Base function that loads/saves email user and pw settings file.

        if file does not exist saves a new json file in the
        supplied directory that a user should fill out.
        This is to avoid having sensitive information saved
        to the project directory. There are probably much more
        graceful ways to handle this.
        '''
        home_dir = os.path.expanduser("~")
        settings_dir = os.path.join(home_dir, sdir)
        settings_file = os.path.join(settings_dir, 'settings.json')

        try:
            with open(settings_file, 'r') as sf:
                settings = json.load(sf)
                email = settings['email']
                password = settings['password']
                if email == '' or password == '':
                    raise KeyError
            return email, password
        except IOError:
            if not os.path.isdir(settings_dir):
                os.mkdir(settings_dir)
            with open(settings_file, 'w') as sf:
                json.dump({'email': '', 'password': ''}, sf, indent=4)
            sys.exit('\n\nNew settings file created. {}\nPlease edit your settings file, and rerun script.\n\n'.format(settings_file))
        except KeyError:
            sys.exit('\n\nPlease recheck your settings file or delete if formatting is incorect.\n\n')

    def send_email(self, to, subject, text, attach=None):
        msg = MIMEMultipart()

        msg['From'] = self.user
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
        mailServer.login(self.user, self.pwd)
        mailServer.sendmail(self.user, to, msg.as_string())
        mailServer.close()
