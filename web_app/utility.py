import streamlit as st
import re
import requests
from googlesearch import search
import pandas as pd
import openai
import datetime


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
        try: 
            html_string = requests.get(url, timeout=2.5).content
        except:
            html_string = ''
            
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
def generate_topic_instruction(keywords:list, num_topics:int):
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
def generate_article_instruction(keywords_selected, topic_selected, num_article_words):
    instruction = \
    '\n' \
    "Schreibe einen Artikel von \n" \
    '' + str(num_article_words) + " Wörtern zum Thema: " + '\n' \
    ' ' + str(topic_selected) + '. \n' + \
    "Der Artikel soll die Schlüsselbegriffe " + '\n' \
    ' ' + str(keywords_selected) + '\n' \
    "enthalten." + '\n' \
    "Desweiteren soll der Artikel in Absätze und Überschriften unterteilt sein." + '\n' + \
    "Desweiteren sollen die Überschriften die Schlüsselbegriffe enthalten."
    print(instruction)
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
def chatgpt_generate_text(instruction, num_tokens)->pd.DataFrame:
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
    text_seo = response['choices'][0].text
    return text_seo


