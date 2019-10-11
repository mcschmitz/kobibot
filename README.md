# Kobibot

**Analysis of WhatsApp data.**

For over 7 years I have been in a WhatsApp Group chat with few of the
funniest and lovely lunatics which I like to refer to as my friend from
school. After switching to Threema for obvious reasons I asked oen of
them to pass me a dump of 7 years of the group chat to see if I could
find insights from the data.

This project is still ongoing. For now three main parts are planned: 
1. Meta-Data Analysis
2. Analyzing the Messages
3. Building a chat bot that talks and behaves like me and my friends
   (Heaven forbid!)
   
First step - as in every data science project is data cleansing and
preprocessin. This is done in [this script](preprocess_data.py). It
requires the data to be in text format where each line is one message
with timestamp and sender name. Depending on the language settings of
your phone the data has a different format. In my case the dump came
from a german phone. Therefore, the data had the following format: 
```text
dd.mm.yy, HH:MM - <sender name>: <message>
```
After removing system messages and the script basically extracts the
timestamp, the sender name, the message, the number of words in the
message, the number of letters in the message as well as information of
the first responder and to whom this given message was a response and
dumps this information to a CSV File. Also dumps a list of the plain
messages without timestamp or sender information as a corpus used for
the chatbot training.