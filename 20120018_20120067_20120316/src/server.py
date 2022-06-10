from mail import *
import controller
import platform
import time
import logging, dotenv
from dotenv import load_dotenv

load_dotenv()

OS_NAME = platform.system()
REFRESH_RATE = 2
LOG_FILE = 'logs/log.txt'
IS_STOPPED = False
MAIL_ADDRESS = os.getenv('MAIL_ADDRESS')
KEY = os.getenv('KEY')
if KEY == 'NULL':
    KEY = get_random_string()
    dotenv.set_key("KEY", KEY)

def start_listening_email():
    global KEY
    logging.info("Start listening for new mail at {} with KEY='{}'.".format(MAIL_ADDRESS, KEY))
    while True:
        del os.environ['KEY']
        load_dotenv()
        if os.getenv('KEY') != KEY:
            logging.info("Key changed to '{}'".format(os.getenv('KEY')))
        KEY = os.getenv('KEY')
        received_mails = fetch_mail(search_criteria='(UNSEEN SUBJECT "{}")'.format(KEY))
        for mail in received_mails:
            valid = False
            for command in controller.COMMANDS:
                if command in mail['Subject']:
                    logging.info("Received {} request from {}.".format(command, extract_mail_address(mail['From'])))
                    logging.info("Executing {} command...".format(command))
                    respone_mail = controller.EXECUTE[command](mail)
                    logging.info("Executed {} command successfully.".format(command))
                    send_mail(respone_mail)
                    valid = True
                    break
            if not valid:
                logging.info("Received invalid request from {}.".format(extract_mail_address(mail['From'])))
                respone_mail = controller.EXECUTE['HELP'](req=mail, isInvalid=True)
                send_mail(respone_mail)
        if IS_STOPPED:
            break
        time.sleep(REFRESH_RATE)
def stop_listening_email():
    global IS_STOPPED
    IS_STOPPED = True
    logging.info("Stop listening for new mail.")
if __name__ == "__main__":
    mkdir('logs')
    logging.basicConfig(
        format='%(asctime)s - %(message)s', 
        level=logging.INFO, 
        datefmt=DATE_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, 'a', 'utf-8'),
            logging.StreamHandler()
        ]
    )
    if OS_NAME == "Windows":
        start_listening_email()
    else:
        logging.error("This program is only for Windows.")