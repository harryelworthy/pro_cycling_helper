import random
from moviepy.editor import VideoFileClip
import pandas as pd
import os
from data_collection.video_cleaner import crop_video, timestamp_to_seconds

def save_random_images(input_file, input_path, output_path, num_images=1, start_time=None,end_time=None):
    # Load the video file
    video = VideoFileClip(f"{input_path}{input_file}.mp4")

    # Crop the video
    video = crop_video(video, start_time, end_time)
    
    # Get the total duration of the video
    video_duration = video.duration
    
    # Generate random times for the images
    start_times = [random.uniform(0, video_duration) for _ in range(num_images)]
    
    for i, start_time in enumerate(start_times):
        # Save the image to a file
        frame_output_file = f"{output_path}{input_file}_image_{i+1}.png"
        video.save_frame(frame_output_file,t=start_time)

    # Close the video file
    video.close()

if __name__ == "__main__":
    # Number of images per race
    num_images = 100
    # List of Videos to chop
    videos = pd.read_csv("video_metadata.csv")
    # Directories
    input_path = "raw_videos/"
    output_path = "images/"
    # Convert times to seconds
    videos["footage_start_ts"] = videos["footage_start_ts"].apply(timestamp_to_seconds)
    videos["footage_end_ts"] = videos["footage_end_ts"].apply(timestamp_to_seconds)


    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Crop and save images
    for index, video in videos.iterrows():
        # Save images
        save_random_images(video['race_name'],input_path,output_path, num_images=num_images, start_time=video["footage_start_ts"],end_time=video["footage_end_ts"])
        # Update progress
        print(f"Saved snippets for {video['race_name']}")