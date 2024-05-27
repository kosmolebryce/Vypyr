import os
from pathlib import Path

HOME = Path.home().resolve()
WORKSPACES_DIR = HOME / 'workspaces'
VYPYR_DIR = WORKSPACES_DIR / 'vypyr'
SRC_DIR = VYPYR_DIR / 'src'
SHYFT_DIR = SRC_DIR / 'shyft'
LOGS_DIR = SHYFT_DIR / 'logs'
DATA_PATH = SHYFT_DIR / 'data.json'
KEMIST_DIR = SRC_DIR / 'kemist'
KEMIST_IMG_DIR = KEMIST_DIR / 'images'

PWD = os.getcwd()
if PWD != WORKSPACES_DIR:
    os.chdir(WORKSPACES_DIR)
else:
    pass

try:
    import vypyr
    from vypyr.src import *
    from src.kemist import main
    from kemist.main import main as kem
    from shyft import main as shyft
    from medulla.main import *
    
    div()
    typyr('    Vypyr has been successfully initialized.')
    div()
except Exception as e:
    print(f'ERROR:                {e}')
