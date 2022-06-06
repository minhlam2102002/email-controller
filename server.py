from mail import *
import controller
import platform
import time
import logging

OS_NAME = platform.system()
REFRESH_RATE = 0
LOG_FILE = 'logs/log.txt'
IS_STOPPED = False
KEY = os.environ["KEY"]
if KEY == "NULL":
    KEY = get_random_string()
    dotenv.set_key(dotenv_file, "KEY", KEY)

def start_listening_email():
    logging.info("Start listening for new mail with KEY='{}'.".format(KEY))
    while True:
        received_mails = fetch_mail()
        for mail in received_mails:
            valid = False
            for command in controller.COMMANDS:
                if command in mail['Subject']:
                    logging.info("Received {} request from {}.".format(command, extract_mail_address(mail['From'])))
                    logging.info("Executing {} command...".format(command))
                    respone_mail = controller.EXECUTE[command](mail)
                    logging.info("Executed {} command.".format(command))
                    logging.info("Preparing response mail...")
                    send_mail(respone_mail)
                    logging.info("Response mail sent.")
                    valid = True
                    break
            if not valid:
                respone_mail = controller.EXECUTE['HELP'](mail)
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