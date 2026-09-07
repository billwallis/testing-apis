from __future__ import annotations

import dataclasses
import functools
import json
import pathlib
from typing import Literal

import dataiku_parser
import sqlfluff
import sqlglot.optimizer


@dataclasses.dataclass
class Entity:
    project_key: str
    name: str
    identifier: str
    entity_type: Literal["dataset", "recipe"]
    type: Literal[
        "UploadedFiles",
        "CustomPython_googlesheets-sheet",
        "Snowflake",
    ]
    sql: str = dataclasses.field(init=False, repr=False)
    data: dict = dataclasses.field(init=False, repr=False)

    @classmethod
    def from_json(cls, data: str) -> Entity:
        jsn = json.loads(data)
        return cls(
            project_key=jsn["project_key"],
            name=jsn["name"],
            identifier=jsn["identifier"],
            entity_type=jsn["entity_type"],
            type=jsn["type"],
        )


def download_to_sql(target: pathlib.Path, entities: list[Entity]) -> None:
    for i, entity in enumerate(entities):
        print(entity.name)
        # if entity.entity_type == "dataset":
        #     print(f"\t{entity.identifier}")
        if entity.entity_type == "recipe":
            type_, data = dataiku_parser.get_recipe_definition(
                entity.project_key, entity.name
            )
            target = target / f"{i:04d}-{entity.name}.{type_}"
            if type_ == "sql":
                target.write_text(data)
            if type_ == "json":
                with open(target, "w+") as f:
                    json.dump(data, f, indent=2)


def optimise_sql(src: pathlib.Path, dst: pathlib.Path) -> None:
    for f in src.glob(pattern=r"*.sql"):
        print(f.relative_to(src))
        sql = f.read_text()

        target = dst / f.name
        optimised = sqlglot.optimizer.optimize(
            expression=sql,
            dialect="snowflake",
        ).sql()

        # fix needs to be run at least twice: https://github.com/sqlfluff/sqlfluff/issues/2584
        fix = functools.partial(sqlfluff.fix, config_path=".sqlfluff")
        fixed = prev_fixed = fix(optimised)
        while True:
            fixed = fix(fixed)
            if fixed == prev_fixed:
                break
            prev_fixed = fixed

        target.write_text(fixed)


def main() -> int:
    data = (dataiku_parser.DATA / "flow.jsonl").read_text()
    entities = [Entity.from_json(d) for d in data.splitlines()]

    sql_defs = dataiku_parser.DATA / "defs"
    download_to_sql(
        target=sql_defs,
        entities=entities,
    )

    optimised_sql = dataiku_parser.DATA / "models"
    optimise_sql(
        src=sql_defs,
        dst=optimised_sql,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
