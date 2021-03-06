import smtplib
import config
from emails.Monitor import Monitor
import time
import datetime
import sched
import pytz

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


s = sched.scheduler(time.time, time.sleep)


def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_email(user):
    u = datetime.datetime.utcnow()
    u = u.replace(tzinfo=pytz.utc)
    m = Monitor(s, user, send_email_task,
                u+datetime.timedelta(0, 8))
    m.start()


def send_email_task(user):
    names, emails = get_contacts('./emails/contacts')  # read contacts
    message_template = read_template('./emails/message')
    user_data = str(user)
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(config.MY_ADDRESS, config.PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message
        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title(), USER_DATA=user_data)

        # setup the parameters of the message
        msg['From'] = config.MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "This is TEST"

        # add in the message body
        msg.attach(MIMEText(message, 'html'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()
