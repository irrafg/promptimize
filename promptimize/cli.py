from textwrap import dedent

import click

from promptimize.crawler import discover_objects
from promptimize.prompt_cases import BasePromptCase
from promptimize.reports import Report
from promptimize.suite import Suite
from promptimize import utils


@click.group(help="💡¡promptimize!💡 CLI. `p9e` works too!")
def cli():
    pass


@click.command(help="run some prompts")
@click.argument(
    "path",
    required=True,
    type=click.Path(exists=True),
)
@click.option("--verbose", "-v", is_flag=True, help="Trigger more verbose output")
@click.option(
    "--style",
    "-s",
    type=click.Choice(["json", "yaml"], case_sensitive=False),
    default="yaml",
    help="json or yaml formatting",
)
@click.option(
    "--max-tokens",
    "-m",
    type=click.INT,
    default=1000,
    help="max_tokens passed to the model",
)
@click.option(
    "--temperature",
    "-t",
    type=click.FLOAT,
    default=0.5,
    help="max_tokens passed to the model",
)
@click.option(
    "--engine",
    "-e",
    type=click.STRING,
    default="text-davinci-003",
    help="model as accepted by the openai API",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
)
@click.option("--silent", "-s", is_flag=True)
def run(path, verbose, style, temperature, max_tokens, engine, output, silent):
    click.secho("💡 ¡promptimize! 💡", fg="cyan")
    uses_cases = discover_objects(path, BasePromptCase)
    completion_create_kwargs = {
        "engine": engine,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    report = None
    if output:
        report = Report.from_path(output)

    suite = Suite(uses_cases, completion_create_kwargs)
    suite.execute(verbose=verbose, style=style, silent=silent, report=report)

    if output:
        output_report = Report.from_suite(suite)
        output_report.write(output)


cli.add_command(run)
