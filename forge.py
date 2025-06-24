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

MARKDOWN_EXTENSIONS = [
    "markdown.extensions.attr_list",
    "markdown.extensions.def_list",
    "markdown.extensions.tables",
    "pymdownx.b64",
    "pymdownx.betterem",
    "pymdownx.blocks.admonition",
    "pymdownx.blocks.definition",
    "pymdownx.blocks.details",
    "pymdownx.caret",
    "pymdownx.details",
    "pymdownx.emoji",
    "pymdownx.escapeall",
    "pymdownx.fancylists",
    "pymdownx.magiclink",
    "pymdownx.mark",
    "pymdownx.progressbar",
    "pymdownx.saneheaders",
    "pymdownx.smartsymbols",
    "pymdownx.tasklist",
    "pymdownx.tilde",
]


class Color:
    R = "\033[0m"
    B = "\033[1m"
    U = "\033[4m"
    I = "\033[3m"
    FAIL = "\033[31m"
    WARN = "\033[33m"
    INFO = "\033[32m"
    TEXT = "\033[37m"
    LINK = "\033[36m"

    FAIL_HEADER = f"{FAIL}{B}FAIL:{R}{FAIL}"
    WARN_HEADER = f"{WARN}{B}WARN:{R}{WARN}"
    INFO_HEADER = f"{INFO}{B}INFO:{R}{INFO}"

    @classmethod
    def colorize(cls, text: str) -> str:
        reset = cls.R
        if text.startswith("WARN:"):
            reset += cls.WARN
            text = cls.WARN_HEADER + text[5:] + cls.R
        elif text.startswith("FAIL:"):
            reset += cls.FAIL
            text = cls.FAIL_HEADER + text[5:] + cls.R
        elif text.startswith("INFO:"):
            reset += cls.INFO
            text = cls.INFO_HEADER + text[5:] + cls.R
        for match in re.findall(r"('[^']+')", text):
            text = text.replace(match, f"{cls.R}{cls.TEXT}{match[1:-1]}{reset}")
        for match in re.findall(r"(@[^@]+@)", text):
            text = text.replace(match, f"{cls.R}{cls.U}{cls.LINK}{match[1:-1]}{reset}")
        return text


def escape_name(name: str) -> str:
    return re.sub(r"[^\w\.\-#]", "", name.replace(" ", "_")).lower()


def random_str(size: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=size))


class SubScene:
    def __init__(self, path: str, scene_name: str, name: str):
        self.path = path
        self.scene_name = scene_name
        self.name = escape_name(name)
        self.raw_content = []
        self.changes: list[str] = []
        self.actions: list[tuple[str, str | None]] = []
        self.show: list[str] = []
        self.color: str | None = None
        self.has_error = False

    def __repr__(self):
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.scene_name}#{self.name}"

    def parse(self, lines: list[str]) -> "SubScene":
        action_raw = None
        for line in lines:
            if re.match(r"^/\w+", line):
                cmd, *args = line.split(" ")
                if cmd.lower() == "/set":
                    self.changes += [" ".join(args).replace(" = ", "=")]
                elif cmd.lower() == "/start" and len(args) == 1:
                    self.changes += [args[0] + "=1"]
                elif cmd.lower() == "/end" and len(args) == 1:
                    self.changes += [args[0] + "=2"]
                elif cmd.lower() == "/show":
                    self.show += [" ".join(args)]
                elif cmd.lower() == "/color":
                    color = " ".join(args)
                    if re.match(r"^\d+\.?\d*, *\d+\.?\d*%$", color):
                        self.color = color
                    else:
                        print(
                            Color.colorize(
                                f"WARN: invalid color '{line}' (must be hue, saturation like '180, 30%') at @{self}@"
                            ),
                            file=sys.stderr,
                        )
                else:
                    print(
                        Color.colorize(f"WARN: invalid command '{line}' at @{self}@"),
                        file=sys.stderr,
                    )
                    self.has_error = True
            elif line.startswith("*"):
                action_raw = line[2:]
            elif (
                action_raw is not None
                and (match := re.match(r"\* *\[\[([^\]]*)\]\]", line.strip()))
                is not None
            ):
                raw_subscene_name = escape_name(match.group(1))
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
                    print(
                        Color.colorize(
                            f"WARN: action '{action_raw}' has invalid link: '{line.strip().strip('*').strip()}' at @{self}@"
                        ),
                        file=sys.stderr,
                    )
                    action_raw = None
                    self.has_error = True
                self.raw_content += [line]
        if action_raw is not None:
            self.actions += [(action_raw, None)]
        return self

    def link_scenes(self, subscenes: dict[str, "SubScene"]) -> None:
        for i, action_data in enumerate(self.actions):
            action_raw, subscene_name = action_data
            if subscene_name is not None and subscene_name not in subscenes:
                for other_subscene_name in subscenes:
                    if other_subscene_name.startswith(
                        subscene_name + "#"
                        if "#" not in subscene_name
                        else subscene_name
                    ):
                        self.actions[i] = (action_raw, other_subscene_name)
                        break
                else:
                    print(
                        Color.colorize(
                            f"WARN: subscene not found '{subscene_name}' at @{self}@"
                        ),
                        file=sys.stderr,
                    )
                    self.has_error = True
                    self.actions[i] = (action_raw, None)

    def get_z_data(self, namespace: str) -> str:
        header = markdown.markdown(
            "\n".join(self.raw_content),
            extensions=MARKDOWN_EXTENSIONS,
            extension_configs={
                "pymdownx.b64": {"base_path": os.path.dirname(self.path)},
                "pymdownx.blocks.admonition": {
                    "types": [
                        "note",
                        "info",
                        "warn",
                        "warning",
                        "success",
                        "danger",
                        "error",
                    ]
                },
            },
        ).replace("\n", "")
        z_data = [header, namespace]
        if self.color is not None:
            z_data += [self.color]
        z_data += [
            str(len(self.show)),
            *self.show,
        ]
        rand_var = None
        percent_start = 0
        z_data_actions = []
        for action_raw, subscene_name in self.actions:
            full_condition = []
            button_title = action_raw
            with_invert = False
            for match in re.findall(r"[\[\{][^\]\}]+[\]\}]", action_raw):
                condition = match[1:-1]
                if condition.startswith("{"):
                    continue
                if re.match(r"^\d+\.?\d*%$", condition):
                    if rand_var is None:
                        rand_var = "rand_" + random_str(4).lower()
                    percent_value = float(condition[:-1])
                    if percent_start == 0:
                        full_condition += [f"({rand_var}<{percent_value})"]
                    else:
                        full_condition += [
                            f"({rand_var}>{percent_start}&&{rand_var}<{percent_start+percent_value})"
                        ]
                    percent_start += percent_value
                else:
                    full_condition += [f"({condition})"]
                if match.startswith("{"):
                    button_title = button_title.replace(match, "")
                else:
                    with_invert = True
            classes = []
            classes = ["button"]
            for match in re.findall(r"\#[\w-]+", button_title):
                classes += [match[1:]]
                button_title = button_title.replace(match, "")
            html_content_disabled = (
                f'<span class="button disabled">{button_title}</span>'
            )
            if subscene_name is None:
                html_content = html_content_disabled
            else:
                html_content = f'<a class="{" ".join(classes)}" href="{subscene_name}-{len(subscene_name)}">{button_title}</a>'
            if len(full_condition):
                z_data_actions += ["&&".join(full_condition), html_content]
            else:
                z_data_actions += ["true", html_content]
            if with_invert:
                z_data_actions += [
                    "!(" + "&&".join(full_condition) + ")",
                    html_content_disabled,
                ]
        if rand_var is not None:
            self.changes += [f"{rand_var}=Math.random()*100"]
        z_data += [str(len(self.changes)), *self.changes]
        z_data += z_data_actions
        return "\n".join(z_data)

    def get_app(self, **kwargs) -> linker.Link:
        return linker.Link(
            APP, f"{self.full_name}-{len(self.full_name)}", self.get_z_data(**kwargs)
        )


class Scene:
    def __init__(self, path: str):
        self.path = path
        self.name = escape_name(pathlib.Path(path).stem)
        self.subscenes: list[SubScene] = []

    def __repr__(self):
        return self.name

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
            if re.match(r"#{2}[^#]+", line):
                if subscene_name is not None:
                    self.subscenes += [
                        SubScene(self.path, self.name, subscene_name).parse(
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
                SubScene(self.path, self.name, subscene_name).parse(
                    scene_data + subscene_data
                )
            ]
        elif not len(self.subscenes) and len(scene_data):
            self.subscenes += [
                SubScene(self.path, self.name, "default").parse(scene_data)
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
        print(Color.colorize(f"FAIL: Cannot read directory @{dir}@"), file=sys.stderr)
        sys.exit(1)
    if len(files) == 0:
        print(
            Color.colorize(f"FAIL: No markdown files found in @{dir}@"), file=sys.stderr
        )
        sys.exit(1)
    return sorted(files)


def get_file_content(path: str, seen: list[str] = []) -> list[str] | None:
    if path in seen:
        return None
    try:
        with open(path) as file:
            raw_content = file.readlines()
            if len(raw_content) == 0:
                print(
                    Color.colorize(f"FAIL: Empty file at @{path}@"),
                    file=sys.stderr,
                )
                sys.exit(1)
            i = 0
            while i < len(raw_content):
                line = raw_content[i].replace("\n", "")
                if line.startswith("/include"):
                    _, *args = line.split(" ")
                    new_lines = []
                    for arg in args:
                        include_path = os.path.realpath(
                            os.path.join(os.path.dirname(path), arg)
                        )
                        new_content = get_file_content(include_path, seen + [path])
                        if new_content is None:
                            print(
                                Color.colorize(
                                    f"FAIL: Circular dependency '{line}' at @{path}@"
                                ),
                                file=sys.stderr,
                            )
                            return None
                        new_lines += new_content
                    raw_content = raw_content[:i] + new_lines + raw_content[i + 1 :]
                else:
                    i += 1
            return raw_content
    except OSError:
        print(Color.colorize(f"FAIL: Cannot read @{path}@"), file=sys.stderr)
        sys.exit(1)


def parse_scene_file(path: str) -> Scene:
    raw_content = get_file_content(path)
    if raw_content is None:
        print(Color.colorize(f"FAIL: Cannot read @{path}@"), file=sys.stderr)
        sys.exit(1)
    return Scene(path).parse(raw_content)


def link_scenes(scenes: list["Scene"]) -> None:
    subscenes: dict[str, SubScene] = dict()
    for scene in scenes:
        for subscene in scene.subscenes:
            subscenes[subscene.full_name] = subscene
    for scene in scenes:
        for subscene in scene.subscenes:
            subscene.link_scenes(subscenes)
    print(Color.colorize(f"INFO: linked {len(subscenes)} subscenes"))


def count_errors(scenes: list["Scene"]) -> int:
    return sum(
        sum(subscene.has_error for subscene in scene.subscenes) for scene in scenes
    )


def scenes_to_apps(scenes: list["Scene"], **kwargs) -> list[linker.Link]:
    apps = []
    for scene in scenes:
        apps += scene.get_apps(**kwargs)
    return apps


def make_linker_output(apps: list[linker.Link], dir_path: str) -> None:
    path = os.path.abspath(dir_path + ".txt")
    separator = linker.APPS[APP][0] * 5
    with open(path, mode="w") as file:
        for app in apps:
            file.write(separator + " " + app.link_name + "\n" + app.data + "\n")
    print(Color.colorize(f"INFO: generated z-app linker file at @{path}@"))


def add_links_to_apps(apps: list[linker.Link], dir_path: str) -> None:
    name = os.path.abspath(dir_path + ".csv")
    apps_dict = {app.link_name: app for app in apps}
    if os.path.exists(name):
        found = 0
        with open(name) as file:
            file.readline()  # ignore headers
            for line in file:
                link_name, link = line.strip().split(",")[:2]
                if link_name in apps_dict:
                    apps_dict[link_name].link = link
                    found += 1
        print(Color.colorize(f"INFO: found {found} matching links in @{name}@"))
    else:
        print(Color.colorize(f"WARN: no links file found at @{name}@"))


def save_apps_links(apps: list[linker.Link], dir_path: str) -> None:
    name = os.path.abspath(dir_path + ".csv")
    with open(name, mode="w") as file:
        file.write("link_name,link\n")
        for app in apps:
            file.write(f"{app.link_name},{app.link}\n")
    print(Color.colorize(f"INFO: generated links file @{name}@"))


def __main():
    parser = argparse.ArgumentParser(
        description="creates a z-hero-quest adventure from markdown data (see sample directory or DOC.md)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Markdown syntax uses extensions defined in https://python-markdown.github.io/extensions/ and https://facelessuser.github.io/pymdown-extensions/ \nActive extensions:\n* "
        + "\n* ".join(MARKDOWN_EXTENSIONS),
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
    parser.add_argument(
        "--force",
        action="store_true",
        help="force computation even with errors",
        default=False,
    )
    args = parser.parse_args()

    files = get_md_files(args.dir_path)

    scenes = [parse_scene_file(path) for path in files]

    print(Color.colorize(f"INFO: parsed {len(scenes)} scenes"))

    link_scenes(scenes)

    errors = count_errors(scenes)

    if errors > 0:
        print(Color.colorize(f"WARN: {errors} errors found"), file=sys.stderr)
        if not args.force:
            print(Color.colorize(f"WARN: (pass --force to continue)"), file=sys.stderr)
            sys.exit(1)

    namespace = args.namespace if args.namespace is not None else random_str(10)

    apps = scenes_to_apps(scenes, namespace=namespace)

    linker.link_all_apps(apps)

    make_linker_output(apps, args.dir_path)

    if args.preview:
        print(Color.colorize(f"INFO: generating preview for {len(apps)} elements..."))
        linker.Preview(apps).compute()

    if not args.dry:
        add_links_to_apps(apps, args.dir_path)

        linker.resolve_all_apps(apps, quiet=True)

        save_apps_links(apps, args.dir_path)


if __name__ == "__main__":
    dotenv.load_dotenv()
    __main()
