"""Generate the sources chart (docs/sources.svg, docs/sources-compact.svg): what the
asteroid-mining pipeline's numbers rest on, one bar for each domain of General_Research's
registry, the most sources first.

Each bar is split by the registry's tiers of authority, from T1 (peer-reviewed papers) to
T4 (grey sources: company documents, price pages, news, my audit records); the three cited tiers are steps
of one blue, brightest for the most authoritative, and T4 is drawn hollow, so the tiers
read apart without colour too. Beside each bar, its count.

The numbers are refresh_counts.py's, read from General_Research's sources.csv and kept in
tools/counts.json ("research"), so this draws the same thing until they change. When the
chart loads the bars grow from the left, a row at a time; with reduced motion they are
drawn finished.

`sources.svg` is for desktop widths, all the domains in two columns. `sources-compact.svg`
shows the ten largest with larger text and counts the rest, for phones; the README swaps
it in with <picture>.
"""
import html
import json
import re
import sys
from pathlib import Path

import panel

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
BLUE, TEXT, DIM, LABEL = "#5ba3dc", "#dbe3f5", "#7d8fb3", "#b9c6e4"
SMALL = panel.SMALL

# T1 to T3: one blue, lighter for more authority (checked for separation against the
# panel's navy, as the dataviz palette validator does); T4 is hollow.
TIERS = (("T1", "journal papers", "#d2e9fb"), ("T2", "agency reports", "#6aaee6"),
         ("T3", "government data", "#3474b8"), ("T4", "grey sources", None))
# How the profile names a few domains; the rest are named from their folder.
NAMES = {
    "02_composition_value": "Composition and value",
    "03_dv_propulsion": "Δv and propulsion",
    "06_commodity_market_pricing": "Commodity prices",
    "07_mission_program_costs": "Mission and program costs",
    "08_nea_accessibility_oracles": "NEA accessibility",
    "09_delivery_mass_fractions_edl_survival": "Delivery and EDL survival",
    "10_launch_vehicle_engine_hardware": "Launch vehicles, engines",
    "11_spacecraft_power_electric_propulsion": "Electric propulsion",
    "12_destination_environments_physical_constants": "Destination environments",
    "13_astrodynamics_methods_ephemerides_software": "Astrodynamics software",
    "14_propellant_consumable_prices": "Propellant prices",
    "15_inspace_demand_market_absorption": "In-space demand",
    "16_reliability_learning_service_life": "Reliability, service life",
    "17_cost_of_capital_contingency_insurance": "Capital and insurance",
    "18_licensing_planetary_protection_space_law": "Licensing and space law",
    "19_asteroid_excavation_beneficiation": "Excavation, beneficiation",
    "20_mission_operations_communications": "Operations and comms",
    "21_mass_cost_estimating_relationships": "Mass and cost estimates",
    "22_prior_art_techno_economic_benchmarks": "Earlier economic studies",
    "23_cost_indices_dollar_years": "Cost indices",
    "24_aerocapture_aerobraking": "Aerocapture, aerobraking",
    "25_net_smelter_return_refining_terms": "Refining terms",
    "26_spacecraft_storage_energy_properties": "Storage and energy",
    "27_orbital_debris_collision_risk": "Orbital debris",
    "28_radiation_shielding_value_of_materials": "Radiation shielding",
    "29_structural_metals_inspace_manufacturing": "In-space manufacturing",
    "30_volatiles_chemicals_catalysts_inspace_use": "Volatiles and chemicals",
}
COMPACT_ROWS = 10


def label(domain):
    """'04_launch_economics' -> 'Launch economics', unless NAMES says otherwise."""
    if domain in NAMES:
        return NAMES[domain]
    words = re.sub(r"^\d+_", "", domain).replace("inspace", "in-space").split("_")
    return " ".join(words).capitalize()


def ranked(rows):
    """The domains, the most sources first; a tie keeps the registry's order."""
    return sorted(rows, key=lambda r: -sum(r["tiers"]))


def share(rows, tiers):
    """The percentage of all sources in the given tiers (indexes into TIERS)."""
    return 100 * sum(r["tiers"][t] for r in rows for t in tiers) / sum(sum(r["tiers"]) for r in rows)


def biggest(rows):
    """What the README says of the largest domain: its size and the tier it leans on."""
    top = ranked(rows)[0]
    n, k = sum(top["tiers"]), max(range(len(TIERS)), key=lambda t: top["tiers"][t])
    lean = "mostly" if top["tiers"][k] * 2 > n else "largely"
    name = label(top["domain"])
    name = name if name[:2].isupper() else name[0].lower() + name[1:]     # "NEA accessibility" keeps its capitals
    return f"The biggest, {name} with {n}, is {lean} {TIERS[k][1]} ({top['tiers'][k]})."


ROWS = json.loads((Path(__file__).parent / "counts.json").read_text(encoding="utf-8"))["research"]
TOTAL = sum(sum(r["tiers"]) for r in ROWS)
ALT = (f"What the asteroid-mining pipeline's numbers rest on: {TOTAL:,} sources in General_Research, "
       f"in {len(ROWS)} domains, by tier (T1 journal papers, T2 agency reports, T3 government data, T4 grey sources): "
       + "; ".join(f"{label(r['domain'])} {sum(r['tiers'])} ("
                   + ", ".join(f"{n} {TIERS[t][0]}" for t, n in enumerate(r["tiers"]) if n) + ")" for r in ranked(ROWS))
       + ".")


def background(w, h, seed):
    return panel.background(w, h, seed, ALT, rules=panel.GROW, animated=("grow",))


def swatch(x, y, s, tier):
    colour = TIERS[tier][2]
    if colour:
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" rx="2" fill="{colour}"/>'
    return (f'<rect x="{x + 0.75:.1f}" y="{y + 0.75:.1f}" width="{s - 1.5:.1f}" height="{s - 1.5:.1f}" rx="2" '
            f'fill="{DIM}" fill-opacity="0.15" stroke="{DIM}" stroke-width="1.5"/>')


def bar(x, y, h, counts, unit):
    """One row's stacked segments, T1 first, with a 2px gap of the panel between them."""
    parts, at = [], x
    for t, n in enumerate(counts):
        if not n:
            continue
        w = n * unit
        drawn = max(w - 2, 1.5)
        colour = TIERS[t][2]
        if colour:
            parts.append(f'<rect x="{at:.1f}" y="{y:.1f}" width="{drawn:.1f}" height="{h:.1f}" rx="1.5" fill="{colour}"/>')
        else:
            parts.append(f'<rect x="{at + 0.75:.1f}" y="{y + 0.75:.1f}" width="{max(drawn - 1.5, 0.5):.1f}" height="{h - 1.5:.1f}" '
                         f'rx="1.5" fill="{DIM}" fill-opacity="0.15" stroke="{DIM}" stroke-width="1.5"/>')
        at += w
    return parts


def render(w, seed, pad, big, size, row_gap, name_w, cols, shown, legend_rows):
    rows = ranked(ROWS)[:shown]
    per_col = -(-len(rows) // cols)
    col_gap = size * 2.4
    col_w = (w - 2 * pad - col_gap * (cols - 1)) / cols
    track = col_w - name_w - size * 2.6
    unit = track / max(sum(r["tiers"]) for r in rows)
    head = pad + big * 0.8
    legend_y = head + size * 1.6 + size * 1.25 + size * 1.5
    top = legend_y + size * 1.4 * (legend_rows - 1) + row_gap * 1.4
    rest = ranked(ROWS)[shown:]
    h = round(top + (per_col - 1) * row_gap + (row_gap * 1.2 if rest else 0) + size * 0.6 + pad)
    parts = [background(w, h, seed), f'<g font-family="{FONT}">',
             f'<text x="{pad}" y="{head:.1f}" font-size="{big}" font-weight="700" fill="{BLUE}">{TOTAL:,}</text>',
             f'<text x="{pad}" y="{head + size * 1.6:.1f}" font-size="{size}" fill="{TEXT}">'
             + ("sources behind the pipeline, by what they back and how authoritative they are" if cols > 1
                else "sources behind the pipeline") + '</text>',
             f'<text x="{pad}" y="{head + size * 2.85:.1f}" font-size="{size * SMALL:.1f}" fill="{DIM}">'
             + html.escape(f"General_Research's registry: one bar for each of its {len(ROWS)} domains, the most sources first."
                           if cols > 1 else f"The ten largest of its {len(ROWS)} domains.", quote=False) + '</text>']
    # The legend: a swatch and a name for each tier, in as many rows as it is given.
    s, per_row = size * SMALL * 0.8, -(-len(TIERS) // legend_rows)
    for t, (tier, name, _) in enumerate(TIERS):
        x = pad + (t % per_row) * (size * SMALL * 11.5)
        y = legend_y + (t // per_row) * size * 1.4
        parts.append(swatch(x, y - s * 0.9, s, t))
        parts.append(f'<text x="{x + s + size * 0.4:.1f}" y="{y:.1f}" font-size="{size * SMALL:.1f}" fill="{LABEL}">'
                     f'<tspan font-weight="700">{tier}</tspan> {name}</text>')
    for k, r in enumerate(rows):
        c, i = divmod(k, per_col)
        x = pad + c * (col_w + col_gap)
        y = top + i * row_gap
        n = sum(r["tiers"])
        parts.append(f'<text x="{x:.1f}" y="{y + size * 0.35:.1f}" font-size="{size}" fill="{LABEL}">{html.escape(label(r["domain"]))}</text>')
        parts.append(f'<g class="grow" style="animation-delay:{0.15 + 0.04 * k:.2f}s">')
        parts += bar(x + name_w, y - size * 0.36, size * 0.72, r["tiers"], unit)
        parts.append("</g>")
        parts.append(f'<text x="{x + name_w + n * unit + size * 0.4:.1f}" y="{y + size * 0.35:.1f}" font-size="{size * SMALL:.1f}" '
                     f'fill="{TEXT}">{n}</text>')
    if rest:
        y = top + (per_col - 1) * row_gap + row_gap * 1.2
        parts.append(f'<text x="{pad}" y="{y + size * 0.35:.1f}" font-size="{size * SMALL:.1f}" fill="{DIM}">'
                     f'and {len(rest)} more, with {sum(sum(r["tiers"]) for r in rest)} sources between them</text>')
    parts.append("</g>\n</svg>\n")
    return panel.keep_clear("\n".join(parts))


def sentence(rows):
    """The README's sentence above the chart, after its first: the share in the top two
    tiers and the largest domain, from the numbers."""
    return f"{share(rows, (0, 1)):.0f}% are T1 or T2. {biggest(rows)}"


def update_readme(readme):
    """The README with this chart's alt text written in, and the sentences above it saying
    the total and what the chart shows of it. refresh_counts.py calls it after refreshing the
    counts; check.py checks it."""
    readme = panel.write_alt(readme, "sources.svg", ALT)
    readme, n = re.subn(r"(\*\*What it rests on\.\*\* The )[\d,]+( sources in General_Research, in )\d+( domains[^.]*\. )[^\n]*",
                        lambda m: f"{m[1]}{TOTAL:,}{m[2]}{len(ROWS)}{m[3]}{sentence(ROWS)}", readme)
    if n != 1:
        sys.exit(f"README's sentences above the sources chart matched {n} times, expected 1")
    return readme


def files():
    return {
        "sources.svg": render(1200, 51, 40, 52, 17, 27, 232, 2, len(ROWS), 1),
        "sources-compact.svg": render(680, 52, 36, 60, 24, 40, 300, 1, COMPACT_ROWS, 2),
    }


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for file, svg in files().items():
        (out / file).write_text(svg, encoding="utf-8", newline="\n")
        print(file)


if __name__ == "__main__":
    main()
