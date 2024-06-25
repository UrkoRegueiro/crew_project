from googleapiclient.discovery import build
from langchain_community.document_loaders import YoutubeLoader
from datetime import datetime, timedelta, timezone
import os


def transcriptor(url):
    '''
    Función utilizada para la transcripción de videos y su resumen.

    Inputs:
        - url: str -> La url del video.

    Output:
        - resumen: str -> El resumen del video.
    '''

    # Cargo y transcribo:
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True, language=["es"])
    transcript = loader.load()

    return transcript[0].page_content

def search_videos():
    '''
    Función que devuelve los videos de los últimos 5 días

    Input:
        - xxxx: str -->

    Output:
        - results: object --> JSON con la información obtenida(titulo, fecha y url)
    '''

    # Fecha de hace 5 días
    today = datetime(datetime.now().year, datetime.now().month, datetime.now().day, tzinfo=timezone.utc)
    two_days_ago = today - timedelta(days=1)
    date_format = two_days_ago.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    youtube = build("youtube", "v3", developerKey= os.getenv('YOUTUBE_API_KEY'))
    request = youtube.search().list(part= "snippet",
                                    order= "date",
                                    type= "video",
                                    videoDuration= "medium",
                                    publishedAfter= date_format,
                                    channelId= "UCBLCvUUCiSqBCEc-TqZ9rGw",
                                    maxResults=5
                                   )
    
    response = request.execute()

    results = {"results": []}

    for video in response["items"]:

        title = video["snippet"]["title"]
        author = video["snippet"]["channelTitle"]
        date = video["snippet"]["publishTime"]
        id= video["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={id}&ab_channel=JuanRam%C3%B3nRallo"
        text = transcriptor(url)
        
        results["results"].append({"title": title,
                                   "author": author,
                                   "date": date,
                                   "text": text,
                                   "url": url
                                  })
    
    return results