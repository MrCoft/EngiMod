from engi_mod import *

WIP(
    name = "Spare Parts",
    type = "power",
    target = "self",
    rarity = "uncommon",
    cost = 2,
    const = dict(
        COST_UPGRADE = 1,
        AMOUNT = 1,
        MAGIC_NUMBER = "AMOUNT",
    ),
    desc = "At the start of your turn, reduce the cost of a random card in your hand by 1 until end of turn.",
    upgrade_code = """
        upgradeName();
        upgradeBaseCost(COST_UPGRADE);
    """,
)




WIP(
    name = "Lightning Rod",
    desc = [
        "Your first Attack each turn deals ",
        " additional damage and applies ",
        " Weak.",
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
