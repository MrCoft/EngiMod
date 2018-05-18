from engi_mod import *

Card(
    name = "Combat Capsule",
    type = "attack",
    target = "enemy",
    rarity = "rare",
    cost = 2,
    const = dict(
        BLOCK = 0,
        DAMAGE = 0,
    ),
    desc = "Target an enemy. NL Exhaust a Strike or Defend from your hand and gain its effect for this combat.",
    code = """
        AbstractDungeon.actionManager.addToBottom(new CombatCapsuleAction(p, this, p, m));
    """,
    upgrade_code = """
        upgradeName();
        initializeDescription();
    """,
    methods = """
        public void initializeDescription() {
            String desc = "";
            if (baseDamage <= 0 && baseBlock <= 0)
                desc += "Target an enemy. ";
            if (baseBlock > 0)
                desc += "Gain !B! Block. ";
            if (baseDamage > 0)
                desc += "Deal !D! damage. ";
            desc += "NL Exhaust a ";
            if (!upgraded)
                desc += "random ";
            desc += "Strike or Defend from your hand and gain its effect for this combat.";
            rawDescription = desc;
            super.initializeDescription();
        }
    """,
)
Java(
    # NOTE: correctly consumes Lightsaber stats
    path = "fruitymod.actions.unique.CombatCapsuleAction",
    base = "ChooseCardActionBase",
    code = """
        private AbstractCard capsule;
        private AbstractPlayer p;
        private AbstractMonster m;
        public CombatCapsuleAction(final AbstractCreature source, AbstractCard capsule, AbstractPlayer p, AbstractMonster m) {
            super(source, 1, "Exhaust", false, false, !capsule.upgraded);
            this.capsule = capsule;
            this.p = p;
            this.m = m;
            actionType = AbstractGameAction.ActionType.EXHAUST;
            // duration = Settings.ACTION_DUR_FAST;
        }

        @Override
        public boolean cardFilter(AbstractCard card) {
            return p.hand.contains(card) && card.rarity == AbstractCard.CardRarity.BASIC && (card.name.startsWith("Strike") || card.name.startsWith("Defend"));
        }
        @Override
        public void cardChosen(AbstractCard card) {
            SpireUtils.exhaust(card);

            if (card.baseDamage > 0) {
                capsule.baseDamage += card.baseDamage;
                capsule.upgradedDamage = true;
            }
            if (card.baseBlock > 0) {
                capsule.baseBlock += card.baseBlock;
                capsule.upgradedBlock = true;
            }
        }

        @Override
        public void finish() {
            super.finish();

            capsule.calculateCardDamage(m);
            capsule.initializeDescription();
            if (capsule.baseBlock > 0)
                AbstractDungeon.actionManager.addToBottom(new GainBlockAction(p, p, capsule.block));
            if (capsule.baseDamage > 0)
            AbstractDungeon.actionManager.addToBottom(
                new DamageAction(m, new DamageInfo(p, capsule.damage, capsule.damageTypeForTurn), AbstractGameAction.AttackEffect.SLASH_HEAVY)
            );
        }
    """,
)
# weak. it's a horrible true grit
