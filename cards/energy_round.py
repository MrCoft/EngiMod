from engi_mod import *

Card(
    name = "Energy Round",
    type = "attack",
    target = "enemy",
    rarity = "uncommon",
    cost = 2,
    const = dict(
        DAMAGE = 15,
        DAMAGE_UPGRADE = 5,
    ),
    desc = "Deal !D! damage. NL Energize.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new DamageAction(m, new DamageInfo(p, damage, damageTypeForTurn), AbstractGameAction.AttackEffect.SLASH_HEAVY)
        );
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(p, p, new EngiEnergizedPower(p, 1), 1)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeDamage(DAMAGE_UPGRADE);
    """,
)
