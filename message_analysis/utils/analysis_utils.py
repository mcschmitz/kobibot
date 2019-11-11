import emoji


def count_emojis(messages):
    emojis = {}
    for msg in messages:
        for word in msg:
            if word in list(emoji.UNICODE_EMOJI_ALIAS.values()):
                if word not in emojis:
                    emojis[word] = 1
                else:
                    emojis[word] += 1
    return emojis
