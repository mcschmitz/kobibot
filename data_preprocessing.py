import re
import pandas as pd
import emoji


def preprocess_msg(msg=str):
    msg = msg.replace('ü', 'ue')
    msg = msg.replace('ö', 'oe')
    msg = msg.replace('ä', 'ae')
    msg = msg.replace('ß', 'ss')
    msg = msg.encode('utf8')
    msg = re.sub('\\\\x..', '', str(msg))
    msg = msg.replace('b\' ', '')
    msg = msg.replace('\'', '')
    msg = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", msg)
    msg = (msg.lstrip().rstrip())
    msg = msg.lower()
    return msg


# PARAMETERS
DATA_PATH = '../Data/kobibot/raw_chat.txt'
DATA_OUT_PATH = '../Data/kobibot/prepro_data.csv'

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
    for msg in MsgTable['Message']:
        msgs.append(preprocess_msg(msg))
    MsgTable['Message'] = msgs
    MsgTable = MsgTable["Message"]
    MsgTable.to_csv(DATA_OUT_PATH, index=False)
