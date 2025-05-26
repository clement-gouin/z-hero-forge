#!/bin/python3

import os
import re
import sys
import argparse

# submodule library
import z_app_linker.linker as linker

# external library
import dotenv


class SubScene:
    def __init__(self):
        # TODO
        pass

    def get_app(self) -> linker.Link:
        pass  # TODO


class Scene:
    def __init__(self):
        # TODO
        pass

    @classmethod
    def from_raw_content(cls, lines: list[str]) -> "Scene":
        # TODO
        return Scene()

    def get_apps(self) -> linker.Link:
        pass  # TODO

    @classmethod
    def convert_to_apps(cls, scenes: list["Scene"]) -> list[linker.Link]:
        apps = []
        for scene in scenes:
            apps += scene.get_apps()
        return apps


def get_md_files(dir: str) -> list[str]:
    files = []
    dir = os.path.abspath(dir)
    try:
        for file in os.listdir(dir):
            path = os.path.join(dir, file)
            if os.path.isfile(path) and file.endswith(".md"):
                files += [path]
    except:
        print(f"Cannot read directory '{dir}'", file=sys.stderr)
        sys.exit(1)
    if len(files) == 0:
        print(f"No markdown files found in '{dir}'", file=sys.stderr)
        sys.exit(1)
    return sorted(files)


def read_scene_file(path: str) -> Scene:
    try:
        with open(path) as file:
            raw_content = file.readlines()
            return Scene.from_raw_content(raw_content)
    except:
        print(f"Cannot read '{path}'", file=sys.stderr)
        sys.exit(1)


def __main():
    parser = argparse.ArgumentParser(
        description="creates a z-hero-quest adventure from markdown data (see sample directory)"
    )
    parser.add_argument(
        "dir_path", help="data file path (default: data.txt)", metavar="DIR"
    )
    parser.add_argument(
        "-n",
        "--namespace",
        help="hero quest namespace (default: random)",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-c",
        "--color",
        help="hero quest color as: Hue (number), Saturation (percent)  (default: 180, 30%%)",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-s",
        "--start",
        help='start scene (default: "start.md" or first file by name)',
        required=False,
        default=None,
    )
    parser.add_argument(
        "-p",
        "--preview",
        action="store_true",
        help="show links tree in a preview.png file",
        default=False,
    )
    parser.add_argument(
        "-d",
        "--dry",
        action="store_true",
        help="do not compute links",
        default=False,
    )
    args = parser.parse_args()

    files = get_md_files(args.dir_path)

    scenes = [read_scene_file(path) for path in files]

    apps = Scene.convert_to_apps(scenes)

    linker.link_all_apps(apps)

    if args.preview:
        print(f"generating preview for {len(apps)} elements...")
        linker.Preview(apps).compute()

    if not args.dry:
        linker.resolve_all_apps(apps)


if __name__ == "__main__":
    dotenv.load_dotenv()
    __main()
