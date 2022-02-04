from rich.panel import Panel
import requests as req
from pprint import pprint

from helper import *


def welcome():
    log.print("""███████╗ █████╗ ███╗   ███╗███████╗██╗  ██╗ █████╗ ██████╗  █████╗ ██╗  ██╗██╗   ██╗
██╔════╝██╔══██╗████╗ ████║██╔════╝██║  ██║██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██║   ██║
███████╗███████║██╔████╔██║█████╗  ███████║███████║██║  ██║███████║█████╔╝ ██║   ██║
╚════██║██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██║██╔══██║██║  ██║██╔══██║██╔═██╗ ██║   ██║
███████║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║██║  ██║██████╔╝██║  ██║██║  ██╗╚██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝
""", justify="center", style="blue")

    log.print(""" ██████╗██╗     ██╗
██╔════╝██║     ██║
██║     ██║     ██║
██║     ██║     ██║
╚██████╗███████╗██║
 ╚═════╝╚══════╝╚═╝
    """, justify="center", style="yellow")
    log.print("Created By: Hanivan Rizky", style="purple")
    log.print("Github: @Hanivan")
    log.print("Youtube: Lintasan Video\n", style="red")


def main():
    res = showMenu()
    if res == "List All Anime":
        allAnime(anime)
    elif res == "Search Anime":
        searchAnime()
    elif res == "List Ongoing Anime":
        ongoingAnime(ongoing)
    elif res == "Show Schedule Anime":
        print('Comming Soon')
    return True


def allAnime(url):
    result = req.get(url)
    items = result.json()['anime_list']
    generateTable(items)
    # ask user to input number of anime
    while True:
        try:
            menuList = ['Next Page', 'Prev Page', 'Show Detail Anime',
                        'Watch Anime Episode', 'Download Anime Episode', 'Main Menu']
            nextLink = result.json()['next_page']
            prevLink = result.json()['prev_page']
            res = menu(menuList, "What do you want to do?")

            if res == "Next Page":
                if nextLink == "#":
                    log.print("Page does not exist", style="bold red")
                    continue
                allAnime(nextLink)
            if res == "Prev Page":
                if prevLink == "#":
                    log.print("Page does not exist", style="bold red")
                    continue
                allAnime(prevLink)
            elif res == "Show Detail Anime":
                res = getDetailAnime(items)
                detailAnime(res)
            elif res == "Watch Anime Episode":
                res = getAnimeEpisode(items)
                watchEpisode(res)
            elif res == "Download Anime Episode":
                res = getEpisodeDownload(items)
                downloadEpisode(res)
            elif res == "Main Menu":
                main()
            break
        except ValueError:
            log.print("Unknown Command", style="bold red")


def ongoingAnime(url):
    result = req.get(url)
    items = result.json()['anime_list']
    generateTable(items)
    # ask user to input number of anime
    while True:
        try:
            menuList = ['Watch Anime Episode',
                        'Download Anime Episode', 'Main Menu']
            res = menu(menuList, "What do you want to do?")

            if res == "Watch Anime Episode":
                res = getAnimeEpisode(items)
                watchEpisode(res)
            elif res == "Download Anime Episode":
                res = getEpisodeDownload(items)
                downloadEpisode(res)
            elif res == "Main Menu":
                main()
            break
        except ValueError:
            log.print("Unknown Command", style="bold red")


def detailAnime(id):
    result = req.get(f"{anime}{id}")
    item = result.json()
    # get episode from item and iterate using for loop
    episodes = item['episode_list']
    producers = item['producer_list']
    studios = item['studio_list']

    episodeList = []
    for episode in episodes:
        episodeList.append(episode['id'])
    # iterate studio and get producer_name
    producerList = []
    for producer in producers:
        producerList.append(producer['producer_name'])
    # join item in producers then print
    producer = ", ".join(producerList)
    # iterate studio and get producer_name
    studioList = []
    for studio in studios:
        studioList.append(studio['studio_name'])
    # join item in producers then print
    studio = ", ".join(studioList)

    content = Table.grid(padding=1)
    content.add_column(style="green", justify="left")
    window = Panel(
        content,
        padding=1,
        title="Detail's Anime",
        border_style="bright_blue",
    )

    content.add_row(
        "Title",
        item['title']
    )
    content.add_row(
        "Synopsis",
        item['synopsis']
    )
    content.add_row(
        "Score",
        str(item['score'])
    )
    content.add_row(
        "Status",
        item['status']
    )
    content.add_row(
        "Release Date",
        item['release_date']
    )
    content.add_row(
        "Producers",
        producer
    )
    content.add_row(
        "Studio",
        studio
    )

    log.print(window)

    while True:
        try:
            menuList = ['Watch Episode', 'Download Episode',
                        'List All Anime', 'Search Anime', 'Main Menu']
            res = menu(menuList, "What do you want to do?")

            if res == "Watch Episode":
                res = getEpisode(episodes)
                watchEpisode(res)
            elif res == "Download Episode":
                res = getEpisode(episodes)
                downloadEpisode(res)
            elif res == "List All Anime":
                allAnime(anime)
            elif res == "Search Anime":
                searchAnime()
            elif res == "Main Menu":
                main()
            break
        except ValueError:
            log.print("Unknown Command", style="bold red")


def downloadEpisode(anime):
    # check anime['download_list'][0] is not empty then pass to variable name download else value is None using ternary operator
    downloadMKV = anime['download_list'][0] if anime['download_list'][0] is not None else {}
    downloadMP4 = anime['download_list'][1] if anime['download_list'][1] is not None else {}
    downloadx265 = anime['download_list'][2] if anime['download_list'][2] is not None else {
    }

    while True:
        try:
            menuList = ['MKV', 'MP4', 'x265']
            res = menu(
                menuList, "What video type do you want to download?")
            if res == "MKV":
                getQualityVideo(downloadMKV)
            elif res == "MP4":
                getQualityVideo(downloadMP4)
            elif res == "x265":
                getQualityVideo(downloadx265)
            break
        except ValueError:
            log.print("Unknown Command", style="bold red")


def watchEpisode(episode):
    # ubah animeId, ambil link dari all_episode (alias detail anime)
    streamLink = episode['stream_list'][0]
    hQuality = streamLink['high_quality']
    mQuality = streamLink['medium_quality']
    lQuality = streamLink['low_quality']
    nextEpisode = episode['next_eps']
    prevEpisode = episode['prev_eps']
    animeId = nextEpisode.replace(eps, "")
    animeId = "-".join(animeId.split("-")[:-2]) + '/'
    nextEpisode = nextEpisode.replace(eps, "")
    prevEpisode = prevEpisode.replace(eps, "")
    while True:
        try:
            qualityList = [
                'High Quality (720p)', 'Medium Quality (480p)', 'Low Quality (360p)']
            res = menu(
                qualityList, "Which quality do you want to watch?")
            log.print(
                "Please close the video player to select different options...", style="blue")
            if res == "High Quality (720p)" and is_downloadable(hQuality):
                if playVideo(hQuality):
                    pass
            elif res == "Medium Quality (480p)" and is_downloadable(mQuality):
                if playVideo(mQuality):
                    pass
            elif res == "Low Quality (360p)" and is_downloadable(lQuality):
                if playVideo(lQuality):
                    pass
            else:
                log.print("Link isn't valid", style="bold red")

            break
        except ValueError:
            log.print("Unknown Command", style="bold red")

    while True:
        try:
            menuList = ['Next Episode', 'Prev Episode', 'Select Different Episode',
                        'Search Anime', 'Show All Anime']
            res = menu(menuList, "What do you want to do?")
            if res == "Next Episode":
                res = generateEpisodeDetail(nextEpisode)
                watchEpisode(res)
            if res == "Prev Episode":
                res = generateEpisodeDetail(prevEpisode)
                watchEpisode(res)
            elif res == "Select Different Episode":
                res = generateAnimeDetail(animeId)
                episodeId = int(input("Which Episode? "))
                for index, episode in enumerate(reversed(res["episode_list"])):
                    if index == episodeId - 1:
                        res = generateEpisodeDetail(episode['id'])
                        watchEpisode(res)
            elif res == "Search Anime":
                searchAnime()
            elif res == "Show All Anime":
                allAnime(anime)
            break
        except ValueError:
            log.print("Unknown Command", style="bold red")


def searchAnime():
    # get input user, split it and join with '+'
    query = input("What anime are you looking for? ")
    query = "+".join(query.split()).lower()
    result = req.get(f"{search}{query}")
    items = result.json()['anime_list']
    generateTable(items)
    while True:
        try:
            menuList = ['Show Detail Anime',
                        'Watch Anime Episode', 'Download Anime Episode', 'Search Anime', 'Main Menu']
            res = menu(menuList, "What do you want to do?")

            if res == "Show Detail Anime":
                res = getDetailAnime(items)
                detailAnime(res)
            elif res == "Watch Anime Episode":
                res = getAnimeEpisode(items)
                watchEpisode(res)
            elif res == "Download Anime Episode":
                res = getEpisodeDownload(items)
                downloadEpisode(res)
            elif res == "Search Anime":
                searchAnime()
            elif res == "Main Menu":
                main()
            break
        except ValueError:
            log.print("Unknown Command", style="bold red")


if __name__ == "__main__":
    main()
