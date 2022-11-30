import os

from HdRezkaApi import *
import requests


def download_video(directory, file_name, link):
    r = requests.get(link, stream=True)

    directory_exists = os.path.exists(directory)

    if not directory_exists:
        os.makedirs(directory)

    with open("{}/{}.mp4".format(directory, file_name), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)


url = input('Enter url: ')

rezka = HdRezkaApi(url)

seasons = rezka.getSeasons()
translations = list(rezka.getTranslations().keys())

qualities = list(rezka.getStream(1, 1).videos.keys())

for i in range(0, len(qualities)):
    print("{}. {}".format(i + 1, qualities[i]))

user_choice = input("\nSelect quality: ")
quality = qualities[int(user_choice) - 1]

print("\n\n")

for i in range(0, len(translations)):
    print("{}. {}".format(i + 1, translations[i]))

user_choice = input("\nSelect translation: ")
translation = translations[int(user_choice) - 1]

seasons_count = len(seasons[translation]['seasons'])

film_name = url.split('/')[-1].split('.')[0]

for i in range(1, seasons_count + 1):
    print("Downloading season {}/{}".format(i, seasons_count))

    episode_count = 0

    while True:
        try:
            episode_count += 1
            print("Downloading episode {}".format(episode_count))

            name = "{}-{}".format(i, episode_count)

            download_video(film_name, name, rezka.getStream(i, episode_count, translation)(quality))
        except:
            break
