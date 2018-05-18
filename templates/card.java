package fruitymod.cards;

import basemod.abstracts.CustomCard;

import com.megacrit.cardcrawl.cards.*;
import com.megacrit.cardcrawl.characters.*;
import com.megacrit.cardcrawl.monsters.*;
import com.megacrit.cardcrawl.core.*;
import com.megacrit.cardcrawl.dungeons.*;
import com.megacrit.cardcrawl.actions.common.*;
import com.megacrit.cardcrawl.actions.*;
import com.megacrit.cardcrawl.actions.utility.*;
import com.megacrit.cardcrawl.actions.unique.*;
import com.megacrit.cardcrawl.localization.*;
import com.megacrit.cardcrawl.core.CardCrawlGame;
import com.megacrit.cardcrawl.cards.DamageInfo;
import com.megacrit.cardcrawl.powers.*;

import fruitymod.FruityMod;
import fruitymod.patches.AbstractCardEnum;
import fruitymod.cards.*;
import fruitymod.powers.*;
import fruitymod.actions.unique.*;

public class {{ name_id(name) }}
extends CustomCard {
    public static final String ID = "{{ name }}";
    private static final CardStrings cardStrings = CardCrawlGame.languagePack.getCardStrings(ID);
    public static final String NAME = cardStrings.NAME;
    public static final String DESCRIPTION = cardStrings.DESCRIPTION;
    {% if upgrade_desc -%}
    public static final String UPGRADE_DESCRIPTION = cardStrings.UPGRADE_DESCRIPTION;
    {% endif -%}
    private static final int COST = {{ cost }};
    {% for name, value in const.items() if name not in "MAGIC_NUMBER".split() -%}
    private static final {{ "int" }} {{ name }} = {{ json.dumps(value) }};
    {% endfor -%}
    private static final int POOL = {{ 1 if rarity != "special" else 0}};

    public {{ name_id(name) }}() {
        super(ID, NAME, FruityMod.makePath(FruityMod.{{ name_id(name, upper=True) }}), COST, DESCRIPTION,
        		AbstractCard.CardType.{{ type.upper() }}, AbstractCardEnum.PURPLE,
        		AbstractCard.CardRarity.{{ rarity.upper() }}, AbstractCard.CardTarget.{{ (target if target != "all_enemies" else "all_enemy").upper() }}, POOL);
        {% for name, value in flags.items() -%}
        {{ name }} = {{ value }};
        {% endfor -%}
        {% if "DAMAGE" in const and const.get("MAGIC_NUMBER") != "DAMAGE" -%}
        baseDamage = DAMAGE;
        {% endif -%}
        {% if "BLOCK" in const -%}
        baseBlock = BLOCK;
        {% endif -%}
        {% if "MAGIC_NUMBER" in const -%}
        magicNumber = baseMagicNumber = {{ const["MAGIC_NUMBER"] }};
        {% endif -%}
    }

    @Override
    public void use(AbstractPlayer p, AbstractMonster m) {
        {{ textwrap.indent(code["use"], " " * 4 * 2).lstrip() }}
    }

    @Override
    public AbstractCard makeCopy() {
        return new {{ name_id(name) }}();
    }

    @Override
    public void upgrade() {
        {{ textwrap.indent(code["upgrade"], " " * 4 * 2).lstrip() }}
    }

    {{ textwrap.indent(code["methods"], " " * 4).lstrip() }}
}
