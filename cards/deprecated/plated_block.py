from engi_mod import *

Card(
    name = "Plated Block",
    type = "skill",
    target = "self",
    rarity = "common",
    cost = 1,
    const = dict(
        BLOCK = 6,
        BLOCK_UPGRADE = 3,
        PLATED_ARMOR = 1,
    ),
    desc = "Gain !B! Block. NL Gain 1 Plated Armor.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new GainBlockAction(p, p, block)
        );
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(p, p, new PlatedArmorPower(p, PLATED_ARMOR), PLATED_ARMOR)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeBlock(BLOCK_UPGRADE);
    """,
)
