import numpy as np
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, WeightedRandomSampler

from utils.preprocessing import get_transforms


def create_loaders(train_dir: str = 'data/train', val_dir: str = 'data/val', batch_size: int = 32):
    """Return train and validation DataLoaders with weighted sampling."""
    train_ds = ImageFolder(train_dir, transform=get_transforms(True))

    class_counts = np.bincount(train_ds.targets)
    sample_weights = 1.0 / class_counts[train_ds.targets]
    loader_weights = WeightedRandomSampler(
        sample_weights,
        num_samples=len(train_ds),
        replacement=True,
    )

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        sampler=loader_weights,
        num_workers=4,
    )

    val_loader = DataLoader(
        ImageFolder(val_dir, transform=get_transforms(False)),
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
    )

    return train_loader, val_loader


if __name__ == "__main__":
    train_loader, _ = create_loaders()
    print(next(iter(train_loader))[0].shape)
