import time


class Position:
    def __init__(self, line, word, index):
        self.line = line
        self.word = word
        self.index = index


class GameState:
    def __init__(self):
        with open('text.txt') as text:
            self.text = [line.split() for line in text.read().split('\n')]
        for line in self.text:
            for i in range(1, len(line)):
                line.insert(i * 2 - 1, ' ')
        self.active = False
        self.position = Position(0, 0, 0)
        self.amount_of_characters = 0
        self.observers = []
        self.begin = None
        self.timer = None
        self.errors = 0
        self.press = 1

    def next_position(self):
        self.position.index += 1
        self.amount_of_characters += 1
        if self.position.index == len(self.text[self.position.line][self.position.word]):
            self.position.word += 1
            self.position.index = 0
            if self.position.word == len(self.text[self.position.line]):
                self.position.line += 1
                self.position.word = 0

    def add_observer(self, observer):
        self.observers.append(observer)

    def correct_invoke_observers(self, keyboard_input):
        for observer in self.observers:
            observer.correct_invoke(keyboard_input, self.position)

    def incorrect_invoke_observers(self, keyboard_input):
        for observer in self.observers:
            observer.incorrect_invoke(keyboard_input, self.position)

    def check_correct_input(self, keyboard_input):
        self.press += 1
        if keyboard_input == self.text[self.position.line][self.position.word][self.position.index]:
            self.correct_invoke_observers(keyboard_input)
            self.next_position()
            return True
        self.errors += 1
        self.incorrect_invoke_observers(keyboard_input)
        return False

    def check_text_end(self):
        end = (self.position.line >= len(self.text))
        if end:
            self.active = False
            self.timer = time.time()
        return end

    def start(self):
        self.begin = time.time()
        self.active = True

    def get_time(self):
        if self.active:
            self.timer = time.time()
        return self.timer

    def get_wpm(self):
        return round(self.amount_of_characters / 5 / ((self.get_time() - self.begin) / 60))  # I count a word as 5 symbols

    def get_percent(self):
        return round(100 - self.errors / self.press * 100)
