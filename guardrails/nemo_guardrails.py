from pathlib import Path

from nemoguardrails import RailsConfig, LLMRails

from config.settings import PROJECT_ROOT


GUARDRAIL_CONFIG = (
    PROJECT_ROOT
    / "guardrails"
    / "config"
)


def get_guardrails():

    config = RailsConfig.from_path(
        str(GUARDRAIL_CONFIG)
    )

    rails = LLMRails(config)

    return rails