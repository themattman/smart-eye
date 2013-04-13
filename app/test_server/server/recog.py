#!/usr/bin/env python2.7
import cv
import sys
import os
import socket
import getopt
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

# For OpenCV
HAAR_CASCADE_PATH = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
CAMERA_INDEX = 0

# For Email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "smart.eye.team@gmail.com"
SMTP_PASSWORD = "hillshire4farms"

EMAIL_FROM = "the.smarteye.team@gmail.com"
EMAIL_SUBJECT = "Intrusion Alert!!"

DATE_FORMAT = "%d/%m/%Y"
EMAIL_SPACE = ", "

DATA = "This is an auto-generated email from the SmartEye Android App. An intruder was detected."

def email_user(email_address, file_name):
    msg = MIMEMultipart(DATA)
    print 'email_address'
    print email_address
    print type(email_address)

    fp = open(file_name, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    msg.attach(MIMEText(DATA, 'plain'))

    msg['Subject'] = EMAIL_SUBJECT
    msg['To'] = EMAIL_SPACE.join(email_address)
    msg['From'] = EMAIL_FROM

    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, email_address, msg.as_string())
    mail.quit()
    
    print 'Email sent!'

def contact_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "localhost"
    port = 3000
    s.connect((host, port))
    s.send("GET /\n\n")
    s.close()
 
def detect_faces(image):
    faces = []
    detected = cv.HaarDetectObjects(image, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    if detected:
        for (x,y,w,h),n in detected:
            faces.append((x,y,w,h))
    return faces
 
if __name__ == "__main__":
    print "Starting!"
    args = getopt.getopt(sys.argv[1:], 'x:y:')
    if len(args[1]) < 2:
        raise Exception('Error: No email addresses specified.')
    #print args[1][1:]
    #sys.exit()
    cv.NamedWindow("Video", cv.CV_WINDOW_AUTOSIZE)
 
    #capture = cv.CaptureFromCAM(CAMERA_INDEX)

    '''
    while True:
        cv.GrabFrame(video)
        frame = cv.RetrieveFrame(video)
        cv.ShowImage("IP Camera", frame)
        cv.WaitKey(50)
    '''


    #print args[1][0]
    try: capture = cv.CaptureFromFile(args[1][0])
    except: print 'Error: File won\'t open.'
    if not capture:
        raise Exception('Error: File won\'t open.')

    storage = cv.CreateMemStorage()
    cascade = cv.Load(HAAR_CASCADE_PATH)
    faces = []
 
    i = 0
    while True:
        cv.GrabFrame(capture)
        frameImg = cv.RetrieveFrame(capture)

        if i%5==0 and frameImg is not None:
            #print type(frameImg)
            faces = detect_faces(frameImg)
            for (x,y,w,h) in faces:
                cv.Rectangle(frameImg, (x,y), (x+w,y+h), 255)
            face_list = faces
            if len(faces) > 0:
                cv.SaveImage('frameImg2.png', frameImg)
                sys.stdout.write("Num faces detected = %d [%d]\n" % (len(faces), i))
                sys.stdout.flush()
                #contact_server()
                print os.path.dirname(os.path.realpath(__file__))
                email_user(args[1][1:], '/Users/mattman/Development/Web/nodeFun/smart-eye/app/test_server/frameImg2.png')
                sys.exit()
 
        #for (x,y,w,h) in faces:
            #cv.Rectangle(frameImg, (x,y), (x+w,y+h), 255)
 
        cv.ShowImage("w1", frameImg)
        cv.WaitKey( 50 )
        if i > 600:
            cv.DestroyWindow( "My Video Window" )
            sys.exit()
        i += 1

    cv.DestroyWindow( "My Video Window" )

# 8 minutes / 2 min Q&A (6/7 slides)
# 1) Title
# 2) Problem
# 3) Solution
# 4) Show 'em
# 5) 3 things you learned
# 6) What didn't work/What's next/Thumgs up or thumbs down (explain why you're happy/sad)
# 7) Who's your competition



# USE FAKE GMAIL ACCOUNT