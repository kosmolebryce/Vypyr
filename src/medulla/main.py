# main.py

import json
import os
import shutil
import sys
from pathlib import Path as p
from time import sleep as wait


# ENVIRONMENT VARIABLES
HOME = os.environ.get("HOME")
if HOME is None:
    HOME = p.home()
else:
    pass

PATH = sys.path
USER = os.environ.get("USER")
PYTHONHOME = os.environ.get("PYTHONHOME")
PYTHONPATH = os.environ.get("PYTHONPATH")


# ANSI color escape sequences
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
LIGHT_GRAY = "\033[38;5;7m"
LIGHT_RED = "\033[38;5;9m"
LIGHT_GREEN = "\033[38;5;10m"
LIGHT_YELLOW = "\033[38;5;11m"
LIGHT_BLUE =  "\033[38;5;12m"
LIGHT_MAGENTA = "\033[38;5;13m"
LIGHT_CYAN = "\033[38;5;14m"
NORM = "\033[0m"
ORANGE = "\033[38;5;208m"  # 208 is the index for orange in 256-color mode"
PEACH = "\033[38;5;222m"
TEAL = "\033[38;5;37m"
GOLDENROD = "\033[38;5;220m"

# ANSI background color escape sequences
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"


# ANSI style escape sequences
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
REVERSED = "\033[7m"


# DYNAMIC EVALUATIONS
def get_width():
    terminal_size = shutil.get_terminal_size()
    return terminal_size.columns


# GLOBAL CONTROLLERS
s = 0.001  # Printing speed
width = get_width()


# TOOLKIT


# `div`
# - a simple divider
#   * accepts a single argument, `l`, short for "length", which must be a
#     a positive integer. `l` represents the length in columns
def div(l=width):
    symbol = "═"
    print()
    typyr(symbol * l)
    print()

# `typyr`
# - a cuter way to print to stdout
#   * accepts only `str` as an argument
def typyr(text):
    global s
    for char in text:
        print(char, end="", flush=True)
        wait(s)
    print()


# `pwd`
# - returns current working directory as `str`
def pwd():
    return os.getcwd()


# `dir` and `ls`
# - These are equivalent; both return the contents of the current working
#   directory.
def dir():
    files = os.listdir()
    for item in files:
        print(f"{item}\n", end="", flush=True)
        wait(0.001)


def ls():
    dir()


# `home`
# - navigate to user's home directory
#   * assumes that user's home directory is set by system's `HOME`
#     shell environment variable
def home():
    os.chdir(f"{HOME}")
    div()
    fp = pwd()
    typyr("Your current working directory is now:")
    typyr(fp)
    div()


def cd(path):
    os.chdir(path)
    

def mkdir(path):
    os.mkdir(path)
    wait(0.5)
    typyr("Success.")
    div()
    fp = pwd()
    typyr("Your current working directory is now:")
    typyr(fp)

    div()


def rmdir(path):
    typyr("\nRemoving directory...")
    os.rmdir(path)
    wait(0.5)
    typyr("Success.")
    div()


def touch(path):
    div()
    typyr("\nCreating file...")
    with open(path, "w") as f:
        f.write("")
    wait(0.5)
    typyr("Done.")
    div()


def rm(path):
    div()
    typyr("\nRemoving file...")
    os.remove(path)
    typyr("Done.")
    div()
    fp = pwd()
    typyr("Your current working directory is now:")
    typyr(fp)
    div()


def mv(path):
    typyr("\nRemoving file...")
    os.rename(path)
    typyr("Done.")
    div()
    fp = pwd()
    typyr("Your current working directory is now:")
    typyr(fp)
    div()


def cp(path):
    div()
    typyr(f"\nCopying file to <{path}>...")
    os.copy(path)
    typyr("Done.")
    div()


def cat(path):
    typyr("\nBOF\n")
    with open(path, "r") as f:
        typyr(f.read())
    typyr("\nEOF\n")
    wait(0.5)
    typyr("Done.")
    wait(0.5)
    div()
    fp = pwd()
    typyr("Your current working directory is now:")
    typyr(fp)
    print()


def clear():
    os.system("clear")


def exit():
    typyr("\nExiting...")
    wait(0.5)
    typyr("Done.")
    wait(0.5)
    div()
    fp = pwd()
    typyr("Your current working directory is now:")
    typyr(fp)
    print()


def pen(text, path):
    typyr(f"\nPrinting to <{path}>...")
    with open(path, "w") as f:
        f.write(text)
    wait(0.5)
    typyr("Done.")


def apen(text, path):
    typyr(f"\nAppending to <{path}>...")
    with open(path, "a") as f:
        f.write(text)
    wait(0.5)
    typyr("Done.")


def jsonic(path):
    jd = {}
    with open(path, "r") as f:
        jd = json.load(f)
        return jd


def jsoner(path):
    jd = {}
    while True:
        typyr("\nEnter a key: ")
        key = input()
        typyr("\nEnter a value: ")
        value = input()
        jd.update({key: value})
        typyr("\nEnter another key?")
        typyr("\n[Y]es/[N]o")
        ans = input()
        if ans.lower() == "y":
            pass
        else:
            break
    typyr("\nSaving JSON object to <{path}>...")
    with open(path, "w") as f:
        json.dump(jd, f, indent=4)
    wait(0.5)
    typyr("Done.")


def o(file):
    with open(file, "r+") as f:
        data = f.read()
    return data


def up():
    return cd("..")


def help():
    typyr("\nHelp:")
    typyr("  - `div`")
    typyr("    * a simple divider")
    typyr("  - `typyr`")
    typyr("    * a cuter way to print to stdout")
    typyr("  - `pwd`")
    typyr("    * returns current working directory as `str`")
    typyr("  - `dir` and `ls`")
    typyr("    * These are equivalent; both return the contents of the current working")
    typyr("      directory.")
    typyr("  - `home`")
    typyr("    * navigate to user's home directory")
    typyr("      * assumes that user's home directory is set by system's `HOME`")
    typyr("        shell environment variable")
    typyr("  - `cd`")
    typyr("    * navigate to a specific directory")
    typyr("  - `mkdir`")
    typyr("    * create a directory")
    typyr("  - `rmdir`")
    typyr("    * remove a directory")

    typyr("  - `touch`")
    typyr("    * create a file")
    typyr("  - `rm`")
    typyr("    * remove a file")
    typyr("  - `mv`")
    typyr("    * move a file")
    typyr("  - `cp`")
    typyr("    * copy a file")
    typyr("  - `cat`")
    typyr("    * print a file")
    typyr("  - `clear`")
    typyr("    * clear the screen")
    typyr("  - `exit`")
    typyr("    * exit the program")
    typyr("  - `help`")
    typyr("    * print this help menu")
    print()


def main():
    pass


if __name__ == "__main__":
    main()
