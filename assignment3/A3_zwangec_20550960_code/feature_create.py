import scipy.misc as misc
import pickle
import tensorflow as tf
from tqdm import tqdm
import numpy as np
import argparse
import fnmatch
import sys
import os

sys.path.insert(0, 'nets/')

slim = tf.contrib.slim


def getPaths(data_dir):
    image_paths = []
    ps = ['jpg', 'jpeg', 'JPG', 'JPEG', 'bmp', 'BMP', 'png', 'PNG']
    for p in ps:
        pattern = '*.' + p
        for d, s, fList in os.walk(data_dir):
            for filename in fList:
                if fnmatch.fnmatch(filename, pattern):
                    fname_ = os.path.join(d, filename)
                    image_paths.append(fname_)
    return image_paths


if __name__ == '__main__':

    data_dir = 'images/'
    checkpoint_file = 'resnet_v1_101.ckpt'

    x = tf.placeholder(tf.float32, shape=(1, 224, 224, 3))

    from resnet_v1 import *

    '''
    using resnet_v1_101 pretrained model
    '''
    arg_scope = resnet_arg_scope()
    with slim.arg_scope(arg_scope):
        logits, end_points = resnet_v1_101(x, is_training=False, num_classes=1000)
        features = end_points['global_pool']
    sess = tf.Session()
    saver = tf.train.Saver()
    saver.restore(sess, checkpoint_file)

    feat_dict = {}
    paths = getPaths(data_dir)
    '''
    show the procedure
    '''
    for path in tqdm(paths):
        image = misc.imread(path)
        image = misc.imresize(image, (224, 224))
        '''
        resize all the picture
        '''
        image = np.expand_dims(image, 0)
        feat = np.squeeze(sess.run(features, feed_dict={x: image}))
        feat_dict[path] = feat

    exp_pkl = open('features.pkl', 'wb')
    data = pickle.dumps(feat_dict)
    exp_pkl.write(data)
    exp_pkl.close()
