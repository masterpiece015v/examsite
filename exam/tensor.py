import tensorflow as tf
from PIL import Image
from matplotlib import pylab as plt
import numpy as np
import os
from django.conf import settings

class Ainum:
    sess = tf.InteractiveSession()
    #入力データ
    x = tf.placeholder("float",shape=[None,784])
    #正解データ
    y_ = tf.placeholder( "float" ,shape=[None,10])

    def weight_variable( shape ):
        initial = tf.truncated_normal( shape,stddev=0.1)
        return tf.Variable(initial)

    def bias_variable( shape ):
        initial = tf.constant( 0.1, shape=shape)
        return tf.Variable( initial )

    def conv2d( x,W ):
        return tf.nn.conv2d( x , W , strides=[1,1,1,1], padding='SAME')

    def max_pool_2x2( x ):
        return tf.nn.max_pool( x, ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

    W_conv1 = weight_variable([5,5,1,32])
    b_conv1 = bias_variable([32])

    x_image = tf.reshape(x,[-1,28,28,1])

    h_conv1 = tf.nn.relu( conv2d(x_image,W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2( h_conv1 )

    W_conv2 = weight_variable( [5,5,32,64] )
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu( conv2d(h_pool1,W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2( h_conv2 )

    W_fc1 = weight_variable([7*7*64,1024])
    b_fc1 = bias_variable( [1024] )

    h_pool2_flat = tf.reshape( h_pool2,[-1,7*7*64])

    h_fc1 = tf.nn.relu( tf.matmul(h_pool2_flat,W_fc1) + b_fc1 )

    keep_prob = tf.placeholder("float")
    h_fc1_drop = tf.nn.dropout( h_fc1,keep_prob)

    W_fc2 = weight_variable( [1024,10] )
    b_fc2 = bias_variable( [10] )

    #y_conv = tf.nn.softmax( tf.matmul( h_fc1_drop , W_fc2 ) + b_fc2 )
    y_conv = tf.nn.softmax( tf.matmul( h_fc1 , W_fc2 ) + b_fc2 )
    sess.run( tf.initialize_all_variables() )

    saver = tf.train.Saver()

    path = settings.BASE_DIR
    print( path )
    #saver.restore( sess, os.path.join(path,"exam","CNN","CNN.ckpt"))
    saver.restore( sess, "/var/www/env/examsite/exam/CNN/CNN.ckpt")
    print("学習データを読み込みました")

    def get_num(self,source):
        img = Image.fromarray( source ).convert('L')
        plt.imshow( img )
        img.thumbnail((28,28))

        img = np.array(img,dtype=np.float32)
        img = 1 - np.array( img / 255 )
        img = img.reshape( 1 , 784 )

        p = self.sess.run( self.y_conv, feed_dict={self.x:img , self.y_:[[0.0] * 10], self.keep_prob:0.5})[0]

        return np.argmax(p)
