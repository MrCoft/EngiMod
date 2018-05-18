from engi_mod import *

Card(
    name = "Exosuit",
    type = "skill",
    target = "self",
    rarity = "rare",
    cost = 3,
    const = dict(
        BLOCK = 25,
        STRENGTH = 10,
        BLOCK_UPGRADE = 10,
        STRENGTH_UPGRADE = 5,
    ),
    desc = "Gain !B! Block. NL Energize. Gain 10 Strength for your next turn.",
    upgrade_desc = "Gain !B! Block. NL Energize. Gain 15 Strength for your next turn.",
    code = """
        int strength = STRENGTH;
        if (upgraded) {
            strength += STRENGTH_UPGRADE;
        }
        AbstractDungeon.actionManager.addToBottom(
            new GainBlockAction(p, p, block)
        );
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(p, p, new EngiEnergizedPower(p, 1), 1)
        );
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(p, p, new ExosuitPower(p, strength), strength)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeBlock(BLOCK_UPGRADE);
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """,
) # upgrades. exhausts?
"""
mega-suit
   next turn each time you play a card you deal 5 damage to a random enemy and block 5
"""
Power(
    name = "Exosuit",
    desc = [
        "At the start of your next turn, gain #b",
        " #yStrength until end of turn.",
    ],
    desc_expr = " DESCRIPTIONS[0] + amount + DESCRIPTIONS[1]",
    code = """
        @Override
        public void atStartOfTurn() {
            flash();
            AbstractDungeon.actionManager.addToBottom(new ApplyPowerAction(owner, owner, new StrengthPower(owner, amount), amount));
            AbstractDungeon.actionManager.addToBottom(new ApplyPowerAction(owner, owner, new LoseStrengthPower(owner, amount), amount));
            AbstractDungeon.actionManager.addToBottom(new RemoveSpecificPowerAction(owner, owner, POWER_ID));
        }
    """,
    icon = "flex",
)
