import tensorflow as tf
import keras
import numpy as np
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from keras.layers import Input, Embedding, Bidirectional, Dense, GaussianNoise, Dropout, LSTM
from keras.models import Model

tokenizer = None
max_len = 200

with open('toxic-tokenizer.pickle','rb') as f:
    #global tokeniz
    tokenizer = pickle.load(f)

vocab_size = 210444
embedding_matrix = np.load('toxic-embed.npy')

def civitas_model():
    i = Input((200,))
    e = Embedding(vocab_size,25,weights = [embedding_matrix],input_length=max_len ,trainable = False)(i)
    #e = GaussianNoise(.05)(e)
    b = Bidirectional(LSTM(256))(e)
    b = Dropout(.3)(b)
    d1 = Dense(128,activation = 'relu')(b)
    d1 = Dense(128,activation = 'relu')(d1)
    d1 = Dense(128,activation = 'relu')(d1)
    d2 = Dense(2,activation = 'softmax')(d1)

    return keras.models.Model(inputs = i, outputs = d2)

model = civitas_model()
model.summary()
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics = ['accuracy', 'categorical_crossentropy'])

model.load_weights('civitas-2class-fixed.h5')

def infer_list(text):

    seq = tokenizer.texts_to_sequences(text)
    max_len = 200
    pad_seq = pad_sequences(seq,maxlen=max_len)

    return (model.predict(pad_seq)[0][1])

def infer(text):
    return infer_list([text])
