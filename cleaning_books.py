# Author
# archoudh , dpatnaik, jaineets, namitb, niyatim
# The purpose of this file is to clean the extracted data from webscraping_books.py.
# After cleaning the data we also extract the description of each book by visiting each book link
# individually (get_description does this functionality)

from selenium import webdriver
from time import sleep
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


# Clean the raw_books.csv file extracted by webscrping
def clean_books():
    # Opening the books dataset that has just been created
    books_df = pd.read_csv("raw_books.csv")
    # Printing the total number of books in the data set
    print(books_df)
    # Printing the information for the entire dataset of books
    print(books_df.info())
    # Printing the data types of each column to understand what all processing can be done on each column
    print(books_df.dtypes)

    # ----- Removing the Duplicate Books based on name of the books-------

    # Finding the number of unique books in the dataset based on the name of the books
    print(len(books_df['product'].unique()))
    # Viewing all the duplicate books in the dataset
    print(books_df[books_df['product'].duplicated()])

    # Getting only the unique books in a new data set
    books_df_unique = books_df.drop_duplicates('product')
    # Printing the information for the new dataset of books which contains all unique books
    print(books_df_unique.info())
    # Resetting the index values of the new dataset
    books_df_unique.reset_index(drop=True, inplace=True)

    # ----- Removing the Rows in which both the rating count and the rating is not present for the books-------
    books_df_nr = books_df_unique.dropna(axis=0, subset=['rating_count', 'rating'])
    # Printing the information for the new dataset of books which does not contain NA values of Ratings and Rating Count
    print(books_df_nr.info())
    # Resetting the index values of the new dataset
    books_df_nr.reset_index(drop=True, inplace=True)
    # Printing the information for the new dataset of books which does not contain NA values of Ratings and Rating Count
    print(books_df_nr.info())

    # ----- Modifying some rows from the dataset for which proper author names were not found -------
    # Looking at the data we found that some rows in the dataset had years for the author names,
    # and we realized that this is due to the way html tags of the amazon website, so we decided to simply
    # replace author names for those columns with Not Found

    books_df_nr.loc[books_df_nr["author"] == '2001', "author"] = "Not Found"
    books_df_nr.loc[books_df_nr["author"] == '2019', "author"] = "Not Found"
    books_df_nr.loc[books_df_nr["author"] == '1975', "author"] = "Not Found"
    books_df_nr.loc[books_df_nr["author"] == '2002', "author"] = "Not Found"
    books_df_nr.loc[books_df_nr["author"] == '2020', "author"] = "Not Found"
    books_df_nr.loc[books_df_nr["author"] == '2017', "author"] = "Not Found"
    books_df_nr.loc[books_df_nr["author"] == '2015', "author"] = "Not Found"
    books_df_nr.loc[books_df_nr["author"] == '2021', "author"] = "Not Found"
    books_df_nr.loc[books_df_nr["author"] == '2004', "author"] = "Not Found"

    return books_df_nr


# Extract the description for the cleaned books from amazon
def get_description(url):
    path = r"C:\Users\ac253\Downloads\chromedriver_win32\chromedriver.exe"
    browser = webdriver.Chrome(executable_path=path)
    browser.get(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/107.0.0.0 Safari/537.36", 'Accept-Language': 'en-US, en;q=0.5'}
    page = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    sleep(5)
    desc = soup2.find('div', {'id': 'bookDescription_feature_div'}).text

    # Cleaning the extracted description so to not include unwanted characters and emoji's
    regex = r"[^a-zA-Z0-9\s\.\,\?]"
    desc = re.sub(regex, "", desc)
    desc = " ".join(desc.split())
    return desc


# Main function to run both the clean and the get_description function
# The file final_books_dataset.csv is generated here, which is being used as the final dataset for our project
# implementation
if __name__ == '__main__':
    df = clean_books()
    df['description'] = None
    # Many a times due to reasons not in our control, the scraping does not happen on the
    # first try. Hence, we run this loop thrice. The if loop in the following code is
    # checks if the description is already scraped. Thus, saving time in the 2nd and
    # 3rd time the inner for loop executes.
    for j in range(3):
        for i in range(0, df.shape[0]):
            description = df['description'].iloc[i]
            if description is None:
                try:  # This try and except block is used because sometimes the scraping is unsuccessful.
                    description = get_description(df['product_url'].loc[i])
                except:
                    pass
                df['description'].iloc[i] = description

    df.reset_index(drop=True, inplace=True)
    df.to_csv('final_books_dataset.csv', index=False)

