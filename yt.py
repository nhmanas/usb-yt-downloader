from pytube import YouTube, Playlist
import os
import moviepy.editor as mp
import shutil
import sys

class YouTubePlaylistProcessor:
    def __init__(self, playlist_url, destination_path):
        self.playlist_url = playlist_url
        self.destination_path = destination_path
        self.folder = "./download"
        os.makedirs(self.folder, exist_ok=True)

    def download_and_convert(self, url, notDownloaded):
        try:
            print("Downloading:", url)
            video = YouTube(url)
            video.streams.filter(only_audio=True).first().download(self.folder)

            # Convert to mp3
            mp4_path = os.path.join(self.folder, video.title + ".mp4")
            mp3_path = os.path.join(self.folder, os.path.splitext(video.title)[0] + '.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)

        except Exception as e:
            notDownloaded.append(url)
            print("Error downloading/processing:", url)
            print(e)

    def move_to_usb_drive(self, usb_drive_path):
        for file in os.listdir(self.folder):
            if file.endswith('.mp3'):
                src_path = os.path.join(self.folder, file)
                dst_path = os.path.join(usb_drive_path, file)

                # Check if the file already exists on the USB drive before copying
                if not os.path.exists(dst_path):
                    shutil.move(src_path, dst_path)
                    print("Transferred:", file)
                else:
                    print("Skipped (already exists):", file)

    def process_playlist(self):
        try:
            playlist = Playlist(self.playlist_url)
            os.makedirs(self.destination_path, exist_ok=True)
            notDownloaded = []

            # Step 1: Compare Songs
            if os.path.exists(self.destination_path):
                usb_songs = set(os.listdir(self.destination_path))
                for url in playlist:
                    video = YouTube(url)
                    mp3_filename = os.path.splitext(video.title)[0] + '.mp3'
                    if mp3_filename not in usb_songs:
                        self.download_and_convert(url, notDownloaded)
                print("Comparison completed.")
            else:
                print("Destination path not found.")

            # Step 2: Move MP3 files to the USB flash drive
            if os.path.exists(self.destination_path):
                self.move_to_usb_drive(self.destination_path)
                print("MP3 files have been transferred to the USB flash drive.")
            else:
                print("Destination path not found.")

        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    with open("/tmp/yt_python_version.log", "a") as log_file:
        log_file.write("Running yt.py with Python {}\n".format(sys.version))
    
    playlist_url = "https://www.youtube.com/watch?v=my-awesome-playlist"
    destination_path = os.path.join(os.sep, "media", "username", "myflash", "metal-music")

    YouTubePlaylistProcessor(playlist_url, destination_path).process_playlist()
