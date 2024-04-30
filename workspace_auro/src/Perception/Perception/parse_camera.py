#!/usr/bin/env python3
import rclpy # is the python library for ROS2
from rclpy.node import Node

import cv2

# In computer's terminal, if we do "ros2 run rqt_image_view rqt_image_view", we see the BELOW topic is what gets Real-Time Camera feed from the TurtleBot
# If we do "ros2 topic info /oakd/rgb/preview/image_raw"
# We see it has msgs of the below type 
from sensor_msgs.msg import Image

from threading import Lock
from cv_bridge import CvBridge, CvBridgeError

import tensorflow as tf
from tensorflow import keras

import math


import numpy as np
import os




# Inherit from Node class (has all the ros functionality for rclpy)
class ImagePipeline(Node):

    def __init__(self):
        self.mutex = Lock()
        # Pass in the name we want our node to be
        super().__init__("parse_camera")
        self.get_logger().info("parse_camera node has been started")
        self.bridge = CvBridge()

        # Create Subscruber
        imRos = self.create_subscription(Image, '/oakd/rgb/preview/image_raw', self.imageCallBack, 3)
        # Create Publisher
        self.ImOut = self.create_publisher(Image, "out/image", 3)

        # Create the ML model that can classify numbers
        self.model = keras.models.load_model('./workspace_auro/src/Perception/Perception/digit_classifier.h5')

        # Using absolute path
        #model_path = os.path.abspath('./digit_classifier.h5')
        #self.model = keras.models.load_model(model_path)

    def imageCallBack(self, inp_im : Image):

        # Declare Variable
        imCV = None

        try:
            imCV = self.bridge.imgmsg_to_cv2(inp_im, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        if imCV is None:
            print('frame dropped, skipping tracking')
        else:
            self.ImageProcessor(imCV)
    
    def ImageProcessor(self, imCV):

        img = cv2.cvtColor(imCV, cv2.COLOR_BGR2GRAY)
        img_org = imCV

        # Preprocess the images
        ret,thresh = cv2.threshold(img,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        # Detect Numbers- first convert to a Gray image
        #gray = cv2.cvtColor(imCV, cv2.COLOR_BGR2GRAY)
        # First, preprocess the image
        # First, conver to an opencv image

        for j,cnt in enumerate(contours):
            epsilon = 0.01*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            
            hull = cv2.convexHull(cnt)
            k = cv2.isContourConvex(cnt)
            x,y,w,h = cv2.boundingRect(cnt)
            
            if(hierarchy[0][j][3]!=-1 and w>10 and h>10):
                #putting boundary on each digit
                cv2.rectangle(img_org,(x,y),(x+w,y+h),(0,255,0),2)
                
                #cropping each image and process
                roi = img[y:y+h, x:x+w]
                roi = cv2.bitwise_not(roi)
                roi = self.image_refiner(roi)
                th,fnl = cv2.threshold(roi,127,255,cv2.THRESH_BINARY)

                # getting prediction of cropped image
                pred = self.predict_digit(roi)
                self.get_logger().info("The predicted digit is %d\n" % pred)

                print(pred)
                
                # placing label on each digit
                (x,y),radius = cv2.minEnclosingCircle(cnt)
                img_org = self.put_label(img_org,pred,x,y)
    # --------------------- Functions to Identify Digits -------------------------#
    def predict_digit(self, img):
        test_image = img.reshape(-1,28,28,1)
        return np.argmax(self.model.predict(test_image))


    #pitting label
    def put_label(self, t_img,label,x,y):
        font = cv2.FONT_HERSHEY_SIMPLEX
        l_x = int(x) - 10
        l_y = int(y) + 10
        cv2.rectangle(t_img,(l_x,l_y+5),(l_x+35,l_y-35),(0,255,0),-1) 
        cv2.putText(t_img,str(label),(l_x,l_y), font,1.5,(255,0,0),1,cv2.LINE_AA)
        return t_img

    # refining each digit
    def image_refiner(self, gray):
        org_size = 22
        img_size = 28
        rows,cols = gray.shape
        
        if rows > cols:
            factor = org_size/rows
            rows = org_size
            cols = int(round(cols*factor))        
        else:
            factor = org_size/cols
            cols = org_size
            rows = int(round(rows*factor))
        gray = cv2.resize(gray, (cols, rows))
        
        #get padding 
        colsPadding = (int(math.ceil((img_size-cols)/2.0)),int(math.floor((img_size-cols)/2.0)))
        rowsPadding = (int(math.ceil((img_size-rows)/2.0)),int(math.floor((img_size-rows)/2.0)))
        
        #apply apdding 
        gray = np.lib.pad(gray,(rowsPadding,colsPadding),'constant')
        return gray



    # ----------------------------------------------------------------------------#



def main(args=None):
    rclpy.init(args=args) # Initialize ROS2 communications
    # create node inside main
    node = ImagePipeline()
    rclpy.spin(node)
    rclpy.shutdown # last line, shuts down node and all ROS2 communications
    pass

if __name__ == '__main__':
    main()