import torch
import torchvision
from dataset import CarvanaDataset
from torch.utils.data import DataLoader
from os import path
from os import makedirs

import numpy as np


def save_checkpoint(state, filename="my_checkpoint.pth.tar"):
    print("=> Saving checkpoint")
    torch.save(state, filename)


def load_checkpoint(checkpoint, model):
    print("=> Loading checkpoint")
    model.load_state_dict(checkpoint["state_dict"])


def get_loaders(
    train_dir,
    train_maskdir,
    val_dir,
    val_maskdir,
    batch_size,
    train_transform,
    val_transform,
    num_workers=4,
    pin_memory=True,
):
    train_ds = CarvanaDataset(
        image_dir=train_dir,
        mask_dir=train_maskdir,
        transform=train_transform,
    )

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=True,
    )

    val_ds = CarvanaDataset(
        image_dir=val_dir,
        mask_dir=val_maskdir,
        transform=val_transform,
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=False,
    )

    return train_loader, val_loader


def check_accuracy(loader, model, device="cuda"):
    num_correct = 0
    num_pixels = 0
    num_wrong = 0
    dice_score = 0
    model.eval()

    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            y = y.to(device).unsqueeze(1)
            preds = torch.sigmoid(model(x))
            preds = (preds > 0.5).float() # think like creating it like binary, true or false
            num_correct += (preds == y).sum()
            num_pixels += torch.numel(preds)
            dice_score += (2 * (preds * y).sum()) / (
                (preds + y).sum() + 1e-8 # 1e-8 is there to prevent divide by 0 errors
            )

    print(
        f"Got {num_correct} out of {num_pixels} with acc {num_correct/num_pixels*100:.2f}"
    )
    print(f"Dice score: {dice_score/len(loader)}")

    # switches the model back into training mode
    model.train()
    # better metrics for measuring accuracy, dice scores are one example **TODO**
    # look more into dice scores or any other form of measurement, and maybe allow it where you can customize which metric is used


def save_predictions_as_imgs(loader, model, folder="saved_images/", device="cuda", epoch=1):
    model.eval()

    # making folder for the epoch
    if not path.exists(f"{folder}/epoch_{epoch}"):
        makedirs(f"{folder}/epoch_{epoch}")

    # setting folder to be the new path w/ the corresponding epoch
    folder = f"{folder}/epoch_{epoch}"

    # for an index loop through images and masks of the loader
    for idx, (x, y) in enumerate(loader):
        x = x.to(device=device)

        with torch.no_grad():
            # turning it into BW masks I believe
            preds = torch.sigmoid(model(x))
            #preds[preds > 0] = 255
            preds = preds.float()
        # saving the prediction to the inputted folder
        torchvision.utils.save_image(
            preds, f"{folder}/{idx}_pred_{epoch}.png"
        )

        # saving the original image.
        torchvision.utils.save_image(y.unsqueeze(1), f"{folder}/ {idx} - ground_truth.png")
        torchvision.utils.save_image(x, f"{folder}/ {idx} - og_image.png")

        overlayed_image = x + y.unsqueeze(1)
        torchvision.utils.save_image(overlayed_image, f"{folder}/ {idx} - overlayed_image.png")

    model.train()
