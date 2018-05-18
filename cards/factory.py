from engi_mod import *

Card(
    name = "Factory",
    type = "power",
    target = "self",
    rarity = "uncommon",
    cost = 1,
    const = dict(
        AMOUNT = 3,
        MAGIC_NUMBER = "AMOUNT",
        AMOUNT_UPGRADE = 2,
    ),
    desc = "At the start of your turn, upgrade !M! random cards anywhere.",
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(AMOUNT_UPGRADE);
    """,
)
Power(
    name = "Factory",
    desc = [
        "At the start of your turn, #yUpgrade ",
        "a random card anywhere.",
        " random cards anywhere.",
    ],
    desc_CODE = """
        if (amount == 1) {
            description = DESCRIPTIONS[0] + DESCRIPTIONS[1];
        }
        else {
            description = DESCRIPTIONS[0] + "#b" + amount + DESCRIPTIONS[2];
        }
    """,
    init = 'img = ImageMaster.loadImage("images/powers/32/drawCard.png");',
    code = """
        @Override
        public void atStartOfTurn() {
            flash();
            AbstractDungeon.actionManager.addToBottom(new FactoryUpgradeAction(amount));
        }
    """,
)
Action(
    id = "FactoryUpgradeAction",
    args = """
        int amount
    """,
    flags = dict(
        duration = "Settings.ACTION_DUR_FASTER",
        actionType = "ActionType.CARD_MANIPULATION",
    ),
    code = """
        AbstractPlayer player = AbstractDungeon.player;

        CardGroup cards = new CardGroup(CardGroup.CardGroupType.UNSPECIFIED);
        CardGroup[] groups = new CardGroup[]{player.drawPile, player.hand, player.discardPile};
        for (CardGroup group : groups) {
            for (AbstractCard card : group.group) {
                if (card.canUpgrade()) {
                    cards.addToTop(card);
                }
            }
        }
        ArrayList<AbstractCard> upgraded = new ArrayList<AbstractCard>();
        for (int i = 0; i < amount; ++i) {
            cards.shuffle();
            AbstractCard card = cards.getTopCard();
            card.upgrade();
            if (!upgraded.contains(card))
                upgraded.add(card);
            if (!card.canUpgrade()) {
                cards.group.remove(card);
                if (cards.isEmpty())
                    break;
            }
        }
        for (AbstractCard card : upgraded) {
            if (player.hand.contains(card))
                card.superFlash();
            card.applyPowers();
        }
        AbstractDungeon.effectsQueue.add(new UpgradeShineEffect(Settings.WIDTH / 2.0f, Settings.HEIGHT / 2.0f));
        SpireUtils.showCards(upgraded);
        isDone = true;
    """,
)
