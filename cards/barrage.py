from engi_mod import *

Card(
    name = "Barrage",
    type = "attack",
    target = "enemy",
    rarity = "common",
    cost = 2,
    const = dict(
        DAMAGE = 5,
        MAGIC_NUMBER = 2,
    ),
    desc = "Deal !D! damage !M! times. Apply !M! Vulnerable.",
    code = """
        for (int i = 0; i < magicNumber; ++i) {
            AbstractDungeon.actionManager.addToBottom(
                new DamageAction(m, new DamageInfo(p, damage, damageTypeForTurn), AbstractGameAction.AttackEffect.SLASH_HORIZONTAL)
            );
        }
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(m, p, new VulnerablePower(m, magicNumber, false), magicNumber)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(1);
    """
)
