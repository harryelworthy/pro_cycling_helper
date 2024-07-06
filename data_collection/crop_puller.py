from image_puller import save_random_images
from moviepy.editor import VideoFileClip
import os
import pandas as pd
from data_collection.video_cleaner import timestamp_to_seconds
from ultralytics import YOLO

def save_random_crops(model, input_file, input_path, output_path, num_images=1, start_time=None,end_time=None):
    save_random_images(input_file, input_path, output_path, num_images, start_time, end_time)
    for i in range(num_images):
        input_file = f"{output_path}{input_file}_image_{i+1}.png"
        results = model.predict(input_file, conf=0.8)
        os.remove(f"{output_path}{input_file}_image_{i+1}.png")
        results.save_crop(savedir = output_path, file_name = f"{input_file}_image_{i+1}")

if __name__ == "__main__":
    # Number of images per race
    num_images = 20
    # List of Videos to chop
    videos = pd.read_csv("video_metadata.csv")
    # Directories
    input_path = "raw_videos/"
    output_path = "annotated_crops/"
    # Convert times to seconds
    videos["footage_start_ts"] = videos["footage_start_ts"].apply(timestamp_to_seconds)
    videos["footage_end_ts"] = videos["footage_end_ts"].apply(timestamp_to_seconds)


    if not os.path.exists(output_path):
        os.makedirs(output_path)

    model = YOLO("models/best_model.pt")

    # Save crops
    for index, video in videos.iterrows():
        # Save images
        save_random_crops(model, video['race_name'],input_path,output_path, num_images=num_images, start_time=video["footage_start_ts"],end_time=video["footage_end_ts"])
        # Update progress
        print(f"Saved crops for {video['race_name']}")