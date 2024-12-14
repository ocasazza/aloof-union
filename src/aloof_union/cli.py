import json

import click

from aloof_union import AutomationType, WorkflowTranspiler


@click.group()
def cli():
    """Aloof Union - Workflow Transpiler CLI"""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option(
    "--from-type", "-f", type=click.Choice(["fs", "jsm", "mermaid"]), required=True
)
@click.option(
    "--to-type", "-t", type=click.Choice(["fs", "jsm", "mermaid"]), required=True
)
def convert(input_file, output_file, from_type, to_type):
    """Convert workflow from one format to another."""
    format_map = {
        "fs": AutomationType.FRESHSERVICE,
        "jsm": AutomationType.JSM,
        "mermaid": AutomationType.MERMAID,
    }

    transpiler = WorkflowTranspiler()

    with open(input_file, "r") as f:
        content = f.read()
        if from_type != "mermaid":
            content = json.loads(content)

    result = transpiler.transpile(
        content, from_type=format_map[from_type], to_type=format_map[to_type]
    )

    with open(output_file, "w") as f:
        if to_type == "mermaid":
            f.write(result)
        else:
            json.dump(result, f, indent=2)


if __name__ == "__main__":
    cli()
