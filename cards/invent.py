from engi_mod import *

Card(
    name = "Invent",
    type = "skill",
    target = "self",
    rarity = "common",
    cost = 1,
    const = dict(
        DRAW = 3,
        MAGIC_NUMBER = "DRAW",
    ),
    desc = "Draw !M! cards.",
    upgrade_desc = "Upgrade and draw !M! cards.",
    code = """
        if (!upgraded)
            AbstractDungeon.actionManager.addToBottom(new DrawCardAction(p, magicNumber));
        else
            AbstractDungeon.actionManager.addToBottom(new DrawAndUpgradeCardAction(p, magicNumber));
    """,
    upgrade_code = """
        upgradeName();
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """
)
Java(
    path = "fruitymod.actions.unique.DrawAndUpgradeCardAction",
    base = "DrawCardActionBase",
    code = """
        ArrayList<AbstractCard> upgraded;

        public DrawAndUpgradeCardAction(final AbstractCreature source, final int amount) {
            super(source, amount);
            upgraded = new ArrayList<AbstractCard>();
        }

        @Override
        public boolean cardPriority(AbstractCard card) {
            return card.canUpgrade();
        }
        @Override
        public void onSelect(AbstractCard card) {
            if (card.canUpgrade()) {
                card.superFlash();
                card.upgrade();
                card.applyPowers();
                if (!upgraded.contains(card))
                    upgraded.add(card);
            }
        }
        @Override
        public void finish() {
            super.finish();
            if (!upgraded.isEmpty()) {
                AbstractDungeon.effectsQueue.add(new UpgradeShineEffect(Settings.WIDTH / 2.0f, Settings.HEIGHT / 2.0f));
                SpireUtils.showCards(upgraded);
            }
        }
    """,
)
