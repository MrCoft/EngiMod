from engi_mod import *

Card(
    name = "Gloves",
    type = "power",
    target = "self",
    rarity = "common",
    cost = 0,
    const = dict(
        PLATED_ARMOR = 2,
        MAGIC_NUMBER = "PLATED_ARMOR",
    ),
    desc = "Gain !M! Plated Armor.",
    upgrade_desc = "Innate. NL Gain !M! Plated Armor.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(p, p, new PlatedArmorPower(p, magicNumber), magicNumber)
        );
    """,
    upgrade_code = """
        upgradeName();
        isInnate = true;
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """,
)
