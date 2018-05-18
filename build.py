import utils
from utils import format
import os
import tempfile
import urllib.request
import shutil
import zipfile

spire_dir = r"D:\Games\Slay the Spire Modded"
mod_dir = os.path.join("cache", "mod")

def build():
    # STEP: clone FruityMod
    if not os.path.exists(mod_dir):
        print("Downloading {}".format("FruityMod"))
        fruity_url = r"https://github.com/gskleres/FruityMod-StS/archive/v0.6.2b.zip"
        utils.mkdir("cache")
        download_file = tempfile.NamedTemporaryFile(suffix=".zip", dir="cache", delete=False).name
        with urllib.request.urlopen(fruity_url) as response, open(download_file, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
        utils.unzip(download_file, mod_dir, shift=1, remove=True)

    # STEP: fetch libs
    mod_jar = os.path.join(spire_dir, "ModTheSpire.jar")
    if not os.path.exists(mod_jar):
        print("Downloading ModTheSpire")
        download_file = tempfile.NamedTemporaryFile(suffix=".zip", dir="..", delete=False).name
        urllib.request.urlretrieve("https://github.com/kiooeht/ModTheSpire/releases/download/v2.6.0/ModTheSpire.zip", download_file)
        with zipfile.ZipFile(download_file, "r") as archive, open(mod_jar, "wb") as file:
            jar_data = archive.read("ModTheSpire.jar")
            file.write(jar_data)
        os.remove(download_file)
    base_jar = os.path.join(spire_dir, "mods", "BaseMod.jar")
    if not os.path.exists(base_jar):
        print("Downloading BaseMod")
        urllib.request.urlretrieve("https://github.com/daviscook477/BaseMod/releases/download/v2.9.1/BaseMod.jar", base_jar)

    from spire import name_id
    import textwrap
    import io
    import json

    print("Generating data")
    image_dir = os.path.join("assets", "images")
    if os.path.exists(os.path.join("cache", "DEBUG")):
        image_dir = os.path.join("todo", "images")

    # STEP: generate cards
    from engi_mod import cards
    with open(os.path.join("templates", "card.java"), encoding="utf-8") as file:
        card_template = file.read()
    for card in cards:
        with open(os.path.join(mod_dir, *r"src\main\java\fruitymod\cards".split("\\"), name_id(card["name"]) + ".java"), "w", encoding="utf-8") as file:
            file.write(format(card_template, card))

    # STEP: patch code
    templates_cache = os.path.join("cache", "templates")
    if not os.path.exists(templates_cache):
        utils.mkdir(templates_cache)
        shutil.copy(os.path.join(mod_dir, *r"src\main\java\fruitymod\FruityMod.java".split("\\")), os.path.join(templates_cache, "FruiyMod.java"))
        shutil.copy(os.path.join(mod_dir, *r"src\main\java\fruitymod\characters\TheSeeker.java".split("\\")), os.path.join(templates_cache, "TheSeeker.java"))
        shutil.copy(os.path.join(mod_dir, *r"src\main\resources\localization\FruityMod-CardStrings.json".split("\\")), os.path.join(templates_cache, "FruityMod-CardStrings.json"))
    image_code = io.StringIO()
    add_code = io.StringIO()
    unlock_code = io.StringIO()
    for card in cards:
        id = name_id(card["name"], upper=True).lower()
        image_file = os.path.join(image_dir, id + ".png")
        image_file = "cards/{}.png".format(id if os.path.exists(image_file) else "runic_binding")
        image_code.write(format(
            'public static final String {{ name_id(card["name"], upper=True) }} = "{{ image_file }}";'
        ) + "\n")
        if card["rarity"] != "special":
            add_code.write(format(
                'BaseMod.addCard(new {{ name_id(card["name"]) }}());'
            ) + "\n")
            unlock_code.write(format(
                'UnlockTracker.unlockCard("{{ card["name"] }}");'
            ) + "\n")

    with open(os.path.join(templates_cache, "FruiyMod.java"), encoding="utf-8") as file:
        fruity_lines = [line for line in file]
    for i, line in enumerate(fruity_lines):
        if "public static final String PHASE_COIL" in line:
            fruity_lines.insert(i + 1, "\n" + textwrap.indent(image_code.getvalue(), " " * 4))
            break
    for i, line in enumerate(fruity_lines):
        if "BaseMod.addCard(new Nexus())" in line:
            fruity_lines.insert(i + 1, "\n" + textwrap.indent(add_code.getvalue(), " " * 4 * 2))
            fruity_lines.insert(i + 2, "\n" + textwrap.indent(unlock_code.getvalue(), " " * 4 * 2))
            break
    with open(os.path.join(mod_dir, *r"src\main\java\fruitymod\FruityMod.java".split("\\")), "w", encoding="utf-8") as file:
        file.write("".join(fruity_lines))

    with open(os.path.join(templates_cache, "TheSeeker.java"), encoding="utf-8") as file:
        seeker_lines = [line for line in file]
    # STEP: starting relic
    from engi_mod import relic
    for i, line in enumerate(seeker_lines):
        if "Arcanosphere" in line:
            del seeker_lines[i:i+2]
            seeker_lines.insert(i, "\n{}\n\n".format(textwrap.indent(textwrap.dedent(format("""
                retVal.add("{{ relic }}");
                UnlockTracker.markRelicAsSeen("{{ relic }}");
            """)).strip(), " " * 4 * 2)))
            break
    # STEP: starting deck
    from engi_mod import deck
    if not deck:
        deck = [card["name"] for card in cards if card["rarity"] != "special"]
    for i, line in enumerate(seeker_lines):
        if "Strike_P" in line:
            for j, line in enumerate(seeker_lines):
                if "AstralHaze" in line:
                    break
            del seeker_lines[i:j+1]
            seeker_lines.insert(i, "\n{}\n\n".format(textwrap.indent(
                    "\n".join('retVal.add("{}");'.format(card) for card in deck)
                , " " * 4 * 2)))
            break
    with open(os.path.join(mod_dir, *r"src\main\java\fruitymod\characters\TheSeeker.java".split("\\")), "w", encoding="utf-8") as file:
        file.write("".join(seeker_lines))

    card_strings = json.load(open(os.path.join(templates_cache, "FruityMod-CardStrings.json"), encoding="utf-8"))
    for card in cards:
        data = {
            "NAME": card["name"],
            "DESCRIPTION": card["desc"],
        }
        desc = card.get("upgrade_desc")
        if desc:
            data["UPGRADE_DESCRIPTION"] = desc
        card_strings[card["name"]] = data
    json.dump(card_strings,
        open(os.path.join(mod_dir, *r"src\main\resources\localization\FruityMod-CardStrings.json".split("\\")),
    "w", encoding="utf-8"), sort_keys=True, indent=4)

    # STEP: generate powers
    from engi_mod import powers
    with open(os.path.join("templates", "power.java"), encoding="utf-8") as file:
        power_template = file.read()
    for power in powers:
        with open(os.path.join(mod_dir, *r"src\main\java\fruitymod\powers".split("\\"), power["id"] + ".java"), "w", encoding="utf-8") as file:
            file.write(format(power_template, power))

    # STEP: generate actions
    from engi_mod import actions
    with open(os.path.join("templates", "action.java"), encoding="utf-8") as file:
        action_template = file.read()
    for action in actions:
        with open(os.path.join(mod_dir, *r"src\main\java\fruitymod\actions\unique".split("\\"), action["id"] + ".java"), "w", encoding="utf-8") as file:
            file.write(format(action_template, action))

    # STEP: generate java files
    from engi_mod import javas
    with open(os.path.join("templates", "java.java"), encoding="utf-8") as file:
        java_template = file.read()
    for java in javas:
        with open(os.path.join(mod_dir, *r"src\main\java".split("\\"), *java["package"], java["name"] + ".java"), "w", encoding="utf-8") as file:
            file.write(format(java_template, java))

    # STEP: card images
    print("Generating images")
    import numpy as np
    portrait_masks = {}
    for type in "attack skill power".split():
        image = utils.open_data(os.path.join("templates", "1024Portraits_{}_mask.png".format(type)))
        image = image / 255
        image = np.repeat(image[:,:,:1], 4, axis=-1)
        portrait_masks[type] = image
    for card in cards:
        id = name_id(card["name"], upper=True).lower()
        image_file = os.path.join(image_dir, id + ".png")
        target_p_file = os.path.join(mod_dir, *r"src\main\resources\img\cards".split("\\"), id + "_p" + ".png")
        target_file = os.path.join(mod_dir, *r"src\main\resources\img\cards".split("\\"), id + ".png")
        if os.path.exists(target_p_file):
            continue
        if os.path.exists(image_file):
            image = utils.open_data(image_file)

            from skimage.transform import resize
            target = 500, 380
            r = image.shape[0] / image.shape[1]
            if r >= target[0] / target[1]:
                size = np.ceil(target[1] * r).astype("int"), target[1]
                x = np.round((size[0] - target[0]) / 2).astype("int")
                image = resize(image, size, mode="edge")[x:x+target[0]]
            else:
                size = target[0], np.ceil(target[0] / r).astype("int")
                image = resize(image, size, mode="edge")[:,:target[1]]
            image *= portrait_masks[card["type"]]
            from PIL import Image
            img = Image.fromarray(np.round(image * 255).astype("uint8").transpose((1, 0, 2)))
            img.save(target_p_file)

            target = 250, 190
            image = resize(image, target, mode="edge")
            img = Image.fromarray(np.round(image * 255).astype("uint8").transpose((1, 0, 2)))
            img.save(target_file)

    # STEP: card borders
    utils.sync(os.path.join("assets", "512"), os.path.join(mod_dir, *r"src\main\resources\img\512".split("\\")))
    utils.sync(os.path.join("assets", "1024"), os.path.join(mod_dir, *r"src\main\resources\img\1024".split("\\")))

    # STEP: keywords
    from engi_mod import keywords
    keyword_code = io.StringIO()
    for name, keyword in keywords.items():
        words = ", ".join('"{}"'.format(word) for word in [name.lower()] + keyword["words"])
        keyword_code.write(format(
            'BaseMod.addKeyword(new String[] {"{{ name }}", {{ words }}}, "{{ keyword["desc"] }}");'
        ) + "\n")

    with open(os.path.join(mod_dir, *r"src\main\java\fruitymod\FruityMod.java".split("\\")), encoding="utf-8") as file:
        fruity_lines = [line for line in file]
    for i, line in enumerate(fruity_lines):
        if '{"intangible", "Intangible"}, "All damage and HP loss you suffer is reduced to 1."' in line:
            fruity_lines.insert(i + 1, "\n" + textwrap.indent(keyword_code.getvalue(), " " * 4 * 2))
            break
    with open(os.path.join(mod_dir, *r"src\main\java\fruitymod\FruityMod.java".split("\\")), "w", encoding="utf-8") as file:
        file.write("".join(fruity_lines))

    # STEP: mod info
    old_info = os.path.join(mod_dir, *r"src\main\resources\ModTheSpire.config".split("\\"))
    if os.path.exists(old_info):
        os.remove(old_info)
    from engi_mod import info
    json.dump(info, open(os.path.join(mod_dir, *r"src\main\resources\ModTheSpire.json".split("\\")), "w", encoding="utf-8"), indent=4)

    # STEP: maven project
    pom_template = os.path.join(templates_cache, "pom.xml")
    if not os.path.exists(pom_template):
        shutil.copy(os.path.join(mod_dir, "pom.xml"), pom_template)
    with open(pom_template, encoding="utf-8") as file:
        pom = file.read()
    pom = pom.replace("${basedir}/../lib/ModTheSpire.jar", "/".join(spire_dir.split(os.path.sep) + ["ModTheSpire.jar"]))
    pom = pom.replace("${basedir}/../lib/BaseMod.jar", "/".join(spire_dir.split(os.path.sep) + ["mods", "BaseMod.jar"]))
    pom = pom.replace("${basedir}/../lib/desktop-1.0.jar", "/".join(spire_dir.split(os.path.sep) + ["desktop-1.0.jar"]))
    jar_file = os.path.join(spire_dir, "mods", "EngiMod.jar")
    pom = pom.replace("../_ModTheSpire/mods/FruityMod.jar", "/".join(jar_file.split(os.path.sep)))
    with open(os.path.join(mod_dir, "pom.xml"), "w", encoding="utf-8") as file:
        file.write(pom)

    # STEP: compile
    if os.path.exists(jar_file):
        os.remove(jar_file)
    with utils.cd(mod_dir):
        os.system("mvn package")
    if not os.path.exists(jar_file):
        print("Compilation failed")
        return

    # STEP: test
    with utils.cd(spire_dir):
        os.system("ModTheSpire.jar")

if __name__ == "__main__":
    build()
