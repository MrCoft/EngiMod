from engi_mod import *

Card(
    name = "Take Flight",
    type = "skill",
    target = "self",
    rarity = "common",
    cost = 1,
    const = dict(
        BLOCK = 5,
        DEX_AMOUNT = 2,
        COST_UPGRADE = 0,
        MAGIC_NUMBER = "DEX_AMOUNT",
    ),
    desc = "Gain !B! Block NL and !M! Dexterity. NL At the end of your turn, lose !M! Dexterity.",
    code = """
        AbstractDungeon.actionManager.addToBottom(new GainBlockAction(p, p, block));
        AbstractDungeon.actionManager.addToBottom(new ApplyPowerAction(p, p, new DexterityPower(p, magicNumber), magicNumber));
        AbstractDungeon.actionManager.addToBottom(new ApplyPowerAction(p, p, new LoseDexterityPower(p, magicNumber), magicNumber));
    """,
    upgrade_code = """
        upgradeName();
        upgradeBaseCost(COST_UPGRADE);
    """
)
