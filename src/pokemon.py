from evolutions import get_evolutions
from emoji import typing_emoji, stats_rating_emoji
from misc import get_abilities, get_gender_percentage, stat_abbr


def get_base_data(pk, pkmn_data, species, extra_data):
    name = species.names[7].name
    artwork_link = pkmn_data.sprites.front_default.replace("pokemon", "pokemon/other/official-artwork")
    dex_number = species.order
    types = [ty.type.name.title() for ty in pkmn_data.types]
    types_text = " / ".join(types)
    emoji = typing_emoji(types[0])
    abilities = get_abilities(pkmn_data)
    abilities_text = " / ".join(abilities["abilities"])
    hidden_ability = abilities["hidden_ability"] if abilities["hidden_ability"] else "---"
    evolution_text = get_evolutions(pk, species)
    stats = {stat.stat.name: stat.base_stat for stat in pkmn_data.stats}
    rating = stats_rating_emoji(stats)
    genus = species.genera[7].genus
    height = str(pkmn_data.height / 10) + " m"
    weight = str(pkmn_data.weight / 10) + " kg"
    text = f"""<b><u>{name}</u></b> <a href="{artwork_link}">{emoji}</a>
<b>Species</b>: {genus}
<b>National Dex number</b>: {dex_number}
<b>Type</b>: {types_text}
<b>Abilities</b>: {abilities_text}
<b>Hidden Ability</b>: {hidden_ability}
<b>Height</b>: {height}
<b>Weight</b>: {weight}

<b><u>Evolutions</u></b>
{evolution_text}
{extra_data}
<b><u>Base stats</u></b>
{stats["hp"]} HP {rating["hp"]}
{stats["attack"]} ATK {rating["attack"]}
{stats["defense"]} DEF {rating["defense"]}
{stats["special-attack"]} SPA {rating["special-attack"]}
{stats["special-defense"]} SPD {rating["special-defense"]}
{stats["speed"]} SPE {rating["speed"]}
    """
    return text


def get_advanced_data(pkmn_data, species):
    gender_percentage = get_gender_percentage(species)
    base_friendship = species.base_happiness
    ev_yield = {stat_abbr(stat.stat.name): stat.effort for stat in pkmn_data.stats if stat.effort != 0}
    ev_yield_text = " / ".join([str(ev_yield[stat]) + " " + stat for stat in ev_yield])
    catch_rate = species.capture_rate
    growth_rate = species.growth_rate.name.title().replace("-", " ")
    egg_groups = [group.name.title().replace("-", " ") for group in species.egg_groups]
    egg_groups_text = " / ".join(egg_groups)
    egg_cycles = species.hatch_counter
    text = f"""\n<b><u>Games data</u></b>
<b>Gender (male/female)</b>: {gender_percentage}
<b>Base friendship</b>: {base_friendship}
<b>EV yield</b>: {ev_yield_text}
<b>Catch rate</b>: {catch_rate}
<b>Growth rate</b>: {growth_rate}
<b>Egg groups</b>: {egg_groups_text}
<b>Egg cycles</b>: {egg_cycles}
"""
    return text


def pokemon_text(pk, pkmn, expanded):
    pkmn_data = pk.get_pokemon(pkmn)
    species = pk.get_pokemon_species(pkmn)
    extra_data = get_advanced_data(pkmn_data, species) if expanded else ""
    return get_base_data(pk, pkmn_data, species, extra_data)
