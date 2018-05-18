from engi_mod import *

Card(
    name = "Turret",
    type = "power",
    target = "self",
    rarity = "uncommon",
    cost = 1,
    const = dict(
        DAMAGE = 6,
        DAMAGE_UPGRADE = 3,
        MAGIC_NUMBER = "DAMAGE",
    ),
    desc = "At the end of your turn, deal !M! damage to a random enemy.",
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(DAMAGE_UPGRADE);
    """,
)
Power(
    name = "Turret",
    desc = [
        "At the end of your turn, deal #b",
        " damage to a random enemy."
    ],
    desc_expr = "DESCRIPTIONS[0] + amount + DESCRIPTIONS[1]",
    code = """
        @Override
        public void atEndOfTurn(final boolean isPlayer) {
            if (AbstractDungeon.getCurrRoom().monsters.areMonstersBasicallyDead()) {
                AbstractDungeon.actionManager.clearPostCombatActions();
                return;
            }
            flash();
            AbstractMonster target = AbstractDungeon.getMonsters().getRandomMonster(true);
            if (target.currentHealth > 0) {
                AbstractDungeon.actionManager.addToBottom(
                    new DamageAction((AbstractCreature)target, new DamageInfo(owner, amount, DamageInfo.DamageType.THORNS))
                );
            }
        }
    """,
    icon = "armor",
)
