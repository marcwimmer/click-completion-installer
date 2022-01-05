# Click Completion Installer

Helps setting up click-completion when a pip package with click is installed.
Supports

* bash
* fish (currently not implemented)
* zsh (currently not implemented)


## Using in your setup.py (setuptools)

* append as requirement to your setup.py

```python
REQUIRED = [ 'click', 'inquirer', 'arrow', 'pathlib', 'click-completion-helper', 'click-default-group' ]
...

class InstallCommand(install):
    def run(self):
        install.run(self)
        self.setup_click_autocompletion()

    def setup_click_autocompletion(self):
        for console_script in setup_cfg['options']['entry_points']['console_scripts']:
            console_call = console_script.split("=")[0].strip()

            try:
                subprocess.check_output(["which", "click-completion-helper"])
            except subprocess.CalledProcessError:
                pass
            else:
                subprocess.check_call([
                    "click-completion-helper",
                    "setup",
                    console_call,
                ])


```