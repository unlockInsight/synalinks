import click

from synalinks.cli.banners import banner
from synalinks.cli.utils.setup_utils import base_setup_config
from synalinks.cli.utils.setup_utils import models_setup_config
from synalinks.cli.utils.setup_utils import maybe_setup_project
from synalinks.cli.utils.setup_utils import secrets_setup_config
from synalinks.cli.utils.setup_utils import setup_project
from synalinks.src.api_export import synalinks_export
from synalinks.src.version import version as get_version


@click.group()
def magic_cli():
    """Synalinks AI powered command-line interface."""
    pass


@magic_cli.command()
def version():
    """Print synalinks version"""
    click.echo(banner())
    click.echo(f"Version: {get_version()}")


@magic_cli.command()
def init():
    """Initializes a new project"""
    click.echo(banner())
    config = base_setup_config()
    config = models_setup_config(config)
    secrets = secrets_setup_config(config)
    setup_project(config, secrets)


if __name__ == "__main__":
    magic_cli()
