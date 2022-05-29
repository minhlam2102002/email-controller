from mail import *
from command import *
import platform
import time
OS_NAME = platform.system()
REFRESH_DELAY = 1

def start_listening_email():
    print("Starting listening email...")
    while True:
        request_emails = read_request_emails()
        for request_email in request_emails:
            # print("Received mail: {}".format(mail))
            for command in EXECUTE:
                if command in request_email['subject']:
                    print("Received {} request.".format(command))
                    print("Executing {}...".format(command))
                    respone_mail = globals()[command](request_email)
                    if respone_mail:
                        print("Sending response mail...")
                        send_email(respone_mail)
                        print("Response mail sent.")
                    break
        time.sleep(REFRESH_DELAY)

if __name__ == "__main__":
    if OS_NAME == "Windows":
        start_listening_email()
    else:
        print("This program is only for Windows.")