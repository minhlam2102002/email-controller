import imaplib
import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import os
import smtplib
import dotenv
from matplotlib.pyplot import prism
from utils import *
# import logging

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

USERNAME = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
MY_EMAIL = os.environ["MY_EMAIL"]
KEY = os.environ["KEY"]
IMAP_SERVER = os.environ["IMAP_SERVER"]
IMAP_PORT = os.environ["IMAP_PORT"]
SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = os.environ["SMTP_PORT"]
EMAIL_LOG_FOLDER = 'logs'
ATTACHMENT_FOLDER = os.path.join(EMAIL_LOG_FOLDER, 'attachments')
# LOG_FILE = os.path.join(EMAIL_LOG_FOLDER, "log.txt")
# LOG_FILE_LENGTH = 40

def read_email(num_of_mail=5, search_criteria='(UNSEEN SUBJECT "{}")'.format(KEY), mail_box="INBOX"):
    # search_criteria: https://afterlogic.com/mailbee-net/docs/MailBee.ImapMail.Imap.Search_overload_2.html
    # mailbox: https://docs.python.org/3/library/imaplib.html#imaplib.IMAP4.select
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(USERNAME, PASSWORD)
    # print("Logged in successfully!")
    # login each time because if a new mail has been sent AFTER the imap is created, it is not being fetched.
    imap.select(mail_box)
    status, messages = imap.search(None, search_criteria)
    if status != 'OK':
        print("Error searching mail")
        return
    mail_recieved = []
    messages = messages[0].split()
    for id in messages[-num_of_mail:]:
        res, msg = imap.fetch(id, "(RFC822)")
        # imap.store(id, '+FLAGS', '\\Seen')
        if res != 'OK':
            print("Error fetching mail")
            return
        mail_recieved.append(msg)
    imap.close()
    imap.logout()
    return mail_recieved
def reply_email(headers, text, html='', original=None):
    msg = MIMEMultipart('mixed')
    body = MIMEMultipart('alternative')
    for key, value in headers.items():
        msg[key] = value
    if original is not None:
        msg['In-Reply-To'] = original['Message-ID']
        msg['References'] = original['Message-ID']
        msg['Subject'] = 'Re: ' + original['Subject']
        msg['From'] = MY_EMAIL
        msg['To'] = original['Reply-To'] or original['From']
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))
    body.attach(MIMEText(text, 'plain'))
    if html is not None and html != '':
        body.attach(MIMEText(html, 'html'))
    msg.attach(body)