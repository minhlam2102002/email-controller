import imaplib, smtplib
import os, logging, dotenv
from dotenv import load_dotenv
from email import message_from_bytes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from utils import *

load_dotenv()

USERNAME = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
MAIL_ADDRESS = os.environ["MAIL_ADDRESS"]
IMAP_SERVER = os.environ["IMAP_SERVER"]
IMAP_PORT = os.environ["IMAP_PORT"]
SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = os.environ["SMTP_PORT"]

def fetch_mail(num_of_mail=0, search_criteria='(UNSEEN SUBJECT "{}")'.format(os.environ["KEY"]), mail_box="INBOX"):
    logging.info("Connecting to IMAP server...")
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(USERNAME, PASSWORD)
    imap.select(mail_box)
    logging.info("Logged in to IMAP server successfully.")
    logging.info("Searching mail...")
    status, mail_ids = imap.search(None, search_criteria)
    if status != 'OK':
        logging.error("Error searching mail")
        logging.error("Status: {}".format(status))
        imap.close()
        imap.logout()
        logging.error("Logged out from IMAP server.")
        return
    received_mails = []
    mail_ids = mail_ids[0].split()
    logging.info("Found {} mails.".format(len(mail_ids)))
    if len(mail_ids) == 0:
        imap.close()
        imap.logout()
        logging.info("Logged out from IMAP server.")
        return []
    for cnt, id in enumerate(mail_ids[-num_of_mail:]):
        status, mail = imap.fetch(id, "(RFC822)")
        imap.store(id, '+FLAGS', '\\Seen')
        if status != 'OK':
            logging.error("Error fetching mail")
            imap.close()
            imap.logout()
            return
        mail = message_from_bytes(mail[0][1])
        log_name = '{}.txt'.format(mail['Message-ID'])
        mkdir('logs/mail')
        log_name = 'logs/mail/' + clean_file_name(log_name)
        with open(log_name, 'w') as f:
            f.write(mail.as_string())
        received_mails.append(mail)
        logging.info("Fetched {}/{} mails.".format(cnt + 1, len(mail_ids[-num_of_mail:])))
    logging.info("Fetched {} mails.".format(len(received_mails)))
    imap.close()
    imap.logout()
    logging.info("Logged out from IMAP server.")
    return received_mails

def create_mail(receiver=None, subject=None, plain_content=None, html_content=None, attachments=None, header=None, original=None, alias_attachment_name=None):
    if receiver is None and original is None:
        logging.error("No receiver or original mail provided.")
        return
    logging.info("Creating mail to {}...".format(receiver))
    mail = MIMEMultipart('alternative')
    if header is not None:
        for key, value in header.items():
            mail[key] = value
    if subject is None:
        logging.warning("No subject specified. Default subject will be used.")
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
            logging.error('No receiver specified.')
            return
    if plain_content is not None:
        mail.attach(MIMEText(plain_content, 'plain'))
    if html_content is not None:
        mail.attach(MIMEText(html_content, 'plain'))
    if attachments is not None:
        for id, file_path in enumerate(attachments):
            with open(file_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
            file_name = os.path.basename(file_path)
            if alias_attachment_name is not None:
                file_name = alias_attachment_name[id]
            part['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
            mail.attach(part)
    return mail
def send_mail(mail):
    logging.info("Connecting to SMTP server...")
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    smtp.login(USERNAME, PASSWORD)
    logging.info("Connected to SMTP server successfully.")
    logging.info("Sending mail to {}...".format(extract_mail_address(mail['To'])))
    smtp.sendmail(mail['From'], mail['To'], mail.as_string())
    logging.info("Mail sent successfully.")
    smtp.quit()
    logging.info("Disconnected from SMTP server.")
