import os
from pathlib import Path

HOME = os.getenv('HOME')
CLOUD_DIR = os.getenv('CLOUD_DIR')
APPS_DIR = os.getenv('APPS_DIR')
APPS_DATA_DIR = os.getenv('APPS_DATA_DIR')
VYPYR_DIR = os.getenv('VYPYR_DIR')
VYPYR_SRC_DIR = os.getenv('VYPYR_SRC_DIR')
SHYFT_DIR = os.getenv('SHYFT_DIR')
LOGS_DIR = os.getenv('LOGS_DIR')
SHYFT_DATA_PATH = Path(SHYFT_DIR, 'data.json')
KEMIST_DIR = os.getenv('KEMIST_DIR')
KEMIST_IMG_DIR = Path(KEMIST_DIR, 'images')

PWD = os.getcwd()
if PWD != APPS_DIR:
    os.chdir(APPS_DIR)

try:
    import vypyr
    from vypyr.src.kemist import main
    from vypyr.src.kemist.main import main as kem
    from vypyr.src import shyft 
    from vypyr.src.shyft.shyft import main as shyft_gui
    from vypyr.src.medulla.main import *

    div()
    typyr('    Vypyr has been successfully initialized.')
    
except Exception as e:
    print(f'ERROR:                {e}')
    
finally:
    old_pwd = os.getenv('OLDPWD')
    try:
        os.chdir(old_pwd)
        cwd = os.getcwd()
        typyr(f"Working directory:  {cwd}")
        div()
    except FileNotFoundError as e:
        print(f"ERROR:              {e}")
    
    

    
