from engi_mod import *

Card(
    name = "Crash Land",
    type = "attack",
    target = "all_enemies",
    rarity = "rare",
    cost = 0,
    const = dict(
        SELF_DAMAGE = 10,
        DAMAGE = 17,
        DAMAGE_UPGRADE = 4,
    ),
    desc = "Take 10 damage. NL Deal !D! damage to ALL enemies.",
    code = """
        AbstractDungeon.actionManager.addToTop(
            new DamageAction(
                (AbstractCreature)AbstractDungeon.player,
                new DamageInfo(AbstractDungeon.player, SELF_DAMAGE, DamageInfo.DamageType.THORNS),
                AbstractGameAction.AttackEffect.FIRE
            )
        );
        AbstractDungeon.actionManager.addToBottom(
            new DamageAllEnemiesAction(p, multiDamage, damageTypeForTurn, AbstractGameAction.AttackEffect.NONE)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeDamage(DAMAGE_UPGRADE);
    """,
)
