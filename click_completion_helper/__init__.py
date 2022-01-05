import click
import subprocess
import os
import stat
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

    def get_template(shell):
        template = (current_dir / 'data' / shell).read_text()
        name1 = name.replace("-", "_")
        name_upper = name1.upper()
        template = template.replace("||name||", name)
        template = template.replace("||name1||", name1)
        template = template.replace("||name_upper||", name_upper)
        return template.encode('utf-8')

    def setup_for_shell_generic(shell):
        path = Path(f"/etc/{shell}_completion.d")
        NAME = name.upper().replace("-", "_")
        completion = get_template(shell)
        if path.exists():
            if os.access(path, os.W_OK):
                (path / name).write_bytes(completion)
                return

        if not (path / name).exists():
            rc = Path(os.path.expanduser("~")) / f'.{shell}rc'
            if not rc.exists():
                return
            complete_file = rc.parent / f'.{name}-completion.sh'
            complete_file.write_bytes(completion)
            if complete_file.name not in rc.read_text():
                content = rc.read_text()
                content += '\nsource ~/' + complete_file.name
                rc.write_text(content)

    setup_for_shell_generic(shellingham.detect_shell()[0])