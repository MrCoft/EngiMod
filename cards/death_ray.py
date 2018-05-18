from engi_mod import *

Card(
    name = "Death Ray",
    # comparison to Bludgeon:
    # - exhausts
    # - doesn't kill attacking enemies immediately
    # - overkills small enemies, requiring another source of Vulnerable to make Death Pulse free
    # - bad against Artifact
    # - Time Eater stacks
    # + always Vulnerable
    type = "skill",
    target = "enemy",
    rarity = "rare",
    cost = 3,
    const = dict(
        VULNER_STACKS = 6,
        PULSE_NUM = 2,
    ),
    flags = dict(
        exhaust = "true",
    ),
    desc = "Apply 6 Vulnerable. NL Shuffle 2 Death Pulses into your draw pile. Exhaust.",
    upgrade_desc = "Apply 8 Vulnerable. NL Shuffle 3 Death Pulses into your draw pile. Exhaust.",
    code = """
        int stacks = VULNER_STACKS;
        int cards = PULSE_NUM;
        if (upgraded) {
            stacks += 2;
            cards += 1;
        }
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(m, p, new VulnerablePower(m, stacks, false), stacks)
        );
        AbstractDungeon.actionManager.addToBottom(
            new MakeTempCardInDrawPileAction(p, p, new DeathPulse(), cards, true, true)
        );
    """,
    upgrade_code = """
        upgradeName();
        rawDescription = UPGRADE_DESCRIPTION;
        initializeDescription();
    """
)
Card(
    name = "Death Pulse",
    type = "attack",
    target = "enemy",
    rarity = "special",
    cost = 2,
    const = dict(
        DAMAGE = 14,
        DAMAGE_UPGRADE = 6,
    ),
    flags = dict(
        exhaust = "true",
    ),
    desc = "Deal !D! damage. If the target is Vulnerable, gain [R] [R] and draw 1 card. Exhaust.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new DeathPulseAction(m)
        );
        AbstractDungeon.actionManager.addToBottom(
            new DamageAction(m, new DamageInfo(p, damage, damageTypeForTurn), AbstractGameAction.AttackEffect.BLUNT_HEAVY)
        );
    """,
    upgrade_code_FULL = """
        upgradeName();
        upgradeDamage(DAMAGE_UPGRADE);
    """
)
Action(
    id = "DeathPulseAction",
    args = """
        AbstractCreature target
    """,
    flags = dict(
        duration = "Settings.ACTION_DUR_XFAST",
        actionType = "ActionType.BLOCK",
    ),
    code = """
        if (target != null && target.hasPower("Vulnerable")) {
            AbstractDungeon.actionManager.addToTop(new DrawCardAction(AbstractDungeon.player, 1));
            AbstractDungeon.actionManager.addToTop(new GainEnergyAction(2));
        }
        isDone = true;
    """,
)
