from engi_mod import *

Card(
    name = "Strength Block",
    type = "skill",
    target = "self",
    rarity = "uncommon",
    cost = 2,
    const = dict(
        BLOCK = 12,
        BLOCK_UPGRADE = 3,
        STRENGTH = 1,
    ),
    desc = "Gain !B! Block. NL Gain 1 Strength.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new GainBlockAction(p, p, block)
        );
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(p, p, new StrengthPower(p, STRENGTH), STRENGTH)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeBlock(BLOCK_UPGRADE);
    """,
)
