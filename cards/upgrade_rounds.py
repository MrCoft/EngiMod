from engi_mod import *

Card(
    name = "Upgrade Rounds",
    type = "skill",
    target = "self",
    rarity = "rare",
    cost = 1,
    flags = dict(
        exhaust = "true",
    ),
    desc = 'Upgrade ALL of your Attack cards containing "Round" for the rest of combat. NL Exhaust.',
    upgrade_desc = 'Upgrade ALL of your Attack cards containing "Round" for the rest of combat.',
    code = """
        AbstractDungeon.actionManager.addToBottom(new UpgradeRoundsAction());
    """,
    upgrade_code = """
        upgradeName();
        exhaust = false;
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """,
)
Action(
    id = "UpgradeRoundsAction",
    flags = dict(
        duration = "Settings.ACTION_DUR_MED",
        actionType = "ActionType.WAIT",
    ),
    code_FULL = r"""
        ArrayList<AbstractCard> upgraded;

        @Override
        public void update() {
            if (duration == Settings.ACTION_DUR_MED) {
                upgraded = new ArrayList<AbstractCard>();

                final AbstractPlayer p = AbstractDungeon.player;
                upgradeAllCardsInGroup(p.hand);
                upgradeAllCardsInGroup(p.drawPile);
                upgradeAllCardsInGroup(p.discardPile);
                upgradeAllCardsInGroup(p.exhaustPile);
                isDone = true;
                if (!upgraded.isEmpty()) {
                    AbstractDungeon.effectsQueue.add(new UpgradeShineEffect(Settings.WIDTH / 2.0f, Settings.HEIGHT / 2.0f));
                    SpireUtils.showCards(upgraded);
                }
            }
        }

        private void upgradeAllCardsInGroup(final CardGroup cardGroup) {
            for (final AbstractCard card : cardGroup.group) {
                if (RoundUtils.isRound(card) && card.canUpgrade()) {
                    if (cardGroup.type == CardGroup.CardGroupType.HAND) {
                        card.superFlash();
                    }
                    card.upgrade();
                    card.applyPowers();

                    upgraded.add(card);
                }
            }
        }
    """,
)
