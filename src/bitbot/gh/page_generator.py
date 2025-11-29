"""Landing page generation for BitBot."""

from pathlib import Path
from typing import Any

import deal
from beartype import beartype
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from returns.result import Failure, Result, Success

from bitbot import paths
from bitbot.core.errors import PageGeneratorError


@deal.pre(
    lambda releases_data, output_path, template_name: len(str(output_path)) > 0,
    message="Output path cannot be empty - must specify where to save HTML file",
)
@deal.pre(
    lambda releases_data, output_path, template_name: len(template_name) > 0,
    message="Template name cannot be empty - must specify which template to use",
)
@beartype
def generate_landing_page(
    releases_data: dict[str, Any],
    output_path: Path | str,
    template_name: str = "default_landing_page.html",
) -> Result[Path, PageGeneratorError]:
    """Generate HTML landing page from template."""
    try:
        env = Environment(loader=FileSystemLoader(paths.TEMPLATES_DIR))
        template = env.get_template(template_name)

        rendered = template.render(**releases_data)

        output = Path(output_path) if isinstance(output_path, str) else output_path
        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(rendered, encoding="utf-8")

        return Success(output)

    except TemplateNotFound:
        return Failure(PageGeneratorError(f"Template not found: {template_name}"))
    except (OSError, ValueError) as e:
        return Failure(PageGeneratorError(f"Failed to generate page: {e}"))
