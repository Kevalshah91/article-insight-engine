import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
nltk.download('punkt')

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1').get_text() if soup.find('h1') else ''
        paragraphs = soup.find_all('p')
        article_text = '\n'.join([para.get_text() for para in paragraphs])
        
        return title, article_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return '', ''

def positive_score(text):
    positive_words = set(open('positive-words.txt', encoding='ISO-8859-1').read().split())
    words = word_tokenize(text.lower())
    return sum(1 for word in words if word in positive_words)

def negative_score(text):
    negative_words = set(open('negative-words.txt', encoding='ISO-8859-1').read().split())
    words = word_tokenize(text.lower())
    return sum(1 for word in words if word in negative_words)

def polarity_score(pos_score, neg_score):
    return (pos_score - neg_score) / ((pos_score + neg_score) + 0.000001)

def subjectivity_score(text):
    blob = TextBlob(text)
    return blob.sentiment.subjectivity

def avg_sentence_length(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return len(words) / len(sentences)

def percentage_complex_words(text):
    def is_complex(word):
        vowels = "aeiou"
        return sum(1 for char in word if char in vowels) > 2
    
    words = word_tokenize(text)
    complex_words = [word for word in words if is_complex(word)]
    return len(complex_words) / len(words) * 100

def fog_index(avg_sentence_length, percentage_complex_words):
    return 0.4 * (avg_sentence_length + percentage_complex_words)

def avg_words_per_sentence(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return len(words) / len(sentences)

def complex_word_count(text):
    def is_complex(word):
        vowels = "aeiou"
        return sum(1 for char in word if char in vowels) > 2
    
    words = word_tokenize(text)
    return sum(1 for word in words if is_complex(word))

def word_count(text):
    words = word_tokenize(text)
    return len(words)

def syllable_per_word(text):
    def count_syllables(word):
        vowels = "aeiou"
        return sum(1 for char in word if char in vowels)
    
    words = word_tokenize(text)
    return sum(count_syllables(word) for word in words) / len(words)

def personal_pronouns(text):
    pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, re.I)
    return len(pronouns)

def avg_word_length(text):
    words = word_tokenize(text)
    return sum(len(word) for word in words) / len(words)

def process_text_file(file, input_df):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    pos_score = positive_score(text)
    neg_score = negative_score(text)
    pol_score = polarity_score(pos_score, neg_score)
    subj_score = subjectivity_score(text)
    avg_sent_len = avg_sentence_length(text)
    perc_complex_words = percentage_complex_words(text)
    fog_idx = fog_index(avg_sent_len, perc_complex_words)
    avg_words_sent = avg_words_per_sentence(text)
    comp_word_count = complex_word_count(text)
    word_cnt = word_count(text)
    syll_per_word = syllable_per_word(text)
    pers_pronouns = personal_pronouns(text)
    avg_word_len = avg_word_length(text)
    
    url_id = os.path.splitext(os.path.basename(file))[0] 
    matching_rows = input_df[input_df['URL_ID'] == url_id]
    
    if not matching_rows.empty:
        input_row = matching_rows.to_dict(orient='records')[0]
        
        result = {
            **input_row,
            'Positive Score': pos_score,
            'Negative Score': neg_score,
            'Polarity Score': pol_score,
            'Subjectivity Score': subj_score,
            'Avg Sentence Length': avg_sent_len,
            'Percentage of Complex Words': perc_complex_words,
            'Fog Index': fog_idx,
            'Avg Number of Words per Sentence': avg_words_sent,
            'Complex Word Count': comp_word_count,
            'Word Count': word_cnt,
            'Syllable per Word': syll_per_word,
            'Personal Pronouns': pers_pronouns,
            'Avg Word Length': avg_word_len
        }
        
        return result
    else:
        print(f'No matching URL_ID found for file: {file}')
        return None

# Directories to create
directories_to_create = [
    '20211030 Test Assignment-20240709T080606Z-001/MasterDictionary',
    'NLP_Assignment'
]

# Ensure directories exist
for directory in directories_to_create:
    ensure_directory(directory)

# Read input data
input_df = pd.read_excel('Input.xlsx')

# Folder where scraped content is stored
content_folder = 'NLP_Assignment'

for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    title, article_text = extract_article_text(url)
    with open(f'{content_folder}\{url_id}.txt', 'w', encoding='utf-8') as file:
        file.write(title +'\n'+article_text)
    
# Process each text file
text_files = [os.path.join(content_folder, f) for f in os.listdir(content_folder) if f.endswith('.txt')]
results = []

for file in text_files:
    result = process_text_file(file, input_df)
    if result:
        results.append(result)

output_df = pd.DataFrame(results)
output_df.to_excel('Output Data Structure.xlsx', index=False)
print("Output saved to 'Output Data Structure.xlsx'")

