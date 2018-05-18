from engi_mod import *

Card(
    name = "Lightning Rod",
    type = "power",
    target = "self",
    rarity = "uncommon",
    cost = 1,
    const = dict(
        COST_UPGRADE = 0,
        AMOUNT = 1,
        MAGIC_NUMBER = "AMOUNT",
    ),
    desc = "The first time you play an Attack each turn, deal 2 damage and apply 1 Weak.",
    upgrade_code = """
        upgradeName();
        upgradeBaseCost(COST_UPGRADE);
    """,
)
Power(
    name = "Lightning Rod",
    desc = [
        "The first time you play an #yAttack each turn, deal #b",
        " damage and apply #b",
        " #yWeak.",
    ],
    desc_expr = "DESCRIPTIONS[0] + 2 * amount + DESCRIPTIONS[1] + amount + DESCRIPTIONS[2]",
    init = """
        type = AbstractPower.PowerType.BUFF;
        isTurnBased = false;
        priority = 90;
        img = FruityMod.getEnigmaPowerTexture();
    """,
    code = """
        @Override
        public void onInitialApplication() {
            atStartOfTurn();
        }

        @Override
        public void atStartOfTurn() {
            AbstractDungeon.actionManager.addToBottom(new ApplyPowerAction(owner, owner, new ElectricChargePower(owner, amount), amount));
        }
    """,
)
