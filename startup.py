import click
import os
import logging
from pathlib import Path
import traceback
import sys

# Configure logging to log to stderr
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

HOME = os.getenv("HOME")
CLOUD_DIR = os.getenv("CLOUD_DIR")
APPS_DIR = os.getenv("APPS_DIR")
APPS_DATA_DIR = os.getenv("APPS_DATA_DIR")
VYPYR_DIR = os.getenv("VYPYR_DIR")
VYPYR_SRC_DIR = os.getenv("VYPYR_SRC_DIR")
SHYFT_DIR = os.getenv("SHYFT_DIR")
LOGS_DIR = os.getenv("LOGS_DIR")
SHYFT_DATA_PATH = Path(SHYFT_DIR, "data.json")
KEMIST_DIR = os.getenv("KEMIST_DIR")
KEMIST_IMG_DIR = Path(KEMIST_DIR, "images")

def clean_exit():
    # Function to cleanly exit without raising SystemExit
    print("\n" * 2)
    typyr(f"{PEACH}Exiting...")
    div()

try:
    import vypyr
    from vypyr.src import *
    from vypyr.src import contryvere
    from vypyr.src.kemist.main import main as mol
    from vypyr.src.medulla.main import *
    from vypyr.src.scholyr import main as start_scholyr
    print(PEACH)
    div()
    typyr(f"{BOLD}{PEACH}Vypyr{NORM}{PEACH} has been successfully initialized.{NORM} ✨{PEACH}")
    div()
    typyr(f"{TEAL}Should Vypyr load your {GOLDENROD}{BOLD}Contryvere{NORM}{TEAL} personas now?{PEACH}")
    try:
        response = click.prompt(f"Enter 'y' or 'n'", type=str, default="N").upper()
        if response == "Y":
            from contryvere.main import *
        elif response == "N":
            div()
    except click.exceptions.Abort:
        print("\n" * 2)
        click.echo(f"{GOLDENROD}{BOLD}Drats!{NORM}{TEAL}{BOLD} Something went wrong.")
        click.echo(f"{NORM}{PEACH}Here's what Python had to say about it: ")
        print()
        info = f"""
        {BG_BLACK}{LIGHT_RED}>>> Python received a keyboard input signal to end the
        startup process prematurely. Usually, this happens whenever a
        user enters some key combination (e.g., `^C` or `^X`) via the
        command line.
        """
    
        click.echo(info)
        logger.info('KeyboardInterrupt received, exiting gracefully.')
        clean_exit()
        sys.exit(0)

except ImportError as e:
    print("\n" * 2)
    click.echo(f"{GOLDENROD}{BOLD}Drats!{NORM}{TEAL}{BOLD} Something went wrong.")
    click.echo(f"{NORM}{PEACH}Here's what Python had to say about it: ")
    
    info = f"""
    {BG_BLACK}{LIGHT_RED}>>> Python could not locate one or more of the modules specified in
    the `startup.py` import statements. Consider reviewing your `PATH` and 
    `PYTHONPATH` environment variables. You can access their values by entering
    the following commands from the command line:

        ```
        echo $PATH
        ```
        > This command will print the contents of your `PATH` environment
          variable to the command line output.

        ```
        echo $PYTHONPATH
        ```
        > This command will print the contents of your `PYTHONPATH` environment
          variable to the command line output.
    """

    click.echo(info)
    logger.error(traceback.format_exc())
    sys.exit(1)
    
except Exception as e:
    print("\n" * 2)
    click.echo(f"{GOLDENROD}{BOLD}Drats!{NORM}{TEAL}{BOLD} Something went wrong.")
    click.echo(f"{NORM}{PEACH}Here's what Python had to say about it: ")
    
    info = f"""
    {BG_BLACK}{LIGHT_RED}>>> Python encountered an error while attempting to load 
    `startup.py`, but the resulting Exception is unspecified. See `stderr` 
    output for more detailed information.{NORM}
    """

    click.echo(info)
    logger.error(traceback.format_exc())
    sys.exit(1)
