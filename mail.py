import imaplib, smtplib
import os, dotenv
from email import message_from_bytes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from utils import *
# import logging

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

USERNAME = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
MAIL_ADDRESS = os.environ["MAIL_ADDRESS"]
KEY = os.environ["KEY"]
IMAP_SERVER = os.environ["IMAP_SERVER"]
IMAP_PORT = os.environ["IMAP_PORT"]
SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = os.environ["SMTP_PORT"]

def read_mail(num_of_mail='all', search_criteria='(UNSEEN SUBJECT "{}")'.format(KEY), mail_box="INBOX"):
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(USERNAME, PASSWORD)
    imap.select(mail_box)
    status, mail_ids = imap.search(None, search_criteria)
    if status != 'OK':
        print("Error searching mail")
        return
    received_mails = []
    mail_ids = mail_ids[0].split()
    if num_of_mail == 'all':
        num_of_mail = len(mail_ids)
    for id in mail_ids[-num_of_mail:]:
        status, mail = imap.fetch(id, "(RFC822)")
        # imap.store(id, '+FLAGS', '\\Seen')
        if status != 'OK':
            print("Error fetching mail")
            return
        mail = message_from_bytes(mail[0][1])
        received_mails.append(mail)
    imap.close()
    imap.logout()
    return received_mails

def create_mail(receiver=None, subject=None, plain_content=None, html_content=None, attachments=None, original=None):
    mail = MIMEMultipart('alternative')
    if original is not None:
        mail['References'] = mail['In-Reply-To'] = original['Message-ID']
        mail['Subject'] = subject or 'Re: ' + original['Subject']
        mail['From'] = MAIL_ADDRESS
        mail['To'] = original['Reply-To'] or original['From']
    else:
        if receiver is not None:
            mail['Subject'] = subject or 'A mail with out from {}'.format(MAIL_ADDRESS)
            mail['From'] = MAIL_ADDRESS
            mail['To'] = receiver
        else:
            print('No receiver')
            return
    if plain_content is not None:
        mail.attach(MIMEText(plain_content, 'plain'))
    if html_content is not None:
        mail.attach(MIMEText(html_content, 'plain'))
    if attachments is not None:
        for file_path in attachments:
            with open(file_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
            part['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(file_path))
            mail.attach(part)
    return mail
def send_mail(mail):
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    smtp.login(USERNAME, PASSWORD)
    smtp.sendmail(mail['From'], mail['To'], mail.as_string())
    smtp.quit()

mails = read_mail()
send_mail(create_mail(plain_content='hahahhhaa', original=mails[0]))
