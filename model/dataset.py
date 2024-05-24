from torch.utils.data import Dataset
import cv2 as cv
import torch


class CachedImageDataset(Dataset):
    def __init__(self, image_paths, device, img_size=(640, 640)):
        self.image_paths = image_paths
        self.device = device
        self.img_size = img_size
        self.cache = {}

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        if idx in self.cache:
            return self.cache[idx]

        image_path = self.image_paths[idx]
        image = cv.imread(image_path, cv.IMREAD_UNCHANGED)

        if image is None:
            raise ValueError(f"Failed to load image at path: {image_path}")

        if image.ndim == 2:
            image = cv.cvtColor(image, cv.COLOR_GRAY2RGB)
        elif image.shape[2] == 1:
            image = cv.cvtColor(image, cv.COLOR_GRAY2RGB)

        image = cv.resize(image, self.img_size)
        image = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
        image = image.to(self.device)

        self.cache[idx] = image
        return image