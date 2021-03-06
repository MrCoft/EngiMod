from engi_mod import *

Card(
    name = "Glide",
    type = "skill",
    target = "self",
    rarity = "common",
    cost = 0,
    const = dict(
        BLOCK = 3,
        MAGIC_NUMBER = 1,
    ),
    desc = "Gain !B! Block. NL Draw 1 card. NL Discard 1 card.",
    upgrade_desc = "Gain !B! Block. NL Draw 2 cards. NL Discard 2 cards.",
    code = """
        AbstractDungeon.actionManager.addToBottom(new GainBlockAction(p, p, block));
        AbstractDungeon.actionManager.addToBottom(new DrawCardAction(p, magicNumber));
        AbstractDungeon.actionManager.addToBottom(new DiscardAction(p, p, magicNumber, false));
    """,
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(1);
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """
)
