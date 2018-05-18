from engi_mod import *

Java(
    path = "fruitymod.actions.ChooseCardActionBase",
    base = "AbstractGameAction",
    code = """
        protected AbstractPlayer p;
        private String text;
        private boolean isDraw = false; // NOTE: to trigger events and disable on "No Draw"
        private boolean putsIntoHand = true; // NOTE: to make decisions if hand is full
        private boolean random = false; // NOTE: skip selection

        public ChooseCardActionBase(final AbstractCreature source, int amount, String text, boolean isDraw, boolean putsIntoHand, boolean random) {
            this.isDraw = isDraw;
            if (isDraw && AbstractDungeon.player.hasPower("No Draw")) {
                // NOTE: "put into hand" is not draw
                AbstractDungeon.player.getPower("No Draw").flash();
                setValues(AbstractDungeon.player, source, amount);
                isDone = true;
                duration = 0.0f;
                actionType = ActionType.WAIT;
                return;
            }
            if (isDraw)
                putsIntoHand = true;
            p = AbstractDungeon.player;
            this.text = text;
            this.putsIntoHand = putsIntoHand;
            this.random = random;
            setValues(null, source, amount);
            actionType = ActionType.CARD_MANIPULATION;
            if (isDraw)
                actionType = ActionType.DRAW;
            duration = Settings.ACTION_DUR_FASTER;
        }

        private CardGroup cards;
        private HashMap<AbstractCard,AbstractCard> handMap;

        @Override
        public void update() {
            if (AbstractDungeon.getCurrRoom().isBattleEnding()) {
                isDone = true;
                return;
            }
            if (duration == Settings.ACTION_DUR_FASTER) {
                cards = new CardGroup(CardGroup.CardGroupType.UNSPECIFIED);
                handMap = new HashMap<AbstractCard,AbstractCard>();
                CardGroup[] groups = new CardGroup[]{p.drawPile, p.hand, p.discardPile, p.exhaustPile};
                for (CardGroup group : groups) {
                    for (AbstractCard card : group.group) {
                        if (cardFilter(card)) {
                            if (group == p.hand) {
                                AbstractCard copy = card.makeStatEquivalentCopy();
                                handMap.put(copy, card);
                                card = copy;
                            }
                            cards.addToTop(card);
                            card.stopGlowing();
                            card.unhover();
                            card.unfadeOut();
                        }
                    }
                    if (group == p.drawPile)
                        cards.shuffle();
                }
                init();
                if (cards.isEmpty()) {
                    isDone = true;
                    finish();
                    return;
                }
                if (random) {
                    cards.shuffle(); // NOTE: random order even if instant
                    if (cards.size() > amount)
                        cards.group.subList(amount, cards.size()).clear();
                    isDone = true;
                    for (AbstractCard card : cards.group) {
                        card = handMap.getOrDefault(card, card);
                        cardChosen(card);
                        if (isDraw)
                            SpireUtils.drawTriggers(card);
                    }
                    finish();
                    return;
                }
                if (cards.size() <= amount && (!putsIntoHand || (putsIntoHand && cards.size() <= 10 - p.hand.size()))) {
                    isDone = true;
                    for (AbstractCard card : cards.group) {
                        card = handMap.getOrDefault(card, card);
                        cardChosen(card);
                        if (isDraw)
                            SpireUtils.drawTriggers(card);
                    }
                    finish();
                    return;
                } else {
                    AbstractDungeon.gridSelectScreen.open(cards, amount, text, false, false, false, false);
                    tickDuration();
                    return;
                }
            }
            if (!AbstractDungeon.gridSelectScreen.selectedCards.isEmpty()) {
                for (AbstractCard card : AbstractDungeon.gridSelectScreen.selectedCards) {
                    card = handMap.getOrDefault(card, card);
                    cardChosen(card);
                    if (isDraw)
                        SpireUtils.drawTriggers(card);
                }
                for (AbstractCard card : cards.group) {
                    card = handMap.getOrDefault(card, card);
                    card.unhover();
                    card.untip(); // NOTE: after duplicating a card, the original is drawn still showing the tooltip
                }
                AbstractDungeon.gridSelectScreen.selectedCards.clear();
                finish();
            }
            tickDuration();
        }

        public boolean cardFilter(AbstractCard card) {
            return true;
        }

        public void cardChosen(AbstractCard card) {}

        protected CardDraw cardDraw;
        public void init() {
            cardDraw = new CardDraw();
        }
        public void finish() {
            p.hand.refreshHandLayout();
            cardDraw.msg();
        }
    """
)
Java(
    # NOTE: PRIORITY
    # to upgrade and draw cards, you look through the deck,
    # picking unupgraded cards first
    # NOTE: SHUFFLE
    # if there are less than `amount` unupgraded cards,
    # you draw upgraded cards off the top
    # this special seeking only sees to the bottom of the deck
    # which is shuffled when empty, so drawing with an empty deck is worse
    # than with a full one, as it has more prioritized cards to find
    # NOTE: FULL HAND
    # when the hand is full, the extra cards aren't drawn,
    # but they can be selected, so the full amount is upgraded
    # even if it isn't drawn
    # NOTE: REPEATED UPGRADES
    # if being upgradable gives a card priority, repeatedly upgradable cards
    # could be found as the first prioritized card repeatedly
    # e.g. Battle Trance
    path = "fruitymod.actions.DrawCardActionBase",
    base = "AbstractGameAction",
    code = """
        private boolean shuffleCheck;
        private static final Logger logger;

        public DrawCardActionBase(final AbstractCreature source, final int amount, final boolean endTurnDraw) {
            this.shuffleCheck = false;
            if (endTurnDraw) {
                AbstractDungeon.topLevelEffects.add(new PlayerTurnEffect());
            }
            else if (AbstractDungeon.player.hasPower("No Draw")) {
                AbstractDungeon.player.getPower("No Draw").flash();
                this.setValues(AbstractDungeon.player, source, amount);
                this.duration = 0.0f;
                this.actionType = ActionType.WAIT;
                return;
            }
            this.setValues(AbstractDungeon.player, source, amount);
            this.actionType = ActionType.DRAW;
            if (Settings.FAST_MODE) {
                this.duration = Settings.ACTION_DUR_XFAST;
            }
            else {
                this.duration = Settings.ACTION_DUR_FASTER;
            }
        }

        public DrawCardActionBase(final AbstractCreature source, final int amount) {
            this(source, amount, false);
        }

        @Override
        public void update() {
            if (this.actionType == ActionType.WAIT) {
                this.isDone = true;
                finish();
                return;
            }
            if (this.amount <= 0) {
                this.isDone = true;
                return;
            }
            final int deckSize = AbstractDungeon.player.drawPile.size();
            final int discardSize = AbstractDungeon.player.discardPile.size();
            if (SoulGroup.isActive()) {
                return;
            }
            if (deckSize + discardSize == 0) {
                this.isDone = true;
                return;
            }
            if (AbstractDungeon.player.hand.size() == 10) {
                finish();
                AbstractDungeon.player.createHandIsFullDialog();
                this.isDone = true;
                return;
            }
            if (!this.shuffleCheck) {
                if (this.amount > deckSize) {
                    final int tmp = this.amount - deckSize;
                    AbstractDungeon.actionManager.addToTop(new DrawCardActionBase(AbstractDungeon.player, tmp));
                    AbstractDungeon.actionManager.addToTop(new EmptyDeckShuffleAction());
                    if (deckSize != 0) {
                        AbstractDungeon.actionManager.addToTop(new DrawCardActionBase(AbstractDungeon.player, deckSize));
                    }
                    this.amount = 0;
                    this.isDone = true;
                }
                this.shuffleCheck = true;
            }
            this.duration -= Gdx.graphics.getDeltaTime();
            if (this.amount != 0 && this.duration < 0.0f) {
                if (Settings.FAST_MODE) {
                    this.duration = Settings.ACTION_DUR_XFAST;
                }
                else {
                    this.duration = Settings.ACTION_DUR_FASTER;
                }
                --this.amount;
                if (!AbstractDungeon.player.drawPile.isEmpty()) {
                    AbstractCard card = findCard();
                    AbstractDungeon.player.drawPile.group.remove(card);
                    AbstractDungeon.player.drawPile.addToTop(card);
                    onSelect(card);
                    AbstractDungeon.player.draw();
                    AbstractDungeon.player.hand.refreshHandLayout();
                    onDraw(card);
                }
                else {
                    DrawCardActionBase.logger.warn("Player attempted to draw from an empty drawpile mid-DrawAction?MASTER DECK: " + AbstractDungeon.player.masterDeck.getCardNames());
                    this.isDone = true;
                }
                if (this.amount == 0) {
                    this.isDone = true;
                    finish();
                }
            }
        }
        public AbstractCard findCard() {
            if (AbstractDungeon.player.drawPile.isEmpty()) {
                return null;
            }
            for (int i = 0; i < AbstractDungeon.player.drawPile.size(); ++i) {
                AbstractCard card = AbstractDungeon.player.drawPile.getNCardFromTop(i);
                if (cardPriority(card)) {
                    return card;
                }
            }
            return AbstractDungeon.player.drawPile.getTopCard();
        }
        public void finish() {
            for (int i = 0; i < amount; ++i) {
                AbstractCard card = findCard();
                if (card == null)
                    return;
                onSelect(card);
            }
        }

        public boolean cardPriority(AbstractCard card) { return false; }
        public void onSelect(AbstractCard card) {}
        public void onDraw(AbstractCard card) {}

        static {
            logger = LogManager.getLogger(DrawCardActionBase.class.getName());
        }
    """
)
Java(
    path = "fruitymod.actions.DrawSpecificCardAction",
    base = "AbstractGameAction",
    code = """
        public DrawCardActionBase drawAction;
        public AbstractCard card;

        public DrawSpecificCardAction(final AbstractCreature source) {
            if (AbstractDungeon.player.hasPower("No Draw")) {
                AbstractDungeon.player.getPower("No Draw").flash();
                this.setValues(AbstractDungeon.player, source, amount);
                this.duration = 0.0f;
                this.actionType = ActionType.WAIT;
                return;
            }
            this.setValues(AbstractDungeon.player, source, 1);
            this.actionType = ActionType.DRAW;
            if (Settings.FAST_MODE) {
                this.duration = Settings.ACTION_DUR_XFAST;
            }
            else {
                this.duration = Settings.ACTION_DUR_FASTER;
            }
        }

        @Override
        public void update() {
            if (this.actionType == ActionType.WAIT) {
                drawAction.onSelect(card);
                this.isDone = true;
                return;
            }
            if (AbstractDungeon.player.hand.size() == 10) {
                drawAction.onSelect(card);
                AbstractDungeon.player.createHandIsFullDialog();
                this.isDone = true;
                return;
            }
            this.duration -= Gdx.graphics.getDeltaTime();
            if (this.amount != 0 && this.duration < 0.0f) {
                AbstractDungeon.player.drawPile.group.remove(card);
                AbstractDungeon.player.drawPile.addToTop(card);
                drawAction.onSelect(card);
                AbstractDungeon.player.draw();
                AbstractDungeon.player.hand.refreshHandLayout();
                drawAction.onDraw(card);

                this.isDone = true;
            }
        }
    """
)
Java(
    path = "fruitymod.CardDraw",
    code = """
        private boolean failed = false;

        public AbstractCard get(AbstractCard card) {
            if (AbstractDungeon.player.hand.size() == 10) {
                failed = true;
                return null;
            }
            card.unfadeOut();
            card.unhover();
            card.fadingOut = false;
            return card;
        }
        public void msg() {
            if (failed)
                AbstractDungeon.player.createHandIsFullDialog();
        }
    """
)

# problem - because of animations, shuffling is solved by parting the problem into "draw deck / shuffle / draw rest"

# find the cards first, then push their specific

# continue doing it until empty, then push reshuffle, then a revive?

# i hate this code so much
