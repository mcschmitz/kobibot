import re
import pandas as pd
import emoji
from tqdm import tqdm


def preprocess_msg(msg=str):
    msg = msg.replace('ü', 'ue')
    msg = msg.replace('ö', 'oe')
    msg = msg.replace('ä', 'ae')
    msg = msg.replace('ß', 'ss')
    msg = re.sub('\\x00', '', str(msg))
    msg = msg.replace('b\' ', '')
    msg = msg.replace('\'', '')
    msg = msg.strip()
    msg = msg.encode('ascii', 'ignore').decode("utf-8")
    return msg


# PARAMETERS
DATA_PATH = '../Data/kobibot/raw_chat.txt'
DATA_OUT_PATH = '../Data/kobibot/prepro_data.txt'

if __name__ == "__main__":
    with open(DATA_PATH, 'r', encoding="utf-8") as f:
        string = f.read()

    strings = string.split('\n')

    d_format = re.compile('\d{2}.\d{2}.\d{2},\s\d{2}:\d{2}')
    dates = []
    senders = []
    msgs = []
    for s in strings:
        date = s.split(' - ')[0]
        if d_format.match(date)is not None:
            dates.append(date)
            remaining_s = re.sub(date + ' - ', '', s)
            sender = remaining_s.split(': ')[0]
            senders.append(sender)
            msg = re.sub(sender + ': ', '', remaining_s)
            msgs.append(msg)

    # Convert list to a dataframe and name columns
    MsgTable = pd.DataFrame({'Time': dates, 'Sender': senders, 'Message': msgs})
    MsgTable["Sender"].value_counts()
    MsgTable = MsgTable[['Medien ausgeschlossen' not in msg for msg in MsgTable['Message']]]
    possible_senders = ['CP', 'MS', 'CZ', 'MSt', 'FA', 'FB', 'TT', 'MK', 'BH', 'CD', 'LM', 'MSc', 'CK']
    MsgTable = MsgTable[[sender in possible_senders for sender in MsgTable["Sender"]]]

    # delete Emojis
    MsgTable['Message'] = [emoji.demojize(m) for m in MsgTable["Message"]]
    MsgTable['Message'] = [re.sub(':*.*:', '', msg) for msg in MsgTable['Message']]
    MsgTable = MsgTable[[msg != '' for msg in MsgTable['Message']]]

    msgs = []
    for msg in tqdm(MsgTable['Message']):
        preprocessed_msg = preprocess_msg(msg)
        if len(preprocessed_msg) > 0:
            msgs.append(preprocessed_msg)
    with open(DATA_OUT_PATH, 'w') as f:
        for msg in msgs:
            f.write("%s\n" % msg)
