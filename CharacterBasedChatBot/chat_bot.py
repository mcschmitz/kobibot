import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import Adam

from CharacterBasedChatBot.network_definition import character_based_lstm
from DataLoader import CharacterEmbedder
from plot_loss import PlotLearning
from preprocess_data import DATA_OUT_PATH as DATA_INPUT_PATH

# PARAMETERS
MIN_SEQ_LEN = 1
MAX_SEQ_LEN = 120
BATCH_SIZE = 64
EPOCHS = 1000
LATENT_DIM = 256
MODEL_PATH = 'models/CharacterBasedChatBot.h5'
PROGRESS_PATH = "models/CharacterBasedChatBot_progress.png"

loader = CharacterEmbedder(DATA_INPUT_PATH)
loader.filter_sequences(min_sequence_length=MIN_SEQ_LEN, max_sequence_length=MAX_SEQ_LEN)
loader.create_char_dictionary(loader.short_questions, loader.short_answers)
escape_dict = {"eos": "$", 'unk': "§"}
loader.char_dictionary_to_int(answers=loader.short_answers, questions=loader.short_questions, escape_codes=escape_dict)
loader.txt2int(loader.short_questions, loader.short_answers)

questions = loader.short_questions
answers = loader.short_answers
answers_int = loader.answers_int
answers_int_to_vocab = loader.answers_int_to_wd
questions_int = loader.questions_int
questions_int_to_vocab = loader.questions_int_to_wd

encoder_input_data = np.zeros((len(questions), MAX_SEQ_LEN + 1, len(questions_int_to_vocab)), dtype='float32')
decoder_target_data = np.zeros((len(answers), MAX_SEQ_LEN + 1, len(answers_int_to_vocab)), dtype='float32')

for idx, question_int in enumerate(questions_int):
    for t, q in enumerate(question_int):
        encoder_input_data[idx, t, q] = 1

for idx, answer_int in enumerate(answers_int):
    for t, q in enumerate(answer_int):
        decoder_target_data[idx, t, q] = 1

early_stopper = EarlyStopping(patience=100)
model_saver = ModelCheckpoint(MODEL_PATH, save_best_only=True)
progress_plotter = PlotLearning(file_path=PROGRESS_PATH)
model = character_based_lstm(timesteps=MAX_SEQ_LEN + 1, num_encoder_tokens=len(questions_int_to_vocab),
                             num_decoder_tokens=len(answers_int_to_vocab))
model.compile(optimizer=Adam(.0005), loss='categorical_crossentropy', metrics=["accuracy"])
model.fit(encoder_input_data, decoder_target_data, batch_size=BATCH_SIZE, epochs=EPOCHS,
          validation_split=0.25, callbacks=[early_stopper, model_saver], verbose=2)
