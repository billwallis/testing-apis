"""
Lint the coverage configuration file.
"""

import argparse
import glob
import pathlib
from collections.abc import Sequence

import tomlkit

SUCCESS = 0
FAILURE = 1
TARGET_DIR_GLOB = "projects/*/src"


def _get_source_paths(root_dir: pathlib.Path) -> list[str]:
    return sorted(
        [
            pathlib.Path(p).relative_to(root_dir).as_posix()
            for p in glob.glob(str(root_dir / TARGET_DIR_GLOB))
        ]
    )


def lint_coverage(root_dir: pathlib.Path, coverage_file: pathlib.Path) -> int:
    with open(coverage_file, encoding="utf-8") as f:
        content = tomlkit.load(f)

    source_array = content["run"]["source"].multiline(True)
    source_array.clear()
    source_array.add_line(*_get_source_paths(root_dir))

    with open(coverage_file, "w", newline="\n", encoding="utf-8") as f:
        tomlkit.dump(content, f)

    return SUCCESS


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the hook.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    parser.add_argument("--root-dir", required=True)
    args = parser.parse_args(argv)

    if not args.filenames:
        parser.print_help()
        return FAILURE

    outcome = SUCCESS
    root_dir = pathlib.Path(args.root_dir).resolve()
    for filename in args.filenames:
        outcome |= lint_coverage(root_dir, filename)

    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
