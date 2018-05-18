from engi_mod import *

Card(
    name = "Shock",
    type = "attack",
    target = "all_enemies",
    rarity = "common",
    cost = 1,
    const = dict(
        DAMAGE = 4,
        DAMAGE_UPGRADE = 3,
    ),
    desc = "Deal !D! damage and apply 1 Weak to ALL enemies.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new DamageAllEnemiesAction(p, multiDamage, damageTypeForTurn, AbstractGameAction.AttackEffect.NONE)
        );
        for (final AbstractMonster mo : AbstractDungeon.getCurrRoom().monsters.monsters) {
            AbstractDungeon.actionManager.addToBottom(
                new ApplyPowerAction(mo, p, new WeakPower(mo, 1, false), 1, true, AbstractGameAction.AttackEffect.NONE)
            );
        }
    """,
    upgrade_code = """
        upgradeName();
        upgradeDamage(DAMAGE_UPGRADE);
    """,
)
