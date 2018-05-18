from engi_mod import *

Card(
    name = "Full Charge",
    type = "skill",
    target = "self",
    rarity = "common",
    cost = 1,
    const = dict(
        AMOUNT = 1,
        MAGIC_NUMBER = "AMOUNT",
    ),
    desc = "Energize.",
    upgrade_desc = "Energize twice.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(p, p, new EngiEnergizedPower(p, magicNumber), magicNumber)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(1);
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """,
)
