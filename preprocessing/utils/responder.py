import numpy as np

from preprocess_data import msg_table


def get_responder(senders: list):
    """Extracts the first responder out of a list of senders.

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
    """Extracts the questioner out of a list of senders.

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
    unique_senders = list(set(senders))
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
