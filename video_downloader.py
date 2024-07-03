from pytube import YouTube
import os
import pandas as pd

def download_video(video_url, output_path, name):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path, filename=f"{name}.mp4")
        print(f"Downloaded: {yt.title}")
    except Exception as e:
        print(f"Error downloading {video_url}: {e}")

def download_videos(video_urls, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for index, video in video_urls.iterrows():
        download_video(video["link"], output_path, video["race_name"])

if __name__ == "__main__":
    # List of YouTube URLs to download
    videos = pd.read_csv("video_metadata.csv")
    # Output directory
    output_path = "raw_videos/"

    download_videos(videos, output_path)
