"""A factory for creating services."""

from pathlib import Path
from typing import Any, Dict

from .file_config_manager import FileConfigManager
from .file_state_manager import FileStateManager
from .file_template_manager import FileTemplateManager
from .github_manager import GitHubManager
from .praw_manager import PrawManager
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result  # for the yield case
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result  # for the yield case
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_yield_from_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = yield from orig(*call_args, **call_kwargs)
        return result  # for the yield case
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = yield from orig(*call_args, **call_kwargs)
        return result  # for the yield case
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = yield from mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = yield from mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_create_services__mutmut_orig(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_1(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "XXconfig_managerXX": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_2(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "CONFIG_MANAGER": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_3(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "Config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_4(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(None),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_5(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path(None)),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_6(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("XXdata/config.tomlXX")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_7(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("DATA/CONFIG.TOML")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_8(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("Data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_9(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "XXstate_managerXX": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_10(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "STATE_MANAGER": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_11(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "State_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_12(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(None),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_13(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path(None)),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_14(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("XXdata/bot_state.jsonXX")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_15(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("DATA/BOT_STATE.JSON")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_16(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("Data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_17(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "XXtemplate_managerXX": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_18(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "TEMPLATE_MANAGER": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_19(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "Template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_20(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(None),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_21(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path(None)),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_22(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("XXtemplatesXX")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_23(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("TEMPLATES")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_24(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("Templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_25(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "XXgithub_managerXX": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_26(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "GITHUB_MANAGER": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_27(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "Github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_28(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(None),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_29(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["XXGITHUB_TOKENXX"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_30(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["github_token"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_31(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["Github_token"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_32(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "XXreddit_managerXX": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_33(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "REDDIT_MANAGER": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_34(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "Reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_35(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=None,
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_36(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=None,
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_37(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=None,
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_38(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=None,
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_39(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=None,
        ),
    }


def x_create_services__mutmut_40(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_41(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_42(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_43(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_44(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
        ),
    }


def x_create_services__mutmut_45(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["XXREDDIT_CLIENT_IDXX"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_46(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["reddit_client_id"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_47(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["Reddit_client_id"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_48(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["XXREDDIT_CLIENT_SECRETXX"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_49(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["reddit_client_secret"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_50(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["Reddit_client_secret"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_51(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["XXREDDIT_USER_AGENTXX"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_52(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["reddit_user_agent"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_53(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["Reddit_user_agent"],
            username=env["REDDIT_USERNAME"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_54(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["XXREDDIT_USERNAMEXX"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_55(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["reddit_username"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_56(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["Reddit_username"],
            password=env["REDDIT_PASSWORD"],
        ),
    }


def x_create_services__mutmut_57(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["XXREDDIT_PASSWORDXX"],
        ),
    }


def x_create_services__mutmut_58(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["reddit_password"],
        ),
    }


def x_create_services__mutmut_59(env: Dict[str, Any]) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("data/config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(env["GITHUB_TOKEN"]),
        "reddit_manager": PrawManager(
            client_id=env["REDDIT_CLIENT_ID"],
            client_secret=env["REDDIT_CLIENT_SECRET"],
            user_agent=env["REDDIT_USER_AGENT"],
            username=env["REDDIT_USERNAME"],
            password=env["Reddit_password"],
        ),
    }


x_create_services__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_services__mutmut_1": x_create_services__mutmut_1,
    "x_create_services__mutmut_2": x_create_services__mutmut_2,
    "x_create_services__mutmut_3": x_create_services__mutmut_3,
    "x_create_services__mutmut_4": x_create_services__mutmut_4,
    "x_create_services__mutmut_5": x_create_services__mutmut_5,
    "x_create_services__mutmut_6": x_create_services__mutmut_6,
    "x_create_services__mutmut_7": x_create_services__mutmut_7,
    "x_create_services__mutmut_8": x_create_services__mutmut_8,
    "x_create_services__mutmut_9": x_create_services__mutmut_9,
    "x_create_services__mutmut_10": x_create_services__mutmut_10,
    "x_create_services__mutmut_11": x_create_services__mutmut_11,
    "x_create_services__mutmut_12": x_create_services__mutmut_12,
    "x_create_services__mutmut_13": x_create_services__mutmut_13,
    "x_create_services__mutmut_14": x_create_services__mutmut_14,
    "x_create_services__mutmut_15": x_create_services__mutmut_15,
    "x_create_services__mutmut_16": x_create_services__mutmut_16,
    "x_create_services__mutmut_17": x_create_services__mutmut_17,
    "x_create_services__mutmut_18": x_create_services__mutmut_18,
    "x_create_services__mutmut_19": x_create_services__mutmut_19,
    "x_create_services__mutmut_20": x_create_services__mutmut_20,
    "x_create_services__mutmut_21": x_create_services__mutmut_21,
    "x_create_services__mutmut_22": x_create_services__mutmut_22,
    "x_create_services__mutmut_23": x_create_services__mutmut_23,
    "x_create_services__mutmut_24": x_create_services__mutmut_24,
    "x_create_services__mutmut_25": x_create_services__mutmut_25,
    "x_create_services__mutmut_26": x_create_services__mutmut_26,
    "x_create_services__mutmut_27": x_create_services__mutmut_27,
    "x_create_services__mutmut_28": x_create_services__mutmut_28,
    "x_create_services__mutmut_29": x_create_services__mutmut_29,
    "x_create_services__mutmut_30": x_create_services__mutmut_30,
    "x_create_services__mutmut_31": x_create_services__mutmut_31,
    "x_create_services__mutmut_32": x_create_services__mutmut_32,
    "x_create_services__mutmut_33": x_create_services__mutmut_33,
    "x_create_services__mutmut_34": x_create_services__mutmut_34,
    "x_create_services__mutmut_35": x_create_services__mutmut_35,
    "x_create_services__mutmut_36": x_create_services__mutmut_36,
    "x_create_services__mutmut_37": x_create_services__mutmut_37,
    "x_create_services__mutmut_38": x_create_services__mutmut_38,
    "x_create_services__mutmut_39": x_create_services__mutmut_39,
    "x_create_services__mutmut_40": x_create_services__mutmut_40,
    "x_create_services__mutmut_41": x_create_services__mutmut_41,
    "x_create_services__mutmut_42": x_create_services__mutmut_42,
    "x_create_services__mutmut_43": x_create_services__mutmut_43,
    "x_create_services__mutmut_44": x_create_services__mutmut_44,
    "x_create_services__mutmut_45": x_create_services__mutmut_45,
    "x_create_services__mutmut_46": x_create_services__mutmut_46,
    "x_create_services__mutmut_47": x_create_services__mutmut_47,
    "x_create_services__mutmut_48": x_create_services__mutmut_48,
    "x_create_services__mutmut_49": x_create_services__mutmut_49,
    "x_create_services__mutmut_50": x_create_services__mutmut_50,
    "x_create_services__mutmut_51": x_create_services__mutmut_51,
    "x_create_services__mutmut_52": x_create_services__mutmut_52,
    "x_create_services__mutmut_53": x_create_services__mutmut_53,
    "x_create_services__mutmut_54": x_create_services__mutmut_54,
    "x_create_services__mutmut_55": x_create_services__mutmut_55,
    "x_create_services__mutmut_56": x_create_services__mutmut_56,
    "x_create_services__mutmut_57": x_create_services__mutmut_57,
    "x_create_services__mutmut_58": x_create_services__mutmut_58,
    "x_create_services__mutmut_59": x_create_services__mutmut_59,
}


def create_services(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_services__mutmut_orig, x_create_services__mutmut_mutants, args, kwargs
    )
    return result


create_services.__signature__ = _mutmut_signature(x_create_services__mutmut_orig)
x_create_services__mutmut_orig.__name__ = "x_create_services"
