#!/usr/bin/env python
import cPickle

def read():
    path = '/media/bsb/666/human_anticipation_data/result'
    detection_human_data = cPickle.load(open('{0}/detection_human_677107.pik'.format(path)))
    anticipation_human_data = cPickle.load(open('{0}/anticipation_human_677107.pik'.format(path)))
    detection_object_data = cPickle.load(open('{0}/detection_object_677107.pik'.format(path)))
    anticipation_object_data = cPickle.load(open('{0}/anticipation_object_677107.pik'.format(path)))

    path2 = '/media/bsb/666/human_anticipation_data/CAD_120/features_cad120_ground_truth_segmentation/dataset/fold_1'
    ground_truth_test_data = cPickle.load(open('{0}/grount_truth_test_data_677107.pik'.format(path2)))
    ground_truth_label_human = ground_truth_test_data['labels_human']
    ground_truth_label_object = ground_truth_test_data['labels_objects']

    human_label = {1: 'reaching', 2: 'moving', 3: 'pouring', 4: 'eating', 5: 'drinking',
                     6: 'opening', 7: 'placing', 8: 'closing', 9: 'null', 10: 'cleaning'}
    object_label = {1: 'mvable', 2: 'stationary', 3: 'reachable', 4: 'pourable', 5: 'pourto',
                    6: 'containable', 7: 'drinkable', 8: 'openable', 9: 'placeable', 10: 'closeable', 11: 'cleanable',
                    12: 'cleaner'}

    print ground_truth_label_human[5].T
    print detection_human_data[5].T
    print anticipation_human_data[5].T
    print ground_truth_label_object[5].T
    print detection_object_data[5].T
    print anticipation_object_data[5].T

if __name__ =="__main__":
    read()

