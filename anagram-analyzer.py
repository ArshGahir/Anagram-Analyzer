# -*- coding: utf-8 -*-
"""

Written by: Arshveer Singh Gahir

Description:

This program looks for words which may be anagrams of each other in a block of text of any size.

  Upload your book to the program by changing the name of file in 'f'

  The Program then reads the book, cleans up punctuation marks, removes un-interesting words, stop words, 
  connecting words; and then sorts and stores unique words in a dictionary {word:frequency}.

  The Program then assigns a creates a hash value based on the letters and number of letters, so anagrams
  would have the same hash value

  Elements of same hash value are stored in a dictionary {hash:frequency}

  Elements of same hash value are stored in another dictionary {hash:[word, anagrams]} , Elements are sorted, 
  and only the ones with more than one value in key:value pair are kept

  2 Dictionaries are cross-referenced, and a new dictionary stores {[word, anagrams]: frequency}

  Final Dictionary is then converted to a DataFrame

  Search Function takes a string input and searches for the word or anagram


"""

from collections import Counter
import sys
import time
import pandas as pd
from tabulate import tabulate

# Using a Dictionary

f = open('adventures_of_huckleberry_finn.txt', 'r', errors='ignore')
dictionary = f.read()


def make_hash(v):
    hashed = sum((hash(x) for x in list(v)))
    return hashed


###Select all words from Book, remove punctuation symbols, remove stop words, remove duplicate words
processed_words = []


def cleanup(file_contents):
    # Here is a list of punctuations and uninteresting words you can use to process your text
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
                           "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its",
                           "they", "them", \
                           "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be",
                           "been", "being", \
                           "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when",
                           "where", "how", \
                           "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very",
                           "can", "will", "just", \
                           'there', 'for', "in"]

    # Process String Data into Lists

    processed_file_contents = file_contents.split()
    processed_punctuations = punctuations.split()
    frequency_processed_words = {}

    # Iterate over each word

    for word in processed_file_contents:

        # Iterate over each alphabet of every VALID word
        if word.lower() not in uninteresting_words:
            clean_word = ""
            letters = word.split()
            for letter in letters:
                if letter not in processed_punctuations:
                    if letter.isalpha():
                        clean_word += letter
                        processed_words.append("".join(clean_word.upper()))

    for word in processed_words:
        if word not in frequency_processed_words.keys():
            frequency_processed_words[word] = 1
        else:
            frequency_processed_words[word] += 1

    ##Return unique, clean, uppercase words, with frequencies
    return frequency_processed_words


clean_book = cleanup(dictionary)
# Number of Words
print("Number of Words in book = {}".format(len(clean_book)))


def anagram_analyzer(frequency_processed_words):
    ###Pairing Anagrams by Hash value

    global hash_register
    hash_register = {}

    for i in processed_words:
        if make_hash(i) not in hash_register.keys():
            hash_register[make_hash(i)] = [i]
        elif i in hash_register[make_hash(i)]:
            pass
        else:
            hash_register[make_hash(i)].extend([i])

    ####Clean hash register, only contains 2 or more values

    global anagram_hash_register
    anagram_hash_register = {}

    for k, v in hash_register.items():
        if len(v) > 1:
            anagram_hash_register[k] = v

    ####Creates Hash values for all keys in clean_book

    global hash_book
    hash_book = {}

    for k, v in clean_book.items():
        if make_hash(k) not in hash_book:
            hash_book[make_hash(k)] = v
        else:
            hash_book[make_hash(k)] += v

    ###Match Clean register with frequency

    global anagram_frequency_table
    anagram_frequency_table = {}

    for k, v in anagram_hash_register.items():
        if k in hash_book:
            anagram_frequency_table['{}'.format(v)] = hash_book[k]

    return anagram_frequency_table


def make_df(final_dict):
    ###Convert dictionary to dataframe

    final_df = pd.DataFrame.from_dict(final_dict, orient='index')
    final_df.reset_index(inplace=True)
    final_df.rename(columns={final_df.columns[0]: 'Anagrams', final_df.columns[1]: 'Frequency'}, inplace=True)

    return final_df


def search_anagram():
    ###Convert input to hash value, and search

    query = input(str("What word would you like to search?  "))
    query_hashed = make_hash(query.upper())
    output = ''

    
    if query_hashed in hash_register.keys():
        output = f'Anagrams: {hash_register[query_hashed]}, Frequency: {hash_book[query_hashed]}'
    else:
        output = f'Neither the word,*** {query} ***, or it\'s anagram are present in the text.'

    return output


if __name__ == '__main__':
    start = time.time()
    test_anagrams = anagram_analyzer(clean_book)
    print(test_anagrams)
    stop = time.time()
    # Number of Words
    print("Total Number of Words in book = {}".format(len(clean_book)))
    print(f"Number of anagrams: {len(test_anagrams)}")
    print(f"Time Taken: {round(stop - start, 2)} seconds")
    print(make_df(test_anagrams))
    # Search Feature
    while True:
        result = search_anagram()
        print(result)
