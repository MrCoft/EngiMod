package fruitymod.actions.unique;
import com.megacrit.cardcrawl.actions.*;
import com.megacrit.cardcrawl.actions.common.*;
import com.megacrit.cardcrawl.cards.DamageInfo;
import com.megacrit.cardcrawl.characters.*;
import com.megacrit.cardcrawl.core.*;
import com.megacrit.cardcrawl.dungeons.*;
import com.megacrit.cardcrawl.monsters.*;
import com.megacrit.cardcrawl.relics.*;
import com.megacrit.cardcrawl.ui.panels.*;
import com.megacrit.cardcrawl.powers.*;
import com.megacrit.cardcrawl.cards.*;
import com.megacrit.cardcrawl.vfx.*;
import com.megacrit.cardcrawl.vfx.combat.*;

import fruitymod.actions.*;
import fruitymod.*;
import java.util.*;

public class {{ id }}
extends AbstractGameAction {
    {% for type, name in vars if name not in "target".split() -%}
    private {{ type }} {{ name }};
    {% endfor -%}

    public {{ id }}(
            {% for type, name in vars[:-1] -%}
            {{ type }} {{ name }},
            {% endfor -%}
            {% if vars -%}
            {{ vars[-1][0] }} {{ vars[-1][1] }}
            {% endif -%}
    ) {
        {% for type, name in vars -%}
        this.{{ name }} = {{ name }};
        {% endfor -%}
        {% for name, value in flags.items() -%}
        this.{{ name }} = {{ value }};
        {% endfor -%}
    }

    {{ textwrap.indent(code, " " * 4).lstrip() }}
}
