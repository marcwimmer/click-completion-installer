import click
import subprocess
import os
import sys
from pathlib import Path
import shellingham

import inspect
import os
from pathlib import Path
current_dir = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

@click.group()
def cli():
    pass

@cli.command(help="Name of the console call.")
@click.argument("name")
def setup(name):
    def setup_for_shell_generic(shell):

        template = (current_dir / 'data' / shell).read_text()
        template = template.format(
            NAME=name,
            NAME_UPPER=name.upper().replace("-", "_"),
        )

        path = Path(f"/etc/{shell}_completion.d")
        if path.exists():
            if os.access(path, os.W_OK):
                (path / name).write_bytes(template)
                return

        if not (path / name).exists():
            rc = Path(os.path.expanduser("~")) / f'.{shell}rc'
            if not rc.exists():
                return
            complete_file = rc.parent / f'.{name}-completion.sh'
            complete_file.write_bytes(name)
            if complete_file.name not in rc.read_text():
                content = rc.read_text()
                content += '\nsource ~/' + complete_file.name
                rc.write_text(content)

    shell = shellingham.detect_shell()[0]
    setup_for_shell_generic(shell, name)