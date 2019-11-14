import json
import operator
import os

import pandas as pd
from keras.preprocessing.text import Tokenizer, text_to_word_sequence

from preprocessing.preprocess_data import CORRECTION_MAP_DIR
from preprocessing.preprocess_data import MSG_TABLE_OUT_PATH

if __name__ == "__main__":
    data = pd.read_csv(MSG_TABLE_OUT_PATH, encoding="utf-8")
    tokenizer = Tokenizer(lower=False, filters='"#$%&()*+,-/;<=>@[\\]^`{|}~\t\n')
    tokenizer.fit_on_texts(data["Message"])

    ordered = sorted(tokenizer.word_counts.items(), key=operator.itemgetter(1))

    if os.path.exists(CORRECTION_MAP_DIR):
        with open(CORRECTION_MAP_DIR, 'r', encoding="utf-8") as f:
            map = json.load(f)
    else:
        map = {"smileys": {},
               "words": {}}

    standardized_msgs = [tokenizer.split.join(text_to_word_sequence(msg, filters=tokenizer.filters, lower=False)) for
                         msg in data["Message"]]

    for idx, (word, freq) in enumerate(ordered):
        if word not in map["words"]:
            examples = [msg for msg in standardized_msgs if word in msg.split(" ")][:3]
            print("({}/{}) - {} has a frequency of {}.\n".format(idx, len(ordered), word, freq),
                  "Examples are: {}\n".format(", ".join(examples)),
                  "If you want to replace is enter a string. Else press Enter.")
            new_seq = input()
            new_seq = new_seq if new_seq != "" else word
            map["words"][word] = new_seq
            with open(CORRECTION_MAP_DIR, 'w', encoding="utf-8") as fp:
                json.dump(map, fp, indent=4)
