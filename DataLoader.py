class DataLoader:
    def __init__(self, file_path):
        self.lines = open(file_path, encoding='utf-8', errors='ignore').read().split('\n')[1:]
        self.questions, self.answers = self.get_qa()
        print("# of questions:", len(self.questions))
        print("# of answers:", len(self.answers))

        self.sequence_lengths = self.get_sequence_length()
        self.questions_int_to_vocab = {}
        self.answers_int_to_vocab = {}
        self.questions_int = []
        self.answers_int = []

    def get_qa(self):
        questions = []
        answers = []
        for i, l in enumerate(self.lines):
            if i == 0 or i > len(self.lines) - 2:
                continue
            questions.append(self.lines[i])
            answers.append(self.lines[i + 1])
        return questions, answers

    def get_sequence_length(self):
        lengths = []
        for q in self.questions:
            lengths.append(len(q.split()))
        for a in self.answers:
            lengths.append(len(a.split()))
        return lengths

    def filter_sequences(self, min_sequence_length=2, max_sequence_length=40):
        self.short_questions = []
        self.short_answers = []
        for question, answer in zip(self.questions, self.answers):
            question_in_range = min_sequence_length <= len(question.split()) <= max_sequence_length
            answer_in_range = min_sequence_length <= len(answer.split()) <= max_sequence_length
            if question_in_range and answer_in_range:
                self.short_questions.append(question)
                self.short_answers.append(answer)
        print("# of shortened questions:", len(self.short_questions))
        print("# of shortened answers:", len(self.short_answers))
        print("% of data used: {}%".format(round(len(self.short_questions) / len(self.questions), 4) * 100))

    def create_vocab(self, questions, answers):
        self.vocab = {}
        if questions is None:
            questions = self.questions
        if answers is None:
            answers = self.answers
        for question in questions:
            for word in question.split():
                if word not in self.vocab:
                    self.vocab[word] = 1
                else:
                    self.vocab[word] += 1
        for answer in answers:
            for word in answer.split():
                if word not in self.vocab:
                    self.vocab[word] = 1
                else:
                    self.vocab[word] += 1

    def vocab_to_int(self, answers):
        self.questions_vocab_to_int = {}
        self.answers_vocab_to_int = {}

        if answers is None:
            answers = self.answers

        word_num = 0
        for word, count in self.vocab.items():
            self.questions_vocab_to_int[word] = word_num
            word_num += 1

        word_num = 0
        for word, count in self.vocab.items():
            self.answers_vocab_to_int[word] = word_num
            word_num += 1

        codes = ['<PAD>', '<EOS>', '<UNK>', '<GO>']
        for code in codes:
            self.questions_vocab_to_int[code] = len(self.questions_vocab_to_int) + 1

        for code in codes:
            self.answers_vocab_to_int[code] = len(self.answers_vocab_to_int) + 1

        self.questions_int_to_vocab = {v_i: v for v, v_i in self.questions_vocab_to_int.items()}
        self.answers_int_to_vocab = {v_i: v for v, v_i in self.answers_vocab_to_int.items()}

        for i in range(len(answers)):
            answers[i] += ' <EOS>'

    def txt2int(self, questions, answers):
        if questions is None:
            questions = self.questions
        if answers is None:
            answers =  self.answers
        self.questions_int = []
        for question in questions:
            ints = []
            for word in question.split():
                if word not in self.questions_vocab_to_int:
                    ints.append(self.questions_vocab_to_int['<UNK>'])
                else:
                    ints.append(self.questions_vocab_to_int[word])
            self.questions_int.append(ints)

        self.answers_int = []
        for answer in answers:
            ints = []
            for word in answer.split():
                if word not in self.answers_vocab_to_int:
                    ints.append(self.answers_vocab_to_int['<UNK>'])
                else:
                    ints.append(self.answers_vocab_to_int[word])
            self.answers_int.append(ints)
