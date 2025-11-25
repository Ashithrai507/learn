import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

# Load image (grayscale or RGB)
img = Image.open("image.jpeg").convert("RGB")

# Convert image to tensor (C, H, W)
transform = transforms.ToTensor()
img_tensor = transform(img).unsqueeze(0)  # shape: (1, 3, H, W)

# Create a Conv layer
conv = nn.Conv2d(in_channels=3, out_channels=8, kernel_size=3)
# Random filters (like initial CNN layers)

# Apply convolution
feature_maps = conv(img_tensor)
print("Feature map shape:", feature_maps.shape)

# Plot the feature maps
feature_maps = feature_maps.detach().squeeze(0)  # shape: (8, H, W)

plt.figure(figsize=(12,8))
for i in range(8):
    plt.subplot(2, 4, i+1)
    plt.imshow(feature_maps[i], cmap='gray')
    plt.title(f"Filter {i}")
plt.show()
