from engi_mod import *

Card(
    name = "Conduct",
    type = "skill",
    target = "self",
    rarity = "common",
    cost = 1,
    const = dict(
        BLOCK = 6,
        BLOCK_UPGRADE = 3,
    ),
    desc = "Gain !B! Block. NL Next time you play an Attack, deal 2 damage and apply 1 Weak.",
    code = """
        AbstractDungeon.actionManager.addToBottom(new GainBlockAction(p, p, block));
        AbstractDungeon.actionManager.addToBottom(new ApplyPowerAction(p, p, new ElectricChargePower(p, 1), 1));
    """,
    upgrade_code = """
        upgradeName();
        upgradeBlock(BLOCK_UPGRADE);
    """,
)
