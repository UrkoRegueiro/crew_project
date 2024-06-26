from googleapiclient.discovery import build
from langchain_community.document_loaders import YoutubeLoader
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from datetime import datetime, timedelta, timezone
import os

llm_summary = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=os.getenv('OPENAI_API_KEY'))


prompt_template = """Write an article in SPANISH for a newspaper summarizing the following:
    {text}
    SUMMARY:"""
prompt = PromptTemplate.from_template(prompt_template)

refine_template = (
    "Your job is to produce a final newspaper article in SPANISH\n"
    "We have provided an existing summary of a text in spanish up to a certain point: {existing_answer}\n"
    "We have the opportunity to refine the existing summary"
    "(only if needed) with some more context below.\n"
    "------------\n"
    "{text}\n"
    "------------\n"
    "Given the new context, refine the original summary"
    "If the context isn't useful, return the original summary."
)
refine_prompt = PromptTemplate.from_template(refine_template)

# Chain
chain = load_summarize_chain(llm=llm_summary,
                             chain_type="refine",
                             question_prompt=prompt,
                             refine_prompt=refine_prompt,
                             return_intermediate_steps=False,
                             input_key="input_documents",
                             output_key="output_text",
                             )
def transcriptor(url: str):
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

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3500, chunk_overlap=500)
    chunks = text_splitter.split_documents(transcript)

    summary = chain.invoke({"input_documents": chunks}, return_only_outputs=True)["output_text"]

    return summary

def info_videos(dias=3):
    '''
    Función que devuelve los videos de los últimos 5 días

    Input:
        - xxxx: str -->

    Output:
        - results: object --> JSON con la información obtenida(titulo, fecha y url)
    '''

    # Fecha de hace 5 días
    today = datetime(datetime.now().year, datetime.now().month, datetime.now().day, tzinfo=timezone.utc)
    two_days_ago = today - timedelta(days=dias)
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
        summary = transcriptor(url)
        
        results["results"].append({"title": title,
                                   "author": author,
                                   "date": date,
                                   "url": url,
                                   "summary": summary
                                  })
    
    return results

