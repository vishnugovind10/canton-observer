from importlib.resources import files

import yaml

from canton_observer.models import Scenario


def scenario_names() -> list[str]:
    root = files("canton_observer.scenarios")
    return sorted(
        item.name.removesuffix(".yaml") for item in root.iterdir() if item.name.endswith(".yaml")
    )


def load_scenario(name: str) -> Scenario:
    if name not in scenario_names():
        raise ValueError(f"Unknown scenario: {name}")
    resource = files("canton_observer.scenarios").joinpath(f"{name}.yaml")
    return Scenario.model_validate(yaml.safe_load(resource.read_text(encoding="utf-8")))
