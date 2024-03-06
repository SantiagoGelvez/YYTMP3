import re
import shutil

from pytube import YouTube, Playlist
from moviepy.editor import *
from pytube.exceptions import AgeRestrictedError


def download_audio(link_url, folder=None):
    yt = YouTube(link_url)
    filename = f'{yt.title[:50]} - {yt.author[:25]}.mp3'
    filename = re.sub(r'[\\/*¿?:;{}¡!"<>|°+#$,]', '', filename)
    if os.path.exists(filename if not folder else f'{folder}/{filename}'):
        print('File already exists!')
        return

    try:
        audio = yt.streams.filter(mime_type='audio/mp4').order_by('abr').desc().first()

        audio_file_mp4 = audio.download()
        audio_mp4 = AudioFileClip(audio_file_mp4)
        audio_mp4.write_audiofile(filename)

        if folder:
            if not os.path.exists(folder):
                os.makedirs(folder)
            shutil.move(filename, folder)

        os.remove(audio_file_mp4)
    except AgeRestrictedError:
        print(f'<{yt.title}> is an age restricted video, skipping...')


def get_link_videos(playlist_url, folder=None):
    print('Getting videos links...')
    playlist = Playlist(playlist_url)
    links = playlist.video_urls

    print(f'Playlist: {playlist.title} - {len(links)} videos')
    print('Downloading videos...')
    for idx, url in enumerate(links):
        print(f'{round(idx*100/len(links), 1)}% processed')
        download_audio(url, folder)


def init_download(link_url, is_playlist=False, folder=None):
    if is_playlist:
        get_link_videos(link_url, folder)
    else:
        print('Init download...')
        download_audio(link_url, folder)


if __name__ == '__main__':
    LINK = ''  # Link to playlist or video
    FOLDER_NAME = ''  # Folder to save the audio
    IS_PLAYLIST = True  # True if the link is a playlist

    init_download(LINK, folder=FOLDER_NAME, is_playlist=IS_PLAYLIST)
    print('Download completed!')
