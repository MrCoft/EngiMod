from engi_mod import *

Card(
    # DESIGN: fixes the issue of 0-cost cantrips being "free" by detering decks that don't want rounds in them
    name = "Reload",
    type = "skill",
    target = "self",
    rarity = "common",
    cost = 0,
    const = dict(
        ROUND_NUM = 1,
        MAGIC_NUMBER = "ROUND_NUM",
    ),
    desc = "Shuffle a Round into your draw pile.",
    upgrade_desc = "Shuffle a Round into your draw pile. NL Draw a card.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new MakeTempCardInDrawPileAction(p, p, new Round(), magicNumber, true, true)
        );
        if (upgraded)
            AbstractDungeon.actionManager.addToBottom(new DrawCardAction(p, 1));
    """,
    upgrade_code = """
        upgradeName();
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """
)
