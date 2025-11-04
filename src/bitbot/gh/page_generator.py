"""Landing page generation for BitBot."""

from pathlib import Path
from typing import Any

import deal
from beartype import beartype
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from bitbot import paths
from bitbot.core.errors import PageGeneratorError
from bitbot.core.result import Err, Ok, Result


@deal.pre(
    lambda releases_data, **_: isinstance(releases_data, dict),
    message="Releases data must be a dictionary",
)
@deal.pre(
    lambda output_path, **_: len(output_path) > 0,
    message="Output path cannot be empty - must specify where to save HTML file",
)
@deal.pre(
    lambda template_name, **_: len(template_name) > 0,
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

        return Ok(output)

    except TemplateNotFound:
        return Err(PageGeneratorError(f"Template not found: {template_name}"))
    except (OSError, ValueError) as e:
        return Err(PageGeneratorError(f"Failed to generate page: {e}"))
