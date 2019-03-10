from keras import Sequential
from keras.layers import *

from Attention import AttentionDecoder


def character_based_lstm(timesteps, num_encoder_tokens, num_decoder_tokens):
    model = Sequential()
    model.add(LSTM(128, input_shape=(timesteps, num_encoder_tokens), return_sequences=True))
    model.add(LSTM(128, return_sequences=True))
    model.add(AttentionDecoder(128, num_decoder_tokens))
    return model
