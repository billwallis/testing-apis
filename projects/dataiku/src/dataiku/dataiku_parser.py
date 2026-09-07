"""
Simple CLI for the Dataiku API client.

- https://developer.dataiku.com/latest/tutorials/devtools/python-client/index.html


Debug connection:

    python dataiku_parser.py debug

List datasets:

    python dataiku_parser.py datasets --project '<project name>'

List recipes:

    python dataiku_parser.py recipes --project '<project name>'

Print recipe SQL:

    python dataiku_parser.py recipe \
        --project '<project name>' \
        --recipe '<recipe name>'


Pipe to SQLFluff:

    pip install sqlfluff

    python dataiku_parser.py recipe \
        --project '<project name>' \
        --recipe '<recipe name>' \
        -- | sqlfluff format --dialect snowflake -
"""

# Download with:
#
#     curl https://dssdesign.{org-name}.org/public/packages/dataiku-internal-client.tar.gz --output deps/dataiku-internal-client.tar.gz
#
# Then install with:
#
#     pip install deps/dataiku-internal-client.tar.gz
#     pip install pandas==2.2.2
#     pip install dataiku-api-client

from __future__ import annotations

import argparse
import functools
import json
import os
import pathlib
import textwrap
import warnings
from collections.abc import Sequence
from typing import Literal, overload

from dataikuapi import DSSClient
from dataikuapi.dss.dataset import DSSDatasetListItem
from dataikuapi.dss.project import DSSProject
from dataikuapi.dss.recipe import DSSRecipe, DSSRecipeListItem

import dataiku

SUCCESS = 0
FAILURE = 1
HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"


def _ensure_env(environment_variable_name: str) -> None:
    if not os.getenv(environment_variable_name):
        raise OSError(
            f"Environment variable '{environment_variable_name}' is required"
        )


@functools.cache  # lazy singleton
def _get_client() -> DSSClient:
    _ensure_env("DKU_DSS_URL")
    _ensure_env("DKU_API_KEY")

    return dataiku.api_client()


def get_project(project_key: str) -> DSSProject:
    return _get_client().get_project(project_key.upper())


def _list_or_export_entities(
    entity_type: Literal["recipe", "dataset"], args: argparse.Namespace
) -> int:
    entities = getattr(get_project(args.project), f"list_{entity_type}s")()
    expected_type = {
        "recipe": DSSRecipeListItem,
        "dataset": DSSDatasetListItem,
    }[entity_type]
    if not all(isinstance(entity, expected_type) for entity in entities):
        warnings.warn(
            f"Found at least one {entity_type} not of type {expected_type}",
            stacklevel=2,
        )

    if args.action == "list":
        print(json.dumps(entities, indent=2))

    if args.action == "export":
        target = DATA / f"{args.project}-{entity_type}s.json"
        with open(target, "w+") as f:
            json.dump(entities, f, indent=2)
        print(f"{entity_type.capitalize()}s exported to {str(target)!r}")

    return SUCCESS


def _datasets(args: argparse.Namespace) -> int:
    return _list_or_export_entities("dataset", args)


def _recipes(args: argparse.Namespace) -> int:
    return _list_or_export_entities("recipe", args)


def _get_recipe_definition(
    recipe: DSSRecipe,
) -> tuple[Literal["sql", "json"], str | dict]:
    recipe_data = recipe.get_status().data
    if sql := recipe_data.get("sql"):
        return "sql", sql
    else:
        return "json", recipe_data


def _print_recipe(recipe: DSSRecipe) -> None:
    type_, data = _get_recipe_definition(recipe)
    if type_ == "sql":
        print(data)
    elif type_ == "json":
        print(textwrap.indent(json.dumps(data, indent=2), "\t"))


def _recipe(args: argparse.Namespace) -> int:
    _print_recipe(get_project(args.project).get_recipe(args.recipe))

    return SUCCESS


@overload
def get_recipe_definition(
    project_key: str, recipe_name: str
) -> tuple[Literal["sql"], str]: ...
@overload
def get_recipe_definition(
    project_key: str, recipe_name: str
) -> tuple[Literal["json"], dict]: ...
def get_recipe_definition(project_key, recipe_name):
    return _get_recipe_definition(
        recipe=get_project(project_key).get_recipe(recipe_name)
    )


def main(argv: Sequence[str] | None = None) -> int:
    """
    Convert a Dataiku recipe into SQL.
    """

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("debug")

    parser__datasets = subparsers.add_parser("datasets")
    parser__datasets.add_argument("--project")
    parser__datasets.add_argument(
        "action",
        choices=("list", "export"),
    )

    parser__recipes = subparsers.add_parser("recipes")
    parser__recipes.add_argument("--project")
    parser__recipes.add_argument(
        "action",
        choices=("list", "export"),
    )

    parser__recipe = subparsers.add_parser("recipe")
    parser__recipe.add_argument("--project")
    parser__recipe.add_argument("--recipe")

    args = parser.parse_args(argv)
    # print(args)
    if args.command == "debug":
        auth_info = _get_client().get_auth_info()
        print(json.dumps(auth_info, indent=2))
        return not bool(auth_info)
    if args.command == "datasets":
        return _datasets(args)
    if args.command == "recipes":
        return _recipes(args)
    if args.command == "recipe":
        return _recipe(args)

    parser.print_help()
    return SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
