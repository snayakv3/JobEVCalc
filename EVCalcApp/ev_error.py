import smtplib
import logging, time, os, threading
from multiprocessing import Process
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


NOT_DONE = None
NUM_OF_CHECKS = 3
DEFAULT_MESSAGE = 'Could not complete the calculation, please try again later'
ERROR_DIR = './EVCalcApp/logs/error_input/'
check_message = { None: "not been done", False: "failed", True: "passed" }
CRED_INDEX = 1
error_logger = logging.getLogger('error_logger')
logging.Formatter.converter = time.gmtime
formatter = logging.Formatter(fmt="%(levelname)s(%(thread)d): %(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler = logging.FileHandler('./EVCalcApp/logs/application.log')
file_handler.setFormatter(formatter)
error_logger.addHandler(file_handler)
error_logger.setLevel(logging.INFO)


def get_email_and_password():
    email_address = None
    password = None
    file = None
    try:
        with open("key") as file:
            email_address, password = file.readlines()[CRED_INDEX].split(' ')
    except (IndexError, FileNotFoundError, ValueError) as e:
        error_logger.warning("Not able to get email and password for logging due to {}".format(e))
        if file is not None:
            file.close()
    return email_address, password

def create_error_file(ip, user_input, error_messages):
    address, password = get_email_and_password()
    if address is not None:
        message = MIMEMultipart()
        message['From'] = address
        message['To'] = address
        message['Subject'] = 'Error for {}'.format(ip)
        text = '\n'.join(error_messages)
        message.attach(MIMEText(text, 'plain'))
        part = MIMEApplication(user_input)
        part['Content-Disposition'] = 'attachment; filename="user_input.txt"'
        message.attach(part)
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(address, password)
        text = message.as_string()
        session.sendmail(address, address, text)
        session.quit()

def write_logs(ip_address, team_data, *error_messages):
    for err_msg in error_messages:
        error_logger.error(err_msg)
    error_file_process = Process(target=create_error_file, args=(ip_address, team_data, error_messages))
    error_file_process.start()

def create_logs(ip_address, team_data, setup_check, number_of_days_check, evs_fulfilled_check):
    setup_error = "Check for stat EV splits in stat mapping setup accounted for: {}".format(check_message[setup_check])
    number_of_days_error = "Check for amount of pokemon in all days account for amount of pokemon needs in stat mapping: {}".format(check_message[number_of_days_check])
    evs_fulfilled_error = "Check for total EV's for each pokemon in all days account for their EV needs: {}".format(check_message[evs_fulfilled_check])
    write_logs(ip_address, team_data, setup_error, number_of_days_error, evs_fulfilled_error)
