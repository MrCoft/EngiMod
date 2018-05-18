from engi_mod import *

Java(
    path = "fruitymod.SpireUtils",
    code = r"""
        public static void drawTriggers(AbstractCard card) {
            AbstractPlayer player = AbstractDungeon.player;
            if (player.hasPower("Confusion") && card.cost > -1 && card.color != AbstractCard.CardColor.CURSE && card.type != AbstractCard.CardType.STATUS) {
                final int newCost = AbstractDungeon.cardRandomRng.random(3);
                if (card.cost != newCost) {
                    card.cost = newCost;
                    card.costForTurn = card.cost;
                    card.isCostModified = true;
                }
            }
            card.triggerWhenDrawn();
            if (AbstractDungeon.player.hasPower("Corruption") && card.type.equals(AbstractCard.CardType.SKILL)) {
                card.setCostForTurn(-9);
            }
            for (final AbstractRelic r : player.relics) {
                r.onCardDraw(card);
            }
        }
        public static void drawEffect(AbstractCard card) {
            card.current_x = CardGroup.DRAW_PILE_X;
            card.current_y = CardGroup.DRAW_PILE_Y;
            card.setAngle(0.0f, true);
            card.lighten(false);
            card.drawScale = 0.12f;
            card.targetDrawScale = 0.75f;
        }
        public static void showCards(ArrayList<AbstractCard> cards) {
            int n = cards.size();
            if (n == 1) {
                AbstractDungeon.topLevelEffects.add(new ShowCardBrieflyEffect(cards.get(0).makeStatEquivalentCopy()));
            } else if (n <= 3) {
                for (int i = 0; i < n; ++i) {
                    AbstractDungeon.topLevelEffects.add(
                        new ShowCardBrieflyEffect(
                            cards.get(i).makeStatEquivalentCopy(),
                            Settings.WIDTH / 2.0f + (AbstractCard.IMG_WIDTH + 40.0f * Settings.scale) * (-(((float) n) - 1.0f) / 2.0f + i),
                            Settings.HEIGHT / 2.0f
                        )
                    );
                }
            } else {
                for (AbstractCard card : cards)
                    AbstractDungeon.topLevelEffects.add(
                        new ShowCardBrieflyEffect(
                            card.makeStatEquivalentCopy(),
                            MathUtils.random(0.1f, 0.9f) * Settings.WIDTH,
                            MathUtils.random(0.2f, 0.8f) * Settings.HEIGHT
                        )
                    );
            }
        }
        public static void exhaust(AbstractCard card) {
            AbstractPlayer p = AbstractDungeon.player;
            CardGroup[] groups = new CardGroup[]{p.drawPile, p.hand, p.discardPile};
            for (CardGroup group : groups) {
                if (group.contains(card))
                    group.moveToExhaustPile(card);
            }

            CardCrawlGame.dungeon.checkForPactAchievement();
            card.exhaustOnUseOnce = false;
            card.freeToPlayOnce = false;
        }
    """,
)

# fetching makes them stuck at source