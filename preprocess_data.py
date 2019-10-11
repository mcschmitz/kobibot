import re

import emoji
import numpy as np
import pandas as pd
from tqdm import tqdm


def standardize_str(s: str):
    """
    Standardizes a string by replacing umlauts and escape characters

    Args:
        s: the input string

    Returns:
        The standardized string
    """
    s = s.replace('ü', 'ue')
    s = s.replace('ö', 'oe')
    s = s.replace('ä', 'ae')
    s = s.replace('ß', 'ss')
    s = re.sub('\\x00', '', str(s))
    s = s.replace('b\' ', '')
    s = s.replace('\'', '')
    s = s.strip()
    s = s.encode('ascii', 'ignore').decode("utf-8")
    return s


def get_responder(senders: list):
    """
    Extract the responder out of a list of senders.

    Takes a list of senders and creates a list of responders of equal length. If the next message is from the current
    sender itself the value in the list is none

    Args:
        senders: list of senders

    Returns:
        list o responders
    """
    response_from = np.repeat(None, len(senders))
    idx = 0
    possible_responders = {}
    unique_senders = list(set(senders))
    while senders:
        sender = senders.pop(0)
        if sender not in possible_responders.keys():
            possible_responders[sender] = [cs for cs in unique_senders if cs != sender]
        for r in senders:
            if r in possible_responders[sender]:
                response_from[idx] = r
                if response_from[idx] == response_from[idx - 1]:
                    response_from[idx - 1] = None
                break
        idx += 1
    return response_from


def get_questioner(senders: list):
    """
    Extract the questionner out of a list of senders.

    Takes a list of senders and creates a list of questioners of equal length. If the previous message is from the
    current sender itself the value in the list is none

    Args:
        senders: list of senders

    Returns:
        list of questioners
    """
    response_to = np.repeat(None, len(senders))
    idx = len(msg_table) - 1
    possible_questioners = {}
    unique_senders = list(set(responder))
    while senders:
        sender = senders.pop(0)
        if sender not in possible_questioners.keys():
            possible_questioners[sender] = [cs for cs in unique_senders if cs != sender]
        for q in senders:
            if q in possible_questioners[sender]:
                response_to[idx] = q
                break
        idx -= 1
    current_responder = None
    for idx, rt in enumerate(response_to):
        if idx < len(response_to):
            if rt == current_responder:
                response_to[idx] = None
            else:
                current_responder = rt
    return response_to


# PARAMETERS
DATA_PATH = "data/raw_chat.txt"
MSG_TABLE_OUT_PATH = "data/msg_table.csv"
DATA_OUT_PATH = "data/prepro_data.txt"


if __name__ == "__main__":
    # Load lines from text file
    with open(DATA_PATH, 'r', encoding="utf-8") as f:
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
    # Remove uncommon senders to ger rid of system messages
    print(msg_table["Sender"].value_counts())
    common_senders = msg_table["Sender"].value_counts().index[msg_table["Sender"].value_counts() > 10]
    msg_table = msg_table[msg_table["Sender"].isin(common_senders)]

    # Remove media excluded system message
    msg_table = msg_table[['<Medien ausgeschlossen>' not in msg for msg in msg_table['Message']]].reset_index(drop=True)
    msg_table["nWords"] = [len(m.split()) for m in msg_table["Message"]]
    msg_table["nLetters"] = [len(m) for m in msg_table["Message"]]

    responder = msg_table["Sender"].values.tolist()
    response_from = get_responder(responder)
    msg_table["ResponseFrom"] = response_from

    questioner = list(reversed(msg_table["Sender"].values.tolist()))
    response_to = get_questioner(questioner)
    msg_table["ResponseTo"] = response_to
    msg_table.to_csv(MSG_TABLE_OUT_PATH, index=False, encoding="utf-8")

    # delete Emojis
    msg_table['Message'] = [emoji.demojize(m) for m in msg_table["Message"]]
    msg_table['Message'] = [re.sub(':*.*:', '', msg) for msg in msg_table['Message']]
    msg_table = msg_table[[msg != '' for msg in msg_table['Message']]]

    msgs = []
    for msg in tqdm(msg_table['Message']):
        preprocessed_msg = standardize_str(msg)
        if len(preprocessed_msg) > 0:
            msgs.append(preprocessed_msg)
    with open(DATA_OUT_PATH, 'w') as f:
        for msg in msgs:
            f.write("%s\n" % msg)
