#!/bin/python3

import os
import re
import sys
import argparse
import pathlib
import random
import string

# submodule library
import z_app_linker.linker as linker

# external library
import dotenv
import markdown

APP = "https://clement-gouin.github.io/z-hero-quest"


def escape_name(name: str) -> str:
    return re.sub(r"[^\w\.\-#]", "", name)


def name_to_link(name: str) -> str:
    return f"LINK_{name.upper()}_"


def random_str(size: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=size))


class SubScene:
    def __init__(self, scene_name: str, name: str):
        self.scene_name = scene_name
        self.name = escape_name(name)
        self.link_name = name_to_link(name)
        self.raw_content = []
        self.changes: list[str] = []
        self.actions: list[tuple[str, str | None]] = []

    @property
    def full_name(self) -> str:
        return f"{self.scene_name}#{self.name}"

    def parse(self, lines: list[str]) -> "SubScene":
        action_raw = None
        for line in lines:
            if line.startswith("/"):
                cmd, *args = line.split(" ")
                if cmd.lower() == "/set":
                    self.changes += [" ".join(args)]
                elif cmd.lower() == "/start" and len(args) == 1:
                    self.changes += [args[0] + " = 1"]
                elif cmd.lower() == "/end" and len(args) == 1:
                    self.changes += [args[0] + " = 2"]
                else:
                    print(f"WARN: invalid command '{line}'", file=sys.stderr)
                # TODO /show
            elif line.startswith("*"):
                action_raw = line[2:]
            elif (
                action_raw is not None
                and (match := re.match(r"\* \[\[([\w\-\#\.]*)\]\]", line.strip()))
                is not None
            ):
                raw_subscene_name = match.group(1)
                if raw_subscene_name == "":
                    self.actions += [(action_raw, self.full_name)]
                elif raw_subscene_name == "#":
                    self.actions += [(action_raw, f"{self.scene_name}")]
                elif raw_subscene_name.startswith("#"):
                    self.actions += [
                        (action_raw, f"{self.scene_name}{raw_subscene_name}")
                    ]
                else:
                    self.actions += [(action_raw, raw_subscene_name)]
                action_raw = None
            else:
                if action_raw is not None:
                    self.actions += [(action_raw, None)]
                    action_raw = None
                self.raw_content += [line]
        if action_raw is not None:
            self.actions += [(action_raw, None)]
        return self

    def link_scenes(self, subscene_names: list[str]) -> None:
        for i, action_data in enumerate(self.actions):
            action_raw, subscene_name = action_data
            if subscene_name is not None and subscene_name not in subscene_names:
                for other_subscene_name in subscene_names:
                    if other_subscene_name.startswith(subscene_name):
                        self.actions[i] = (action_raw, other_subscene_name)
                        break
                else:
                    print(
                        f"WARN: ({self.full_name}) subscene not found '{subscene_name}'"
                    )
                    self.actions[i] = (action_raw, None)

    def get_z_data(self, namespace: str, color: str | None = None) -> str:
        return ""  # TODO

    def get_app(self, **kwargs) -> linker.Link:
        return linker.Link(APP, name_to_link(self.name), self.get_z_data(**kwargs))


class Scene:
    def __init__(self, name: str):
        self.name = escape_name(name)
        self.subscenes: list[SubScene] = []

    def parse(self, lines: list[str]) -> "Scene":
        scene_data = []
        subscene_data = []
        subscene_name = None
        for line in lines:
            line = line.replace("\n", "")
            line_escaped = re.sub("<!--.*-->", "", line)
            if len(line) and not len(line_escaped.strip()):
                continue
            line = line_escaped
            if line.startswith("##"):
                if subscene_name is not None:
                    self.subscenes += [
                        SubScene(self.name, subscene_name).parse(
                            scene_data + subscene_data
                        )
                    ]
                subscene_name = line[2:].strip()
                subscene_data = []
            elif subscene_name is None:
                scene_data += [line]
            else:
                subscene_data += [line]
        if subscene_name is not None:
            self.subscenes += [
                SubScene(self.name, subscene_name).parse(scene_data + subscene_data)
            ]
        return self

    def get_all_subscene_names(self) -> list[str]:
        return [subscene.full_name for subscene in self.subscenes]

    def link_scenes(self, subscene_names: list[str]) -> None:
        for subscene in self.subscenes:
            subscene.link_scenes(subscene_names)

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
            if len(raw_content) == 0:
                print(f"ERROR: Empty scene file '{path}'", file=sys.stderr)
                sys.exit(1)
            return Scene(pathlib.Path(path).stem).parse(raw_content)
    except OSError:
        print(f"ERROR: Cannot read '{path}'", file=sys.stderr)
        sys.exit(1)


def link_scenes(scenes: list["Scene"]) -> None:
    subscene_names = []
    for scene in scenes:
        subscene_names += scene.get_all_subscene_names()
    print(subscene_names)
    for scene in scenes:
        scene.link_scenes(subscene_names)


def scenes_to_apps(scenes: list["Scene"], **kwargs) -> list[linker.Link]:
    apps = []
    for scene in scenes:
        apps += scene.get_apps(**kwargs)
    return apps


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

    link_scenes(scenes)

    namespace = args.namespace if args.namespace is not None else random_str(10)

    apps = scenes_to_apps(scenes, namespace=namespace, color=args.color)

    linker.link_all_apps(apps)

    if args.preview:
        print(f"generating preview for {len(apps)} elements...")
        linker.Preview(apps).compute()

    if not args.dry:
        linker.resolve_all_apps(apps)


if __name__ == "__main__":
    dotenv.load_dotenv()
    __main()
