from rich.console import Console
from rich.layout import Layout
from zippyshare_downloader import download
import requests as req
import enquiries as qst
from dotenv import load_dotenv, dotenv_values
import os
from pprint import pprint

log = Console()
layout = Layout()
load_dotenv()
config = dotenv_values(".env")
anime = f"{config['BASEURL']}{config['ANIME']}"
ongoing = f"{config['BASEURL']}{config['ONGOING']}"
eps = f"{config['BASEURL']}{config['EPS']}"
schedule = f"{config['BASEURL']}{config['SCHEDULE']}"
search = f"{config['BASEURL']}{config['SEARCH']}"
vplayer = f"{config['VPLAYER']}"


def showMenu():
    options = ['Search Anime', 'List All Anime', 'List Ongoing Anime',
               'Show Schedule Anime']
    response = qst.choose(
        "Please Select One Of Them: (Use Arrow Keys) ", options)
    return format(response)


def menu(items, msg):
    options = []
    for item in items:
        options.append(item)
    # options = ['Next Page', 'Show Detail Anime', 'Watch Anime Episode', 'Show Schedule Anime']
    response = qst.choose(
        f"{msg} (Use Arrow Keys) ", options)
    return format(response)


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = req.head(url, allow_redirects=False)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def playVideo(url):
    if vplayer == "mpv":
        # ref: https://stackoverflow.com/questions/12373563/python-try-block-does-not-catch-os-system-exceptions
        if os.system(f"mpv --terminal=no {url}") != 0:
            print('Sorry, this video player do not support video format fo this episode')
        else:
            return True
    elif vplayer == "vlc":
        print('Comming Soon')
    else:
        print("There is no suppport video player. Try mpv or vlc")


def getAnimeDetail(id):
    result = req.get(f"https://samehadaku-api.herokuapp.com/api/anime/{id}")
    item = result.json()
    return item


def getEpisodeDetail(id):
    result = req.get(f"https://samehadaku-api.herokuapp.com/api/eps/{id}")
    item = result.json()
    return item


def getQualityVideo(links):
    qty360 = links['content'][0] if links['content'][0] is not None else {}
    qty480 = links['content'][1] if links['content'][1] is not None else {}
    qty720 = links['content'][2] if links['content'][2] is not None else {}
    qty1080 = links['content'][3] if links['content'][3] is not None else {}

    while True:
        try:
            qualityList = ['360p', '480p', '720p', '1080p']
            qty = menu(qualityList, "What quality do you want to download?")

            if qty == "360p":
                getLinkDownload(qty360['vendor'], links)
            elif qty == "480p":
                getLinkDownload(qty480['vendor'], links)
            elif qty == "720p":
                getLinkDownload(qty720['vendor'], links)
            elif qty == "1080p":
                getLinkDownload(qty1080['vendor'], links)
            else:
                log.print("Resolution Not Available", style="red")
            break
        except ValueError:
            log.print("Unknown Command", style="bold red")


def getLinkDownload(contents, links):
    # iterate contents and check if content['link'] == 'Zippyshare' then print link
    try:
        for content in contents:
            if content['name'] == 'Zippyshare':
                # check if folder download is exist, if not create folder
                if not os.path.exists('download'):
                    os.makedirs('download')
                download(content['link'], folder="download")
                break
            else:
                log.print(
                    "Sorry, link download from Zippyshare not available", style="bold red")
    except FileNotFoundError:
        log.print(
            "File Not Available, Please Select Different Resolution or Format Video", style="bold red")
        getQualityVideo(links)
