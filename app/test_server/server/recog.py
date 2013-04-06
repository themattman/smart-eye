#!/usr/bin/env python2.7
import cv
import sys
import os
import socket
#import httplib2

 
HAAR_CASCADE_PATH = "/opt/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
CAMERA_INDEX = 0
 
def detect_faces(image):
    faces = []
    detected = cv.HaarDetectObjects(image, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    if detected:
        for (x,y,w,h),n in detected:
            faces.append((x,y,w,h))
    return faces
 
if __name__ == "__main__":
    print os.getppid()
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #resp, content = httplib2.Http().request("http://example.com/foo/bar")
    cv.NamedWindow("Video", cv.CV_WINDOW_AUTOSIZE)
 
    #capture = cv.CaptureFromCAM(CAMERA_INDEX)
    capture = cv.CaptureFromFile('/Users/mattman/Downloads/IMG_0288.MOV')
    storage = cv.CreateMemStorage()
    cascade = cv.Load(HAAR_CASCADE_PATH)
    faces = []
 
    nFrames = int(  cv.GetCaptureProperty( capture, cv.CV_CAP_PROP_FRAME_COUNT ) )
    fps = cv.GetCaptureProperty( capture, cv.CV_CAP_PROP_FPS )
    waitPerFrameInMillisec = int( 1/fps * 1000/1 )

    print 'Num. Frames = ', nFrames
    print 'Frame Rate = ', fps, ' frames per sec'

    i = 0
    while True:
        capture = cv.CaptureFromFile('/Users/mattman/Downloads/IMG_0288.MOV')
        for f in xrange( nFrames ):
            frameImg = cv.QueryFrame( capture )
            #cv.ShowImage('both', cv.fromarray(frameImg.array(da[::2,::2,::-1])))
            cv.ShowImage( "My Video Window",  frameImg )
            cv.WaitKey( waitPerFrameInMillisec  )

            if i%3==0 and frameImg is not None:
                print type(frameImg)
                faces = detect_faces(frameImg)
                face_list = faces
                if len(faces) > 0:
                    sys.stdout.write("Num faces detected = %d [%d]\n" % (len(faces), i))
                    sys.stdout.flush()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    host = "localhost"
                    port = 3000
                    s.connect((host, port))
                    s.send("GET /\n\n")
                    s.close()
     
            for (x,y,w,h) in faces:
                cv.Rectangle(frameImg, (x,y), (x+w,y+h), 255)
     
            cv.ShowImage("w1", frameImg)
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