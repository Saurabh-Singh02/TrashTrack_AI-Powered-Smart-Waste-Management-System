import cv2
import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
import torch.nn.functional as F

# Class labels
class_names = ['Organic', 'Recyclable', 'E-waste']

# CNN model architecture
class WasteClassifier(nn.Module):
    def __init__(self, num_classes=3):
        super(WasteClassifier, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.fc1 = nn.Linear(32 * 56 * 56, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 32 * 56 * 56)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Load trained model
model = WasteClassifier(num_classes=len(class_names))
model.load_state_dict(torch.load(r'E:\Working Directory\Jupyter notebook\waste_combined.pth', map_location=torch.device('cpu')))
model.eval()

# Transform for input image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

def predict_frame(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img)
    input_tensor = transform(pil_img).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.softmax(output, dim=1)
        _, predicted = torch.max(probs, 1)
        confidence = probs[0][predicted.item()].item()
        return class_names[predicted.item()], confidence

# Start webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow('Waste Classifier', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Waste Classifier', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
print("Press 'q' to quit.")

# Focus area settings
focus_size = 0.5  # Smaller focus area (50% of frame size)
focus_color = (0, 255, 0)  # Green
crosshair_color = (0, 165, 255)  # Orange

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    
    # Focus area dimensions (smaller for more precision)
    focus_w, focus_h = int(width * focus_size), int(height * focus_size)
    x1, y1 = (width - focus_w) // 2, (height - focus_h) // 2
    x2, y2 = x1 + focus_w, y1 + focus_h
    
    # Extract focus area for prediction
    focus_area = frame[y1:y2, x1:x2]
    
    # Predict only on the focus area
    pred_class, conf = predict_frame(focus_area)
    label = f"{pred_class} ({conf * 100:.1f}%)"
    
    # Draw subtle focus rectangle (thinner border)
    cv2.rectangle(frame, (x1, y1), (x2, y2), focus_color, 2)
    
    # Draw precise crosshair
    center_x, center_y = width // 2, height // 2
    crosshair_size = 15  # Smaller crosshair
    
    # Horizontal line
    cv2.line(frame, (center_x - crosshair_size, center_y), 
             (center_x + crosshair_size, center_y), crosshair_color, 2)
    # Vertical line
    cv2.line(frame, (center_x, center_y - crosshair_size), 
             (center_x, center_y + crosshair_size), crosshair_color, 2)
    
    # Draw small circles at crosshair ends for better visibility
    cv2.circle(frame, (center_x - crosshair_size, center_y), 3, crosshair_color, -1)
    cv2.circle(frame, (center_x + crosshair_size, center_y), 3, crosshair_color, -1)
    cv2.circle(frame, (center_x, center_y - crosshair_size), 3, crosshair_color, -1)
    cv2.circle(frame, (center_x, center_y + crosshair_size), 3, crosshair_color, -1)
    
    # Display prediction (cleaner presentation)
    text_bg_height = 50
    cv2.rectangle(frame, (0, 0), (width, text_bg_height), (0, 0, 0), -1)
    cv2.putText(frame, label, (width//2 - 150, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Help text at bottom
    cv2.putText(frame, "Align object with the orange crosshair", (width//2 - 200, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    cv2.imshow('Waste Classifier', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()