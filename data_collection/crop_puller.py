from image_puller import save_random_images
import os
import pandas as pd
from video_cleaner import timestamp_to_seconds
from ultralytics import YOLO
from PIL import Image
from shutil import rmtree

def save_random_crops(model, input_file, input_path, output_path, 
                      num_crops=1, 
                      start_time=None,
                      end_time=None,
                      min_pixels=15000):
    # We don't know how many crops each image will generate, so we use a while loop to keep generating crops until we reach the desired number
    # Sometimes this will slightly overshoot, that's OK
    crops = 0
    # Create empty directories
    for path in [f"{output_path}temp/",f"{output_path}temp/cyclist/"]:
        if not os.path.exists(path):
            os.mkdir(path)
    
    while crops < num_crops:
        # Generate one image
        save_random_images(input_file, input_path, output_path, 1, start_time, end_time)
        input_file_full = f"{output_path}{input_file}_image_1.png"
        results = model.predict(input_file_full, conf=0.8, verbose=False)
        for result in results:
            # Save crops to a temp folder
            result.save_crop(save_dir = f"{output_path}temp/", file_name = f"{input_file}_image_{crops}")
            saved_crops = 0
            # Go through all saved jpgs and check if they are large enough
            for filename in os.listdir(f"{output_path}temp/cyclist"):
                if filename.lower().endswith('.jpg'): # Check it's an image
                    with Image.open(f"{output_path}temp/cyclist/{filename}") as img:
                        width, height = img.size
                        if width * height >= min_pixels:
                            crops += 1
                            print(f"Saved crop {crops} for {input_file}")
                            # Move crop into the main folder and rename it
                            os.rename(f"{output_path}temp/cyclist/{filename}", f"{output_path}{input_file}_image_{crops}.jpg")
        os.remove(f"{output_path}{input_file}_image_1.png") # Delete the original image
    # When we have enough crops, delete the temp folder
    rmtree(f"{output_path}temp/")

if __name__ == "__main__":
    # Number of images per race
    num_crops = 50
    # Min image size - checked by eye, this is about the smallest size that is still usually clear to the human eye
    min_pixels = 15000
    # List of Videos to chop
    videos = pd.read_csv("video_metadata.csv")
    # Directories
    input_path = "raw_videos/"
    output_path = "crops/"
    # Convert times to seconds
    videos["footage_start_ts"] = videos["footage_start_ts"].apply(timestamp_to_seconds)
    videos["footage_end_ts"] = videos["footage_end_ts"].apply(timestamp_to_seconds)


    if not os.path.exists(output_path):
        os.makedirs(output_path)

    model = YOLO("models/best.pt")

    # Save crops
    for index, video in videos.iterrows():
        # Save images
        save_random_crops(model, video['race_name'],input_path,output_path, num_crops=num_crops, start_time=video["footage_start_ts"],end_time=video["footage_end_ts"], min_pixels=min_pixels)
        # Update progress
        print(f"Saved crops for {video['race_name']}")