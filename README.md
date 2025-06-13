#aesthetic-procedure-recommender

This project provides a very small scaffold for experimenting with machine learning models that recommend aesthetic procedures.

## Install

Install the core dependencies with pip:

```bash
pip install torch torchvision
```

## Download Data

Use the provided script to download the aesthetic face recognition dataset:

```bash
./utils/download_dataset.sh
```

After downloading, organize the images into training and validation folders:

```bash
python utils/split_dataset.py
```

## Train

Use the provided notebook to verify that PyTorch sees your GPU and to begin model development:

```bash
jupyter notebook model.ipynb
```

## Infer

Load your trained model and perform inference using your own script or an interactive Python session:

```bash
python -c "import torch; print('GPU available:', torch.cuda.is_available())"
```
