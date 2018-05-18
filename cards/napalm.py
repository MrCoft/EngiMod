from engi_mod import *

Card(
    name = "Napalm",
    type = "attack",
    target = "all_enemies",
    rarity = "uncommon",
    cost = "x",
    const = dict(
        DAMAGE = 5,
    ),
    flags = dict(
        exhaust = "true",
    ),
    desc = "Spend all [R]. Deal !D! damage to a random enemy X times, it loses 1 Strength each time. Exhaust.",
    upgrade_desc = "Spend all [R]. Deal !D! damage to a random enemy X+1 times, it loses 1 Strength each time. Exhaust.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new NapalmAction(p, m, damage, upgraded, damageTypeForTurn, freeToPlayOnce, energyOnUse)
        );
    """,
    upgrade_code = """
        upgradeName();
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """
)
Action(
    id = "NapalmAction",
    args = """
        AbstractPlayer p
        AbstractMonster m
        int damage
        boolean upgraded
        DamageInfo.DamageType damageTypeForTurn
        boolean freeToPlayOnce
        int energyOnUse
    """,
    flags = dict(
        duration = "Settings.ACTION_DUR_XFAST",
        actionType = "AbstractGameAction.ActionType.SPECIAL",
    ),
    code = """
        int effect = EnergyPanel.totalCount;
        if (energyOnUse != -1) {
            effect = energyOnUse;
        }
        if (upgraded) {
            ++effect;
        }
        if (effect > 0) {
            for (int i = 0; i < effect; ++i) {
                if (AbstractDungeon.getCurrRoom().monsters.areMonstersBasicallyDead()) {
                    AbstractDungeon.actionManager.clearPostCombatActions();
                    break;
                }
                AbstractMonster target = AbstractDungeon.getMonsters().getRandomMonster(true);
                if (target.currentHealth > 0) {
                    AbstractDungeon.actionManager.addToBottom(
                        new DamageAction((AbstractCreature)target, new DamageInfo(p, damage, damageTypeForTurn), AbstractGameAction.AttackEffect.BLUNT_LIGHT)
                    );
                    AbstractDungeon.actionManager.addToBottom(
                        new ApplyPowerAction(target, p, new StrengthPower(target, -1), -1)
                    );
                }
            }
            if (!freeToPlayOnce) {
                p.energy.use(EnergyPanel.totalCount);
            }
        }
        isDone = true;
    """,
)
