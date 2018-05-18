from engi_mod import *

Card(
    name = "Construction",
    type = "skill",
    target = "self",
    rarity = "uncommon",
    cost = 2,
    const = dict(
        ENERGY = 3,
        MAGIC_NUMBER = "ENERGY",
    ),
    desc = "Gain [R] [R] [R]. NL You cannot play Attacks this turn.",
    upgrade_desc = "Gain [R] [R] [R] [R]. NL You cannot play Attacks this turn.",
    code = """
        AbstractDungeon.actionManager.addToBottom(new GainEnergyAction(magicNumber));
        if (!p.hasPower("Entangled"))
            AbstractDungeon.actionManager.addToBottom(new ApplyPowerAction(p, p, new EntanglePower(p), 1));
    """,
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(1);
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """,
)
