import utils
import os
import subprocess
import shutil
from collections import namedtuple
import shlex
import random
import builtins

class Context:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass
    def __call__(self):
        self.__enter__()
    def __invert__(self):
        return reverse_context(self)
class reverse_context(Context):
    def __init__(self, context):
        self.context = context
    def __enter__(self):
        self.context.__exit__(None, None, None)
    def __exit__(self, exc_type, exc, tb):
        self.context.__enter__()


OS = "unknown"
if os.name == "nt":
    OS = "windows"
if os.name == "posix":
    OS = "linux"

class cd(Context):
    def __init__(self, path):
        self.path = os.path.abspath(path)
    def __enter__(self):
        self.old_path = os.getcwd()
        os.chdir(self.path)
    def __exit__(self, exc_type, exc, tb):
        os.chdir(self.old_path)

def cmd(args, silent=False):
    if not silent:
        if type(args) is list:
            print(*args)
        else:
            print(args)
    return subprocess.call(args, shell=True)
def cmd_dialog(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    output = process.communicate()[0].decode("utf-8", errors="ignore")
    output = "\n".join(output.splitlines())
    return namedtuple("Output", "output code")(output, process.returncode)
def shell_escape(cmd):
    if OS == "windows":
        return '"{}"'.format(cmd)
    if OS == "linux":
        return shlex.quote(cmd)

def list_files(path="."):
    root, dirs, files = next(os.walk(path, followlinks=True))
    ls = []
    for file in files:
        ls += [os.path.abspath(os.path.join(root, file))[len(os.path.abspath(path)):].lstrip(os.sep)]
    return sorted(ls)
def list_dirs(path="."):
    root, dirs, files = next(os.walk(path, followlinks=True))
    ls = []
    for dir in dirs:
        ls += [os.path.abspath(os.path.join(root, dir))[len(os.path.abspath(path)):].lstrip(os.sep)]
    return sorted(ls)
def dir_contents(path="."):
    return sorted(list_files(path) + list_dirs(path))

def sync(source, target, silent=True):
    if OS == "windows":
        cmd = 'robocopy {} {} /MIR /XD "*System Volume Information*" /R:0 /W:0'.format(
                shell_escape(source),
                shell_escape(target),
        )
    elif OS == "linux":
        cmd = "rsync {} {} -r".format(
                shell_escape(radd(source, "/")),
                shell_escape(radd(target, "/")),
        )
    file = None if not silent else subprocess.DEVNULL
    subprocess.call(cmd, stdout=file, stderr=file, shell=True)

def mkdir(path):
    path = os.path.abspath(path)
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        mkdir(parent)
    if not os.path.exists(path):
        os.mkdir(path)

def unnest(dir, shift=1):
    if not shift: return
    with cd(dir):
        dir = list_dirs()[0]
        dirs = [dir]
        for i in range(1, shift):
            subdir = list_dirs(dir)[0]
            dir = os.path.join(dir, subdir)
            dirs.append(subdir)
        temp_dir = hex(cond=lambda id: all([id not in dir_contents(scope) for scope in [".", dir]]))
        os.rename(dirs[0], temp_dir)
        dirs[0] = temp_dir
        dir = os.path.join(*dirs)
        for filename in dir_contents(dir):
            shutil.move(os.path.join(dir, filename), filename)
        os.rmdir(temp_dir)

import zipfile
import tarfile
import gzip
archive_formats = [
    (".zip", zipfile.ZipFile, "r"),
    (".tar.gz", tarfile.open, "r:gz"),
    (".tar", tarfile.open, "r:"),
    (".gz", gzip.open, "rb")
]
def unzip(source, target, shift=0, remove=False):
    compr = None
    for ext, method, mode in archive_formats:
        if source.endswith(ext):
            compr = method, mode
            break
    if compr is None:
        raise Exception("No compression method for <{}>.".format(source))
    method, mode = compr
    with method(source, mode) as archive:
        archive.extractall(target)
    if remove:
        os.remove(source)
    if shift:
        unnest(target, shift)

def symlink(link, target, overwrite=False):
    target = os.path.abspath(target)
    link = os.path.abspath(link)
    if os.path.lexists(link):
        if overwrite:
            os.remove(link)
        else:
            return
    if OS == "windows":
        cmd = "mklink {} {} {}".format("/d" if os.path.isdir(target) else "",
                                           shell_escape(link),
                                           shell_escape(target),
                                           )
    if OS == "linux":
        cmd = "ln -s {} {}".format(
                shell_escape(target),
                shell_escape(link),
        )
    utils.cmd(cmd, silent=True)


def conds(*conds):
    return lambda *args, **kwargs: all(cond(*args, **kwargs) for cond in conds if cond)
def gen_cond(gen, cond=None):
    if cond is None:
        cond = lambda val: True
    val = None
    while not val or not cond(val):
        val = gen()
    return val
def hex(n=64, cond=None):
    return gen_cond(lambda: builtins.format(random.getrandbits(n), "x"), conds(lambda id: not id.startswith(tuple("0123456789")), cond))

def merge_dicts(*dicts):
    result = {}
    for dict in dicts:
        result.update(dict)
    return result

def redict(d, remove=None, add=None):
    if remove is None: remove = []
    if add is None: add = []
    d = dict(d)
    for var in remove:
        if var in d:
            del d[var]
    if add:
        d = {key: d[key] for key in add if key in d}
    return d

def radd(text, s):
    if text.endswith(s):
        return text
    return text + s

import inspect
def calling_scope(depth=1):
    frame, filename, lineno, function, code_context, index = inspect.stack(0)[1 + depth]
    scope = {}
    scope.update(frame.f_globals)
    scope.update(frame.f_locals)
    return scope
import jinja2
import pprint
def format(text, scope=None):
    if scope is None: scope = {}
    try:
        template = jinja2.Template(text)
        scope = merge_dicts(dict(builtins.__dict__), calling_scope(), scope)
        return template.render(scope)
    except jinja2.exceptions.TemplateError as error:
        msg = []
        msg += [str(error)]
        msg += [pprint.pformat(redict(error.__dict__, ["source"]), indent=4)]
        if "lineno" in error.__dict__:
            msg += ["at [{}]: {}".format(error.lineno, text.splitlines()[error.lineno - 1].strip())]
        raise Exception("\n".join(msg))

import numpy as np
MAGICK = "magick"
if OS == "linux":
    MAGICK = "convert"
MAGICK_FILTER = "-filter LanczosSharp"
def open_data(path):
    path = shell_escape(path)

    cmd = format('identify -format "%w %h" {{ path }}')
    output, code = cmd_dialog(cmd)
    width, height = output.split()
    width, height = int(width), int(height)

    cmd = format("{{ MAGICK }} {{ MAGICK_FILTER }} -depth 8 {{ path }} rgba:-")
    data = subprocess.check_output(cmd, shell=True)
    img = np.fromstring(data, "uint8").reshape(height, width, 4)
    img = np.transpose(img, (1, 0, 2))
    return img
