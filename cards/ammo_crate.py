from engi_mod import *

Card(
    name = "Ammo Crate",
    type = "skill",
    target = "self",
    rarity = "common",
    cost = 1,
    const = dict(
        ROUND_NUM = 2,
        MAGIC_NUMBER = "ROUND_NUM",
    ),
    desc = "Shuffle !M! Rounds into your draw pile.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new MakeTempCardInDrawPileAction(p, p, new Round(), magicNumber, true, true)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(1);
    """
)
