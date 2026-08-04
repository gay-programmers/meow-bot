import sys
import click
import os
import subprocess

@click.command(help="Run the bot", context_settings={"help_option_names": ["--help", "-h"]})
@click.argument("token", type=str, required=True)
@click.argument("prefix", type=str, default="!")
def main(token: str, prefix: str) -> None:
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "bot.py"), token, prefix])
    return
