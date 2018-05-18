from engi_mod import *

Card(
    name = "Last Round",
    type = "attack",
    target = "enemy",
    rarity = "common",
    cost = 1,
    const = dict(
        DAMAGE = 12,
        DAMAGE_UPGRADE = 5,
    ),
    desc = "Deal !D! damage. NL Gain 1 Weak.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new DamageAction(m, new DamageInfo(p, damage, damageTypeForTurn), AbstractGameAction.AttackEffect.SLASH_HEAVY)
        );
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(p, p, new WeakPower(p, 1, false), 1)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeDamage(DAMAGE_UPGRADE);
    """,
)
