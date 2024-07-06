import random
from moviepy.editor import VideoFileClip
import pandas as pd
import os

def crop_video(video, start_time=None,end_time=None):
    # Video should be a video file clip
    # Get the total duration of the video
    video_duration = video.duration
    
    # Set the start and end times for the crop
    if start_time is None:
        start_time = 0
    if end_time is None:
        end_time = video_duration
    
    # Crop the video
    cropped_video = video.subclip(start_time, end_time)

    return cropped_video

def save_random_snippets(input_file, input_path, output_path, snippet_duration=10, num_snippets=1, start_time=None,end_time=None):
    # Load the video file
    video = VideoFileClip(f"{input_path}{input_file}.mp4")

    # Crop the video
    video = crop_video(video, start_time, end_time)
    
    # Get the total duration of the video
    video_duration = video.duration
    
    # Generate random start times for the snippets
    start_times = [random.uniform(0, video_duration - snippet_duration) for _ in range(num_snippets)]
    
    for i, start_time in enumerate(start_times):
        # Create the snippet
        snippet = video.subclip(start_time, start_time + snippet_duration)
        
        # Save the snippet to a file
        snippet_output_file = f"{output_path}{input_file}_snippet_{i+1}.mp4"
        snippet.write_videofile(snippet_output_file, codec="libx264")

    # Close the video file
    video.close()

def timestamp_to_seconds(timestamp):
    parts = timestamp.split(':')
    
    # If the format is MM:SS
    if len(parts) == 2:
        minutes = int(parts[0])
        seconds = int(parts[1])
        total_seconds = minutes * 60 + seconds
    
    # If the format is HH:MM:SS
    elif len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        total_seconds = hours * 3600 + minutes * 60 + seconds
    
    else:
        raise ValueError("Invalid timestamp format")
    
    return total_seconds

if __name__ == "__main__":
    # List of Videos to chop
    videos = pd.read_csv("video_metadata.csv")
    # Directories
    input_path = "raw_videos/"
    output_path = "video_snippets/"
    # Convert times to seconds
    videos["footage_start_ts"] = videos["footage_start_ts"].apply(timestamp_to_seconds)
    videos["footage_end_ts"] = videos["footage_end_ts"].apply(timestamp_to_seconds)


    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Crop, split and save snippets
    for index, video in videos.iterrows():
        # Save snippets
        save_random_snippets(video['race_name'],input_path,output_path, snippet_duration=10, num_snippets=10, start_time=video["footage_start_ts"],end_time=video["footage_end_ts"])
        # Update progress
        print(f"Saved snippets for {video['race_name']}")