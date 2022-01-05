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
@click.argument("package_name")
@click.argument("pyclass")
def setup(name, package_name, pyclass):

    def call(env):
        _call = Path("_call")
        try:
            _call.write_text("""
    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    import re
    import sys
    from fetch_latest_file import cli
    if __name__ == '__main__':
        sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
        sys.exit(cli())

                """)
            st = os.stat(_call)
            os.chmod(_call, st.st_mode | stat.S_IEXEC)
            env['PYTHONPATH'] = os.getcwd()
            try:
                output = subprocess.check_output([_call], env=env)
            except subprocess.CalledProcessError as ex:
                output = ex.output
        finally:
            if _call.exists():
                _call.unlink()
        return output

    def setup_for_shell_generic(shell):
        path = Path(f"/etc/{shell}_completion.d")
        NAME = name.upper().replace("-", "_")
        env = os.environ.copy()
        env[f"_{NAME}_COMPLETE"] = "source_" + shell
        completion = call(env)
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