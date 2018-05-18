from engi_mod import *

Card(
    # DESIGN NOTES:
    # fills the role of a rare high-damage attack, similiar to Glass Knife, Die Die Die
    # enables a build that turns in-combat upgrades like Invent+ and Factory into damage
    # it's rare and it costs 1 so it scales less than Searing Blow
    # not to incentivize upgrading it out of combat
    # it's easier to find an uncommon early and build around it
    name = "Golden Bullet",
    type = "attack",
    target = "enemy",
    rarity = "rare",
    cost = 1,
    const = dict(
        DAMAGE = 14,
        DAMAGE_UPGRADE = 4,
    ),
    desc = "Deal !D! damage. NL Can be upgraded any number of times.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new DamageAction((AbstractCreature)m, new DamageInfo(p, damage, damageTypeForTurn), AbstractGameAction.AttackEffect.SLASH_HORIZONTAL)
        );
    """,
    upgrade_code_FULL = """
        upgradeDamage(DAMAGE_UPGRADE);
        ++timesUpgraded;
        upgraded = true;
        name = NAME + "+" + timesUpgraded;
        initializeTitle();
    """,
    methods = """
        @Override
        public boolean canUpgrade() {
            return true;
        }
    """,
)
