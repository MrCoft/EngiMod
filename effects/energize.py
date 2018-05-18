from engi_mod import *

Power(
    id = "EngiEnergized",
    name = "Energized",
    desc = [
        "Draw an additional card and gain [G] at the start of your next",
        " turn.",
        " #b",
        " turns."
    ],
    desc_CODE = """
        if (amount == 1) {
            description = DESCRIPTIONS[0] + DESCRIPTIONS[1];
        }
        else {
            description = DESCRIPTIONS[0] + DESCRIPTIONS[2] + amount + DESCRIPTIONS[3];
        }
    """,
    init = 'img = ImageMaster.loadImage("images/powers/32/outmaneuver.png");',
    code = """
        @Override
        public void onEnergyRecharge() {
            AbstractDungeon.actionManager.addToBottom(new DrawCardAction(owner, 1));
            AbstractDungeon.player.gainEnergy(1);

            if (amount == 0) {
                AbstractDungeon.actionManager.addToBottom(new RemoveSpecificPowerAction(owner, owner, POWER_ID));
            }
            else {
                AbstractDungeon.actionManager.addToBottom(new ReducePowerAction(owner, owner, POWER_ID, 1));
            }
        }
    """,
)
