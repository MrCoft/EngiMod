package {{ ".".join(package) }};

import com.megacrit.cardcrawl.cards.*;
import com.megacrit.cardcrawl.cards.AbstractCard;
import com.megacrit.cardcrawl.characters.*;
import com.megacrit.cardcrawl.monsters.*;
import com.megacrit.cardcrawl.core.*;
import com.megacrit.cardcrawl.dungeons.*;
import com.megacrit.cardcrawl.actions.common.*;
import com.megacrit.cardcrawl.actions.*;
import com.megacrit.cardcrawl.actions.utility.*;
import com.megacrit.cardcrawl.localization.*;
import com.megacrit.cardcrawl.core.CardCrawlGame;
import com.megacrit.cardcrawl.cards.DamageInfo;
import com.megacrit.cardcrawl.powers.*;
import com.megacrit.cardcrawl.vfx.*;
import com.megacrit.cardcrawl.vfx.cardManip.*;
import com.megacrit.cardcrawl.relics.*;

import fruitymod.FruityMod;
import fruitymod.patches.AbstractCardEnum;
import fruitymod.cards.*;
import fruitymod.powers.*;
import fruitymod.actions.unique.*;
import fruitymod.actions.*;
import fruitymod.*;
import com.badlogic.gdx.*;
import org.apache.logging.log4j.*;
import java.util.*;
import com.badlogic.gdx.math.*;

public class {{ name }}
{% if base -%}
extends {{ base }}
{% endif -%}
{
    {{ textwrap.indent(code, " " * 4).lstrip() }}
}
