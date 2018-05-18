from engi_mod import *

Card(
    name = "Blueprint",
    type = "skill",
    target = "self",
    rarity = "uncommon",
    cost = 1,
    const = dict(
        NUM_COPIES = 1,
        MAGIC_NUMBER = "NUM_COPIES",
    ),
    desc = 'Create a copy of a Power card anywhere.',
    upgrade_desc = 'Create 2 copies of a Power card anywhere.',
    code = """
        AbstractDungeon.actionManager.addToBottom(new WaitAction(0.33f));
        AbstractDungeon.actionManager.addToBottom(new BlueprintAction(p, magicNumber));
    """,
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(1);
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """,
)
Java(
    path = "fruitymod.actions.unique.BlueprintAction",
    base = "ChooseCardActionBase",
    code = """
        private int copies;

        public BlueprintAction(final AbstractCreature source, int copies) {
            super(source, 1, "Duplicate", false, true, false);
            this.copies = copies;
        }

        @Override
        public boolean cardFilter(AbstractCard card) {
            return !p.exhaustPile.contains(card) && card.type.equals(AbstractCard.CardType.POWER);
        }

        @Override
        public void cardChosen(AbstractCard card) {
            for (int i = 0; i < copies; ++i)
                AbstractDungeon.actionManager.addToTop(new MakeTempCardInHandAction(card.makeStatEquivalentCopy()));
        }
    """,
)
