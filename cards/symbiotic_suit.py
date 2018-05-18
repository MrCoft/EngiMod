from engi_mod import *

Card(
    name = "Symbiotic Suit",
    type = "power",
    target = "self",
    rarity = "rare",
    cost = 0,
    const = dict(
        LIFE_COST = 8,
        HEAL = 4,
        HEAL_UPGRADE = 2,
        MAGIC_NUMBER = "HEAL",
    ),
    desc = "Lose 8 Max HP. NL At the end of your turn, heal !M! HP.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new MaxHPAction(-LIFE_COST)
        );
        AbstractDungeon.actionManager.addToBottom(
            new ApplyPowerAction(p, p, new SymbioticSuitPower(p, magicNumber), magicNumber)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeMagicNumber(HEAL_UPGRADE);
    """
)
Action(
    id = "MaxHPAction",
    args = """
        int amount
    """,
    code = """
        AbstractCreature player = AbstractDungeon.player;
        if (amount > 0) {
            player.increaseMaxHp(amount, false);
        } else {
            player.decreaseMaxHealth(-amount);
        }

        player.damageFlash = true;
        player.damageFlashFrames = 4;
        AbstractDungeon.effectList.add(new FlashAtkImgEffect(player.hb.cX, player.hb.cY, AbstractGameAction.AttackEffect.NONE));
        // NOTE: vfx, not working anyway

        isDone = true;
    """,
)
Power(
    name = "Symbiotic Suit",
    desc = [
        "At the end of your turn, heal #b",
        " HP."
    ],
    desc_expr = "DESCRIPTIONS[0] + amount + DESCRIPTIONS[1]",
    code = """
        @Override
        public void atEndOfTurn(final boolean isPlayer) {
            flash();
            AbstractDungeon.actionManager.addToBottom(
                new HealAction(owner, owner, amount)
            );
        }
    """,
    icon = "armor",
)
