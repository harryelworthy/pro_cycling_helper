# Pro Cycling Helper

The aim of this project is to classify frames of videos of pro cycling with riders split into teams. From this classification we can hopefully produce interesting stats, like which teams have the most TV time in a race, or who spends the most time on the front.

Current status:
* Pulled videos from 3 spring classics, cut them to race time, took 100 random stills from each
* Labelled the stills with YOLOv8x, only looking for people. Converted labels to labelimg format
* Self-annotated 300 images with labelimg
    * Added cyclists that were clearly missed
    * Removed spectators and motos
    * Didn't add every cyclist (would be too much work) - instead tried to stick to similar cyclists to those labelled by YOLO, either close to the camera or without overlap

TODO
* Refactor - most current stuff should be in a utils folder
* Write code to train YOLOv8x with the new data. Will need to colab/GPU
* Benchmark (eye test, plus a real test?)
* Create a function to go through a race video and pull a still at each second and add those stills to a folder, along with metadata on time and overlap
    * Maybe should do embedding here and put into a vectorized DB
* Deal with overlap - maybe don't need to?
* Use a model for embedding the images
* Run clustering of some kind on the embeddings
* Visualize results