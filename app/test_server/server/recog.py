#!/usr/bin/env python2.7
import cv
import sys
import os
import socket
import getopt
import smtplib
#from email.mime.type import MIMEtext
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

HAAR_CASCADE_PATH = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
CAMERA_INDEX = 0

def email_user(email_address, frameImg):
    #Get SMTP server working
    LOGIN = 'elkoyadotcom@gmail.com'
    PASSWORD = 'js5w10up8'
    TO = 'mattknize@gmail.com'
    FROM = 'elkoyadotcom@gmail.com'
    print 'email_user()'
    '''
    msg = MIMEMultipart('related')
    strFrom = 'security@smartEyeCamera.com'
    strTo = email_address
    msg['Subject'] = 'Security Camera Tripped!'
    msg['From'] = strFrom
    msg['To'] = strTo
    '''

    LOGIN    = FROM
    TOADDRS  = ["mattman@umich.edu"]
    SUBJECT  = "Testing!!!"

    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (FROM, ", ".join(TOADDRS), SUBJECT) )
    msg += "some text\r\n"

    # Get the image
    #fp = open(frameImg, 'rb')
    #msgImage = MIMEImage(fp.read())
    #fp.close()
    #msg.attach(msgImage)
    print 'Img attached'

    #s = smtplib.SMTP('localhost')
    #s = smtplib.SMTP('smtp.mattkneiser.com', 25)
    #s = smtplib.SMTP('mail.which.net', 25)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    try:
        failed = s.sendmail(FROM, TOADDRS, msg.as_string())
        s.close()
    except Exception, e:
        errorMsg = "Unable to send email. Error: %s" % str(e)
    #s.connect(smtp.mattkneiser.com, 25)
    #s.sendmail(strFrom, strTo, msg.as_string())
    #s.quit()
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
    print os.getppid()
    email_user('mattman@umich.edu', '/Users/mattman/Desktop/f.jpg')
    sys.exit()
    '''
    print os.getppid()
    print os.getpid()
    args = getopt.getopt(sys.argv[1:], 'x:y:')
    cv.NamedWindow("Video", cv.CV_WINDOW_AUTOSIZE)
 
    #capture = cv.CaptureFromCAM(CAMERA_INDEX)
    #capture = cv.CaptureFromFile('/Users/mattman/Downloads/IMG_0288.MOV')

    
    while True:
        cv.GrabFrame(video)
        frame = cv.RetrieveFrame(video)
        cv.ShowImage("IP Camera", frame)
        cv.WaitKey(50)


    #print args[1][0]
    try: capture = cv.CaptureFromFile(args[1][0])
    except: print 'Error: File won\'t open.'
    #print args[1][0]
    if not capture:
        raise Exception('Error: File won\'t open.')

    storage = cv.CreateMemStorage()
    cascade = cv.Load(HAAR_CASCADE_PATH)
    faces = []
 
    #nFrames = int( cv.GetCaptureProperty( capture, cv.CV_CAP_PROP_FRAME_COUNT ) )
    #fps = cv.GetCaptureProperty( capture, cv.CV_CAP_PROP_FPS )
    #if fps <= 0:
    #raise Exception('Error: FPS is negative.')
    #waitPerFrameInMillisec = int( 1/fps * 1000/1 )

    #print 'wait = ', waitPerFrameInMillisec
    #print 'Num. Frames = ', nFrames
    #print 'Frame Rate = ', fps, ' frames per sec'

    i = 0
    while True:
        cv.GrabFrame(capture)
        frameImg = cv.RetrieveFrame(capture)

        if i%10==0 and frameImg is not None:
            #print type(frameImg)
            faces = detect_faces(frameImg)
            face_list = faces
            if len(faces) > 0:
                sys.stdout.write("Num faces detected = %d [%d]\n" % (len(faces), i))
                sys.stdout.flush()
                contact_server()
                email_user('mattman@umich.edu', frameImg)
 
        for (x,y,w,h) in faces:
            cv.Rectangle(frameImg, (x,y), (x+w,y+h), 255)
 
        cv.ShowImage("w1", frameImg)
        cv.WaitKey( 50 )
        if i > 100:
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
'''