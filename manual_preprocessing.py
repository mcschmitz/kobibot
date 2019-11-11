import json
import operator
import os

import pandas as pd
from keras.preprocessing.text import Tokenizer

from preprocess_data import MSG_TABLE_OUT_PATH

MAP_DIR = "data/correction_map.json"

if __name__ == "__main__":
    data = pd.read_csv(MSG_TABLE_OUT_PATH, encoding="utf-8")
    tokenizer = Tokenizer(lower=False, filters='!"#$%&()*+,-./;<=>?@[\\]^`{|}~\t\n')
    tokenizer.fit_on_texts(data["Message"])

    ordered = sorted(tokenizer.word_counts.items(), key=operator.itemgetter(1))

    if os.path.exists(MAP_DIR):
        with open(MAP_DIR, 'r', encoding="utf-8") as f:
            map = json.load(f)
    else:
        map = {}

    for word, freq in ordered:
        if word not in map:
            examples = [msg for msg in data["Message"] if word in msg][:3]
            print("{} has a frequency of {}.\n".format(word, freq),
                  "Examples are: {}\n".format(", ".join(examples)),
                  "If you want to replace is enter a string. Else press Enter.")
            new_seq = input()
            new_seq = new_seq if new_seq != "" else word
            map[word] = new_seq
            with open(MAP_DIR, 'w', encoding="utf-8") as fp:
                json.dump(map, fp, indent=4)
