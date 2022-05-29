import imaplib
import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import os
import smtplib
import dotenv
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

def new_instance(sender=None, receiver=None, subject=None, content=None, file=None, id=None, date=None):
    return {
        'sender': sender,
        'receiver': receiver,
        'subject': subject,
        'content': content, 
        'file': file, # list of file paths
        'id': id,
        'date': date,
    }

def read_request_emails(num_of_mail=5, search_criteria='(UNSEEN SUBJECT "{}")'.format(KEY), mail_box="INBOX"):
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
    messages = messages[0].split()
    mail_recieved = []
    for e_id in messages[-num_of_mail:]:
        req = new_instance()
        # print("Fetching mail {}".format(e_id))
        res, msg = imap.fetch(e_id, "(RFC822)")
        # imap.store(e_id, '+FLAGS', '\\Seen')
        if res != 'OK':
            print("Error fetching mail")
            return
            
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                print(msg)
                print(msg.items())
                # print(decode_header(msg['Message-ID']))
                req['subject'], encoding = decode_header(msg["Subject"])[0]
                if isinstance(req['subject'], bytes):
                    req['subject'] = req['subject'].decode(encoding)

                sender_name, encoding = decode_header(msg.get("From"))[0]
                if isinstance(sender_name, bytes):
                    sender_name = sender_name.decode(encoding)

                req['sender'] = decode_header(msg.get("From"))[1][0]
                req['sender'] = req['sender'].decode('utf-8')
                req['sender'] = req['sender'].replace('<', '').replace('>', '').replace(' ', '')

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            content = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "filename" not in content_disposition:
                            req['content'] = content
                        elif "filename" in content_disposition:
                            if not os.path.isdir(EMAIL_LOG_FOLDER):
                                os.mkdir(EMAIL_LOG_FOLDER)
                            if not os.path.isdir(ATTACHMENT_FOLDER):
                                os.mkdir(ATTACHMENT_FOLDER)
                            filename = part.get_filename()
                            print(filename)
                            if filename:
                                filepath = os.path.join(ATTACHMENT_FOLDER, filename)
                                open(filepath, "wb").write(part.get_payload(decode=True))
                                if req['file'] is None:
                                    req['file'] = []
                                req['file'].append(filepath)
                else:
                    content_type = msg.get_content_type()
                    content = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        req['content'] = content
                mail_recieved.append(req)
    imap.close()
    imap.logout()
    return mail_recieved

def send_email(mail):
    if mail is None:
        return
    print("Sending email {}".format(mail))
    mail["sender"] = MY_EMAIL
    # initialize the email
    msg = EmailMessage()
    del msg["Subject"]
    del msg["From"]
    del msg["To"]
    del msg["In-Reply-To"]
    del msg["References"]
    msg["Subject"] = mail["subject"]
    msg["From"] = mail["sender"]
    msg["To"] = mail["receiver"]
    msg["In-Reply-To"] = '<CAFkhqbkyau=pwEyA93jqGeNERQdO1f5yc82Whw_3JXjVYbk0eA@mail.gmail.com>'
    msg["References"] = '<CAFkhqbkyau=pwEyA93jqGeNERQdO1f5yc82Whw_3JXjVYbk0eA@mail.gmail.com>'
    msg.set_content(mail["content"])
    print(str(msg))
    #attach files
    if mail["file"] is not None:
        for file in mail["file"]:
            with open(file, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(file)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
    #send the email
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(USERNAME, PASSWORD)
    smtp.sendmail(msg["From"], msg["To"], msg.as_string())
    smtp.quit()
def reply_email(mail):
    if mail is None:
        return
    print("Sending email {}".format(mail))
    mail["sender"] = MY_EMAIL
    # initialize the email
    msg = MIMEMultipart('mixed')
    body = MIMEMultipart('alternative')
    msg["Subject"] = mail["subject"]
    msg["From"] = mail["sender"]
    msg["To"] = mail["receiver"]
    msg["In-Reply-To"] = '<CAFkhqbkyau=pwEyA93jqGeNERQdO1f5yc82Whw_3JXjVYbk0eA@mail.gmail.com>'
    msg["References"] = '<CAFkhqbkyau=pwEyA93jqGeNERQdO1f5yc82Whw_3JXjVYbk0eA@mail.gmail.com>'
    msg["Message-ID"] = '<CAFkhqbkyau=pwEyA93jqGeNERQdO1f5yc82Whw_3JXjVYbk0eA@mail.gmail.com>'

    msg.set_content(mail["content"])
    #attach files
    if mail["file"] is not None:
        for file in mail["file"]:
            with open(file, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(file)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
    #send the email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()

# print(USERNAME, PASSWORD, IMAP_SERVER, KEY, SMTP_SERVER, SMTP_PORT)
print(read_request_emails(num_of_mail=1))
# send_email(new_instance(sender="minhlam2102002@zohomail.com", receiver="minhlam2102002@gmail.com", subject="Replyabcxy", content="Hello Worldabc"))