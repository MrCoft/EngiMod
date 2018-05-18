from engi_mod import *

Card(
    name = "Bullet Hell", #
    type = "skill",
    target = "self",
    rarity = "uncommon",
    cost = 0,
    const = dict(
    ),
    desc = "Whenever you play an Attack card this turn, Exhaust it and draw 1 card.",
    code = """
        AbstractDungeon.actionManager.addToBottom(new ApplyPowerAction(p, p, new BulletHellPower(p, 1), 1));
    """,
    upgrade_code = """
        upgradeName();
    """, # upgrade
)
Power(
    name = "Bullet Hell",
    desc = [
        "Whenever you play an #yAttack card this turn, #yExhaust it and draw #b",
        "1 card.",
        " cards.",
    ],
    desc_CODE = """
        if (amount == 1) {
            description = DESCRIPTIONS[0] + DESCRIPTIONS[1];
        } else {
            description = DESCRIPTIONS[0] + amount + DESCRIPTIONS[2];
        }
    """,
    init = """
        type = AbstractPower.PowerType.BUFF;
        img = FruityMod.getEnigmaPowerTexture();
    """,
    code = """
        @Override
        public void onAfterCardPlayed(final AbstractCard card) {
            if (card.type == AbstractCard.CardType.ATTACK) {
                flash();
                AbstractDungeon.actionManager.addToBottom(new ExhaustSpecificCardAction(card, AbstractDungeon.player.limbo));
                AbstractDungeon.actionManager.addToBottom(new DrawCardAction(owner, amount));
            }
        }

        @Override
        public void atEndOfTurn(boolean isPlayer) {
            AbstractDungeon.actionManager.addToBottom(new RemoveSpecificPowerAction(owner, owner, POWER_ID));
        }
    """,
)
