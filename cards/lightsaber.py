from engi_mod import *

Card(
    name = "Lightsaber",
    type = "power",
    target = "self",
    rarity = "uncommon",
    cost = 1,
    const = dict(
        COST_UPGRADE = 0,
        AMOUNT = 3,
        MAGIC_NUMBER = "AMOUNT",
    ),
    desc = "Strikes deal !M! additional damage and give !M! Block.",
    upgrade_code = """
        upgradeName();
        upgradeBaseCost(COST_UPGRADE);
    """,
)
Power(
    name = "Lightsaber",
    desc = [
        "#yStrikes deal #b",
        " additional damage and give #b",
        " #yBlock."
    ],
    desc_expr = "DESCRIPTIONS[0] + amount + DESCRIPTIONS[1] + amount + DESCRIPTIONS[2]",
    init = """
        type = AbstractPower.PowerType.BUFF;
        isTurnBased = false;
        priority = 90;
        img = FruityMod.getEnigmaPowerTexture();
        updateStrikesInHand();
    """,
    code = """
        @Override
        public void onInitialApplication() {
            updateStrikesInHand();
        }

        @Override
        public void onDrawOrDiscard() {
            updateStrikesInHand();
        }
        @Override
        public void stackPower(final int stackAmount) {
            amount += stackAmount;
            updateStrikesInHand();
        }

        private void updateStrikesInHand() {
            for (AbstractCard c : AbstractDungeon.player.hand.group) {
                if (c instanceof Strike_Purple) {
                    c.baseDamage = 6 + amount;
                    if (c.upgraded)
                        c.baseDamage += 3;
                    c.baseBlock = amount;
                    c.rawDescription = "Deal !D! damage. NL Gain !B! Block.";
                    c.initializeDescription();
                }
            }
        }
        @Override
        public void onAfterCardPlayed(final AbstractCard card) {
            if (card instanceof Strike_Purple)
                AbstractDungeon.actionManager.addToBottom(new GainBlockAction(owner, owner, card.block));
        }
    """,
)
