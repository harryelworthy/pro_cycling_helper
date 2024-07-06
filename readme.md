# Pro Cycling Helper

The aim of this project is to classify frames of videos of pro cycling with riders split into teams. From this classification we can hopefully produce interesting stats, like which teams have the most TV time in a race, or who spends the most time on the front.

Right now I've pulled images from races and manually updated naive YOLO annotations, and trained a YOLO model on those annotated images to detect cyclists.

TODO
* Eye test trained model
    * It seems to be dropping spectators better than the original, but it is still picking them up sometimes. Maybe I should annotate spectators in the images as well, given their similarity to cyclists?
* Manually classify generated crops into teams

* Use existing model? Or train another YOLO instance to classify teams, then I'll vectorise and cluster to be more flexible
* Visualize results
* Look at vector DB
 
* Write actual inference code
* Deal with overlap - maybe don't need to?

* Clean up data_collection & add readme for that step