from engi_mod import *

Card(
    name = "Shield Up",
    type = "skill",
    target = "self",
    rarity = "uncommon",
    cost = 0,
    const = dict(
        BLOCK = 8,
        BLOCK_UPGRADE = 4,
    ),
    flags = dict(
        exhaust = "true",
        isInnate = "true",
    ),
    desc = "Gain !B! Block. NL Innate. NL Exhaust.",
    code = """
        AbstractDungeon.actionManager.addToBottom(new GainBlockAction(p, p, block));
    """,
    upgrade_code = """
        upgradeName();
        upgradeBlock(BLOCK_UPGRADE);
    """
)
