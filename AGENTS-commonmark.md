

# pshnb – operator notes

Documentation for agents working on this nbdev project. Source notebooks
drive code; most `.py` files are generated.

## Repo layout

- `00_core.ipynb`: Primary nbdev notebook; edit this (not
  `pshnb/core.py`) to change code/doc examples, then run nbdev export.
- `index.ipynb`: Landing notebook that builds the README/home page.
- `pshnb/core.py`: Generated module containing the persistent shell
  magic implementation.
- `pshnb/__init__.py`: Version + re-exports.
- `pshnb/_modidx.py`: nbdev-generated module index; rebuild via nbdev,
  do not hand-edit.
- `settings.ini`, `nbdev.yml`, `_quarto.yml`, `sidebar.yml`: nbdev +
  Quarto config.
- `_docs/`: Built documentation site output (Quarto).
- Packaging: `pyproject.toml`, `setup.py`, `MANIFEST.in`,
  `pshnb.egg-info`, `dist/`.
- Changelogs: `CHANGELOG.md` (+ `.bak`).

## Core behavior (key snippets)

Persistent shell session backed by `pexpect`. Echo-less prompt and
sentinel ensure synchronous command completion:

``` python
class ShellInterpreter:
    def __init__(...):
        shell_path = shutil.which('bash') or os.environ.get('SHELL', '/bin/bash')
        if sudo: shell_path = 'sudo -i ' + shell_path
        self.sh = pexpect.spawn(shell_path, encoding='utf-8', env=dict(os.environ, TERM='dumb'))
        self.sh.sendline('stty -echo'); ...
        self.echo = os.urandom(8).hex()
        self.echo_re = re.compile(fr'^{self.echo}\s*$', flags=re.MULTILINE)

    def _ex(self, s, timeout=None):
        self.sh.sendline(s)
        res = self.wait_echo(timeout=timeout)
        return res

    def __call__(self, cmd, timeout=None):
        output = self._ex(cmd.rstrip(), timeout=timeout)
        return output.replace(cmd + '\r\n', '', 1).rstrip()
```

`PshMagic.bash` wires the IPython `%bash`/`%%bash` magics to the
interpreter. Flags toggle behavior: `-r/--reset` (optionally choose
shell), `-s/-S` sudo, `-x/-X` variable expansion, `-t` timeout, `-c`
sync cwd, `-o` return the magic object. Variable replacement uses
`@{name}` tokens resolved from the user namespace via `shell_replace`.

Installing the magic globally uses the console script `pshnb_install` →
`create_ipython_config`, which appends `pshnb.core` to
`profile_default/ipython_config.py` if absent.

## Working on the project

- Edit notebooks (`00_core.ipynb`, `index.ipynb`) and run
  `nbdev_export`/`nbdev_prepare` to regenerate modules, README, and
  docs; avoid direct edits to generated `.py`/`_modidx.py`.
- Alternatively, edit the .py files and run `nbdev_sync` to push changes
  back into the notebooks
- Dependencies are minimal: `fastcore`, plus `pexpect`/`IPython` pulled
  via the notebook environment. For local dev: `pip install -e .` in the
  repo root.
- Docs build to `_docs/`; Quarto config lives in `_quarto.yml`. The
  published site is configured for
  `https://answerdotai.github.io/pshnb`.
- Entry points defined in `setup.py`: `pshnb_install` (console) and
  IPython extension hook `pshnb.core:load_ipython_extension`.
- No automated tests are present; manual notebook runs are the primary
  verification path, or `nbdev_test` as per standard nbdev practice.
  TIMEOUT exceptions surface from `pexpect` if commands overrun the
  configured timeout.
