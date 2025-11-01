"""Landing page generation for BitBot."""

from pathlib import Path
from typing import Any

import deal
from beartype import beartype
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

import paths
from core.errors import PageGeneratorError
from core.result import Err, Ok, Result


@deal.pre(lambda releases_data, _o, _t: isinstance(releases_data, dict))
@deal.pre(lambda _r, output_path, _t: len(output_path) > 0)
@deal.pre(lambda _r, _o, template_name: len(template_name) > 0)
@beartype
def generate_landing_page(
    releases_data: dict[str, Any],
    output_path: str,
    template_name: str = "default_landing_page.html",
) -> Result[Path, PageGeneratorError]:
    """Generate HTML landing page from template."""
    try:
        env = Environment(loader=FileSystemLoader(paths.TEMPLATES_DIR))
        template = env.get_template(template_name)

        rendered = template.render(**releases_data)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(rendered, encoding="utf-8")

        return Ok(output)

    except TemplateNotFound:
        return Err(PageGeneratorError(f"Template not found: {template_name}"))
    except Exception as e:
        return Err(PageGeneratorError(f"Failed to generate page: {e}"))
