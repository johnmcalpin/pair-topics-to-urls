import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from bs4 import BeautifulSoup
import requests
import csv

# Load the spaCy model
nlp = spacy.load('en_core_web_lg')

# Define a custom tokenizer function
def custom_tokenizer(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    return tokens

# Load topics from text file
with open('topics.txt', 'r') as f:
    topics = f.read().splitlines()

# Load URLs from text file
with open('urls.txt', 'r') as f:
    urls = f.read().splitlines()

# Create CSV file and write header row
with open('results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['URL', 'H1', 'Closest Topic', 'Similarity'])

    # Loop through each URL and scrape the H1 tag
    for url in urls:
        try:
            # Get the HTML content from the URL
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get the H1 tag content
            h1_text = soup.h1.text.strip()

            # Preprocess the H1 text and compute similarity to each topic
            h1_tokens = custom_tokenizer(h1_text)
            max_similarity = 0
            closest_topic = ''
            for topic in topics:
                topic_tokens = custom_tokenizer(topic)
                similarity = nlp(' '.join(h1_tokens)).similarity(nlp(' '.join(topic_tokens)))
                if similarity > max_similarity:
                    max_similarity = similarity
                    closest_topic = topic
            
            # Write result to CSV file and print result
            row = [url, h1_text, closest_topic, max_similarity]
            writer.writerow(row)
            print(row)
        except:
            # If there was an error with the URL, skip to the next URL
            continue
