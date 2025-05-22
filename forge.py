#!/bin/python3

import os
import re
import sys
import argparse

# submodule library
import z_app_linker.linker as linker

# external library
import dotenv


def __main():
    parser = argparse.ArgumentParser(
        description="creates a z-hero-quest adventure from markdown data (see sample directory)"
    )
    parser.add_argument(
        "-p",
        "--preview",
        action="store_true",
        help="show links tree in a preview.png file",
        default=False,
    )
    parser.add_argument(
        "-n",
        "--namespace",
        help="hero quest namespace (default: random)",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--dry",
        action="store_true",
        help="do not compute links",
        default=False,
    )
    parser.add_argument(
        "dir_path", help="data file path (default: data.txt)", metavar="DIR"
    )
    args = parser.parse_args()
    # TODO


if __name__ == "__main__":
    dotenv.load_dotenv()
    __main()
