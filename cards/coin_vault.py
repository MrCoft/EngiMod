from engi_mod import *

Card(
    name = "Coin Vault",
    type = "power",
    target = "self",
    rarity = "rare",
    cost = 2,
    const = dict(
        AMOUNT = 2,
        COST_UPGRADE = 2,
        MAGIC_NUMBER = "AMOUNT",
    ), # scalable
    desc = "At the start of your turn, draw !M! cards and discard !M! cards.",
    upgrade_code = """
        upgradeName();
        upgradeBaseCost(COST_UPGRADE);
    """,
)
Power(
    name = "Coin Vault",
    desc = [
        "At the start of your turn, draw #b",
        " cards and discard #b",
        " cards.",
    ],
    desc_CODE = """
        description = DESCRIPTIONS[0] + amount + DESCRIPTIONS[1] + amount + DESCRIPTIONS[2];
    """,
    init = 'img = ImageMaster.loadImage("images/powers/32/drawCard.png");',
    code = """
        @Override
        public void atStartOfTurnPostDraw() {
            flash();
            AbstractDungeon.actionManager.addToBottom(new DrawCardAction(owner, amount));
            AbstractDungeon.actionManager.addToBottom(new DiscardAction(owner, owner, amount, false));
        }
    """,
)
