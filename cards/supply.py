from engi_mod import *

Card(
    name = "Supply",
    type = "skill",
    target = "self",
    rarity = "uncommon",
    cost = 1,
    const = dict(
        CARDS_NUM = 2,
        MAGIC_NUMBER = "CARDS_NUM",
    ),
    desc = "Shuffle your discard pile into your draw pile. NL Draw !M! Attack cards.",
    code = """
        if (!p.discardPile.isEmpty()) {
            AbstractDungeon.actionManager.addToBottom(new EmptyDeckShuffleAction());
        }
        AbstractDungeon.actionManager.addToBottom(new ShuffleAction(p.drawPile));

        AbstractDungeon.actionManager.addToBottom(new SupplyAction(p, magicNumber));
    """,
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(1);
    """,
)
Java(
    path = "fruitymod.actions.unique.SupplyAction",
    base = "ChooseCardActionBase",
    code = """
        public SupplyAction(final AbstractCreature source, final int amount) {
            super(source, amount, null, true, true, true);
        }

        @Override
        public boolean cardFilter(AbstractCard card) {
            return p.drawPile.contains(card) && card.type.equals(AbstractCard.CardType.ATTACK);
        }

        @Override
        public void cardChosen(AbstractCard card) {
            card = cardDraw.get(card);
            if (card == null)
                return;
            SpireUtils.drawEffect(card);
            p.drawPile.removeCard(card);
            p.hand.addToHand(card);
        }
    """,
)
