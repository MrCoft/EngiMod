from engi_mod import *

Card(
    name = "Rapid Fire",
    type = "power",
    target = "self",
    rarity = "rare",
    cost = 3,
    const = dict(
        COST_UPGRADE = 1,
        AMOUNT = 1,
        MAGIC_NUMBER = "AMOUNT",
    ),
    desc = 'Attack cards containing "Round" cost 1 less [R].',
    upgrade_code = """
        upgradeName();
        upgradeBaseCost(COST_UPGRADE);
    """,
)
Power(
    name = "Rapid Fire",
    desc = [
        '#yAttack cards containing #y"Round" cost #b',
        " less energy.",
    ],
    desc_expr = "DESCRIPTIONS[0] + amount + DESCRIPTIONS[1]",
    init = """
        type = AbstractPower.PowerType.BUFF;
        isTurnBased = false;
        priority = 90;
        img = FruityMod.getEnigmaPowerTexture();

        map = new HashMap<AbstractCard,Integer>();
        updateRounds();
    """,
    code = r"""
        HashMap<AbstractCard,Integer> map;

        @Override
        public void onInitialApplication() {
            updateRounds();
        }

        @Override
        public void onDrawOrDiscard() {
            updateRounds();
        }
        @Override
        public void stackPower(final int stackAmount) {
            amount += stackAmount;
            updateRounds();
        }

        private void updateRounds() {
            for (AbstractCard card : AbstractDungeon.player.hand.group) {
                if (RoundUtils.isRound(card)) {
                    int reduced = map.getOrDefault(card, 0);
                    card.modifyCostForCombat(reduced - amount);
                    map.put(card, amount);
                }
            }
        }
    """,
)
# op i think, nerf to
# The first 1(2) Attack cards containing "Round" you play each turn cost 1 less [R].
