#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys
import rospy
import cv2
#from std_msgs import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import pdb
import time
import cPickle

start_frame = []
end_frame = []
point_object_location = []
activity = '0510143618'   # activity number

def main():
    rospy.init_node('arranging_objects_{0}'.format(activity), anonymous=True)
    image_pub = rospy.Publisher('arranging_objects_{0}'.format(activity), Image, queue_size=1)
    bridge = CvBridge()

    while(image_pub.get_num_connections() < 1):
        print "the number of connection of the arranging_objects_{0} still less than 1.".format(activity)
        time.sleep(1)

    # CAD-120-dataset
    dataset_CAD120_path = '/media/bsb/666/human_anticipation_data/CAD_120'
    image_path = '{0}/person2/Subject3_rgbd_images/arranging_objects/{1}/'.format(dataset_CAD120_path, activity)
    ground_truth_label_activity = '{0}/person2/Subject3_annotations/arranging_objects/labeling.txt'.format(dataset_CAD120_path)
    object_location = '{0}/person2/Subject3_annotations/arranging_objects/{1}_obj1.txt'.format(dataset_CAD120_path, activity)
    print "labeling.txt path:{0}".format(ground_truth_label_activity)

    ground_truth_label_interpreter(ground_truth_label_activity)               
    object_location_interpreter(object_location)

    # ground truth
    human_label = {1: 'reaching', 2: 'moving', 3: 'pouring', 4: 'eating', 5: 'drinking',\
                   6: 'opening', 7: 'placing', 8: 'closing', 9: 'null', 10: 'cleaning',11:'error',12:'error'}
    object_label = {1: 'movable', 2: 'stationary', 3: 'reachable', 4: 'pourable', 5: 'pourto',\
                    6: 'containable', 7: 'drinkable', 8: 'openable', 9: 'placeable', 10: 'closeable', 11: 'cleanable',\
                    12: 'error',13:'error',14:'error'}

    ground_truth_path = '/media/bsb/666/human_anticipation_data/CAD_120/features_cad120_ground_truth_segmentation/dataset/fold_2'
    ground_truth_test_data = cPickle.load(open('{0}/grount_truth_test_data_677107.pik'.format(ground_truth_path)))
    ground_truth_label_human = ground_truth_test_data['labels_human']
    ground_truth_label_object = ground_truth_test_data['labels_objects']

    # detection and anticipation of human and object label
    detection_anticipation_path = '/media/bsb/666/human_anticipation_data/result'
    detection_human_data = cPickle.load(open('{0}/detection_human_677107.pik'.format(detection_anticipation_path)))
    anticipation_human_data = cPickle.load(open('{0}/anticipation_human_677107.pik'.format(detection_anticipation_path)))
    detection_object_data = cPickle.load(open('{0}/detection_object_677107.pik'.format(detection_anticipation_path)))
    anticipation_object_data = cPickle.load(open('{0}/anticipation_object_677107.pik'.format(detection_anticipation_path)))

    # the number '29' is the 30th line of fold2 in the activity fold
    truth_human = ground_truth_label_human[5].T[0]
    #print truth_human
    detect_human = detection_human_data[5].T[0]
    anticipation_human = anticipation_human_data[5].T[0]
    truth_object = ground_truth_label_object[5].T[0]
    detect_object = detection_object_data[5].T[0]
    anticipation_object = anticipation_object_data[5].T[0]

    segement = 0
    point = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    while(segement < len(start_frame)):
        index = start_frame[segement]
        timer = rospy.Rate(20)
        while((not rospy.is_shutdown()) and index <= end_frame[segement]):
            data = cv2.imread('{0}RGB_{1}.png'.format(image_path, index))
            cv2.putText(data, "time{0}:".format(segement), (30,30), font, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(data, 'ground truth human label:{0}'.format(human_label[truth_human[segement]]),(30,50), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(data,'ground truth object label:{0}'.format(object_label[truth_object[segement]]),(30,70), font, 0.5,(0,0,0),1,cv2.LINE_AA)

            cv2.rectangle(data, (point_object_location[point], point_object_location[point + 1]),
                          (point_object_location[point + 2], point_object_location[point + 3]), (0, 255, 0), 2)
            cv2.putText(data,"box",(point_object_location[point],point_object_location[point+1]-10), font, 0.75,(0,255,0),1,cv2.LINE_AA)

            #print '{0}RGB_{1}.png'.format(image_path,index)
            #cv2.putText(data,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
            cv2.putText(data,'detect human label:{0}'.format(human_label[detect_human[segement]]),(30,90), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(data,'detect object label:{0}'.format(object_label[detect_object[segement]]),(30,110), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(data,'anticipation human label:{0}'.format(human_label[anticipation_human[segement]]),(30,130), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(data,'anticipation object label:{0}'.format(object_label[anticipation_object[segement]]),(30,150), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            cv_image = bridge.cv2_to_imgmsg(data,"bgr8")
            image_pub.publish(cv_image)
            index += 1
            point += 4
            timer.sleep()

            # print 'detect human label:{0}'.format(human_label[detect_human[segement]])
            # print 'detect object label:{0}'.format(object_label[detect_object[segement]])
            # print 'anticipation human label:{0}'.format(human_label[anticipation_human[segement]])
            # print 'anticipation object label:{0}'.format(object_label[anticipation_object[segement]])

        time.sleep(2)
        segement += 1

# to get the start and end frame of the activity
def ground_truth_label_interpreter(file):
                global start_frame
                global end_frame
                f = open(file)
                line = f.readline()
                while line:
                    s = line.split(',')
                    if(s[0] == activity):
                        start_frame.append(int(s[1]))
                        end_frame.append(int(s[2]))
                        # pdb.set_trace()
                    line = f.readline()
                f.close()

# to get the object upper left, lower right corner in the picture.
def object_location_interpreter(file):
                global point_object_location
                f = open(file)
                line = f.readline()
                while line:
                    s = line.split(',')
                    point_object_location.append(int(s[2]))
                    point_object_location.append(int(s[3]))
                    point_object_location.append(int(s[4]))
                    point_object_location.append(int(s[5]))
                    # pdb.set_trace()
                    line = f.readline()
                f.close()
if __name__ == "__main__":
                # pdb.set_trace()
                main()
