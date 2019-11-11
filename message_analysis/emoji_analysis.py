import pandas as pd

from message_analysis.utils import count_emojis
from preprocess_data import MSG_TABLE_OUT_PATH

data = pd.read_csv(MSG_TABLE_OUT_PATH, encoding="utf-8")

all_senders = count_emojis(data["Message"].values.tolist())
