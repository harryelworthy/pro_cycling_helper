from ultralytics import YOLO
import cv2
import os

confidence_threshold = 0.8

# Load a pre-trained YOLOv8 model
model = YOLO('yolov8x.pt')

# Directory containing images
image_dir = 'images/'

# Directory to save annotated images
output_dir = 'images/'
os.makedirs(output_dir, exist_ok=True)

# Read class names from classes.txt
with open(f'{image_dir}classes.txt', 'r') as f:
    class_names = [line.strip() for line in f]

# Function to convert bounding box to YOLO format
def convert_to_yolo_format(img_size, box):
    dw = 1. / img_size[0]
    dh = 1. / img_size[1]
    x = (box[0] + box[2]) / 2.0
    y = (box[1] + box[3]) / 2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

# Process images and save YOLO format annotations
for img_name in os.listdir(image_dir):
    if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    
    img_path = os.path.join(image_dir, img_name)
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: Unable to read image {img_path}")
        continue
    h, w, _ = img.shape

    # Run inference
    results = model(img_path, conf = confidence_threshold, classes = [0])
    
    txt_name = os.path.splitext(img_name)[0] + '.txt'
    with open(os.path.join(output_dir, txt_name), 'w') as f:
        for result in results:
            # Iterate over detected boxes
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # Extract coordinates and convert to numpy array
                cls = int(box.cls[0].item())  # Extract class and convert to Python int
                bbox = convert_to_yolo_format((w, h), (x1, y1, x2, y2))
                f.write(f"{cls} {' '.join(map(lambda x: f'{x:.6f}', bbox))}\n")

print("Processing complete. Annotation files have been saved.")