from engi_mod import *

Card(
    name = "Another Round",
    type = "attack",
    target = "enemy",
    rarity = "common",
    cost = 1,
    const = dict(
        DAMAGE = 8,
        DAMAGE_UPGRADE = 4,
    ),
    desc = 'Deal !D! damage. NL Draw an Attack card containing "Round" from your draw pile.',
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new DamageAction(m, new DamageInfo(p, damage, damageTypeForTurn), AbstractGameAction.AttackEffect.SLASH_HEAVY)
        );
        AbstractDungeon.actionManager.addToBottom(
            new AnotherRoundDrawAction(p, 1)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeDamage(DAMAGE_UPGRADE);
    """,
)
Java(
    path = "fruitymod.actions.unique.AnotherRoundDrawAction",
    base = "ChooseCardActionBase",
    code = r"""
        public AnotherRoundDrawAction(final AbstractCreature source, final int amount) {
            super(source, amount, null, true, true, true);
        }

        @Override
        public boolean cardFilter(AbstractCard card) {
            return p.drawPile.contains(card) && RoundUtils.isRound(card);
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
