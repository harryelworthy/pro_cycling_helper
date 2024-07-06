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
* Benchmark trained model (eye test, plus a real test?)
* Write code to randomly pull cyclist images
* Classify them into teams

* Use existing model? Or train another YOLO instance to classify teams, then I'll vectorise and cluster to be more flexible
* Visualize results
* Look at vector DB
 
* Write actual inference code
* Deal with overlap - maybe don't need to?

* Clean up data_collection & add readme for that step