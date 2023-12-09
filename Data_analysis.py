#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import nltk

nltk.download('punkt')

stopwords_folder_path = "C:\\Users\\santh\\Documents\\Blackcoffer_data\\Blackcoffer_data\\StopWords"
stop_words = set()

for filename in os.listdir(stopwords_folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(stopwords_folder_path, filename)
        with open(file_path, 'r', encoding='latin-1') as stop_words_file:
            stop_words.update(stop_words_file.read().splitlines())

master_dictionary_folder_path = "C:\\Users\\santh\\Documents\\Blackcoffer_data\\Blackcoffer_data\\MasterDictionary"
positive_words_path = os.path.join(master_dictionary_folder_path, "positive-words.txt")
negative_words_path = os.path.join(master_dictionary_folder_path, "negative-words.txt")

positive_words = set()
negative_words = set()

def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as words_file:
        return set(words_file.read().splitlines())

positive_words = read_words_from_file(positive_words_path)
negative_words = read_words_from_file(negative_words_path)

data_extraction_results_folder_path = "C:\\Users\\santh\\Documents\\Project Intern Assessment\\output_texts"
text_files = [f for f in os.listdir(data_extraction_results_folder_path) if f.endswith(".txt")]

data_extraction_results_path = "C:\\Users\\santh\\Documents\\Blackcoffer_data\\Blackcoffer_data\\Output Data Structure.xlsx"
output_df = pd.read_excel(data_extraction_results_path)

def clean_text(text):
    words = word_tokenize(text)
    cleaned_words = [word.lower() for word in words if word.lower() not in stop_words and word.isalnum()]
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text

def extract_derived_variables(text):
    blob = TextBlob(text)

    positive_score = sum(1 for sentence in blob.sentences if sentence.sentiment.polarity > 0)
    negative_score = sum(1 for sentence in blob.sentences if sentence.sentiment.polarity < 0)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(word_tokenize(text)) + 0.000001)

    avg_sentence_length = sum(len(word_tokenize(str(sentence))) for sentence in blob.sentences) / len(blob.sentences)
    percentage_of_complex_words = sum(1 for word in word_tokenize(text) if len(word) > 2) / len(word_tokenize(text))
    fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)
    avg_words_per_sentence = len(word_tokenize(text)) / len(blob.sentences)
    complex_word_count = sum(1 for word in word_tokenize(text) if len(word) > 2)
    word_count = len([word for word in word_tokenize(text) if word.lower() not in stop_words and word.isalnum()])
    syllable_count_per_word = sum(syllable_count(word) for word in word_tokenize(text)) / word_count
    personal_pronouns = sum(1 for word in word_tokenize(text) if word.lower() in {'i', 'we', 'my', 'ours', 'us'})
    avg_word_length = sum(len(word) for word in word_tokenize(text)) / word_count

    return (
        positive_score, negative_score, polarity_score, subjectivity_score,
        avg_sentence_length, percentage_of_complex_words, fog_index,
        avg_words_per_sentence, complex_word_count, word_count,
        syllable_count_per_word, personal_pronouns, avg_word_length
    )

def syllable_count(word):
    vowels = "aeiouy"
    count = 0
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count = 1
    return count

for text_file in text_files:
    url_id = int(os.path.splitext(text_file)[0])

    text_file_path = os.path.join(data_extraction_results_folder_path, text_file)
    with open(text_file_path, 'r', encoding='utf-8') as file:
        article_text = file.read()

    cleaned_text = clean_text(article_text)
    derived_variables = extract_derived_variables(cleaned_text)

    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'POSITIVE SCORE'] = derived_variables[0]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'NEGATIVE SCORE'] = derived_variables[1]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'POLARITY SCORE'] = derived_variables[2]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'SUBJECTIVITY SCORE'] = derived_variables[3]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'AVG SENTENCE LENGTH'] = derived_variables[4]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'PERCENTAGE OF COMPLEX WORDS'] = derived_variables[5]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'FOG INDEX'] = derived_variables[6]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'AVG NUMBER OF WORDS PER SENTENCE'] = derived_variables[7]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'COMPLEX WORD COUNT'] = derived_variables[8]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'WORD COUNT'] = derived_variables[9]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'SYLLABLE PER WORD'] = derived_variables[10]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'PERSONAL PRONOUNS'] = derived_variables[11]
    output_df.loc[output_df['URL_ID'].astype(int) == url_id, 'AVG WORD LENGTH'] = derived_variables[12]

output_result_path = "C:\\Users\\santh\\Documents\\Project Intern Assessment\\Blackcoffer_Assessment\\Output.xlsx"
output_df.to_excel(output_result_path, index=False)

print("Derived variable extraction completed.")


# In[ ]:




