import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm  # no idea why but it fixes a later error
import torch.nn as nn
import torch.optim as optim
from UNET_Kevin import UNET
from utils import (
    load_checkpoint,
    save_checkpoint,
    get_loaders,
    check_accuracy,
    save_predictions_as_imgs,
)

#Hyperperameters
learning_rate = 5e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 75
NUM_EPOCHS = 10
NUM_WORKERS = 2
IMAGE_HEIGHT = 100
IMAGE_WIDTH = 100
PIN_MEMORY = True
LOAD_MODEL = False
# some problem is happening with the paths where local paths aren't working
TRAIN_IMG_DIR = "../shape_images/images/train"
#TRAIN_IMG_DIR = "../Unused_Training_Images/Lung_Images/train_images"
TRAIN_IMG_DIR = r"C:\Users\Test0\PycharmProjects\InCartaUNet-v2\shape_images\images\train"
TRAIN_MASK_DIR = "../shape_images/masks/train"
#TRAIN_MASK_DIR = "../Unused_Training_Images/Lung_Images/train_masks"
TRAIN_MASK_DIR = r"C:\Users\Test0\PycharmProjects\InCartaUNet-v2\shape_images\masks\train"
VAL_IMG_DIR = "../shape_images/images/test"
VAL_IMG_DIR = r"C:\Users\Test0\PycharmProjects\InCartaUNet-v2\shape_images\images\test"
#VAL_IMG_DIR = "../Unused_Training_Images/Lung_Images/validation_images"
VAL_MASK_DIR = "../shape_images/masks/test"
VAL_MASK_DIR = r"C:\Users\Test0\PycharmProjects\InCartaUNet-v2\shape_images\masks\test"
#VAL_MASK_DIR = "../Unused_Training_Images/Lung_Images/validation_masks"


# trains for one epoch, edit later to add more options if I want
def train_fn(loader, model, optimizer, loss_fn, scaler):
    loop = tqdm(loader)

    for batch_idx, (data, targets) in enumerate(loop):
        data = data.to(device=DEVICE)
        targets = targets.float().unsqueeze(1).to(device=DEVICE) # adds channel?

        # foward (float 16 training)
        with torch.cuda.amp.autocast():
            predictions = model(data)
            loss = loss_fn(predictions, targets)

        # backward
        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        # update tqdm loop
        loop.set_postfix(loss=loss.item())

def train():
    # from albuementations video, from what I can tell just normalizing images
    train_transform = A.Compose(
        [
            A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
            A.Rotate(limit=35, p=1.0),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.1),
            A.Normalize(
                mean=[0.0, 0.0, 0.0],
                std=[1.0, 1.0, 1.0],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )

    val_transforms = A.Compose(
        [
            A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
            A.Normalize(
                mean=[0.0, 0.0, 0.0],
                std=[1.0, 1.0, 1.0],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )

    model = UNET(in_channels=3, out_channels=1).to(DEVICE) # change outchanels for mult classes and add cross entro
    loss_fn = nn.BCEWithLogitsLoss() # auto does torch.sigmiod ig?
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    train_loader, val_loader = get_loaders(
        TRAIN_IMG_DIR,
        TRAIN_MASK_DIR,
        VAL_IMG_DIR,
        VAL_MASK_DIR,
        BATCH_SIZE,
        train_transform,
        val_transforms,
        NUM_WORKERS,
        PIN_MEMORY,
    )

    scaler = torch.cuda.amp.GradScaler()

    for epoch in range(NUM_EPOCHS):
        train_fn(train_loader, model, optimizer, loss_fn, scaler)

        # check accuracy
        check_accuracy(val_loader, model, device=DEVICE)

        # print some examples to a folder
        save_predictions_as_imgs(
            val_loader, model, folder="C:/Users/Test0/PycharmProjects/InCartaUNet-v2/output_images", device=DEVICE, epoch=epoch
        )

    # save the model after finishing training, could implement later where it saves after set # of epochs
    checkpoint = {
       "state_dict": model.state_dict(),
       "optimizer": optimizer.state_dict(),
    }
    save_checkpoint(checkpoint)

if __name__ == "__main__":
    train()