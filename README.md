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

            # if click completion helper is fresh installed and not available now
            subprocess.run([
                "click-completion-helper",
                "setup",
                console_call,
            ])


setup(
    ...
    setup_requires=['click-completion-helper', ...],

    ...
)

```

or in setup.cfg:

```

[options]
setup_requires =
  click-completion-helper
```