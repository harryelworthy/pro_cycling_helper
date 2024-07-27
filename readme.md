# Pro Cycling Helper

Built using YOLO, this model can detect cyclists and their teams in videos of pro cycling. Currently, the model combines an object detector with a classifier. This means that it will not be able to work well out-of-sample, which is a shame because cycling teams and uniforms change frequently.

I'd like to update it to use clustering, so that it can be used on new team uniforms. I've tried taking embeddings from the classifier with the head chopped off to do this, but could not cluster teams well. I would likely need to do some combination of:
* Training a model like CLIP or DINO, rather than a simple classifier YOLO, which is not designed to have meaningful embeddings. I've tried CLIP without fine-tuning, and it couldn't cluster teams well.
* More manual adjustment to the cyclist images - i.e. cutting to just their outfits

Something like [this setup](https://engineering.atspotify.com/2023/12/recursive-embedding-and-clustering/) from Spotify is what I'm trying to emulate.

## TODO
### Main line
* Write actual inference code + instruction
* Try out clustering steps above
* Test on new teams (e.g. in TDF with some new jerseys, or in older years with all new teams)

### Optimizations/Cleaning
* Improve cyclist detection
    * I think annotating & detecting spectators and motos would help them not be classified as cyclists
* Look at a vector DB
* Clean up data_collection & add readme for that step

### Working with end product
* Check camera time by team by race - who was getting the most exposure this season?
* Combine with face detection to approximate riders being 'in the wind' - which teams spend most time in the wind each race?
* Are there patterns in which teams are on camera early vs. late in the race?