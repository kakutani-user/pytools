import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

MAIL_ADDRESS = 'address'
ACCOUNT = 'account'
PASSWORD = 'pass'

def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg


def send_mail(from_addr, to_addr, body_msg):
    smtpobj = smtplib.SMTP('mail.otsukalab.nitech.ac.jp', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(ACCOUNT, PASSWORD)
    smtpobj.sendmail(from_addr, to_addr, body_msg.as_string())
    smtpobj.close()


msg = create_message(MAIL_ADDRESS, MAIL_ADDRESS, 'test', 'test')
send_mail(MAIL_ADDRESS, MAIL_ADDRESS, msg)