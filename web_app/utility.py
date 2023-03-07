import streamlit as st
import re
import requests
from googlesearch import search
import pandas as pd
import numpy as np
import openai
import datetime
import spacy
import subprocess


@st.cache
def convert_df(df):
    df = df.to_csv(
        sep = ';',
        header = True,
        index = False).encode('utf-8')
    return df

def parse_date_from_html(html_string):
    "parse date from html. Input html as byte object. The output is a string."
    try:
        regex = b"\d{4}-\d{2}-\d{2}" # b stands for byte like! not a string yet
        date = re.search(regex, html_string)[0]
        date_string = date.decode('utf-8') # turn to string
    except:
        try:
            regex = b"\d{4}\/\d{2}\/\d{2}" # b stands for byte like! not a string yet
            date = re.search(regex, html_string)[0]
            date_string = date.decode('utf-8')#.replace("/", "-") # turn to string
        except:
            date_string = 'no date detected'
    return date_string

def parse_title_from_html(html_string):
    "parse_title_from_html. Input html as byte object. The output is a string."
    try:
        title = re.search(b'<title>(.*?)</title>', html_string).group(1)
        title = title.decode('utf-8')
        title = title.split('.')[0].split('&')[0].split('|')[0].split('-')[0]
    except:
        title = 'no title detected'
    return title

@st.cache
def google_query(keywords, num_results)->pd.DataFrame:
  "query google by topics and return the url, the title and the publication date for each search result"
  source_google = []
  titles_google = []
  publication_dates_google = []

  for kw in keywords:
    query = kw
    for url in search(query, num_results, lang="de"):
        # get html string
        html_string = requests.get(url).content     
        # get title
        title = parse_title_from_html(html_string)
        # get date
        date = parse_date_from_html(html_string)
        # save results in lists
        source_google.append(url)
        titles_google.append(title)
        publication_dates_google.append(date)
  # turn titles and sources into dataframe
  return pd.DataFrame({'source': source_google, 'title': titles_google, 'date': publication_dates_google})

@st.cache
def chatgpt_generate_topics(keywords:list, num_topics:int):
    "Give ChatGPT instructions to generate num_topics for the given keywors"
    instruction = \
    '\n' \
    "Nenne zu folgenden Keywords " + '\n' \
    'keywords = ' + str(keywords)  + '\n' \
    ' ' + str(num_topics) + '\n' \
    ' Themenüberschriften.'
    print('Instruction: ', instruction)
    return instruction

@st.cache
def chatgpt_query(instruction, num_tokens)->pd.DataFrame:
    "query ChatGPT by topics and return the source, the title and the publication date for each search result"
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=instruction,
    temperature=.5,
    max_tokens=num_tokens,
    top_p=1,
    n=2,
    presence_penalty=.5,
    frequency_penalty=.5,
    )
    titles_chatgpt = response['choices'][0].text
    titles_chatgpt = [title.strip().replace("\n", "").replace(". ", "") for title in re.split(r'\d+', titles_chatgpt)]
    date_today = datetime.date.today().strftime("%Y-%m-%d")
    df_titles_chatgpt = pd.DataFrame({'source': 'chatgpt', 'title': titles_chatgpt, 'date': date_today})
    return df_titles_chatgpt


@st.cache
def add_keyword_topic_similarity(df_titles:pd.DataFrame, keywords_selected:list)->pd.DataFrame:
    "add keyword-topic similarity to title dataframe using spacy`s German language model"
    # measure similarity between the titles and the keywords
    try: 
        nlp = spacy.load("de_core_news_lg")
    except:
        subprocess.run(["python", "-m", "spacy", "download", "de_core_news_lg"])
        nlp = spacy.load("de_core_news_lg")
    title_keyword_similarity = []
    for title in df_titles['title']:
        sim_score = 0
        for kw in keywords_selected:
            sim_score += nlp(title).similarity(nlp(kw)) / len(keywords_selected) # average similarity score for better interpretability
        # append sum of similarity scores
        title_keyword_similarity.append(np.round(sim_score, 2))
    # Add title-keyword similarity scores to df_titles
    df_titles['keyword_similarity'] = title_keyword_similarity
    return df_titles

