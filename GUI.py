import PySimpleGUI as sg
import pandas as pd
import webbrowser
import books_semanticsearch as bk
import Youtube_Api_Data_Processing as dfpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    try:
        draw_figure.canvas_packed.pop(figure_agg.get_tk_widget())
    except Exception as e:
        print(f'Error removing {figure_agg} from list', e)
    plt.close('all')

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

def video_likes_plot(df3):
    df3 = df3.copy()
    c_labels = ['Vid1','Vid2','Vid3','Vid4','Vid5','Vid6','Vid7','Vid8','Vid9','Vid10']
    fig = plt.figure(figsize = (6, 4))
    plt.bar(range(len(df3)),df3['Likes'], tick_label=c_labels)
    addlabels(range(len(df3)),df3['Likes'])
    plt.xlabel("Youtube Videos as per search query")
    plt.ylabel("No. of Likes")
    plt.title("Videos with their Like count.")
    plt.grid(True)
    plt.ioff()
    fig = plt.gcf()
    return fig


def video_duration_plot(df3):
    df3=df3.copy()
    c_labels = ['Vid1','Vid2','Vid3','Vid4','Vid5','Vid6','Vid7','Vid8','Vid9','Vid10']
    fig = plt.figure(figsize = (6, 4))
    plt.bar(range(len(df3)),df3['Int_Duration']/60, tick_label=c_labels)
    addlabels(range(len(df3)),df3['Int_Duration']//60)
    plt.xlabel("Youtube Videos as per search query")
    plt.ylabel("Duration of video")
    plt.title("Videos with their Duration in minutes")
    plt.grid(True)
    plt.ioff()
    fig = plt.gcf()
    return fig

def video_Comment_Count_plot(df3):
    df3=df3.copy()
    c_labels = ['Vid1','Vid2','Vid3','Vid4','Vid5','Vid6','Vid7','Vid8','Vid9','Vid10']
    fig = plt.figure(figsize = (6, 4))
    plt.bar(range(len(df3)),df3['Comment_Count'], tick_label=c_labels)
    addlabels(range(len(df3)),df3['Comment_Count'])
    plt.xlabel("Youtube Videos as per search query")
    plt.ylabel("Comment Counts of video")
    plt.title("Videos with their Comment Counts")
    plt.grid(True)
    plt.ioff()
    fig = plt.gcf()
    return fig

def book_rating_plot(df): ### books rating graph
    df=df.copy()
    no_of_values = len(df)
    df['Rating'] = df['Rating'].astype(float)
    num_books = ['Book 1', 'Book 2', 'Book 3', 'Book 4', 'Book 5', 'Book 6', 'Book 7','Book 8', 'Book 9', 'Book 10']
    fig = plt.figure(figsize=(6, 4))
    fig = plt.bar(num_books, book_df['Rating'], color='Red')
    plt.title('Books vs Ratings for each book', fontsize=14)
    plt.xlabel('Books', fontsize=14)
    plt.ylabel('Rating of Books', fontsize=14)
    #plt.bar_label(fig, labels=df['Rating'], label_type="edge")
    addlabels(range(len(df)),df['Rating'])
    plt.xticks(range(len(num_books)), num_books, rotation='vertical', fontsize=7)
    plt.grid(True)
    plt.ioff()
    fig = plt.gcf()
    return fig

def book_price_plot(df): ### books price graph
    df=df.copy()
    no_of_values = len(df)
    df['Price'] = df['Price'].astype(float)
    num_books = ['Book 1', 'Book 2', 'Book 3', 'Book 4', 'Book 5', 'Book 6', 'Book 7','Book 8', 'Book 9', 'Book 10']
    fig = plt.figure(figsize=(6, 4))
    fig = plt.bar(num_books, book_df['Price'], color='Red')
    plt.title('Books vs Prices for each book', fontsize=14)
    plt.xlabel('Books', fontsize=14)
    plt.ylabel('Price of Books in $', fontsize=14)
    #plt.bar_label(fig, labels=df['Price'], label_type="edge")
    plt.xticks(range(len(num_books)), num_books, rotation='vertical', fontsize=7)
    plt.grid(True)
    plt.ioff()
    fig = plt.gcf()
    return fig



def create_job_plot(locations, number):
    fig = plt.figure(figsize=(6, 4))
    plt.bar(locations, number, color='maroon', width=0.4)
    plt.title('Location vs number of jobs there', fontsize=14)
    plt.xlabel('Locations', fontsize=14)
    plt.ylabel('Number of Jobs', fontsize=14)
    plt.xticks(range(len(locations)), locations, rotation='vertical', fontsize=6)
    return plt.gcf()

def create_job_lists_plot(df):
    df=df.head(10)
    groups = df.groupby(['Location'])['Location'].count()
    locations = []
    num = []
    for i in groups.iteritems():
        locations.append(i[0])
        num.append(i[1])
    fig = create_job_plot(locations, num)
    return fig


def draw_figure(canvas, figure):

    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# This function extracts jobs with the particular search tag
def get_tag_values(tag):
    df = pd.read_csv("jobs_cleaned_data.csv")

    neww = []
    for i in range(len(df)):
        df['Tags'][i] = df['Tags'][i].lower()
        if tag == None:
            break
        if tag.lower() in df['Tags'][i]:
            neww.append(df.iloc[i])

    a = pd.DataFrame(neww)
    return a

youtdf = pd.read_excel('youtube_complete_data_clean.xlsx')
youtdf1 = pd.DataFrame(youtdf['Summary'])

# Theme
sg.theme("Light Blue")

# ----------- Create the 3 layouts this Window will display -----------
layout0 = [[sg.Image(filename='intro_pic.png')],
           [sg.Text('Welcome to Data PRISM\nYour handy tool to get information about Data Science related books, jobs and tutorials\nPress "Next" button to continue')],]

layout1 = [[sg.Text('Please enter the search term and select the entity you would like to search')],
           [sg.Text('Search: '), sg.Input(key='-SEARCH-')],
           [sg.Text('Entity:  '), sg.Combo(["Books","Tutorials","Jobs"],key='-ENTITY-')]]

layout2 = [[sg.Text('Layout 2')]]

layout3 = [[sg.Text('You have reached the end of Data PRISM\nWe hope you found this application helpful in your data science journey!!! \n\n\nPress the "Return to Start" button to go back to start page\nOr press the "Exit" button to exit the application.')]]

#Has predefined placements for each element. When an event happens, the values are updated.
layout4 =[
    [sg.Text('Greeting message:', key='-SEARCHMESSAGE1-')],
    [sg.Text('JOBS',justification='center', background_color='white', size=(76,1))],
    [sg.Text(key='error', background_color='white')],
    [sg.Text(key='Company_Name1', background_color='white'), sg.Button("Apply", key='job1', visible=False)],
    [sg.Text(key='Position1', background_color='white')],
    [sg.Text(key='Req1', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name2', background_color='white'), sg.Button("Apply", key='job2', visible=False)],
    [sg.Text(key='Position2', background_color='white')],
    [sg.Text(key='Req2', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name3', background_color='white'), sg.Button("Apply", key='job3', visible=False)],
    [sg.Text(key='Position3', background_color='white')],
    [sg.Text(key='Req3', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name4', background_color='white'), sg.Button("Apply", key='job4', visible=False)],
    [sg.Text(key='Position4', background_color='white')],
    [sg.Text(key='Req4', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name5', background_color='white'), sg.Button("Apply", key='job5', visible=False)],
    [sg.Text(key='Position5', background_color='white')],
    [sg.Text(key='Req5', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name6', background_color='white'), sg.Button("Apply", key='job6', visible=False)],
    [sg.Text(key='Position6', background_color='white')],
    [sg.Text(key='Req6', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name7', background_color='white'), sg.Button("Apply", key='job7', visible=False)],
    [sg.Text(key='Position7', background_color='white')],
    [sg.Text(key='Req7', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name8', background_color='white'), sg.Button("Apply", key='job8', visible=False)],
    [sg.Text(key='Position8', background_color='white')],
    [sg.Text(key='Req8', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name9', background_color='white'), sg.Button("Apply", key='job9', visible=False)],
    [sg.Text(key='Position9', background_color='white')],
    [sg.Text(key='Req9', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name10', background_color='white'), sg.Button("Apply", key='job10', visible=False)],
    [sg.Text(key='Position10', background_color='white')],
    [sg.Text(key='Req10', background_color='white')]
]

layout5 =[
    [sg.Text('Greeting message :', key='-SEARCHMESSAGE2-')],
    [sg.Text('BOOKS',justification='center', background_color='white', size=(76,1))],
    [sg.Text(key='error', background_color='white')],
    [sg.Text(key='Book_Name1', background_color='white'), sg.Button("Buy", key='book1', visible=False)],
    [sg.Text(key='Author1', background_color='white')],
    [sg.Text(key='Rating1', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Book_Name2', background_color='white'), sg.Button("Buy", key='book2', visible=False)],
    [sg.Text(key='Author2', background_color='white')],
    [sg.Text(key='Rating2', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Book_Name3', background_color='white'), sg.Button("Buy", key='book3', visible=False)],
    [sg.Text(key='Author3', background_color='white')],
    [sg.Text(key='Rating3', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Book_Name4', background_color='white'), sg.Button("Buy", key='book4', visible=False)],
    [sg.Text(key='Author4', background_color='white')],
    [sg.Text(key='Rating4', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Book_Name5', background_color='white'), sg.Button("Buy", key='book5', visible=False)],
    [sg.Text(key='Author5', background_color='white')],
    [sg.Text(key='Rating5', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Book_Name6', background_color='white'), sg.Button("Buy", key='book6', visible=False)],
    [sg.Text(key='Author6', background_color='white')],
    [sg.Text(key='Rating6', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Book_Name7', background_color='white'), sg.Button("Buy", key='book7', visible=False)],
    [sg.Text(key='Author7', background_color='white')],
    [sg.Text(key='Rating7', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Book_Name8', background_color='white'), sg.Button("Buy", key='book8', visible=False)],
    [sg.Text(key='Author8', background_color='white')],
    [sg.Text(key='Rating8', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Book_Name9', background_color='white'), sg.Button("Buy", key='book9', visible=False)],
    [sg.Text(key='Author9', background_color='white')],
    [sg.Text(key='Rating9', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Book_Name10', background_color='white'), sg.Button("Buy", key='book10', visible=False)],
    [sg.Text(key='Author10', background_color='white')],
    [sg.Text(key='Rating10', background_color='white')]
]

layout6 =[
    [sg.Text('Greeting message:', key='-SEARCHMESSAGE3-')],
    [sg.Text('Tutorials',justification='center', background_color='white', size=(76,1))],
    [sg.Text(key='error', background_color='white')],
    [sg.Text(key='YtTutorial1', background_color='white'), sg.Button("Watch", key='video1', visible=False)],
    [sg.Text(key='Channel_Name1', background_color='white')],
    [sg.Text(key='Other_param1', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='YtTutorial2', background_color='white'), sg.Button("Watch", key='video2', visible=False)],
    [sg.Text(key='Channel_Name2', background_color='white')],
    [sg.Text(key='Other_param2', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='YtTutorial3', background_color='white'), sg.Button("Watch", key='video3', visible=False)],
    [sg.Text(key='Channel_Name3', background_color='white')],
    [sg.Text(key='Other_param3', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='YtTutorial4', background_color='white'), sg.Button("Watch", key='video4', visible=False)],
    [sg.Text(key='Channel_Name4', background_color='white')],
    [sg.Text(key='Other_param4', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='YtTutorial5', background_color='white'), sg.Button("Watch", key='video5', visible=False)],
    [sg.Text(key='Channel_Name5', background_color='white')],
    [sg.Text(key='Other_param5', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='YtTutorial6', background_color='white'), sg.Button("Watch", key='video6', visible=False)],
    [sg.Text(key='Channel_Name6', background_color='white')],
    [sg.Text(key='Other_param6', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='YtTutorial7', background_color='white'), sg.Button("Watch", key='video7', visible=False)],
    [sg.Text(key='Channel_Name7', background_color='white')],
    [sg.Text(key='Other_param7', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='YtTutorial8', background_color='white'), sg.Button("Watch", key='video8', visible=False)],
    [sg.Text(key='Channel_Name8', background_color='white')],
    [sg.Text(key='Other_param8', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='YtTutorial9', background_color='white'), sg.Button("Watch", key='video9', visible=False)],
    [sg.Text(key='Channel_Name9', background_color='white')],
    [sg.Text(key='Other_param9', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='YtTutorial10', background_color='white'), sg.Button("Watch", key='video10', visible=False)],
    [sg.Text(key='Channel_Name10', background_color='white')],
    [sg.Text(key='Other_param10', background_color='white')]
]

layout7 = [[sg.Text('Books Plot: ')],
          [sg.Canvas(size=(500, 500), key='-CANVAS1-')],
          [sg.Canvas(size=(500, 500), key='-CANVAS4-')]]

layout8 = [[sg.Text('Jobs Plot: ')],
          [sg.Canvas(size=(500, 500), key='-CANVAS2-')]]

layout9 = [[sg.Text('Tutorials Plot: ')],
           [sg.Canvas(size=(500, 500), key='-CANVAS3-')],
          [sg.Canvas(size=(500, 500), key='-CANVAS6-')],
          [sg.Canvas(size=(500, 500), key='-CANVAS7-')]]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [[sg.Column(layout0, key='-COL0-'),
           sg.Column(layout1, visible=False, key='-COL1-'),
           sg.Column(layout2, visible=False, key='-COL2-'),
           sg.Column(layout3, visible=False, key='-COL3-'),
           sg.Column(layout4, visible=False, key='-COL4-'),
           sg.Column(layout5, visible=False, key='-COL5-'),
           sg.Column(layout6, visible=False, key='-COL6-'),
           sg.Column(layout7, visible=False, key='-COL7-'),
           sg.Column(layout8, visible=False, key='-COL8-'),
           sg.Column(layout9, visible=False, key='-COL9-')],
          [sg.Button('Next'), sg.Button('Return to Start'), sg.Button('Exit')]]


window = sg.Window('Data PRISM', layout, finalize=True)
figure_agg  = None
figure_agg1 = None
figure_agg2 = None
search=''
entity=''
layoutvar = 0  # The currently visible layout variable
while True:
    event, values = window.read()

    if figure_agg:
        # ** IMPORTANT ** Clean up previous drawing before drawing again
        delete_figure_agg(figure_agg)

    if figure_agg1:
        # ** IMPORTANT ** Clean up previous drawing before drawing again
        delete_figure_agg(figure_agg1)

    if figure_agg2:
        # ** IMPORTANT ** Clean up previous drawing before drawing again
        delete_figure_agg(figure_agg2)

    #if the event happened is of nature job, example - job1
    #refer to "sg.Button("Apply", key='job1', visible=False)]" on col3
    if event[0:3]=='job':
        if len(subset_df)>10:
            for i in range(10):
                if event == 'job'+str(i+1):
                    webbrowser.open(subset_df['Link'][i])
        if len(subset_df)<10:
            for i in range(len(subset_df)):
                if event == 'job'+ str(i+1):
                    webbrowser.open(subset_df['Link'][i])

    if event[0:4]=='book':
        for i in range(10):
            if event == 'book'+str(i+1):
                webbrowser.open(book_df['Book Link'][i])

    if event[0:5]=='video':
        for i in range(10):
            if event == 'video'+str(i+1):
                webbrowser.open(yt_df['Link'][i])

    if event in (None, 'Exit'):
        break
    if event == 'Next':
        window[f'-COL{layoutvar}-'].update(visible=False)
        if layoutvar==0:
            pass
        if layoutvar ==1:
            search = values['-SEARCH-']
            entity = values['-ENTITY-']

        if layoutvar < 3:
            layoutvar += 1
            window[f'-COL{layoutvar}-'].update(visible=True)
        else:
            window[f'-COL3-'].update(visible=True)
            if entity=='Jobs':
                window[f'-COL4-'].update(visible=False)
                window[f'-COL8-'].update(visible=False)
            elif entity=='Books':
                window[f'-COL5-'].update(visible=False)
                window[f'-COL7-'].update(visible=False)
            else:
                window[f'-COL6-'].update(visible=False)
                window[f'-COL9-'].update(visible=False)
        if layoutvar == 2:
            window['-SEARCHMESSAGE1-'].update(f'Thank you for choosing to search "{search}" in "{entity}"')
            window['-SEARCHMESSAGE2-'].update(f'Thank you for choosing to search "{search}" in "{entity}"')
            window['-SEARCHMESSAGE3-'].update(f'Thank you for choosing to search "{search}" in "{entity}"')
            
            # If entity entered by the user is Jobs
            if entity == 'Jobs':
                window[f'-COL2-'].update(visible=False)
                window[f'-COL4-'].update(visible=True)
                subset_df = get_tag_values(search)
                subset_df.reset_index(inplace=True)

                # if the window is closed
                if event == sg.WIN_CLOSED:
                    break

                # if x is not empty and the tag is not null
                if subset_df.empty == False and search != '':
                    if len(subset_df) > 10:
                        for i in range(10):
                            temp1 = 'Company_Name' + str(i + 1)
                            key = 'job' + str(i + 1)
                            window[temp1].Update(f"Company : {subset_df['Company'][i]}", background_color='Light Blue')
                            window[key].Update(visible=True)
                            temp2 = 'Position' + str(i + 1)
                            window[temp2].Update(f"Position : {subset_df['Job Title'][i]}")
                            temp3 = 'Req' + str(i + 1)
                            window[temp3].Update(f"Requirements : {subset_df['Requirements'][i]}")
                            window['error'].Update('')

                    # there are some tags, for which values are less than 5, try- "optimization" tag on GUI, to understand better
                    if len(subset_df) < 10:
                        for i in range(len(subset_df)):
                            temp1 = 'Company_Name' + str(i + 1)
                            key = 'job' + str(i + 1)
                            window[temp1].Update(f"Company : {subset_df['Company'][i]}", background_color='Light Blue')
                            window[key].Update(visible=True)
                            temp2 = 'Position' + str(i + 1)
                            window[temp2].Update(f"Position : {subset_df['Job Title'][i]}")
                            temp3 = 'Req' + str(i + 1)
                            window[temp3].Update(f"Requirements : {subset_df['Requirements'][i]}")
                            window['error'].Update('')
                        for i in range(len(subset_df), 10):
                            temp1 = 'Company_Name' + str(i + 1)
                            key = 'job' + str(i + 1)
                            window[temp1].Update('', background_color='white')
                            window[key].Update(visible=False)
                            temp2 = 'Position' + str(i + 1)
                            window[temp2].Update('', background_color='white')
                            temp3 = 'Req' + str(i + 1)
                            window[temp3].Update('', background_color='white')
                            window['error'].Update('', background_color='white')

                    # if the tag is not relevant, example, if the tag is "heyy"
                    if subset_df.empty == True:
                        window['error'].Update("No matches found")
                        for i in range(10):
                            temp1 = 'Company_Name' + str(i + 1)
                            key = 'job' + str(i + 1)
                            window[temp1].Update('', background_color='white')
                            window[key].Update(visible=False)
                            temp2 = 'Position' + str(i + 1)
                            window[temp2].Update('', background_color='white')
                            temp3 = 'Req' + str(i + 1)
                            window[temp3].Update('', background_color='white')

                window[f'-COL8-'].update(visible=True)

                figure_agg=draw_figure(window[f'-CANVAS2-'].TKCanvas, create_job_lists_plot(subset_df))

            if entity == 'Books':
                book_df=bk.search_similar_books(search)
                window[f'-COL2-'].update(visible=False)
                window[f'-COL5-'].update(visible=True)
                for i in range(10):
                    temp1 = 'Book_Name' + str(i + 1)
                    key = 'book' + str(i + 1)
                    window[temp1].Update(f"Title : {book_df['Book Title'][i]}", background_color='Light Blue')
                    window[key].Update(visible=True)
                    temp2 = 'Author' + str(i + 1)
                    window[temp2].Update(f"Author : {book_df['Author'][i]}")
                    temp3 = 'Rating' + str(i + 1)
                    window[temp3].Update(f"Price: ${book_df['Price'][i]}  | Rating : {book_df['Rating'][i]}/5  | Rating Count: {book_df['Rating Count'][i]}")
                    window['error'].Update()


                window[f'-COL7-'].update(visible=True)

                figure_agg = draw_figure(window[f'-CANVAS1-'].TKCanvas, book_price_plot(book_df))

                figure_agg1 = draw_figure(window[f'-CANVAS4-'].TKCanvas, book_rating_plot(book_df))


                
            if entity == 'Tutorials':
                yt_df = dfpy.search_similar_videos(search, youtdf)
                window[f'-COL2-'].update(visible=False)
                window[f'-COL6-'].update(visible=True)
                for i in range(10):
                    temp1 = 'YtTutorial' + str(i + 1)
                    key = 'video' + str(i + 1)
                    window[temp1].Update(f"Title : {yt_df['Title'][i]}", background_color='Light Blue')
                    window[key].Update(visible=True)
                    temp2 = 'Channel_Name' + str(i + 1)
                    window[temp2].Update(f"Channel name : {yt_df['Channel'][i]}")
                    temp3 = 'Other_param' + str(i + 1)
                    window[temp3].Update(f"Views : {yt_df['Views'][i]}  | Likes : {yt_df['Likes'][i]}  | Duration : {yt_df['Duration'][i]}  | Comment Count : {yt_df['Comment_Count'][i]}")
                    window['error'].Update()

                window[f'-COL9-'].update(visible=True)

                figure_agg = draw_figure(window[f'-CANVAS3-'].TKCanvas, video_likes_plot(yt_df))

                figure_agg1 = draw_figure(window[f'-CANVAS6-'].TKCanvas, video_duration_plot(yt_df))

                figure_agg2 = draw_figure(window[f'-CANVAS7-'].TKCanvas, video_Comment_Count_plot(yt_df))


            layoutvar=3


    elif event == 'Return to Start':
        for i in range(10):
            window[f'-COL{i}-'].update(visible=False)
        window[f'-COL0-'].update(visible=True)
        layoutvar = 0
window.close()