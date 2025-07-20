"""This module handles the creation of GitHub releases."""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from . import crypto
from .logging import get_logger

logger = get_logger(__name__)

# --- Configuration ---
CONFIG_FILE = "config.json"
DOWNLOAD_DIR = "./dist"
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result  # for the yield case
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result  # for the yield case
    mutant_name = mutant_under_test.rpartition('.')[-1]
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


def _mutmut_yield_from_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = yield from orig(*call_args, **call_kwargs)
        return result  # for the yield case
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = yield from orig(*call_args, **call_kwargs)
        return result  # for the yield case
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = yield from mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = yield from mutants[mutant_name](*call_args, **call_kwargs)
    return result


# --- Helper Functions ---


def x_run_command__mutmut_orig(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_1(
    command: List[str], check: bool = False
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_2(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info(None, " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_3(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", None)
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_4(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info(" ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_5(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", )
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_6(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("XXExecuting: %sXX", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_7(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_8(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("EXECUTING: %S", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_9(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(None))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_10(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", "XX XX".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_11(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        None,
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_12(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=None,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_13(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=None,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_14(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=None,
    )


# --- Helper Functions ---


def x_run_command__mutmut_15(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        capture_output=True,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_16(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_17(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_18(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        )


# --- Helper Functions ---


def x_run_command__mutmut_19(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=False,
        text=True,
        check=check,
    )


# --- Helper Functions ---


def x_run_command__mutmut_20(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=False,
        check=check,
    )

x_run_command__mutmut_mutants : ClassVar[MutantDict] = {
'x_run_command__mutmut_1': x_run_command__mutmut_1, 
    'x_run_command__mutmut_2': x_run_command__mutmut_2, 
    'x_run_command__mutmut_3': x_run_command__mutmut_3, 
    'x_run_command__mutmut_4': x_run_command__mutmut_4, 
    'x_run_command__mutmut_5': x_run_command__mutmut_5, 
    'x_run_command__mutmut_6': x_run_command__mutmut_6, 
    'x_run_command__mutmut_7': x_run_command__mutmut_7, 
    'x_run_command__mutmut_8': x_run_command__mutmut_8, 
    'x_run_command__mutmut_9': x_run_command__mutmut_9, 
    'x_run_command__mutmut_10': x_run_command__mutmut_10, 
    'x_run_command__mutmut_11': x_run_command__mutmut_11, 
    'x_run_command__mutmut_12': x_run_command__mutmut_12, 
    'x_run_command__mutmut_13': x_run_command__mutmut_13, 
    'x_run_command__mutmut_14': x_run_command__mutmut_14, 
    'x_run_command__mutmut_15': x_run_command__mutmut_15, 
    'x_run_command__mutmut_16': x_run_command__mutmut_16, 
    'x_run_command__mutmut_17': x_run_command__mutmut_17, 
    'x_run_command__mutmut_18': x_run_command__mutmut_18, 
    'x_run_command__mutmut_19': x_run_command__mutmut_19, 
    'x_run_command__mutmut_20': x_run_command__mutmut_20
}

def run_command(*args, **kwargs):
    result = _mutmut_trampoline(x_run_command__mutmut_orig, x_run_command__mutmut_mutants, args, kwargs)
    return result 

run_command.__signature__ = _mutmut_signature(x_run_command__mutmut_orig)
x_run_command__mutmut_orig.__name__ = 'x_run_command'


def x_load_config__mutmut_orig() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_1() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = None
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_2() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(None)
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_3() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open(None) as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_4() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open("XXrXX") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_5() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open("R") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_6() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open("R") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_7() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open("r") as f:
        return cast(None, json.load(f))


def x_load_config__mutmut_8() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open("r") as f:
        return cast(Dict[str, Any], None)


def x_load_config__mutmut_9() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open("r") as f:
        return cast(json.load(f))


def x_load_config__mutmut_10() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open("r") as f:
        return cast(Dict[str, Any], )


def x_load_config__mutmut_11() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(None))

x_load_config__mutmut_mutants : ClassVar[MutantDict] = {
'x_load_config__mutmut_1': x_load_config__mutmut_1, 
    'x_load_config__mutmut_2': x_load_config__mutmut_2, 
    'x_load_config__mutmut_3': x_load_config__mutmut_3, 
    'x_load_config__mutmut_4': x_load_config__mutmut_4, 
    'x_load_config__mutmut_5': x_load_config__mutmut_5, 
    'x_load_config__mutmut_6': x_load_config__mutmut_6, 
    'x_load_config__mutmut_7': x_load_config__mutmut_7, 
    'x_load_config__mutmut_8': x_load_config__mutmut_8, 
    'x_load_config__mutmut_9': x_load_config__mutmut_9, 
    'x_load_config__mutmut_10': x_load_config__mutmut_10, 
    'x_load_config__mutmut_11': x_load_config__mutmut_11
}

def load_config(*args, **kwargs):
    result = _mutmut_trampoline(x_load_config__mutmut_orig, x_load_config__mutmut_mutants, args, kwargs)
    return result 

load_config.__signature__ = _mutmut_signature(x_load_config__mutmut_orig)
x_load_config__mutmut_orig.__name__ = 'x_load_config'


def x_get_github_data__mutmut_orig(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "api", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


def x_get_github_data__mutmut_1(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = None
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


def x_get_github_data__mutmut_2(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["XXghXX", "api", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


def x_get_github_data__mutmut_3(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["GH", "api", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


def x_get_github_data__mutmut_4(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["Gh", "api", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


def x_get_github_data__mutmut_5(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "XXapiXX", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


def x_get_github_data__mutmut_6(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "API", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


def x_get_github_data__mutmut_7(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "Api", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


def x_get_github_data__mutmut_8(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "api", url]
    result = None
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


def x_get_github_data__mutmut_9(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "api", url]
    result = run_command(None)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


def x_get_github_data__mutmut_10(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "api", url]
    result = run_command(command)
    return cast(None, json.loads(result.stdout))


def x_get_github_data__mutmut_11(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "api", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], None)


def x_get_github_data__mutmut_12(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "api", url]
    result = run_command(command)
    return cast(json.loads(result.stdout))


def x_get_github_data__mutmut_13(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "api", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], )


def x_get_github_data__mutmut_14(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "api", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(None))

x_get_github_data__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_github_data__mutmut_1': x_get_github_data__mutmut_1, 
    'x_get_github_data__mutmut_2': x_get_github_data__mutmut_2, 
    'x_get_github_data__mutmut_3': x_get_github_data__mutmut_3, 
    'x_get_github_data__mutmut_4': x_get_github_data__mutmut_4, 
    'x_get_github_data__mutmut_5': x_get_github_data__mutmut_5, 
    'x_get_github_data__mutmut_6': x_get_github_data__mutmut_6, 
    'x_get_github_data__mutmut_7': x_get_github_data__mutmut_7, 
    'x_get_github_data__mutmut_8': x_get_github_data__mutmut_8, 
    'x_get_github_data__mutmut_9': x_get_github_data__mutmut_9, 
    'x_get_github_data__mutmut_10': x_get_github_data__mutmut_10, 
    'x_get_github_data__mutmut_11': x_get_github_data__mutmut_11, 
    'x_get_github_data__mutmut_12': x_get_github_data__mutmut_12, 
    'x_get_github_data__mutmut_13': x_get_github_data__mutmut_13, 
    'x_get_github_data__mutmut_14': x_get_github_data__mutmut_14
}

def get_github_data(*args, **kwargs):
    result = _mutmut_trampoline(x_get_github_data__mutmut_orig, x_get_github_data__mutmut_mutants, args, kwargs)
    return result 

get_github_data.__signature__ = _mutmut_signature(x_get_github_data__mutmut_orig)
x_get_github_data__mutmut_orig.__name__ = 'x_get_github_data'


# --- Core Logic ---


def x_get_source_releases__mutmut_orig(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info("Fetching latest releases from source repo: %s", repo)
    data = get_github_data(f"/repos/{repo}/releases?per_page=30")
    if isinstance(data, list):
        return data
    return []


# --- Core Logic ---


def x_get_source_releases__mutmut_1(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info(None, repo)
    data = get_github_data(f"/repos/{repo}/releases?per_page=30")
    if isinstance(data, list):
        return data
    return []


# --- Core Logic ---


def x_get_source_releases__mutmut_2(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info("Fetching latest releases from source repo: %s", None)
    data = get_github_data(f"/repos/{repo}/releases?per_page=30")
    if isinstance(data, list):
        return data
    return []


# --- Core Logic ---


def x_get_source_releases__mutmut_3(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info(repo)
    data = get_github_data(f"/repos/{repo}/releases?per_page=30")
    if isinstance(data, list):
        return data
    return []


# --- Core Logic ---


def x_get_source_releases__mutmut_4(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info("Fetching latest releases from source repo: %s", )
    data = get_github_data(f"/repos/{repo}/releases?per_page=30")
    if isinstance(data, list):
        return data
    return []


# --- Core Logic ---


def x_get_source_releases__mutmut_5(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info("XXFetching latest releases from source repo: %sXX", repo)
    data = get_github_data(f"/repos/{repo}/releases?per_page=30")
    if isinstance(data, list):
        return data
    return []


# --- Core Logic ---


def x_get_source_releases__mutmut_6(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info("fetching latest releases from source repo: %s", repo)
    data = get_github_data(f"/repos/{repo}/releases?per_page=30")
    if isinstance(data, list):
        return data
    return []


# --- Core Logic ---


def x_get_source_releases__mutmut_7(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info("FETCHING LATEST RELEASES FROM SOURCE REPO: %S", repo)
    data = get_github_data(f"/repos/{repo}/releases?per_page=30")
    if isinstance(data, list):
        return data
    return []


# --- Core Logic ---


def x_get_source_releases__mutmut_8(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info("Fetching latest releases from source repo: %s", repo)
    data = None
    if isinstance(data, list):
        return data
    return []


# --- Core Logic ---


def x_get_source_releases__mutmut_9(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info("Fetching latest releases from source repo: %s", repo)
    data = get_github_data(None)
    if isinstance(data, list):
        return data
    return []

x_get_source_releases__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_source_releases__mutmut_1': x_get_source_releases__mutmut_1, 
    'x_get_source_releases__mutmut_2': x_get_source_releases__mutmut_2, 
    'x_get_source_releases__mutmut_3': x_get_source_releases__mutmut_3, 
    'x_get_source_releases__mutmut_4': x_get_source_releases__mutmut_4, 
    'x_get_source_releases__mutmut_5': x_get_source_releases__mutmut_5, 
    'x_get_source_releases__mutmut_6': x_get_source_releases__mutmut_6, 
    'x_get_source_releases__mutmut_7': x_get_source_releases__mutmut_7, 
    'x_get_source_releases__mutmut_8': x_get_source_releases__mutmut_8, 
    'x_get_source_releases__mutmut_9': x_get_source_releases__mutmut_9
}

def get_source_releases(*args, **kwargs):
    result = _mutmut_trampoline(x_get_source_releases__mutmut_orig, x_get_source_releases__mutmut_mutants, args, kwargs)
    return result 

get_source_releases.__signature__ = _mutmut_signature(x_get_source_releases__mutmut_orig)
x_get_source_releases__mutmut_orig.__name__ = 'x_get_source_releases'


def x_parse_release_description__mutmut_orig(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_1(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = None
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_2(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["XXdisplayNameXX"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_3(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayname"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_4(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["DISPLAYNAME"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_5(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["Displayname"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_6(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = None
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_7(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            None, description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_8(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", None, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_9(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, None
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_10(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_11(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_12(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_13(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(None)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_14(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = None
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_15(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(None)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_16(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(2)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_17(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                None,
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_18(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                None,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_19(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                None,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_20(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_21(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_22(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_23(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "XXFound app '%s' with version '%s' in description.XX",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_24(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_25(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "FOUND APP '%S' WITH VERSION '%S' IN DESCRIPTION.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def x_parse_release_description__mutmut_26(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["XXidXX"], version)
    return None


def x_parse_release_description__mutmut_27(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["ID"], version)
    return None


def x_parse_release_description__mutmut_28(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["Id"], version)
    return None

x_parse_release_description__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_release_description__mutmut_1': x_parse_release_description__mutmut_1, 
    'x_parse_release_description__mutmut_2': x_parse_release_description__mutmut_2, 
    'x_parse_release_description__mutmut_3': x_parse_release_description__mutmut_3, 
    'x_parse_release_description__mutmut_4': x_parse_release_description__mutmut_4, 
    'x_parse_release_description__mutmut_5': x_parse_release_description__mutmut_5, 
    'x_parse_release_description__mutmut_6': x_parse_release_description__mutmut_6, 
    'x_parse_release_description__mutmut_7': x_parse_release_description__mutmut_7, 
    'x_parse_release_description__mutmut_8': x_parse_release_description__mutmut_8, 
    'x_parse_release_description__mutmut_9': x_parse_release_description__mutmut_9, 
    'x_parse_release_description__mutmut_10': x_parse_release_description__mutmut_10, 
    'x_parse_release_description__mutmut_11': x_parse_release_description__mutmut_11, 
    'x_parse_release_description__mutmut_12': x_parse_release_description__mutmut_12, 
    'x_parse_release_description__mutmut_13': x_parse_release_description__mutmut_13, 
    'x_parse_release_description__mutmut_14': x_parse_release_description__mutmut_14, 
    'x_parse_release_description__mutmut_15': x_parse_release_description__mutmut_15, 
    'x_parse_release_description__mutmut_16': x_parse_release_description__mutmut_16, 
    'x_parse_release_description__mutmut_17': x_parse_release_description__mutmut_17, 
    'x_parse_release_description__mutmut_18': x_parse_release_description__mutmut_18, 
    'x_parse_release_description__mutmut_19': x_parse_release_description__mutmut_19, 
    'x_parse_release_description__mutmut_20': x_parse_release_description__mutmut_20, 
    'x_parse_release_description__mutmut_21': x_parse_release_description__mutmut_21, 
    'x_parse_release_description__mutmut_22': x_parse_release_description__mutmut_22, 
    'x_parse_release_description__mutmut_23': x_parse_release_description__mutmut_23, 
    'x_parse_release_description__mutmut_24': x_parse_release_description__mutmut_24, 
    'x_parse_release_description__mutmut_25': x_parse_release_description__mutmut_25, 
    'x_parse_release_description__mutmut_26': x_parse_release_description__mutmut_26, 
    'x_parse_release_description__mutmut_27': x_parse_release_description__mutmut_27, 
    'x_parse_release_description__mutmut_28': x_parse_release_description__mutmut_28
}

def parse_release_description(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_release_description__mutmut_orig, x_parse_release_description__mutmut_mutants, args, kwargs)
    return result 

parse_release_description.__signature__ = _mutmut_signature(x_parse_release_description__mutmut_orig)
x_parse_release_description__mutmut_orig.__name__ = 'x_parse_release_description'


def x_check_if_bot_release_exists__mutmut_orig(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_1(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(None)
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_2(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["XXghXX", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_3(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["GH", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_4(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["Gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_5(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "XXreleaseXX", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_6(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "RELEASE", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_7(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "Release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_8(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "XXviewXX", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_9(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "VIEW", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_10(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "View", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_11(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "XX--repoXX", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_12(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--REPO", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_13(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info(None, tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_14(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", None, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_15(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, None)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_16(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info(tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_17(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_18(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, )
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_19(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("XXRelease '%s' already exists in %s. Skipping.XX", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_20(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("release '%s' already exists in %s. skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_21(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("RELEASE '%S' ALREADY EXISTS IN %S. SKIPPING.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_22(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_23(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return False
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_24(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info(None, tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_25(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", None, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_26(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, None)
        return False


def x_check_if_bot_release_exists__mutmut_27(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info(tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_28(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_29(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, )
        return False


def x_check_if_bot_release_exists__mutmut_30(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("XXRelease '%s' does not exist in %s. Proceeding.XX", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_31(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("release '%s' does not exist in %s. proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_32(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("RELEASE '%S' DOES NOT EXIST IN %S. PROCEEDING.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_33(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. proceeding.", tag, bot_repo)
        return False


def x_check_if_bot_release_exists__mutmut_34(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return True

x_check_if_bot_release_exists__mutmut_mutants : ClassVar[MutantDict] = {
'x_check_if_bot_release_exists__mutmut_1': x_check_if_bot_release_exists__mutmut_1, 
    'x_check_if_bot_release_exists__mutmut_2': x_check_if_bot_release_exists__mutmut_2, 
    'x_check_if_bot_release_exists__mutmut_3': x_check_if_bot_release_exists__mutmut_3, 
    'x_check_if_bot_release_exists__mutmut_4': x_check_if_bot_release_exists__mutmut_4, 
    'x_check_if_bot_release_exists__mutmut_5': x_check_if_bot_release_exists__mutmut_5, 
    'x_check_if_bot_release_exists__mutmut_6': x_check_if_bot_release_exists__mutmut_6, 
    'x_check_if_bot_release_exists__mutmut_7': x_check_if_bot_release_exists__mutmut_7, 
    'x_check_if_bot_release_exists__mutmut_8': x_check_if_bot_release_exists__mutmut_8, 
    'x_check_if_bot_release_exists__mutmut_9': x_check_if_bot_release_exists__mutmut_9, 
    'x_check_if_bot_release_exists__mutmut_10': x_check_if_bot_release_exists__mutmut_10, 
    'x_check_if_bot_release_exists__mutmut_11': x_check_if_bot_release_exists__mutmut_11, 
    'x_check_if_bot_release_exists__mutmut_12': x_check_if_bot_release_exists__mutmut_12, 
    'x_check_if_bot_release_exists__mutmut_13': x_check_if_bot_release_exists__mutmut_13, 
    'x_check_if_bot_release_exists__mutmut_14': x_check_if_bot_release_exists__mutmut_14, 
    'x_check_if_bot_release_exists__mutmut_15': x_check_if_bot_release_exists__mutmut_15, 
    'x_check_if_bot_release_exists__mutmut_16': x_check_if_bot_release_exists__mutmut_16, 
    'x_check_if_bot_release_exists__mutmut_17': x_check_if_bot_release_exists__mutmut_17, 
    'x_check_if_bot_release_exists__mutmut_18': x_check_if_bot_release_exists__mutmut_18, 
    'x_check_if_bot_release_exists__mutmut_19': x_check_if_bot_release_exists__mutmut_19, 
    'x_check_if_bot_release_exists__mutmut_20': x_check_if_bot_release_exists__mutmut_20, 
    'x_check_if_bot_release_exists__mutmut_21': x_check_if_bot_release_exists__mutmut_21, 
    'x_check_if_bot_release_exists__mutmut_22': x_check_if_bot_release_exists__mutmut_22, 
    'x_check_if_bot_release_exists__mutmut_23': x_check_if_bot_release_exists__mutmut_23, 
    'x_check_if_bot_release_exists__mutmut_24': x_check_if_bot_release_exists__mutmut_24, 
    'x_check_if_bot_release_exists__mutmut_25': x_check_if_bot_release_exists__mutmut_25, 
    'x_check_if_bot_release_exists__mutmut_26': x_check_if_bot_release_exists__mutmut_26, 
    'x_check_if_bot_release_exists__mutmut_27': x_check_if_bot_release_exists__mutmut_27, 
    'x_check_if_bot_release_exists__mutmut_28': x_check_if_bot_release_exists__mutmut_28, 
    'x_check_if_bot_release_exists__mutmut_29': x_check_if_bot_release_exists__mutmut_29, 
    'x_check_if_bot_release_exists__mutmut_30': x_check_if_bot_release_exists__mutmut_30, 
    'x_check_if_bot_release_exists__mutmut_31': x_check_if_bot_release_exists__mutmut_31, 
    'x_check_if_bot_release_exists__mutmut_32': x_check_if_bot_release_exists__mutmut_32, 
    'x_check_if_bot_release_exists__mutmut_33': x_check_if_bot_release_exists__mutmut_33, 
    'x_check_if_bot_release_exists__mutmut_34': x_check_if_bot_release_exists__mutmut_34
}

def check_if_bot_release_exists(*args, **kwargs):
    result = _mutmut_trampoline(x_check_if_bot_release_exists__mutmut_orig, x_check_if_bot_release_exists__mutmut_mutants, args, kwargs)
    return result 

check_if_bot_release_exists.__signature__ = _mutmut_signature(x_check_if_bot_release_exists__mutmut_orig)
x_check_if_bot_release_exists__mutmut_orig.__name__ = 'x_check_if_bot_release_exists'


def x_download_asset__mutmut_orig(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_1(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info(None, asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_2(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", None, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_3(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, None)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_4(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info(asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_5(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_6(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, )
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_7(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("XXDownloading asset '%s' from release ID %sXX", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_8(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("downloading asset '%s' from release id %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_9(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("DOWNLOADING ASSET '%S' FROM RELEASE ID %S", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_10(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release id %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_11(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = None
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_12(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(None)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_13(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=None)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_14(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=False)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_15(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = None
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_16(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(None)
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_17(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = None
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_18(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = None
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_19(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = None

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_20(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        None, None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_21(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_22(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_23(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["XXidXX"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_24(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["ID"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_25(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["Id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_26(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["XXnameXX"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_27(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["NAME"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_28(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["Name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_29(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] != asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_30(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_31(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            None
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_32(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = None
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_33(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = None

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_34(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir * f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_35(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        None
    )
    return str(output_path)


def x_download_asset__mutmut_36(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "XXcurlXX",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_37(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "CURL",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_38(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "Curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_39(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "XX-sLXX",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_40(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sl",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_41(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-SL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_42(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sl",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_43(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "XX-JXX",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_44(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-j",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_45(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-j",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_46(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "XX-HXX",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_47(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-h",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_48(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-h",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_49(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "XXAccept: application/octet-streamXX",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_50(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_51(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "ACCEPT: APPLICATION/OCTET-STREAM",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_52(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "XX-HXX",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_53(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-h",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_54(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-h",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_55(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["XXGITHUB_TOKENXX"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_56(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["github_token"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_57(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["Github_token"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_58(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "XX-oXX",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_59(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-O",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_60(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(None),
            download_url,
        ]
    )
    return str(output_path)


def x_download_asset__mutmut_61(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(None)

x_download_asset__mutmut_mutants : ClassVar[MutantDict] = {
'x_download_asset__mutmut_1': x_download_asset__mutmut_1, 
    'x_download_asset__mutmut_2': x_download_asset__mutmut_2, 
    'x_download_asset__mutmut_3': x_download_asset__mutmut_3, 
    'x_download_asset__mutmut_4': x_download_asset__mutmut_4, 
    'x_download_asset__mutmut_5': x_download_asset__mutmut_5, 
    'x_download_asset__mutmut_6': x_download_asset__mutmut_6, 
    'x_download_asset__mutmut_7': x_download_asset__mutmut_7, 
    'x_download_asset__mutmut_8': x_download_asset__mutmut_8, 
    'x_download_asset__mutmut_9': x_download_asset__mutmut_9, 
    'x_download_asset__mutmut_10': x_download_asset__mutmut_10, 
    'x_download_asset__mutmut_11': x_download_asset__mutmut_11, 
    'x_download_asset__mutmut_12': x_download_asset__mutmut_12, 
    'x_download_asset__mutmut_13': x_download_asset__mutmut_13, 
    'x_download_asset__mutmut_14': x_download_asset__mutmut_14, 
    'x_download_asset__mutmut_15': x_download_asset__mutmut_15, 
    'x_download_asset__mutmut_16': x_download_asset__mutmut_16, 
    'x_download_asset__mutmut_17': x_download_asset__mutmut_17, 
    'x_download_asset__mutmut_18': x_download_asset__mutmut_18, 
    'x_download_asset__mutmut_19': x_download_asset__mutmut_19, 
    'x_download_asset__mutmut_20': x_download_asset__mutmut_20, 
    'x_download_asset__mutmut_21': x_download_asset__mutmut_21, 
    'x_download_asset__mutmut_22': x_download_asset__mutmut_22, 
    'x_download_asset__mutmut_23': x_download_asset__mutmut_23, 
    'x_download_asset__mutmut_24': x_download_asset__mutmut_24, 
    'x_download_asset__mutmut_25': x_download_asset__mutmut_25, 
    'x_download_asset__mutmut_26': x_download_asset__mutmut_26, 
    'x_download_asset__mutmut_27': x_download_asset__mutmut_27, 
    'x_download_asset__mutmut_28': x_download_asset__mutmut_28, 
    'x_download_asset__mutmut_29': x_download_asset__mutmut_29, 
    'x_download_asset__mutmut_30': x_download_asset__mutmut_30, 
    'x_download_asset__mutmut_31': x_download_asset__mutmut_31, 
    'x_download_asset__mutmut_32': x_download_asset__mutmut_32, 
    'x_download_asset__mutmut_33': x_download_asset__mutmut_33, 
    'x_download_asset__mutmut_34': x_download_asset__mutmut_34, 
    'x_download_asset__mutmut_35': x_download_asset__mutmut_35, 
    'x_download_asset__mutmut_36': x_download_asset__mutmut_36, 
    'x_download_asset__mutmut_37': x_download_asset__mutmut_37, 
    'x_download_asset__mutmut_38': x_download_asset__mutmut_38, 
    'x_download_asset__mutmut_39': x_download_asset__mutmut_39, 
    'x_download_asset__mutmut_40': x_download_asset__mutmut_40, 
    'x_download_asset__mutmut_41': x_download_asset__mutmut_41, 
    'x_download_asset__mutmut_42': x_download_asset__mutmut_42, 
    'x_download_asset__mutmut_43': x_download_asset__mutmut_43, 
    'x_download_asset__mutmut_44': x_download_asset__mutmut_44, 
    'x_download_asset__mutmut_45': x_download_asset__mutmut_45, 
    'x_download_asset__mutmut_46': x_download_asset__mutmut_46, 
    'x_download_asset__mutmut_47': x_download_asset__mutmut_47, 
    'x_download_asset__mutmut_48': x_download_asset__mutmut_48, 
    'x_download_asset__mutmut_49': x_download_asset__mutmut_49, 
    'x_download_asset__mutmut_50': x_download_asset__mutmut_50, 
    'x_download_asset__mutmut_51': x_download_asset__mutmut_51, 
    'x_download_asset__mutmut_52': x_download_asset__mutmut_52, 
    'x_download_asset__mutmut_53': x_download_asset__mutmut_53, 
    'x_download_asset__mutmut_54': x_download_asset__mutmut_54, 
    'x_download_asset__mutmut_55': x_download_asset__mutmut_55, 
    'x_download_asset__mutmut_56': x_download_asset__mutmut_56, 
    'x_download_asset__mutmut_57': x_download_asset__mutmut_57, 
    'x_download_asset__mutmut_58': x_download_asset__mutmut_58, 
    'x_download_asset__mutmut_59': x_download_asset__mutmut_59, 
    'x_download_asset__mutmut_60': x_download_asset__mutmut_60, 
    'x_download_asset__mutmut_61': x_download_asset__mutmut_61
}

def download_asset(*args, **kwargs):
    result = _mutmut_trampoline(x_download_asset__mutmut_orig, x_download_asset__mutmut_mutants, args, kwargs)
    return result 

download_asset.__signature__ = _mutmut_signature(x_download_asset__mutmut_orig)
x_download_asset__mutmut_orig.__name__ = 'x_download_asset'


def x_patch_file__mutmut_orig(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_1(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = None
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_2(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(None)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_3(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = None
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_4(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir * asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_5(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info(None, original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_6(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", None, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_7(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, None)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_8(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info(original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_9(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_10(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, )
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_11(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("XXPatching '%s' to '%s'XX", original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_12(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_13(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("PATCHING '%S' TO '%S'", original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_14(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(None, str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_15(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, None)
    return str(patched_path)


def x_patch_file__mutmut_16(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(str(patched_path))
    return str(patched_path)


def x_patch_file__mutmut_17(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, )
    return str(patched_path)


def x_patch_file__mutmut_18(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, str(None))
    return str(patched_path)


def x_patch_file__mutmut_19(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(None)

x_patch_file__mutmut_mutants : ClassVar[MutantDict] = {
'x_patch_file__mutmut_1': x_patch_file__mutmut_1, 
    'x_patch_file__mutmut_2': x_patch_file__mutmut_2, 
    'x_patch_file__mutmut_3': x_patch_file__mutmut_3, 
    'x_patch_file__mutmut_4': x_patch_file__mutmut_4, 
    'x_patch_file__mutmut_5': x_patch_file__mutmut_5, 
    'x_patch_file__mutmut_6': x_patch_file__mutmut_6, 
    'x_patch_file__mutmut_7': x_patch_file__mutmut_7, 
    'x_patch_file__mutmut_8': x_patch_file__mutmut_8, 
    'x_patch_file__mutmut_9': x_patch_file__mutmut_9, 
    'x_patch_file__mutmut_10': x_patch_file__mutmut_10, 
    'x_patch_file__mutmut_11': x_patch_file__mutmut_11, 
    'x_patch_file__mutmut_12': x_patch_file__mutmut_12, 
    'x_patch_file__mutmut_13': x_patch_file__mutmut_13, 
    'x_patch_file__mutmut_14': x_patch_file__mutmut_14, 
    'x_patch_file__mutmut_15': x_patch_file__mutmut_15, 
    'x_patch_file__mutmut_16': x_patch_file__mutmut_16, 
    'x_patch_file__mutmut_17': x_patch_file__mutmut_17, 
    'x_patch_file__mutmut_18': x_patch_file__mutmut_18, 
    'x_patch_file__mutmut_19': x_patch_file__mutmut_19
}

def patch_file(*args, **kwargs):
    result = _mutmut_trampoline(x_patch_file__mutmut_orig, x_patch_file__mutmut_mutants, args, kwargs)
    return result 

patch_file.__signature__ = _mutmut_signature(x_patch_file__mutmut_orig)
x_patch_file__mutmut_orig.__name__ = 'x_patch_file'


def x_create_bot_release__mutmut_orig(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_1(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info(None, tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_2(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", None, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_3(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, None)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_4(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info(tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_5(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_6(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, )
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_7(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("XXCreating new release '%s' in %sXX", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_8(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_9(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("CREATING NEW RELEASE '%S' IN %S", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_10(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        None
    )


def x_create_bot_release__mutmut_11(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "XXghXX",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_12(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "GH",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_13(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "Gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_14(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "XXreleaseXX",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_15(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "RELEASE",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_16(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "Release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_17(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "XXcreateXX",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_18(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "CREATE",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_19(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "Create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_20(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "XX--repoXX",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_21(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--REPO",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_22(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "XX--titleXX",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_23(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--TITLE",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_24(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "XX--notesXX",
            notes,
            file_path,
        ]
    )


def x_create_bot_release__mutmut_25(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--NOTES",
            notes,
            file_path,
        ]
    )

x_create_bot_release__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_bot_release__mutmut_1': x_create_bot_release__mutmut_1, 
    'x_create_bot_release__mutmut_2': x_create_bot_release__mutmut_2, 
    'x_create_bot_release__mutmut_3': x_create_bot_release__mutmut_3, 
    'x_create_bot_release__mutmut_4': x_create_bot_release__mutmut_4, 
    'x_create_bot_release__mutmut_5': x_create_bot_release__mutmut_5, 
    'x_create_bot_release__mutmut_6': x_create_bot_release__mutmut_6, 
    'x_create_bot_release__mutmut_7': x_create_bot_release__mutmut_7, 
    'x_create_bot_release__mutmut_8': x_create_bot_release__mutmut_8, 
    'x_create_bot_release__mutmut_9': x_create_bot_release__mutmut_9, 
    'x_create_bot_release__mutmut_10': x_create_bot_release__mutmut_10, 
    'x_create_bot_release__mutmut_11': x_create_bot_release__mutmut_11, 
    'x_create_bot_release__mutmut_12': x_create_bot_release__mutmut_12, 
    'x_create_bot_release__mutmut_13': x_create_bot_release__mutmut_13, 
    'x_create_bot_release__mutmut_14': x_create_bot_release__mutmut_14, 
    'x_create_bot_release__mutmut_15': x_create_bot_release__mutmut_15, 
    'x_create_bot_release__mutmut_16': x_create_bot_release__mutmut_16, 
    'x_create_bot_release__mutmut_17': x_create_bot_release__mutmut_17, 
    'x_create_bot_release__mutmut_18': x_create_bot_release__mutmut_18, 
    'x_create_bot_release__mutmut_19': x_create_bot_release__mutmut_19, 
    'x_create_bot_release__mutmut_20': x_create_bot_release__mutmut_20, 
    'x_create_bot_release__mutmut_21': x_create_bot_release__mutmut_21, 
    'x_create_bot_release__mutmut_22': x_create_bot_release__mutmut_22, 
    'x_create_bot_release__mutmut_23': x_create_bot_release__mutmut_23, 
    'x_create_bot_release__mutmut_24': x_create_bot_release__mutmut_24, 
    'x_create_bot_release__mutmut_25': x_create_bot_release__mutmut_25
}

def create_bot_release(*args, **kwargs):
    result = _mutmut_trampoline(x_create_bot_release__mutmut_orig, x_create_bot_release__mutmut_mutants, args, kwargs)
    return result 

create_bot_release.__signature__ = _mutmut_signature(x_create_bot_release__mutmut_orig)
x_create_bot_release__mutmut_orig.__name__ = 'x_create_bot_release'


# --- Main Execution ---


def x_main__mutmut_orig() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_1() -> None:
    """The main function for the release module."""
    config = None
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_2() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = None
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_3() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["XXgithubXX"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_4() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["GITHUB"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_5() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["Github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_6() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["XXsourceRepoXX"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_7() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourcerepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_8() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["SOURCEREPO"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_9() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["Sourcerepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_10() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = None
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_11() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["XXgithubXX"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_12() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["GITHUB"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_13() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["Github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_14() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["XXbotRepoXX"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_15() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botrepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_16() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["BOTREPO"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_17() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["Botrepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_18() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = None
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_19() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["XXgithubXX"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_20() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["GITHUB"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_21() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["Github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_22() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["XXassetFileNameXX"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_23() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetfilename"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_24() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["ASSETFILENAME"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_25() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["Assetfilename"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_26() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = None

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_27() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["XXappsXX"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_28() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["APPS"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_29() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["Apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_30() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = None
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_31() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(None)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_32() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = None
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_33() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = ""

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_34() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = None
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_35() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get(None, "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_36() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", None)
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_37() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_38() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", )
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_39() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("XXbodyXX", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_40() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("BODY", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_41() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("Body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_42() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "XXXX")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_43() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_44() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            break

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_45() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = None
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_46() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(None, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_47() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, None)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_48() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_49() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, )
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_50() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_51() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            break

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_52() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = None
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_53() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = None
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_54() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next(None, None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_55() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next(None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_56() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), )
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_57() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["XXidXX"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_58() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["ID"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_59() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["Id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_60() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] != app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_61() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_62() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            break

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_63() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = None

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_64() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_65() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(None, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_66() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, None):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_67() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_68() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, ):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_69() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = None

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_70() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(None, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_71() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, None, asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_72() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], None)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_73() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_74() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_75() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], )

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_76() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["XXidXX"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_77() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["ID"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_78() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["Id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_79() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = None

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_80() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(None, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_81() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, None)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_82() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_83() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, )

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_84() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = None
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_85() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['XXdisplayNameXX']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_86() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayname']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_87() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['DISPLAYNAME']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_88() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['Displayname']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_89() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = None
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_90() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['XXdisplayNameXX']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_91() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayname']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_92() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['DISPLAYNAME']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_93() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['Displayname']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_94() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['XXtag_nameXX']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_95() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['TAG_NAME']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_96() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['Tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_97() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    None,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_98() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    None,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_99() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    None,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_100() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    None,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_101() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    None,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_102() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_103() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_104() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_105() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_106() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_107() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = None
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_108() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = None

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_109() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id != "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_110() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "XXbitlifeXX":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_111() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "BITLIFE":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_112() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "Bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_113() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = None

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_114() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    None,
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_115() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    None,
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_116() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    None,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_117() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=None,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_118() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_119() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_120() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_121() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_122() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "XXFailed to process release %s for app %s.XX",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_123() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_124() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "FAILED TO PROCESS RELEASE %S FOR APP %S.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_125() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["XXtag_nameXX"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_126() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["TAG_NAME"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_127() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["Tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_128() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=False,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_129() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_130() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title or new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_131() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = None
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_132() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            None,
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_133() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            None,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_134() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_135() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_136() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "XXBitLife version not found. Using fallback version '%s' for Reddit title.XX",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_137() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "bitlife version not found. using fallback version '%s' for reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_138() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BITLIFE VERSION NOT FOUND. USING FALLBACK VERSION '%S' FOR REDDIT TITLE.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_139() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "Bitlife version not found. using fallback version '%s' for reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_140() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info(None)
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_141() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("XXNew releases were created. Setting outputs for Reddit job.XX")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_142() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("new releases were created. setting outputs for reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_143() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("NEW RELEASES WERE CREATED. SETTING OUTPUTS FOR REDDIT JOB.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_144() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. setting outputs for reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_145() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = None
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_146() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(None)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_147() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = None
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_148() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get(None, "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_149() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", None)
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_150() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_151() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", )
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_152() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("XXGITHUB_OUTPUTXX", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_153() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("github_output", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_154() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("Github_output", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_155() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "XX/dev/nullXX")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_156() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/DEV/NULL")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_157() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open(None) as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_158() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(None).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_159() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("XXaXX") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_160() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("A") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_161() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("A") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_162() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write(None)
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_163() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("XXnew_releases_found=true\nXX")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_164() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("NEW_RELEASES_FOUND=TRUE\N")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_165() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("New_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_166() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(None)
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_167() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(None)
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_168() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info(None)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_169() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("XXNo new releases to post to Reddit.XX")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_170() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("no new releases to post to reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_171() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("NO NEW RELEASES TO POST TO REDDIT.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_172() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_173() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = None
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_174() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get(None, "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_175() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", None)
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_176() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_177() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", )
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_178() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("XXGITHUB_OUTPUTXX", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_179() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("github_output", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_180() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("Github_output", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_181() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "XX/dev/nullXX")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_182() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/DEV/NULL")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_183() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open(None) as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_184() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(None).open("a") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_185() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("XXaXX") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_186() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("A") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_187() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("A") as f:
            f.write("new_releases_found=false\n")


# --- Main Execution ---


def x_main__mutmut_188() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write(None)


# --- Main Execution ---


def x_main__mutmut_189() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("XXnew_releases_found=false\nXX")


# --- Main Execution ---


def x_main__mutmut_190() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("NEW_RELEASES_FOUND=FALSE\N")


# --- Main Execution ---


def x_main__mutmut_191() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("New_releases_found=false\n")

x_main__mutmut_mutants : ClassVar[MutantDict] = {
'x_main__mutmut_1': x_main__mutmut_1, 
    'x_main__mutmut_2': x_main__mutmut_2, 
    'x_main__mutmut_3': x_main__mutmut_3, 
    'x_main__mutmut_4': x_main__mutmut_4, 
    'x_main__mutmut_5': x_main__mutmut_5, 
    'x_main__mutmut_6': x_main__mutmut_6, 
    'x_main__mutmut_7': x_main__mutmut_7, 
    'x_main__mutmut_8': x_main__mutmut_8, 
    'x_main__mutmut_9': x_main__mutmut_9, 
    'x_main__mutmut_10': x_main__mutmut_10, 
    'x_main__mutmut_11': x_main__mutmut_11, 
    'x_main__mutmut_12': x_main__mutmut_12, 
    'x_main__mutmut_13': x_main__mutmut_13, 
    'x_main__mutmut_14': x_main__mutmut_14, 
    'x_main__mutmut_15': x_main__mutmut_15, 
    'x_main__mutmut_16': x_main__mutmut_16, 
    'x_main__mutmut_17': x_main__mutmut_17, 
    'x_main__mutmut_18': x_main__mutmut_18, 
    'x_main__mutmut_19': x_main__mutmut_19, 
    'x_main__mutmut_20': x_main__mutmut_20, 
    'x_main__mutmut_21': x_main__mutmut_21, 
    'x_main__mutmut_22': x_main__mutmut_22, 
    'x_main__mutmut_23': x_main__mutmut_23, 
    'x_main__mutmut_24': x_main__mutmut_24, 
    'x_main__mutmut_25': x_main__mutmut_25, 
    'x_main__mutmut_26': x_main__mutmut_26, 
    'x_main__mutmut_27': x_main__mutmut_27, 
    'x_main__mutmut_28': x_main__mutmut_28, 
    'x_main__mutmut_29': x_main__mutmut_29, 
    'x_main__mutmut_30': x_main__mutmut_30, 
    'x_main__mutmut_31': x_main__mutmut_31, 
    'x_main__mutmut_32': x_main__mutmut_32, 
    'x_main__mutmut_33': x_main__mutmut_33, 
    'x_main__mutmut_34': x_main__mutmut_34, 
    'x_main__mutmut_35': x_main__mutmut_35, 
    'x_main__mutmut_36': x_main__mutmut_36, 
    'x_main__mutmut_37': x_main__mutmut_37, 
    'x_main__mutmut_38': x_main__mutmut_38, 
    'x_main__mutmut_39': x_main__mutmut_39, 
    'x_main__mutmut_40': x_main__mutmut_40, 
    'x_main__mutmut_41': x_main__mutmut_41, 
    'x_main__mutmut_42': x_main__mutmut_42, 
    'x_main__mutmut_43': x_main__mutmut_43, 
    'x_main__mutmut_44': x_main__mutmut_44, 
    'x_main__mutmut_45': x_main__mutmut_45, 
    'x_main__mutmut_46': x_main__mutmut_46, 
    'x_main__mutmut_47': x_main__mutmut_47, 
    'x_main__mutmut_48': x_main__mutmut_48, 
    'x_main__mutmut_49': x_main__mutmut_49, 
    'x_main__mutmut_50': x_main__mutmut_50, 
    'x_main__mutmut_51': x_main__mutmut_51, 
    'x_main__mutmut_52': x_main__mutmut_52, 
    'x_main__mutmut_53': x_main__mutmut_53, 
    'x_main__mutmut_54': x_main__mutmut_54, 
    'x_main__mutmut_55': x_main__mutmut_55, 
    'x_main__mutmut_56': x_main__mutmut_56, 
    'x_main__mutmut_57': x_main__mutmut_57, 
    'x_main__mutmut_58': x_main__mutmut_58, 
    'x_main__mutmut_59': x_main__mutmut_59, 
    'x_main__mutmut_60': x_main__mutmut_60, 
    'x_main__mutmut_61': x_main__mutmut_61, 
    'x_main__mutmut_62': x_main__mutmut_62, 
    'x_main__mutmut_63': x_main__mutmut_63, 
    'x_main__mutmut_64': x_main__mutmut_64, 
    'x_main__mutmut_65': x_main__mutmut_65, 
    'x_main__mutmut_66': x_main__mutmut_66, 
    'x_main__mutmut_67': x_main__mutmut_67, 
    'x_main__mutmut_68': x_main__mutmut_68, 
    'x_main__mutmut_69': x_main__mutmut_69, 
    'x_main__mutmut_70': x_main__mutmut_70, 
    'x_main__mutmut_71': x_main__mutmut_71, 
    'x_main__mutmut_72': x_main__mutmut_72, 
    'x_main__mutmut_73': x_main__mutmut_73, 
    'x_main__mutmut_74': x_main__mutmut_74, 
    'x_main__mutmut_75': x_main__mutmut_75, 
    'x_main__mutmut_76': x_main__mutmut_76, 
    'x_main__mutmut_77': x_main__mutmut_77, 
    'x_main__mutmut_78': x_main__mutmut_78, 
    'x_main__mutmut_79': x_main__mutmut_79, 
    'x_main__mutmut_80': x_main__mutmut_80, 
    'x_main__mutmut_81': x_main__mutmut_81, 
    'x_main__mutmut_82': x_main__mutmut_82, 
    'x_main__mutmut_83': x_main__mutmut_83, 
    'x_main__mutmut_84': x_main__mutmut_84, 
    'x_main__mutmut_85': x_main__mutmut_85, 
    'x_main__mutmut_86': x_main__mutmut_86, 
    'x_main__mutmut_87': x_main__mutmut_87, 
    'x_main__mutmut_88': x_main__mutmut_88, 
    'x_main__mutmut_89': x_main__mutmut_89, 
    'x_main__mutmut_90': x_main__mutmut_90, 
    'x_main__mutmut_91': x_main__mutmut_91, 
    'x_main__mutmut_92': x_main__mutmut_92, 
    'x_main__mutmut_93': x_main__mutmut_93, 
    'x_main__mutmut_94': x_main__mutmut_94, 
    'x_main__mutmut_95': x_main__mutmut_95, 
    'x_main__mutmut_96': x_main__mutmut_96, 
    'x_main__mutmut_97': x_main__mutmut_97, 
    'x_main__mutmut_98': x_main__mutmut_98, 
    'x_main__mutmut_99': x_main__mutmut_99, 
    'x_main__mutmut_100': x_main__mutmut_100, 
    'x_main__mutmut_101': x_main__mutmut_101, 
    'x_main__mutmut_102': x_main__mutmut_102, 
    'x_main__mutmut_103': x_main__mutmut_103, 
    'x_main__mutmut_104': x_main__mutmut_104, 
    'x_main__mutmut_105': x_main__mutmut_105, 
    'x_main__mutmut_106': x_main__mutmut_106, 
    'x_main__mutmut_107': x_main__mutmut_107, 
    'x_main__mutmut_108': x_main__mutmut_108, 
    'x_main__mutmut_109': x_main__mutmut_109, 
    'x_main__mutmut_110': x_main__mutmut_110, 
    'x_main__mutmut_111': x_main__mutmut_111, 
    'x_main__mutmut_112': x_main__mutmut_112, 
    'x_main__mutmut_113': x_main__mutmut_113, 
    'x_main__mutmut_114': x_main__mutmut_114, 
    'x_main__mutmut_115': x_main__mutmut_115, 
    'x_main__mutmut_116': x_main__mutmut_116, 
    'x_main__mutmut_117': x_main__mutmut_117, 
    'x_main__mutmut_118': x_main__mutmut_118, 
    'x_main__mutmut_119': x_main__mutmut_119, 
    'x_main__mutmut_120': x_main__mutmut_120, 
    'x_main__mutmut_121': x_main__mutmut_121, 
    'x_main__mutmut_122': x_main__mutmut_122, 
    'x_main__mutmut_123': x_main__mutmut_123, 
    'x_main__mutmut_124': x_main__mutmut_124, 
    'x_main__mutmut_125': x_main__mutmut_125, 
    'x_main__mutmut_126': x_main__mutmut_126, 
    'x_main__mutmut_127': x_main__mutmut_127, 
    'x_main__mutmut_128': x_main__mutmut_128, 
    'x_main__mutmut_129': x_main__mutmut_129, 
    'x_main__mutmut_130': x_main__mutmut_130, 
    'x_main__mutmut_131': x_main__mutmut_131, 
    'x_main__mutmut_132': x_main__mutmut_132, 
    'x_main__mutmut_133': x_main__mutmut_133, 
    'x_main__mutmut_134': x_main__mutmut_134, 
    'x_main__mutmut_135': x_main__mutmut_135, 
    'x_main__mutmut_136': x_main__mutmut_136, 
    'x_main__mutmut_137': x_main__mutmut_137, 
    'x_main__mutmut_138': x_main__mutmut_138, 
    'x_main__mutmut_139': x_main__mutmut_139, 
    'x_main__mutmut_140': x_main__mutmut_140, 
    'x_main__mutmut_141': x_main__mutmut_141, 
    'x_main__mutmut_142': x_main__mutmut_142, 
    'x_main__mutmut_143': x_main__mutmut_143, 
    'x_main__mutmut_144': x_main__mutmut_144, 
    'x_main__mutmut_145': x_main__mutmut_145, 
    'x_main__mutmut_146': x_main__mutmut_146, 
    'x_main__mutmut_147': x_main__mutmut_147, 
    'x_main__mutmut_148': x_main__mutmut_148, 
    'x_main__mutmut_149': x_main__mutmut_149, 
    'x_main__mutmut_150': x_main__mutmut_150, 
    'x_main__mutmut_151': x_main__mutmut_151, 
    'x_main__mutmut_152': x_main__mutmut_152, 
    'x_main__mutmut_153': x_main__mutmut_153, 
    'x_main__mutmut_154': x_main__mutmut_154, 
    'x_main__mutmut_155': x_main__mutmut_155, 
    'x_main__mutmut_156': x_main__mutmut_156, 
    'x_main__mutmut_157': x_main__mutmut_157, 
    'x_main__mutmut_158': x_main__mutmut_158, 
    'x_main__mutmut_159': x_main__mutmut_159, 
    'x_main__mutmut_160': x_main__mutmut_160, 
    'x_main__mutmut_161': x_main__mutmut_161, 
    'x_main__mutmut_162': x_main__mutmut_162, 
    'x_main__mutmut_163': x_main__mutmut_163, 
    'x_main__mutmut_164': x_main__mutmut_164, 
    'x_main__mutmut_165': x_main__mutmut_165, 
    'x_main__mutmut_166': x_main__mutmut_166, 
    'x_main__mutmut_167': x_main__mutmut_167, 
    'x_main__mutmut_168': x_main__mutmut_168, 
    'x_main__mutmut_169': x_main__mutmut_169, 
    'x_main__mutmut_170': x_main__mutmut_170, 
    'x_main__mutmut_171': x_main__mutmut_171, 
    'x_main__mutmut_172': x_main__mutmut_172, 
    'x_main__mutmut_173': x_main__mutmut_173, 
    'x_main__mutmut_174': x_main__mutmut_174, 
    'x_main__mutmut_175': x_main__mutmut_175, 
    'x_main__mutmut_176': x_main__mutmut_176, 
    'x_main__mutmut_177': x_main__mutmut_177, 
    'x_main__mutmut_178': x_main__mutmut_178, 
    'x_main__mutmut_179': x_main__mutmut_179, 
    'x_main__mutmut_180': x_main__mutmut_180, 
    'x_main__mutmut_181': x_main__mutmut_181, 
    'x_main__mutmut_182': x_main__mutmut_182, 
    'x_main__mutmut_183': x_main__mutmut_183, 
    'x_main__mutmut_184': x_main__mutmut_184, 
    'x_main__mutmut_185': x_main__mutmut_185, 
    'x_main__mutmut_186': x_main__mutmut_186, 
    'x_main__mutmut_187': x_main__mutmut_187, 
    'x_main__mutmut_188': x_main__mutmut_188, 
    'x_main__mutmut_189': x_main__mutmut_189, 
    'x_main__mutmut_190': x_main__mutmut_190, 
    'x_main__mutmut_191': x_main__mutmut_191
}

def main(*args, **kwargs):
    result = _mutmut_trampoline(x_main__mutmut_orig, x_main__mutmut_mutants, args, kwargs)
    return result 

main.__signature__ = _mutmut_signature(x_main__mutmut_orig)
x_main__mutmut_orig.__name__ = 'x_main'


if __name__ == "__main__":
    main()
