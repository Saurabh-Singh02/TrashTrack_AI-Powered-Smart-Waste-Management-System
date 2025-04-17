import cv2
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from torchvision import models
import os

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define your model architecture
model = models.resnet18(pretrained=False)
num_classes = 2  # Change based on your dataset (e.g., 'O' and 'R')
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

# Load your trained model
model_path = "E:\\Working Directory\\Jupyter notebook\\waste_classification_model.pth"
model.load_state_dict(torch.load(model_path, map_location=device))
print(os.path.exists(model_path))  # Check if path is valid

model.to(device)
model.eval()

# Define the class names in correct order
class_names = ['Organic', 'Recyclable']  # Full names

# Define preprocessing transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],  # Standard for ResNet
                         [0.229, 0.224, 0.225])
])

# Start webcam
cap = cv2.VideoCapture(0)

# Set high resolution for webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Make window fullscreen
cv2.namedWindow("Waste Classification", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Waste Classification", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

print("Webcam started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to PIL Image
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Apply transformation
    input_tensor = transform(image).unsqueeze(0).to(device)

    # Inference
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = output.max(1)
        label = class_names[predicted.item()]

    # Choose text color based on prediction
    if label == 'Organic':
        color = (0, 255, 0)  # Green
    else:
        color = (255, 0, 0)  # Blue

    # Display prediction with colored text
    cv2.putText(frame, f'Prediction: {label}', (50, 80), cv2.FONT_HERSHEY_SIMPLEX,
                2, color, 3, cv2.LINE_AA)

    cv2.imshow("Waste Classification", frame)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
