import datetime as dt
import pandas as pd
import glob
import os
from pathlib import Path

folder_path = './20220706-001'
save_path = './out'
folders = glob.glob('{}/*'.format(folder_path))
os.makedirs(save_path, exist_ok=True)

print(folders)
