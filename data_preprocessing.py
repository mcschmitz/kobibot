import re
import pandas as pd
import emoji


data_path = 'data/raw_data2.txt'

with open(data_path, 'r', encoding="utf-8") as f:
    strings = re.findall('(\d\d.\d\d.\d\d\,\s\d\d\:\d\d)\s+\-\s(\w+\s+\w+\s\w+|\w+\s\w+|\w+)\:(.*)', f.read())

# Convert list to a dataframe and name columns
MsgTable = pd.DataFrame(strings, columns=['DateTime', 'Sender', 'Message'])

del MsgTable['DateTime'], MsgTable['Sender']
MsgTable = MsgTable[['Medien weggelassen' not in msg for msg in MsgTable['Message']]]

# delete Emojis
MsgTable['Message'] = [emoji.demojize(m) for m in MsgTable["Message"]]
MsgTable['Message'] = [re.sub(':*.*:', '', msg) for msg in MsgTable['Message']]
MsgTable = MsgTable[[msg != '' for msg in MsgTable['Message']]]

msgs = []
for msg in MsgTable['Message']:
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
    msgs.append(msg)

MsgTable['Message'] = msgs

MsgTable.to_csv('data/prepro_data.csv', index=False)