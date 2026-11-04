"""Shared file operations for the project-state command entrypoints."""

import argparse
from datetime import date
import json
from pathlib import Path
import re
from string import Template
import sys
import tempfile

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML is required. Install it in your Python environment: python3 -m pip install PyYAML")


PACKAGE = Path(__file__).resolve().parents[1]
DOCUMENTS = ("README.md", "status.md", "context.md", "milestones.md", "changelog.md", "progress.md")
MODES = ("collaborative", "privacy")
STYLES = ("conventional", "phase")
IGNORE = ".checkpoint-karpathy/private/"


class StateError(Exception):
    pass


class ConfigLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently accepting the last value."""


def config_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise StateError("Configuration keys must be unique strings.")
        result[key] = loader.construct_object(value_node)
    return result


ConfigLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, config_mapping)


def local_path(project, path):
    """Do not follow state symlinks when creating or moving project files."""
    for part in (path, *path.parents):
        if part == project:
            break
        if part.is_symlink():
            raise StateError(f"State path is a symlink; resolve it before proceeding: {part}")
    return path


def state_paths(project):
    base = local_path(project, project / ".checkpoint-karpathy")
    return {"collaborative": base, "privacy": local_path(project, base / "private")}


def read_config(project):
    paths = state_paths(project)
    found = [local_path(project, folder / "config.yaml") for folder in paths.values()
             if (folder / "config.yaml").exists() or (folder / "config.yaml").is_symlink()]
    if len(found) > 1:
        raise StateError("Both configuration locations exist; resolve the active configuration with the user.")
    if not found:
        return None, None
    path = found[0]
    config = yaml.load(path.read_text(encoding="utf-8"), Loader=ConfigLoader)
    if not isinstance(config, dict) or set(config) != {"mode", "commit_message_style"}:
        raise StateError(f"Expected mode and commit_message_style in {path}; reconcile configuration before proceeding.")
    if config["mode"] not in MODES or config["commit_message_style"] not in STYLES:
        raise StateError(f"Invalid configuration values in {path}.")
    if path.parent != paths[config["mode"]]:
        raise StateError(f"Configuration mode and location disagree: {path}. Complete the requested mode change first.")
    return path, config


def config_text(mode, style, language):
    template = (PACKAGE / "assets/config" / f"{language}.yaml").read_text(encoding="utf-8")
    return Template(template).substitute(mode=mode, commit_message_style=style)


def ensure_ignore(project):
    path = local_path(project, project / ".gitignore")
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if IGNORE not in text.splitlines():
        with path.open("a", encoding="utf-8") as stream:
            stream.write(("\n" if text and not text.endswith("\n") else "") + IGNORE + "\n")


def prepare(project, documents):
    staging = local_path(project, project / ".checkpoint-karpathy/private/work/staging")
    staging.mkdir(parents=True, exist_ok=True)
    prepared = Path(tempfile.mkdtemp(prefix="goal-", dir=staging))
    try:
        for name, content in documents.items():
            (prepared / name).write_text(content, encoding="utf-8")
    except (OSError, KeyboardInterrupt) as error:
        raise StateError(f"Preparation failed ({error}); inspect staging {prepared}. No goal files activated.") from error
    return prepared


def move(source, destination):
    if destination.exists() or destination.is_symlink():
        raise StateError(f"Refusing to overwrite: {destination}")
    source.rename(destination)


def initialize(project, mode, style=None, language="en"):
    config_path, config = read_config(project)
    if config and (config["mode"] != mode or (style and config["commit_message_style"] != style)):
        raise StateError("Initialization preserves existing configuration. Apply user-requested settings changes separately.")
    paths = state_paths(project)
    state = paths[mode]
    roadmap = local_path(project, state / "roadmap")
    other = local_path(project, paths[MODES[1 - MODES.index(mode)]] / "roadmap")
    if other.exists() and any(other.iterdir()):
        raise StateError(f"Planning content exists outside the selected mode: {other}. Reconcile it first.")
    existing = list(roadmap.iterdir()) if roadmap.exists() else []
    if existing and not all(local_path(project, roadmap / name).is_file() for name in DOCUMENTS):
        raise StateError(f"Partial goal documents in {roadmap}; recover them from evidence before initialization.")
    # Validate the ignore file before creating state.
    local_path(project, project / ".gitignore")
    new_config = config_text(mode, style or "conventional", language) if config_path is None else None
    roadmap.mkdir(parents=True, exist_ok=True)
    local_path(project, project / ".checkpoint-karpathy/private/work").mkdir(parents=True, exist_ok=True)
    ensure_ignore(project)
    if config_path is None:
        config_path = state / "config.yaml"
        with config_path.open("x", encoding="utf-8") as stream:
            stream.write(new_config)
    return roadmap


def create(project, payload, check_only=False):
    from goal_documents import render_goal

    config_path, config = read_config(project)
    if config is None:
        raise StateError("No config.yaml found. Run init_project.py first.")
    # Render and validate the complete set before changing any project files.
    documents = render_goal(payload, config["commit_message_style"], PACKAGE)
    roadmap = local_path(project, config_path.parent / "roadmap")
    other_mode = MODES[1 - MODES.index(config["mode"])]
    other = local_path(project, state_paths(project)[other_mode] / "roadmap")
    if other.exists() and any(other.iterdir()):
        raise StateError(f"Planning content exists outside the selected mode: {other}. Reconcile it first.")
    if check_only:
        return roadmap
    if not roadmap.is_dir():
        raise StateError("Fixed roadmap directory is missing. Run init_project.py first.")
    if any(roadmap.iterdir()):
        raise StateError(f"Refusing to overwrite nonempty roadmap: {roadmap}. Resume, recover, or archive the existing goal first.")
    local_path(project, project / ".gitignore")
    ensure_ignore(project)
    prepared = prepare(project, documents)
    activated = []
    try:
        for name in DOCUMENTS:
            move(prepared / name, roadmap / name)
            activated.append(name)
    except (OSError, StateError, KeyboardInterrupt) as error:
        try:
            for name in reversed(activated):
                move(roadmap / name, prepared / name)
        except (OSError, StateError, KeyboardInterrupt) as recovery_error:
            raise StateError(f"Creation failed ({error}); recovery also failed ({recovery_error}). Inspect roadmap {roadmap} and staging {prepared}. No further operations attempted.") from error
        raise StateError(f"Creation failed ({error}); newly activated files restored to staging {prepared}. Roadmap: {roadmap}.") from error
    prepared.rmdir()
    return roadmap


def completion(roadmap):
    text = (roadmap / "status.md").read_text(encoding="utf-8")
    sections = re.findall(r"^## Completion[ \t]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if len(sections) != 1:
        raise StateError("Cannot identify one Completion section in status.md. Agent must reconcile status before archiving.")
    lines = [line.strip() for line in sections[0].splitlines() if line.strip()]
    if not lines or lines[0] not in ("completed", "cancelled"):
        raise StateError("Archive requires Completion to be completed or cancelled. Agent must verify and reconcile status first.")


def suffix(number):
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(97 + remainder) + result
    return result


def archive(project, title):
    if not re.fullmatch(r"[^\W_]+(?:-[^\W_]+)*", title, re.UNICODE):
        raise StateError("Title must contain letters/numbers separated by hyphens, e.g. linked-market-information.")
    config_path, config = read_config(project)
    if config is None:
        raise StateError("No config.yaml found. Initialize or recover project configuration first.")
    state = config_path.parent
    roadmap = local_path(project, state / "roadmap")
    for name in DOCUMENTS:
        if not local_path(project, roadmap / name).is_file():
            raise StateError(f"Missing {name}; recover partial goal state before archiving.")
    completion(roadmap)
    archive_root = local_path(project, state / "archive")
    local_path(project, project / ".gitignore")
    ensure_ignore(project)
    archive_root.mkdir(parents=True, exist_ok=True)
    index = 1
    while True:
        prefix = f"{date.today():%Y%m%d}{suffix(index)}-"
        if any(item.name.startswith(prefix) for item in archive_root.iterdir()):
            index += 1
            continue
        destination = archive_root / (prefix + title)
        try:
            destination.mkdir()
            break
        except FileExistsError:
            index += 1
    archived = []
    try:
        for item in list(roadmap.iterdir()):
            move(item, destination / item.name)
            archived.append(item.name)
    except (OSError, StateError, KeyboardInterrupt) as error:
        try:
            for name in reversed(archived):
                move(destination / name, roadmap / name)
            destination.rmdir()
        except (OSError, StateError, KeyboardInterrupt) as recovery_error:
            raise StateError(f"Archive failed ({error}); recovery also failed ({recovery_error}). Inspect roadmap {roadmap} and archive {destination}. No further operations attempted.") from error
        raise StateError(f"Archive failed ({error}); original goal restored in {roadmap}.") from error
    return destination, roadmap


def main(command):
    descriptions = {
        "init": "Initialize project configuration and fixed directories.",
        "create": "Render six roadmap documents from structured JSON on stdin, using config.yaml.",
        "archive": "Archive a terminal goal, leaving the fixed roadmap directory empty.",
    }
    parser = argparse.ArgumentParser(description=descriptions[command])
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project root (default: current directory).")
    if command == "init":
        parser.add_argument("--mode", choices=MODES, required=True)
        parser.add_argument("--commit-message-style", choices=STYLES)
        parser.add_argument("--language", choices=("en", "zh"), default="en", help="New configuration comment language (default: en).")
    elif command == "create":
        parser.add_argument("--check-only", action="store_true", help="Validate JSON and render templates without writing, including while an old goal exists.")
    else:
        parser.add_argument("--title", required=True, help="Short hyphenated title describing the old goal.")
    args = parser.parse_args()
    project = args.project.expanduser().resolve()
    if not project.is_dir():
        parser.error(f"Project directory does not exist: {project}")
    try:
        if command == "init":
            print(f"Initialized directories and configuration. Roadmap: {initialize(project, args.mode, args.commit_message_style, args.language)}")
        elif command == "create":
            from goal_documents import unique_object

            payload = json.load(sys.stdin, object_pairs_hook=unique_object)
            roadmap = create(project, payload, args.check_only)
            print("Goal input and templates validated; no files written." if args.check_only else f"Created roadmap: {roadmap}")
        else:
            destination, roadmap = archive(project, args.title)
            print(f"Archived goal: {destination}\nEmpty roadmap: {roadmap}")
    except (StateError, OSError, yaml.YAMLError, KeyError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0
