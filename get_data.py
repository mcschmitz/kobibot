import pandas as pd
import tensorflow as tf


def get_data():
    # Load the data# Load
    lines = open('../Data/kobibot/prepro_data.csv', encoding='utf-8', errors='ignore').read().split('\n')[1:]

    # define Q&A pairs
    questions = []
    answers = []
    for i, l in enumerate(lines):
        if i == 0 or i > len(lines)-2:
            continue
        questions.append(lines[i])
        answers.append(lines[i+1])

    print(len(questions))
    print(len(answers))

    # Find the length of sentences# Find t
    lengths = []
    for q in questions:
        lengths.append(len(q.split()))
    for a in answers:
        lengths.append(len(a.split()))

    # Create a dataframe so that the values can be inspected
    lengths = pd.DataFrame(lengths, columns=['counts'])
    lengths.describe()

    # Remove questions and answers that are shorter than 2 words and longer than 20 words.
    min_line_length = 2
    max_line_length = 40

    # Filter out the questions that are too short/long
    short_questions_temp = []
    short_answers_temp = []

    i = 0
    for question in questions:
        if len(question.split()) >= min_line_length and len(question.split()) <= max_line_length:
            short_questions_temp.append(question)
            short_answers_temp.append(answers[i])
        i += 1

    # Filter out the answers that are too short/long
    short_questions = []
    short_answers = []

    i = 0
    for answer in short_answers_temp:
        if len(answer.split()) >= min_line_length and len(answer.split()) <= max_line_length:
            short_answers.append(answer)
            short_questions.append(short_questions_temp[i])
        i += 1

    # Compare the number of lines we will use with the total number of lines.
    print("# of questions:", len(short_questions))
    print("# of answers:", len(short_answers))
    print("% of data used: {}%".format(round(len(short_questions)/len(questions),4)*100))

    # Create a dictionary for the frequency of the vocabulary
    vocab = {}
    for question in short_questions:
        for word in question.split():
            if word not in vocab:
                vocab[word] = 1
            else:
                vocab[word] += 1

    for answer in short_answers:
        for word in answer.split():
            if word not in vocab:
                vocab[word] = 1
            else:
                vocab[word] += 1

    # Remove rare words from the vocabulary.
    # We will aim to replace fewer than 5% of words with <UNK>
    # You will see this ratio soon.
    threshold = 10
    count = 0
    for k, v in vocab.items():
        if v >= threshold:
            count += 1

    print("Size of total vocab:", len(vocab))
    print("Size of vocab we will use:", count)

    # In case we want to use a different vocabulary sizes for the source and target text,
    # we can set different threshold values.
    # Nonetheless, we will create dictionaries to provide a unique integer for each word.
    questions_vocab_to_int = {}

    word_num = 0
    for word, count in vocab.items():
        if count >= threshold:
            questions_vocab_to_int[word] = word_num
            word_num += 1

    answers_vocab_to_int = {}

    word_num = 0
    for word, count in vocab.items():
        if count >= threshold:
            answers_vocab_to_int[word] = word_num
            word_num += 1

    # Add the unique tokens to the vocabulary dictionaries.
    codes = ['<PAD>', '<EOS>', '<UNK>', '<GO>']

    for code in codes:
        questions_vocab_to_int[code] = len(questions_vocab_to_int) + 1

    for code in codes:
        answers_vocab_to_int[code] = len(answers_vocab_to_int) + 1

    # Create dictionaries to map the unique integers to their respective words.
    # i.e. an inverse dictionary for vocab_to_int.
    questions_int_to_vocab = {v_i: v for v, v_i in questions_vocab_to_int.items()}
    answers_int_to_vocab = {v_i: v for v, v_i in answers_vocab_to_int.items()}

    # Add the end of sentence token to the end of every answer.# Add th
    for i in range(len(short_answers)):
        short_answers[i] += ' <EOS>'

    # Convert the text to integers.
    # Replace any words that are not in the respective vocabulary with <UNK>
    questions_int = []
    for question in short_questions:
        ints = []
        for word in question.split():
            if word not in questions_vocab_to_int:
                ints.append(questions_vocab_to_int['<UNK>'])
            else:
                ints.append(questions_vocab_to_int[word])
        questions_int.append(ints)

    answers_int = []
    for answer in short_answers:
        ints = []
        for word in answer.split():
            if word not in answers_vocab_to_int:
                ints.append(answers_vocab_to_int['<UNK>'])
            else:
                ints.append(answers_vocab_to_int[word])
        answers_int.append(ints)

    # Check the lengths
    print(len(questions_int))
    print(len(answers_int))

    # Calculate what percentage of all words have been replaced with <UNK>
    word_count = 0
    unk_count = 0

    for question in questions_int:
        for word in question:
            if word == questions_vocab_to_int["<UNK>"]:
                unk_count += 1
            word_count += 1

    for answer in answers_int:
        for word in answer:
            if word == answers_vocab_to_int["<UNK>"]:
                unk_count += 1
            word_count += 1

    unk_ratio = round(unk_count / word_count, 4) * 100

    print("Total number of words:", word_count)
    print("Number of times <UNK> is used:", unk_count)
    print("Percent of words that are <UNK>: {}%".format(round(unk_ratio, 3)))

    # Sort questions and answers by the length of questions.
    # This will reduce the amount of padding during training
    # Which should speed up training and help to reduce the loss

    sorted_questions = []
    sorted_answers = []

    for length in range(1, max_line_length+1):
        for i in enumerate(questions_int):
            if len(i[1]) == length:
                sorted_questions.append(questions_int[i[0]])
                sorted_answers.append(answers_int[i[0]])

    return short_answers, answers_int, answers_int_to_vocab, short_questions, questions_int, questions_int_to_vocab
