"""Some useful utilities when dealing with neural nets w/ tensorflow.
Parag K. Mital, Jan. 2016
"""
import tensorflow as tf
from pandas import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
#from libs.utils import load_data, plot_two_lines
def load_data(file_name, cols):
    df = pd.read_csv(file_name, usecols=cols)
    col = []
    for header in cols:
        col.append((df.loc[:,header]).tolist())
    return col
    '''
    >>>price = load_data('0002_out.csv',['Close','Volume'])
    '''
def load_df(data,name):
    return pd.DataFrame(data[0], index=list(range(len(data[0]))),columns=[name])

def load_series(data):
    return pd.Series(data[0], index=list(range(len(data[0]))))

def load_pandas(file_name,cols,pd_cols):
    '''
    convert csv into pandas df
    cols: columns to read in csv
    pd_cols = columns used in df
    >> a = load_pandas('closing_data.csv',
        ['snp_close','nyse_close'],
        ['snp_close','nyse_close'])
    '''
    if len(cols) != len(pd_cols):
        print "length of cols and pd_cols doesn't match"
    df = pd.DataFrame()
    for col, pd_col in zip(cols,pd_cols):
        df[pd_col] = load_series(load_data(file_name,[col]))
    return df


def slice_data(a,size_input,n_sample,constant=False):
    '''
    return random sliced time series
    size_input: length of samples
    n_input: number of samples

    >>>sample = slice_data(data,512,100)
    '''
    output = []
    if constant == False:
        for _ in range(n_sample):
            #print len(a)
            #print len(a)-size_input
            idx = random.randint(0, len(a)-size_input)
            output.append(a[idx:idx+size_input])
    else:
        a = a
        n_sample = len(a)/size_input
        for i in range(n_sample):
            idx = size_input*(i+1)
            #print idx
            #print size_input
            output.append(a[idx-size_input:idx])
    return output

def plot_two_lines(line1,line2):
    index = range(len(line1))
    plt.plot(index,line1,'bs',index,line2,'r--')
    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.show()
    '''
    >>>price = load_data('0002_out.csv',['Close','Volume'])
    >>>plot_two_lines(price[0],price[1])
    '''

def montage_batch(images):
    """Draws all filters (n_input * n_output filters) as a
    montage image separated by 1 pixel borders.

    Parameters
    ----------
    batch : Tensor
        Input tensor to create montage of.

    Returns
    -------
    m : numpy.ndarray
        Montage image.
    """
    img_h = images.shape[1]
    img_w = images.shape[2]
    n_plots = int(np.ceil(np.sqrt(images.shape[0])))
    m = np.ones(
        (images.shape[1] * n_plots + n_plots + 1,
         images.shape[2] * n_plots + n_plots + 1, 3)) * 0.5

    for i in range(n_plots):
        for j in range(n_plots):
            this_filter = i * n_plots + j
            if this_filter < images.shape[0]:
                this_img = images[this_filter, ...]
                m[1 + i + i * img_h:1 + i + (i + 1) * img_h,
                  1 + j + j * img_w:1 + j + (j + 1) * img_w, :] = this_img
    return m


# %%
def montage(W):
    """Draws all filters (n_input * n_output filters) as a
    montage image separated by 1 pixel borders.

    Parameters
    ----------
    W : Tensor
        Input tensor to create montage of.

    Returns
    -------
    m : numpy.ndarray
        Montage image.
    """
    W = np.reshape(W, [W.shape[0], W.shape[1], 1, W.shape[2] * W.shape[3]])
    n_plots = int(np.ceil(np.sqrt(W.shape[-1])))
    m = np.ones(
        (W.shape[0] * n_plots + n_plots + 1,
         W.shape[1] * n_plots + n_plots + 1)) * 0.5
    for i in range(n_plots):
        for j in range(n_plots):
            this_filter = i * n_plots + j
            if this_filter < W.shape[-1]:
                m[1 + i + i * W.shape[0]:1 + i + (i + 1) * W.shape[0],
                  1 + j + j * W.shape[1]:1 + j + (j + 1) * W.shape[1]] = (
                    np.squeeze(W[:, :, :, this_filter]))
    return m




# %%
def corrupt(x,shape,stddev):
    """Take an input tensor and add uniform masking.

    Parameters
    ----------
    x : Tensor/Placeholder
        Input to corrupt.

    Returns
    -------
    x_corrupted : Tensor
        50 pct of values corrupted.
    """
    return tf.add(x, tf.random_normal(shape=shape,
                                               mean=0.0,
                                               stddev=stddev,
                                               dtype=tf.float32))


# %%
def weight_variable(shape):
    '''Helper function to create a weight variable initialized with
    a normal distribution

    Parameters
    ----------
    shape : list
        Size of weight variable
    '''
    initial = tf.random_normal(shape, mean=0.0, stddev=0.01)
    return tf.Variable(initial)


# %%
def bias_variable(shape):
    '''Helper function to create a bias variable initialized with
    a constant value.

    Parameters
    ----------
    shape : list
        Size of weight variable
    '''
    initial = tf.random_normal(shape, mean=0.0, stddev=0.01)
    return tf.Variable(initial)
