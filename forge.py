#!/bin/python3

import os
import re
import sys
import argparse
import pathlib

# submodule library
import z_app_linker.linker as linker

# external library
import dotenv
import markdown


class SubScene:
    def __init__(self, scene_name: str, name: str):
        self.scene_name = scene_name
        self.name = escape_name(name)
        self.link_name = name_to_link(name)
        self.changes: list[str] = []
        self.actions: list[tuple[str, str | None]] = []
        # TODO

    def parse(self, lines: list[str]) -> "SubScene":
        # TODO
        return self

    def get_app(self) -> linker.Link:
        pass  # TODO


class Scene:
    def __init__(self, name: str):
        self.name = escape_name(name)
        self.subscenes: list[SubScene] = []

    def parse(self, lines: list[str]) -> "Scene":
        common_data = []
        scene_data = []
        scene_name = None
        for line in lines:
            line = line.replace("\n", "")
            if line.startswith("##"):
                if scene_name is not None:
                    self.subscenes += [
                        SubScene(self.name, scene_name).parse(common_data + scene_data)
                    ]
                scene_name = line[2:].strip()
                scene_data = []
            elif scene_name is None:
                common_data += [line]
            else:
                scene_data += [line]
        if scene_name is not None:
            self.subscenes += [
                SubScene(self.name, scene_name).parse(common_data + scene_data)
            ]
        return self

    def get_apps(self, **kwargs) -> list[linker.Link]:
        return [subscene.get_app(**kwargs) for subscene in self.subscenes]


def get_md_files(dir: str) -> list[str]:
    files = []
    dir = os.path.abspath(dir)
    try:
        for file in os.listdir(dir):
            path = os.path.join(dir, file)
            if os.path.isfile(path) and file.endswith(".md"):
                files += [path]
    except:
        print(f"ERROR: Cannot read directory '{dir}'", file=sys.stderr)
        sys.exit(1)
    if len(files) == 0:
        print(f"ERROR: No markdown files found in '{dir}'", file=sys.stderr)
        sys.exit(1)
    return sorted(files)


def read_scene_file(path: str) -> Scene:
    try:
        with open(path) as file:
            raw_content = file.readlines()
            return Scene(pathlib.Path(path).stem).parse(raw_content)
    except:
        print(f"ERROR: Cannot read '{path}'", file=sys.stderr)
        sys.exit(1)


def scenes_to_apps(scenes: list["Scene"], **kwargs) -> list[linker.Link]:
    apps = []
    for scene in scenes:
        apps += scene.get_apps(**kwargs)
    return apps


def escape_name(name: str) -> str:
    return re.sub(r"[^\w\.\-#]", "", name)


def name_to_link(name: str) -> str:
    return f"LINK_{name.upper()}_"


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

    apps = scenes_to_apps(scenes)

    linker.link_all_apps(apps)

    if args.preview:
        print(f"generating preview for {len(apps)} elements...")
        linker.Preview(apps).compute()

    if not args.dry:
        linker.resolve_all_apps(apps)


if __name__ == "__main__":
    dotenv.load_dotenv()
    __main()
