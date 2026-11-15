"""
Dynamic Crisis Generator & Mars Emergency Simulation Engine.
Implements scenario-driven planetary emergencies with duration, severity, cascading links,
countermeasures, and deterministic seed-reproducibility.
"""

import random

CRISIS_DEFINITIONS = {
    'dust_storm': {
        'id': 'dust_storm',
        'name': 'Martian Dust Storm (Regional Squall)',
        'severity': 'HIGH',
        'icon': '🌪️',
        'affected_subsystems': ['power', 'thermal'],
        'base_duration': 3,
        'drain_per_sol': {'power': 12, 'temperature': -8},
        'recommended_countermeasures': ['optimize_solar', 'deploy_rover', 'conserve_power'],
        'description': 'Atmospheric opacity spikes (Tau > 3.0). Photovoltaic yield drops sharply and sub-zero chill deepens.',
        'nasa_science': 'Martian dust particles are extremely fine (1-3 micrometers) and stay suspended in the low-density CO2 atmosphere for months, attenuating solar flux according to Beer-Lambert law.'
    },
    'solar_particle_event': {
        'id': 'solar_particle_event',
        'name': 'Coronal Mass Ejection (Class-X Solar Flare)',
        'severity': 'CATASTROPHIC',
        'icon': '☀️',
        'affected_subsystems': ['radiation_shield', 'power'],
        'base_duration': 2,
        'drain_per_sol': {'shielding': 18, 'power': 10},
        'recommended_countermeasures': ['boost_shields', 'emergency_shield'],
        'description': 'High-energy solar protons bombard Mars. Active magnetic deflector coils operate at maximum current.',
        'nasa_science': 'Mars lacks a global intrinsic dipole magnetic field, leaving surface assets exposed to Solar Energetic Particles (SPE) that can deliver lethal Sievert dosages to crew biometrics.'
    },
    'moxie_clog': {
        'id': 'moxie_clog',
        'name': 'MOXIE Intake Regolith Clog',
        'severity': 'HIGH',
        'icon': '🫁',
        'affected_subsystems': ['oxygen'],
        'base_duration': 2,
        'drain_per_sol': {'oxygen': 16},
        'recommended_countermeasures': ['boost_oxygen', 'emergency_o2'],
        'description': 'Fine electrostatic iron-oxide dust clogged the high-temperature SOEC intake filter, starving oxygen production.',
        'nasa_science': 'NASA MOXIE uses scroll compressors to compress Martian atmosphere from 0.08 psi to 1.0 bar before feeding it to zirconia electrolysis membranes operating at 800°C.'
    },
    'water_contamination': {
        'id': 'water_contamination',
        'name': 'Condenser Biofilm Contamination',
        'severity': 'MEDIUM',
        'icon': '💧',
        'affected_subsystems': ['water', 'food'],
        'base_duration': 2,
        'drain_per_sol': {'water': 15, 'food': 8},
        'recommended_countermeasures': ['deploy_drill', 'boost_food'],
        'description': 'Bacterial biofilm colonized the wastewater vapor compression distiller. Hydroponic nutrient circulation impaired.',
        'nasa_science': 'Closed-loop spacecraft water recovery systems (like ISS and Artemis Mars transit) recycle 98% of moisture from humidity condensate and crew sweat using catalytic oxidizers.'
    },
    'greenhouse_freeze': {
        'id': 'greenhouse_freeze',
        'name': 'Thermal Radiator Fluid Freeze',
        'severity': 'HIGH',
        'icon': '❄️',
        'affected_subsystems': ['food', 'thermal'],
        'base_duration': 2,
        'drain_per_sol': {'food': 18, 'temperature': -15},
        'recommended_countermeasures': ['emergency_rtg', 'conserve_power'],
        'description': 'Radiator heat loops froze under -65°C nocturnal chill. Hydroponic root beds approaching freezing point!',
        'nasa_science': 'Mars average surface temperature is -63°C. Without continuous RTG waste-heat recovery or electrical heaters, hydroponic water lines freeze within hours.'
    },
    'hull_puncture': {
        'id': 'hull_puncture',
        'name': 'Micrometeoroid Hull Breach',
        'severity': 'CATASTROPHIC',
        'icon': '💥',
        'affected_subsystems': ['habitat_integrity', 'oxygen'],
        'base_duration': 2,
        'drain_per_sol': {'integrity': 20, 'oxygen': 12},
        'recommended_countermeasures': ['boost_oxygen', 'emergency_o2'],
        'description': 'Hypervelocity space rock punctured habitat dome outer multilayer insulation (MLI). Pressure seal integrity compromised.',
        'nasa_science': 'Due to Mars thin atmosphere (1% of Earth), micrometeoroids reach the ground without burning up, requiring Kevlar-reinforced Whipple shielding.'
    }
}

def generate_crisis_for_sol(level, sol, seed=None):
    """
    Deterministically generates or evaluates active crises based on level progression and optional seed.
    Returns list of active crisis objects.
    """
    if seed is not None:
        rng = random.Random(seed + sol * 100 + level)
    else:
        rng = random.Random(sol * 37 + level * 101)

    active_crises = []

    # Scripted historical crises to ensure level narrative benchmarks
    if level == 1:
        if sol == 4:
            active_crises.append(CRISIS_DEFINITIONS['dust_storm'])
        elif sol == 8:
            active_crises.append(CRISIS_DEFINITIONS['moxie_clog'])
    elif level == 2:
        if sol == 4:
            active_crises.append(CRISIS_DEFINITIONS['dust_storm'])
        elif sol == 9:
            active_crises.append(CRISIS_DEFINITIONS['water_contamination'])
        elif sol == 13:
            active_crises.append(CRISIS_DEFINITIONS['greenhouse_freeze'])
    elif level == 3:
        # Simultaneous double crises
        if sol == 5:
            active_crises.extend([CRISIS_DEFINITIONS['solar_particle_event'], CRISIS_DEFINITIONS['dust_storm']])
        elif sol == 11:
            active_crises.extend([CRISIS_DEFINITIONS['moxie_clog'], CRISIS_DEFINITIONS['water_contamination']])
        elif sol == 16:
            active_crises.extend([CRISIS_DEFINITIONS['greenhouse_freeze'], CRISIS_DEFINITIONS['hull_puncture']])
    elif level == 4:
        # Apocalypse Protocol: Extreme cascading double/triple emergencies
        if sol == 6:
            active_crises.extend([CRISIS_DEFINITIONS['dust_storm'], CRISIS_DEFINITIONS['greenhouse_freeze']])
        elif sol == 14:
            active_crises.extend([CRISIS_DEFINITIONS['solar_particle_event'], CRISIS_DEFINITIONS['moxie_clog']])
        elif sol == 21:
            active_crises.extend([CRISIS_DEFINITIONS['hull_puncture'], CRISIS_DEFINITIONS['water_contamination']])
        elif sol == 27:
            active_crises.extend([CRISIS_DEFINITIONS['solar_particle_event'], CRISIS_DEFINITIONS['dust_storm']])

    return active_crises
