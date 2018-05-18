package fruitymod.powers;
import com.megacrit.cardcrawl.powers.AbstractPower;
import com.megacrit.cardcrawl.monsters.AbstractMonster;
import com.megacrit.cardcrawl.core.*;
import com.megacrit.cardcrawl.dungeons.*;
import com.megacrit.cardcrawl.localization.*;
import com.megacrit.cardcrawl.helpers.*;
import com.megacrit.cardcrawl.actions.common.*;
import com.megacrit.cardcrawl.actions.*;
import com.megacrit.cardcrawl.cards.*;
import com.megacrit.cardcrawl.cards.colorless.*;
import com.megacrit.cardcrawl.powers.*;
import com.megacrit.cardcrawl.vfx.*;
import com.megacrit.cardcrawl.vfx.combat.*;
import com.megacrit.cardcrawl.actions.AbstractGameAction;
import com.megacrit.cardcrawl.cards.DamageInfo;
import java.util.*;

import fruitymod.FruityMod;
import fruitymod.cards.*;
import fruitymod.actions.unique.*;
import fruitymod.*;

public class {{ id }}
extends AbstractPower {
    public static final String POWER_ID = "{{ name }}";
	public static final String NAME = "{{ name }}";
	public static final String[] DESCRIPTIONS = new String[] {
        {{ textwrap.indent(",\n".join(map(json.dumps, desc)), " " * 4 * 2).lstrip() }}
	};

    public {{ id }}(AbstractCreature owner, int amount) {
        ID = POWER_ID;
        name = NAME;
        this.owner = owner;
        this.amount = amount;
        updateDescription();
        {% if icon -%}
        loadRegion("{{ icon }}");
        {% endif -%}
        {{ textwrap.indent(init, " " * 4 * 2).lstrip() if init else "" }}
    }

    @Override
    public void updateDescription() {
        {{ desc_code }};
    }

    {{ textwrap.indent(code, " " * 4).lstrip() }}
}
