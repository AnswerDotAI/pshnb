"""Provides `psh` persistent bash magics in Jupyter and IPython"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_core.ipynb.

# %% auto 0
__all__ = ['BashMagic', 'create_magic', 'load_ipython_extension', 'create_ipython_config']

# %% ../00_core.ipynb
import re,os
from pathlib import Path
from IPython.core.magic import register_cell_magic
from IPython.display import display, Javascript
from IPython.paths import get_ipython_dir

# %% ../00_core.ipynb
class BashMagic:
    def __init__(self):
        self.o = ...
        self._loaded = False

    def bash(self, line, cell=None):
        if line and not cell: cell=line
        if not self._loaded:
            p = Path(__file__).resolve().parent
            self._loaded = True
        disp = True
        if cell.endswith(';'): disp,cell = False,cell[:-1]
        res = self.o.eval(cell) or None
        if disp: return res

# %% ../00_core.ipynb
def create_magic(shell=None):
    if not shell: shell = get_ipython()
    bash_magic = BashMagic()
    shell.register_magic_function(bash_magic, 'line_cell', 'psh')

# %% ../00_core.ipynb
def load_ipython_extension(ipython):
    "Required function for creating magic"
    create_magic(shell=ipython)

# %% ../00_core.ipynb
def create_ipython_config():
    "Called by `bashnb_install` to install magic"
    ipython_dir = Path(get_ipython_dir())
    cf = ipython_dir/'profile_default'/'ipython_config.py'
    cf.parent.mkdir(parents=True, exist_ok=True)
    if cf.exists() and 'bashnb' in cf.read_text(): return print('bashnb already installed!')
    with cf.open(mode='a') as f: f.write("\nc.InteractiveShellApp.extensions.append('bashnb.core')\n\n")
    print(f"Jupyter config updated at {cf}")
