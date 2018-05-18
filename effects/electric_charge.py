from engi_mod import *

Power(
    # DESIGN NOTES:
    # isn't weak every turn stupidly good though?
    name = "Electric Charge",
    desc = [
        "Next time you play an #yAttack, deal #b",
        " damage and apply #b",
        " #yWeak.",
    ],
    desc_expr = "DESCRIPTIONS[0] + 2 * amount + DESCRIPTIONS[1] + amount + DESCRIPTIONS[2]",
    init = """
        type = AbstractPower.PowerType.BUFF;
        isTurnBased = false;
        priority = 90;
        img = FruityMod.getEnigmaPowerTexture();
    """,
    code = """
        @Override
        public void onAttack(final DamageInfo info, final int damageAmount, final AbstractCreature target) {
            AbstractDungeon.actionManager.addToBottom(
                new DamageAction(target, new DamageInfo(owner, 2 * amount, DamageInfo.DamageType.THORNS), AbstractGameAction.AttackEffect.SLASH_HORIZONTAL)
            );
            AbstractDungeon.actionManager.addToBottom(
                new ApplyPowerAction(target, owner, new WeakPower(target, amount, false), amount, true, AbstractGameAction.AttackEffect.NONE)
            );
        }
        @Override
        public void onAfterCardPlayed(final AbstractCard card) {
            if (card.type == AbstractCard.CardType.ATTACK) {
                flash();
                AbstractDungeon.actionManager.addToBottom(new RemoveSpecificPowerAction(owner, owner, POWER_ID));
            }
        }

        @Override
        public void atEndOfTurn(boolean isPlayer) {
            AbstractDungeon.actionManager.addToBottom(new RemoveSpecificPowerAction(owner, owner, POWER_ID));
        }
    """,
)
