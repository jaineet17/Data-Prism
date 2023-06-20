# Author
# archoudh , dpatnaik, jaineets, namitb, niyatim
# Purpose : Semantic Search for Books Dataset

import pandas as pd
import string
import gensim
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from gensim import corpora
from gensim.similarities import MatrixSimilarity
from operator import itemgetter

spacy_nlp = spacy.load('en_core_web_sm')

punctuations = string.punctuation
stop_words = spacy.lang.en.stop_words.STOP_WORDS


# Tokenizing Function
def spacy_tokenizer(sentence):
    # remove distracting single quotes
    sentence = re.sub('\'', '', sentence)

    # remove digits and words containing digits
    sentence = re.sub('\w*\d\w*', '', sentence)

    # replace extra spaces with single space
    sentence = re.sub(' +', ' ', sentence)

    # remove unwanted lines starting from special characters
    sentence = re.sub(r'\n: \'\'.*', '', sentence)
    sentence = re.sub(r'\n!.*', '', sentence)
    sentence = re.sub(r'^:\'\'.*', '', sentence)

    # remove non-breaking new line characters
    sentence = re.sub(r'\n', ' ', sentence)

    # remove punctuations
    sentence = re.sub(r'[^\w\s]', ' ', sentence)

    # creating token object
    tokens = spacy_nlp(sentence)

    # lower, strip and lemmatize
    tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]

    # remove stopwords, and exclude words less than 2 characters
    tokens = [word for word in tokens if word not in stop_words and word not in punctuations and len(word) > 2]

    # return tokens
    return tokens


# Dataframe for all the books
df_books = pd.read_csv('final_books_dataset.csv')
# Dataframe for descriptions of all the books
df_description = pd.DataFrame(df_books['description'], columns=['description'])

df_description_tokenized = pd.DataFrame()
df_description_tokenized['description'] = df_description['description'].map(lambda x: spacy_tokenizer(x))

books_dictionary = corpora.Dictionary(df_description_tokenized['description'])

stoplist = set('hello and if this can would should could tell ask stop come go')
stop_ids = [books_dictionary.token2id[stopword] for stopword in stoplist if stopword in books_dictionary.token2id]
books_dictionary.filter_tokens(stop_ids)

dict_tokens = [[[books_dictionary[key], books_dictionary.token2id[books_dictionary[key]]] for key, value in
                books_dictionary.items() if key <= 50]]

corpus = [books_dictionary.doc2bow(desc) for desc in df_description_tokenized['description']]

word_frequencies = [[(books_dictionary[id], frequency) for id, frequency in line] for line in corpus[0:3]]

books_tfidf_model = gensim.models.TfidfModel(corpus, id2word=books_dictionary)
books_lsi_model = gensim.models.LsiModel(books_tfidf_model[corpus], id2word=books_dictionary, num_topics=50)

gensim.corpora.MmCorpus.serialize('books_tfidf_model_mm', books_tfidf_model[corpus])
gensim.corpora.MmCorpus.serialize('books_lsi_model_mm', books_lsi_model[books_tfidf_model[corpus]])

books_tfidf_corpus = gensim.corpora.MmCorpus('books_tfidf_model_mm')
books_lsi_corpus = gensim.corpora.MmCorpus('books_lsi_model_mm')

books_index = MatrixSimilarity(books_lsi_corpus, num_features=books_lsi_corpus.num_terms)


# Searching the books on the search query given by the user
def search_similar_books(search_term):

    query_bow = books_dictionary.doc2bow(spacy_tokenizer(search_term))
    query_tfidf = books_tfidf_model[query_bow]
    query_lsi = books_lsi_model[query_tfidf]

    books_index.num_best = 10

    books_list = books_index[query_lsi]

    books_list.sort(key=itemgetter(1), reverse=True)
    book_names = []

    for j, book in enumerate(books_list):

        book_names.append(
            {
                'Relevance': round((book[1] * 100), 2),
                'Book Title': df_books['product'][book[0]],
                'Author': df_books['author'][book[0]],
                'Price': df_books['price'][book[0]],
                'Book Link': df_books['product_url'][book[0]],
                'Rating': df_books['rating'][book[0]],
                'Rating Count': df_books['rating_count'][book[0]]
            }

        )
        if j == (books_index.num_best-1):
            break

    return pd.DataFrame(book_names, columns=['Relevance', 'Book Title', 'Author', 'Price', 'Book Link', 'Rating',
                                             'Rating Count'])





