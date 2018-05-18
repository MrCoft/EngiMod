from engi_mod import *

Card(
    # DESIGN NOTES:
    # Rounds are Shivs which you have to draw and pay for
    # Ammo Crate at 0 made for a free decision whether you want these in your deck
    # you could "decide" using Recover, still, I'd rather you decide with your energy as well
    # BALANCE NOTES:
    # card draw is 3 cards for 1 energy (Backflip, Acrobatics, Battle Trance)
    # All-Out Attack (1.67) deals 25% more than Dagger Spray (1.33)
    # 1 buys ~11 damage (Twin Strike, Wild Strike), 2 buys ~17 damage (Predator, Carnage)
    # 3 could buy ~26 damage at common (Bludgeon)
    # picking Ammo Crate puts two Rounds into your deck
    # and a card that makes you lose 1 card draw and 1 energy, a loss of 1.33
    # meaning each Round is worth 1.0 + 0.33 (its draw cost) + 0.67 (half of Ammo Crate)
    # = 2.0 energy, 17 damage
    # or - it's like you put in 2 Rounds and a Curse and pay 1 more mana
    # if Flying Knee, Dagger Throw and basic Strike deal 23 damage and have extra effects
    # 2 Rounds should deal at least 26
    # LATEST DECISION:
    # it's 26 + bonus effects. 11+ on attack would make it a Wild Strike, which has a downside
    # thus it's 15 / Round
    name = "Round",
    type = "attack",
    target = "enemy",
    rarity = "special",
    cost = 1,
    const = dict(
        DAMAGE = 15,
        DAMAGE_UPGRADE = 6,
    ),
    flags = dict(
        exhaust = "true",
    ),
    desc = "Deal !D! damage. NL Exhaust.",
    code = """
        AbstractDungeon.actionManager.addToBottom(
            new DamageAction((AbstractCreature)m, new DamageInfo(p, damage, damageTypeForTurn), AbstractGameAction.AttackEffect.SLASH_HORIZONTAL)
        );
    """,
    upgrade_code = """
        upgradeName();
        upgradeDamage(DAMAGE_UPGRADE);
    """,
)
Java(
    path = "fruitymod.RoundUtils",
    code = r"""
        public static boolean isRound(AbstractCard card) {
            if (!card.type.equals(AbstractCard.CardType.ATTACK))
                return false;
            for (String word : card.name.split("\\s+"))
                if (word.startsWith("Round"))
                    return true;
            return false;
        }
    """,
)
