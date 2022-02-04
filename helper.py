from rich.console import Console
from rich.table import Table
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


def generateTable(*items):
    table = Table()
    table.add_column("#", justify="center", style="green",
                     header_style="yellow", no_wrap=True)
    table.add_column("Title", justify="left", style="cyan",
                     header_style="yellow", no_wrap=True)
    table.add_column("Rating", justify="center", style="magenta",
                     header_style="yellow", no_wrap=True)
    try:
        # iterate items, add index, and add to table then print
        for index, item in enumerate(*items):
            table.add_row(str(index + 1),
                          item['title'], str(item['score']).replace('None', '-'))
    except KeyError:
        for index, item in enumerate(*items):
            table.add_row(str(index + 1),
                          item['title'], '-')
    log.print(table)


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
    if os.name == "nt":
        if vplayer == "mpv":
            # ref: https://stackoverflow.com/questions/12373563/python-try-block-does-not-catch-os-system-exceptions
            if os.system(f"mpv.exe --terminal=no {url}") != 0:
                print(
                    'Sorry, this video player do not support video format fo this episode')
            else:
                return True
        elif vplayer == "vlc":
            print("Comming Soon")
    else:
        if vplayer == "mpv":
            # ref: https://stackoverflow.com/questions/12373563/python-try-block-does-not-catch-os-system-exceptions
            if os.system(f"mpv --terminal=no {url}") != 0:
                print(
                    'Sorry, this video player do not support video format fo this episode')
            else:
                return True
        elif vplayer == "vlc":
            print("Comming Soon")
    print("There is no suppport video player. Try mpv or vlc")


def generateAnimeDetail(id):
    result = req.get(f"{anime}{id}")
    item = result.json()
    return item


def generateEpisodeDetail(id):
    result = req.get(f"{eps}{id}")
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
                generateLinkDownload(qty360['vendor'], links)
            elif qty == "480p":
                generateLinkDownload(qty480['vendor'], links)
            elif qty == "720p":
                generateLinkDownload(qty720['vendor'], links)
            elif qty == "1080p":
                generateLinkDownload(qty1080['vendor'], links)
            else:
                log.print("Resolution Not Available", style="red")
            break
        except ValueError:
            log.print("Unknown Command", style="bold red")


def generateLinkDownload(contents, links):
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


def getAnimeEpisode(items):
    animeId = int(input("Which anime id? "))
    for index, item in enumerate(items):
        if index == animeId - 1:
            animeDetail = generateAnimeDetail(item['id'])
            episodes = animeDetail["episode_list"]
            log.print(
                f"Episode Count {len(episodes)}", style="yellow")
            episodeId = int(input("Which Episode? "))
            for index, episode in enumerate(reversed(episodes)):
                if index == episodeId - 1:
                    return generateEpisodeDetail(episode['id'])


def getDetailAnime(items):
    id = int(input("Which id? "))
    # iterate items and get id
    for index, item in enumerate(items):
        if index == id - 1:
            return item['id']


def getEpisodeDownload(items):
    animeId = int(input("Which anime id? "))
    for index, item in enumerate(items):
        if index == animeId - 1:
            animeDetail = generateAnimeDetail(item['id'])
            episodes = animeDetail["episode_list"]
            episodeId = int(input("Which Episode? "))
            for index, episode in enumerate(reversed(episodes)):
                if index == episodeId - 1:
                    return generateEpisodeDetail(episode['id'])


def getEpisode(items):
    log.print(
        f"Episode Count {len(items)}", style="yellow")
    episodeId = int(input("Which Episode? "))
    for index, episode in enumerate(reversed(items)):
        if index == episodeId - 1:
            return generateEpisodeDetail(episode['id'])
