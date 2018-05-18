from engi_mod import *

Card(
    # DESIGN NOTES:
    # synergizes with Invent+, Exosuit, Golden Bullet
    name = "Recover",
    type = "skill",
    target = "self",
    rarity = "uncommon",
    cost = 0,
    const = dict(
        NUM_CARDS = 1,
        MAGIC_NUMBER = "NUM_CARDS",
    ),
    desc = "Place a card from your discard pile on top of your draw pile.",
    upgrade_desc = "Place 2 cards from your discard pile on top of your draw pile.",
    code = """
        AbstractDungeon.actionManager.addToBottom(new WaitAction(0.33f));
        AbstractDungeon.actionManager.addToBottom(new DiscardPileToTopOfDeckAction(p));
    """,
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(1);
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """,
)
Java(
    path = "fruitymod.actions.unique.DiscardPileToHandAction",
    base = "ChooseCardActionBase",
    code = """
        public DiscardPileToHandAction(final AbstractCreature source, final int amount) {
            super(source, amount, "Select a Card to Return to your Hand.", false, true, false);
        }

        @Override
        public boolean cardFilter(AbstractCard card) {
            return p.discardPile.contains(card);
        }

        @Override
        public void cardChosen(AbstractCard card) {
            card = cardDraw.get(card);
            if (card == null)
                return;
            p.discardPile.removeCard(card);
            p.hand.addToHand(card);

            card.lighten(true); // NOTE: fixes a bug where the card is dark gray if you looked at the discard pile
        }
    """,
) # can't choose 2 now :|
# originally
# 1 cost recover 1, upgraded costs 0
# now 0 cost put 1 on top, upgraded returns 2

# hologram (old)
# 3 block. return random card from grave to hand. upgraded: you can choose.

# hologram (new)
# 3 block. return card. exhaust.    upgraded: 5 block and does not exhaust
