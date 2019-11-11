import json
import os
import re

import pandas as pd
from tqdm import tqdm

from preprocessing.utils import get_responder, get_questioner
from preprocessing.utils import standardize_message, correct_message

# PARAMETERS
DATA_PATH = "data/raw_chat.txt"
CORRECTION_MAP_DIR = "data/correction_map.json"
MSG_TABLE_OUT_PATH = "data/msg_table.csv"
DATA_OUT_PATH = "data/prepro_data.txt"


if __name__ == "__main__":
    # Load lines from text file
    with open(DATA_PATH, 'r', encoding="utf-8", errors="ignore") as f:
        string = f.read()
    strings = string.split('\n')

    # Separate strings into date, sender and message
    date_format = re.compile('\d{2}.\d{2}.\d{2},\s\d{2}:\d{2}')
    dates = []
    senders = []
    msgs = []
    for s in strings:
        date = s.split(' - ')[0]
        if date_format.match(date) is not None:
            dates.append(date)
            remaining_s = re.sub(date + ' - ', '', s)
            sender = remaining_s.split(': ')[0]
            senders.append(sender)
            msg = re.sub(sender + ': ', '', remaining_s)
            msgs.append(msg)

    # Convert list to a dataframe and name columns
    msg_table = pd.DataFrame({'Time': dates, 'Sender': senders, 'Message': msgs})
    # Remove uncommon senders to get rid of system messages
    common_senders = msg_table["Sender"].value_counts().index[msg_table["Sender"].value_counts() > 10]
    msg_table = msg_table[msg_table["Sender"].isin(common_senders)]

    # Remove 'media excluded' system message
    msg_table = msg_table[['<Medien ausgeschlossen>' not in msg for msg in msg_table['Message']]].reset_index(drop=True)
    msgs = []

    if os.path.exists(CORRECTION_MAP_DIR):
        with open(CORRECTION_MAP_DIR, 'r', encoding="utf-8") as f:
            correction_map = json.load(f)
    else:
        correction_map = {}

    for msg in tqdm(msg_table['Message']):
        msg = standardize_message(msg)
        if len(correction_map) > 0:
            msg = correct_message(msg, correction_map["smileys"], smiley=True)
        msgs.append(msg)

    with open(DATA_OUT_PATH, 'w', encoding="utf-8") as f:
        for msg in msgs:
            if len(msg) > 0:
                f.write("%s\n" % msg)

    msg_table["Message"] = msgs
    msg_table = msg_table[msg_table["Message"] != ""]
    msg_table.reset_index(inplace=True)

    msg_table["nWords"] = [len(m.split()) for m in msg_table["Message"]]
    msg_table["nLetters"] = [len(m) for m in msg_table["Message"]]

    responder = msg_table["Sender"].values.tolist()
    response_from = get_responder(responder)
    msg_table["ResponseFrom"] = response_from

    questioner = list(reversed(msg_table["Sender"].values.tolist()))
    response_to = get_questioner(questioner)
    msg_table["ResponseTo"] = response_to
    msg_table.to_csv(MSG_TABLE_OUT_PATH, index=False, encoding="utf-8")
