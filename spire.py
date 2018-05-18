import textwrap
from utils import format

import string
valid_id = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_"
def name_id(name, upper=False):
    if not upper:
        name = name.replace(" ", "")
    else:
        name = name.upper().replace(" ", "_")
    name = name.replace("-", "_")
    name = "".join([char for char in name if char in valid_id])
    while name[0] in string.digits:
        name = name[1:]
    name = name[0].upper() + name[1:]
    return name

def Card(*, name, type, target, color, rarity, cost, const=None, flags=None, desc, upgrade_desc=None, **kwargs):
    if cost == "x":
        cost = -1
    if const is None:
        const = {}
    if flags is None:
        flags = {}

    if target == "all_enemies":
        flags["isMultiDamage"] = "true"

    code = dict(use=None, upgrade=None, methods="")
    arg = kwargs.pop("code", None)
    if arg: code["use"] = arg
    arg = kwargs.pop("upgrade_code", None)
    if arg: code["upgrade"] = textwrap.dedent("""
            if (!this.upgraded) {{
                {}
            }}
        """).strip().format(textwrap.indent(textwrap.dedent(arg).strip(), " " * 4).lstrip())
    arg = kwargs.pop("upgrade_code_FULL", None)
    if arg: code["upgrade"] = arg
    arg = kwargs.pop("methods", None)
    if arg: code["methods"] = arg
    if not code["use"] and type == "power":
        stacks = 1 if not "MAGIC_NUMBER" in const else "magicNumber"
        code["use"] = format("""
            AbstractDungeon.actionManager.addToBottom(
                new ApplyPowerAction(p, p, new {{ name_id(name) }}Power(p, {{ stacks }}), {{ stacks }})
            );
        """)
    code = {name: textwrap.dedent(impl).strip() for name, impl in code.items()}
    if kwargs:
        raise SyntaxError(kwargs)

    return dict(
        name = name,
        type = type,
        target = target,
        color = color,
        rarity = rarity,
        cost = cost,
        const = const,
        flags = flags,
        desc = desc,
        upgrade_desc = upgrade_desc,
        code = code,
    )

def Power(*, id=None, name, desc, init=None, code, icon=None, **kwargs):
    if id is None:
        id = name_id(name)
    id = id + "Power"
    if init:
        init = textwrap.dedent(init).strip()
    desc_code = None
    arg = kwargs.pop("desc_expr", None)
    if arg: desc_code = "description = {};".format(arg)
    arg = kwargs.pop("desc_CODE", None)
    if arg: desc_code = textwrap.dedent(arg).strip()
    code = textwrap.dedent(code).strip()
    if kwargs:
        raise SyntaxError(kwargs)
    return dict(
        id = id,
        name = name,
        desc = desc,
        desc_code = desc_code,
        init = init,
        code = code,
        icon = icon,
    )

def Action(*, id, args=None, flags=None, **kwargs):
    if args is not None:
        vars = [line.split() for line in args.strip().splitlines()]
    else:
        vars = []
    if flags is None:
        flags = {}
    code = None
    arg = kwargs.pop("code", None)
    if arg: code = textwrap.dedent("""
            @Override
            public void update() {{
                {}
            }}
        """).strip().format(textwrap.indent(textwrap.dedent(arg).strip(), " " * 4).lstrip())
    arg = kwargs.pop("code_FULL", None)
    if arg: code = textwrap.dedent(arg).strip()
    if kwargs:
        raise SyntaxError(kwargs)

    return dict(
        id = id,
        vars = vars,
        flags = flags,
        code = code,
    )

def Java(*, path, base=None, code):
    path = path.split(".")
    code = textwrap.dedent(code).strip()
    return dict(
        package = path[:-1],
        name = path[-1],
        base = base,
        code = code,
    )
