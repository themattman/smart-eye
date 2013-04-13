'''
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
textfile = "send.txt"
#fp = open(textfile, 'rb')
# Create a text/plain message
#msg = MIMEText(fp.read())
msg = MIMEText('hello there chap')
#fp.close()

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = 'mattman@umich.edu'
msg['To'] = 'mattknize@gmail.com'

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP()
s.connect()
s.sendmail(me, [you], msg.as_string())
s.quit()
'''


from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage

from email.mime.text import MIMEText
from datetime import date
import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "smart.eye.team@gmail.com"
SMTP_PASSWORD = "hillshire4farms"

EMAIL_TO = ["mattman@umich.edu", "jackwink@umich.edu", "kunyu@umich.edu"]
EMAIL_FROM = "the.smarteye.team@gmail.com"
EMAIL_SUBJECT = "Meeting Tomorrow (Sent via Python ^_^)"

DATE_FORMAT = "%d/%m/%Y"
EMAIL_SPACE = ", "

DATA='Welp, guess this script is working. Jack and I are good to meet at 2 tomorrow, how about you Kunyu? I assume you guys are good with the UGLI, but I\'m flexible'

def send_email():
    #msg = MIMEText(DATA)
    msg = MIMEMultipart(DATA)
    file_name = "/Users/mattman/Pictures/mhacks.jpg"

    fp = open(file_name, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    msg.attach(MIMEText(DATA, 'plain'))

    msg['Subject'] = EMAIL_SUBJECT# + " %s" % (date.today().strftime(DATE_FORMAT))
    msg['To'] = EMAIL_SPACE.join(EMAIL_TO)
    msg['From'] = EMAIL_FROM
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()

if __name__=='__main__':
    send_email()