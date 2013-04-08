#!/usr/bin/env python2.7
import cv
import sys
import os
import socket
import getopt

HAAR_CASCADE_PATH = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
CAMERA_INDEX = 0

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
    args = getopt.getopt(sys.argv[1:], 'x:y:')
    print args[1][0]
    cv.NamedWindow("Video", cv.CV_WINDOW_AUTOSIZE)
 
    #capture = cv.CaptureFromCAM(CAMERA_INDEX)
    #capture = cv.CaptureFromFile('/Users/mattman/Downloads/IMG_0288.MOV')

    '''
    while True:
        cv.GrabFrame(video)
        frame = cv.RetrieveFrame(video)
        cv.ShowImage("IP Camera", frame)
        cv.WaitKey(50)
    '''

    print args[1][0]
    try: capture = cv.CaptureFromFile(args[1][0])
    except: print 'Error: File won\'t open.'
    print args[1][0]
    if not capture:
        raise Exception('Error: File won\'t open.')

    storage = cv.CreateMemStorage()
    cascade = cv.Load(HAAR_CASCADE_PATH)
    faces = []
 
    nFrames = int( cv.GetCaptureProperty( capture, cv.CV_CAP_PROP_FRAME_COUNT ) )
    fps = cv.GetCaptureProperty( capture, cv.CV_CAP_PROP_FPS )
    if fps <= 0:
        raise Exception('Error: FPS is negative.')
    waitPerFrameInMillisec = int( 1/fps * 1000/1 )

    print 'wait = ', waitPerFrameInMillisec
    print 'Num. Frames = ', nFrames
    print 'Frame Rate = ', fps, ' frames per sec'

    i = 0
    while True:
        #for f in xrange( nFrames ):
        cv.GrabFrame(capture)
        frameImg = cv.RetrieveFrame(capture)

        #frameImg = cv.QueryFrame( capture )

        if i%10==0 and frameImg is not None:
            print type(frameImg)
            faces = detect_faces(frameImg)
            face_list = faces
            if len(faces) > 0:
                sys.stdout.write("Num faces detected = %d [%d]\n" % (len(faces), i))
                sys.stdout.flush()
                contact_server()
 
        for (x,y,w,h) in faces:
            cv.Rectangle(frameImg, (x,y), (x+w,y+h), 255)
 
        cv.ShowImage("w1", frameImg)
        #cv.WaitKey( waitPerFrameInMillisec )
        cv.WaitKey( 50 )
        i += 1


    # When playing is done, delete the window
    #  NOTE: this step is not strictly necessary, 
    #         when the script terminates it will close all windows it owns anyways
    cv.DestroyWindow( "My Video Window" )

    #i = 0
    #while True:
        #image = cv.QueryFrame(capture)
 
        # Only run the Detection algorithm every 10 frames to improve performance
        #if i%10==0:
        #    faces = detect_faces(image)
        #    face_list = faces
        #    if len(faces) > 0:
        #        sys.stdout.write("Num faces detected = %d [%d]\n" % (len(faces), i))
        #        sys.stdout.flush()
 
        #for (x,y,w,h) in faces:
        #    cv.Rectangle(image, (x,y), (x+w,y+h), 255)
 
        #cv.ShowImage("w1", image)
        #i += 1