from functools import wraps
from keras import backend as K
from keras.layers import Conv2D, Add, ZeroPadding2D, UpSampling2D, Concatenate, MaxPooling2D, Layer, Lambda
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from utils.utils import compose
import tensorflow as tf

def route_group(input_layer, groups, group_id):
    convs = tf.split(input_layer, num_or_size_splits=groups, axis=-1)
    return convs[group_id]

#--------------------------------------------------#
#   Single convolution
#--------------------------------------------------#
@wraps(Conv2D)
def DarknetConv2D(*args, **kwargs):
    darknet_conv_kwargs = {'kernel_regularizer': l2(5e-4)}
    darknet_conv_kwargs['padding'] = 'valid' if kwargs.get('strides')==(2,2) else 'same'
    darknet_conv_kwargs.update(kwargs)
    return Conv2D(*args, **darknet_conv_kwargs)

#---------------------------------------------------#
#   Convolution block
#   DarknetConv2D + BatchNormalization + LeakyReLU
#---------------------------------------------------#
def DarknetConv2D_BN_Leaky(*args, **kwargs):
    no_bias_kwargs = {'use_bias': False}
    no_bias_kwargs.update(kwargs)
    return compose( 
        DarknetConv2D(*args, **no_bias_kwargs),
        BatchNormalization(),
        LeakyReLU(alpha=0.1))


#---------------------------------------------------#
#   CSPdarknet structure block
#   There is a large residual edge
#   This large residual side bypasses a lot of residual structure
#---------------------------------------------------#
def resblock_body(x, num_filters):
    x = DarknetConv2D_BN_Leaky(num_filters, (3,3))(x)
    route = x
    x = Lambda(route_group,arguments={'groups':2, 'group_id':1})(x) 
    x = DarknetConv2D_BN_Leaky(int(num_filters/2), (3,3))(x)
    route_1 = x
    x = DarknetConv2D_BN_Leaky(int(num_filters/2), (3,3))(x)
    x = Concatenate()([x, route_1])
    x = DarknetConv2D_BN_Leaky(num_filters, (1,1))(x)
    feat = x
    x = Concatenate()([route, x])
    x = MaxPooling2D(pool_size=[2,2],)(x)

    # Finally, the number of channels is integrated
    return x, feat

#---------------------------------------------------#
#   The main part of darknet53
#---------------------------------------------------#
def darknet_body(x):
    # Perform length and width compression
    x = ZeroPadding2D(((1,0),(1,0)))(x)
    x = DarknetConv2D_BN_Leaky(32, (3,3), strides=(2,2))(x)
    # Perform length and width compression
    x = ZeroPadding2D(((1,0),(1,0)))(x)
    x = DarknetConv2D_BN_Leaky(64, (3,3), strides=(2,2))(x)
    
    x, _ = resblock_body(x,num_filters = 64)
    x, _ = resblock_body(x,num_filters = 128)
    x, feat1 = resblock_body(x,num_filters = 256)

    x = DarknetConv2D_BN_Leaky(512, (3,3))(x)

    feat2 = x
    return feat1, feat2

