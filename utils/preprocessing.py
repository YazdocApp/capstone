"""Utility preprocessing functions for the aesthetic-procedure-recommender project."""

from torchvision import transforms


def normalize(data):
    """Placeholder for data normalization logic."""
    pass


def augment(data):
    """Placeholder for data augmentation logic."""
    pass


def get_transforms(train: bool = True) -> transforms.Compose:
    """Return standard image transformations for training or inference."""

    basic = [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]

    if train:
        basic.insert(1, transforms.RandomHorizontalFlip())
        basic.insert(2, transforms.ColorJitter(0.2, 0.2, 0.2, 0.2))

    return transforms.Compose(basic)
