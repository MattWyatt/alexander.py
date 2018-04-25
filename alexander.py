"""
this is a markov-chain algorithm thingy that takes a text as
an input and outputs another text. the results are hilarious
when used on things like shakespeare and song lyrics.
"""

import time
from sys import argv

"""
if you want to use this script as an import statement,
copy and paste everything in between this comment and the next one
"""
from random import randint

def split_text(text):
    words = []
    current_index = 0

    for iterator in range(0, len(text)):
        if text[iterator] == ' ':
            words.append(text[current_index:iterator])
            current_index = iterator + 1
    words.append(text[current_index:])
    return words

class alexander_key:
    def __init__(self, key_name):
        self.key_name = key_name
        self.values = []

    def add(self, value):
        self.values.append(value)

    def get(self):
        try:
            return self.values[randint(0, len(self.values)-1)]
        except IndexError:
            return

    def has_values(self):
        if len(self.values) > 0:
            return True
        else:
            return False

class alexander_parser:
    def __init__(self, input_file, output_file, output_length):
        self.input_file = input_file
        self.output_file = output_file
        self.output_length = output_length
        self.alexander_dictionary = []
        self.response = ""

    def add_to_dictionary(self, key, value):
        for token in self.alexander_dictionary:
            if token.key_name == key:
                token.add(value)
                return
        new_key = alexander_key(key)
        new_key.add(value)
        self.alexander_dictionary.append(new_key)

    def parse_text(self):
        split = split_text(str(open(self.input_file, "r", encoding="utf-8").read()))
        for iterator in range(0, len(split)):
            try:
                self.add_to_dictionary(split[iterator], split[iterator+1])
            except IndexError:
                return

    def get_value(self, key):
        for token in self.alexander_dictionary:
            if token.key_name == key and token.has_values():
                return token.get()
            elif token.key_name == key and not token.has_values():
                return

    def has_value(self, key):
        for token in self.alexander_dictionary:
            if token.key_name == key and token.has_values():
                return True
            elif token.key_name == key and not token.has_values():
                return False

    def construct_response(self):
        response = ""
        word = self.alexander_dictionary[randint(0, len(self.alexander_dictionary))].get()
        found_end = False
        counter = 0
        while not found_end:
            counter += 1
            if self.has_value(word):
                word = self.get_value(word)
                response += word
                response += " "
            elif not self.has_value(word):
                found_end = True
            if counter > self.output_length:
                found_end = True
        self.response = response

    def write_response(self):
    	open(self.output_file, "w").write(self.response)
"""
stop here if you plan to use this like an import statement
"""

def do_parse(input_file, output_file, length):
    print("begin parsing...")
    begin_time = time.time()
    alex = alexander_parser(input_file, output_file, int(length))
    alex.parse_text()
    print("done parsing, took ~{} seconds".format(round(time.time() - begin_time, 2)))
    print("writing the chain...")
    begin_time = time.time()
    alex.construct_response()
    alex.write_response()
    print("wrote text in ~{} seconds".format(round(time.time() - begin_time, 2)))


if len(argv) != 4:
    print("Usage alexander.py input_file output_file number_words")
    print("example: alexander.py input.txt output.txt 200")
else:
    do_parse(argv[1], argv[2], argv[3])