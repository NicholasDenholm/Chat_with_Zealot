# Utils
import os
import sys
from datetime import datetime
import numpy as np
import string
import easygui as g

# Torch related
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torch.utils.bottleneck as bottleneck

# Class inheritance
#from TestCases.test import Testing
from textdataset import TextDataset
from loading import Loading
from textmodel import TextModel
from train import Train
from generate_text import GenerateText
from makemodel import ModelTrainer
