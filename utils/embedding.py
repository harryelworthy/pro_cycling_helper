import umap
import torch
import clip

def get_openai_clip_embedding(imgs, model_name="ViT-B/32", device="cuda"):
  openai_clip_model, openai__preprocess = clip.load(model_name,device)
  with torch.no_grad():
    preprocessed = torch.stack([openai__preprocess(i) for i in imgs]).to(device)
    features = openai_clip_model.encode_image(preprocessed)
    features /= features.norm(dim=-1, keepdim=True)
    return features[0]