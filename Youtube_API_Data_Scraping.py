''' 
Andrew IDs - archoudh , dpatnaik, jaineets, namitb, niyatim
Filename - Youtube_API_Data_Scraping.py
Purpose - Scraping Youtube Video data through the Youtube Data API v3.
'''

from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pandas as pd
import urllib.parse as p
import re
import os
import pickle
import string
from nltk.corpus import stopwords
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token7.pickle"):
        with open("token7.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token7.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)

#Authenticating to YouTube API
youtube = youtube_authenticate()


def get_video_id_by_url(url):
    """
    Return the Video ID from the video `url`
    """
    # split URL parts
    parsed_url = p.urlparse(url)
    # get the video ID by parsing the query of the URL
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")


def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="snippet,contentDetails,statistics",
        **kwargs
    ).execute()


def search(youtube, **kwargs):
    return youtube.search().list(
        part="snippet",
        **kwargs
    ).execute()


def get_comments(youtube, **kwargs):
    return youtube.commentThreads().list(
        part="snippet",
        **kwargs
    ).execute()


def dataframe_video_infos(keywords):
    response1 = search(youtube, q=keywords, maxResults= 50)
    items1 = response1.get("items")
    videos = []
    for item1 in items1:
    # get the video ID
        video = []
        try:
            video_id = item1["id"]["videoId"]
            video_response = get_video_details(youtube, id=video_id)
            items = video_response.get("items")[0]
    # Getting the snippet, statistics & content details from the video response
            snippet         = items["snippet"]
            statistics      = items["statistics"]
            content_details = items["contentDetails"]
    # Getting infos from the snippet
            channel_title = snippet["channelTitle"]
            title         = snippet["title"]
            description   = ''.join(snippet["description"].splitlines())
            # print(''.join(description.splitlines()))
            publish_time  = snippet["publishedAt"]
    # Getting stats infos
            comment_count = statistics["commentCount"]
            like_count   =  statistics["likeCount"]
            view_count   =  statistics["viewCount"]
    # Getting duration from content details
            duration = content_details["duration"]
    # Duration in the form of something like 'PT5H50M15S'
    # Parsing it to be something like '5:50:15'
            parsed_duration = re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration).groups()
            duration_str = ""
            for d in parsed_duration:
                if d:
                    duration_str += f"{d[:-1]}:"
            duration_str = duration_str.strip(":")
            video.extend([title, description, channel_title, publish_time, duration_str, comment_count,like_count,
                   view_count, video_id])  
        except:
            continue             
            
        
        comments = []
        try:    
            params = { 'videoId': video_id, 'maxResults': 20,'order': 'relevance'} # default is 'time' (newest)
            response2 = get_comments(youtube, **params)
            items2 = response2.get("items")
            if not items2:
                break
            for item2 in items2:
                comment = item2["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                updated_at = item2["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
                like_count = item2["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                comment_id = item2["snippet"]["topLevelComment"]["id"]
                comments.append(comment)
        except:
            comments.append("NaN")
                      
        captions = []
        try:
            cc = YouTubeTranscriptApi.get_transcript(video_id)
            for i in cc:
                if 'text' in i.keys():
                    captions.append(' '.join(i['text'].split("\n")))       
            cstr = '. '.join(captions)
        except:
            cstr = 'NaN'
                         
        video.extend([comments,cstr])
        videos.append(video)
            
    return videos

search1 = ['Data Science'
,'NLP'
,'Computer Vision'
,'Python'
,'SQL for Data Science'
,'Tensorflow' 
,'PyTorch'
,'Keras'
,'Neural Networks'
,'Machine Learning'
,'Deep Learning'
,'R Programming'
,'Statistics for Data Science'
,'Data Visualization'
,'Data Science Interview'
,'AI'
,'Cloud Computing'
,'Analytics'
,'AWS'
,'Tableau'
,'Data Mining'
,'Business Intelligence'
,'PowerBI'
,'Sci-kit'
,'Reinforcement Learning'
,'RNN'
]

df = []
for x in search1:
    df.append(dataframe_video_infos(x))

df2 = []
for x in df:
    for y in x:
        df2.append(y)

df2 = [i for i in df2 if i is not None]

df2 = pd.DataFrame(df2)
df2.rename(columns = {0:'Title', 1:'Description',2 :'Channel_Title',
                    3 : 'Publish_Time',4: 'Duration',5: 'Comment_Count',6: 'Like_Count',
                    7:'View_Count',8: 'Video_ID', 9:'Comments',10: 'Captions'}, inplace = True)

print(df2.head())
#print(df2.info())
#print(df2.describe())

df3 = df2.drop_duplicates(subset = ["Video_ID"])
#print(df3.info())

df3 = df3[df3['Captions'] != 'NaN']
#print(df3.info())

convert_dict = {'Comment_Count': int,
                'View_Count': int,
                'Like_Count': int,
                }

df3 = df3.astype(convert_dict)
#print(df3.dtypes)
#print(df3.describe())

df3.to_excel('youtube_output_raw.xlsx')

df1 = df3.copy()
df1 = list(df1.values)

stop_words = stopwords.words("english")
other_exclusions = ["#ff", "ff", "rt","br"]
stop_words.extend(other_exclusions)

def text_preproc(x):
    x = x.lower() # Lowercase the text
    x = ' '.join([word for word in x.split(' ') if word not in stop_words]) # Remove stop words
    x = x.encode('ascii', 'ignore').decode() # Removing unicode characters
    x = re.sub(r'https*\S+', ' ', x) # Removing mentions
    x = re.sub(r'@\S+', ' ', x) # Removing URL
    x = re.sub(r'#\S+', ' ', x) # Remove Hashtags
    x = re.sub(r'\'\w+', '', x) # Remove ticks and the next character
    x = re.sub('[%s]' % re.escape(string.punctuation), ' ', x) # Remove punctuations
    x = re.sub(r'\w*\d+\w*', '', x) # Remove numbers
    x = re.sub(r'\s{2,}', ' ', x) # Replace the over spaces
    x = ' '.join( [w for w in x.split() if len(w)>1] ) # Remove single characters
    return x

for x in df1:
    cl = []
    for y in x[9]:
        cl.append(text_preproc(y))
    x[9] = cl
    x[10] = text_preproc(x[10])
    z = x[3].replace('Z', '')
    z1 = z.replace('T', ' ')
    x[3] = z1
    x[3] = datetime.strptime(x[3], '%Y-%m-%d %H:%M:%S').date()

df1 = pd.DataFrame(df1)
df1.rename(columns = {0:'Title', 1:'Description',2 :'Channel_Title',
                    3 : 'Publish_Time',4: 'Duration',5: 'Comment_Count',6: 'Like_Count',
                    7:'View_Count',8: 'Video_ID', 9:'Comments',10: 'Captions'}, inplace = True)
print(df1.head())
#print(df1.info())
#print(df1.describe())

df1.to_excel('youtube_output_cleaned.xlsx')

