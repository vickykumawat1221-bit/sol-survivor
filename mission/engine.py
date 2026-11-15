"""
Sol Survivor - Mars Mission Control Simulation Engine (Advanced Edition)
Designed for the NASA Space Apps Challenge (Ages 8-16)

Implements:
- 4-Tier Age-Adaptive Progression (Cadet -> Flight Engineer -> Mission Specialist -> Mars Base Commander)
- Interconnected Cascading Failure Engine (Thermal Regulator freeze, Voltage Sag, Radiation avionics degradation)
- Intelligent Houston Flight AI Copilot & Beginner Guidance System
- Diurnal Mars Day/Night Sol Cycle calculations
- Real NASA Telemetry & Scientific Formulas (Beer-Lambert Solar Flux, MOXIE SOEC rates, Atmospheric Tau, Sieverts)
- Crew Biometrics & Vitals Tracking (Commander, Astrobiologist, Flight Engineer, Life Support Specialist)
- Recon Rover & Ingenuity Drone Dispatch Missions (Perseverance dust-brushing, Ingenuity scout, Subsurface drill)
- Emergency Command Overrides (RTG Thermal Overclock, Hyperbaric O2 Purge, Magnetosphere Pulse)
- Dopamine gamification (XP, Clutch Survival bonuses, Ranks, NASA Credentials)
"""

import math
import random

LEVEL_CONFIGS = {
    1: {
        'name': 'Touchdown',
        'tier': 'Cadet Tier (Ages 8+)',
        'target_sols': 10,
        'initial_power': 100,
        'initial_oxygen': 100,
        'initial_food': 100,
        'initial_shielding': 100,
        'initial_water': 100,
        'initial_integrity': 100,
        'base_drain': {'power': 5, 'oxygen': 5, 'food': 4, 'shielding': 3, 'water': 3, 'integrity': 1},
        'description': 'Basic visual color-coded telemetry and forgiving single-crisis trade-offs.'
    },
    2: {
        'name': 'Red Dust',
        'tier': 'Flight Engineer Tier (Ages 10+)',
        'target_sols': 15,
        'initial_power': 80,
        'initial_oxygen': 90,
        'initial_food': 85,
        'initial_shielding': 85,
        'initial_water': 90,
        'initial_integrity': 90,
        'base_drain': {'power': 6, 'oxygen': 6, 'food': 5, 'shielding': 5, 'water': 4, 'integrity': 2},
        'description': 'Tighter initial power (80%) and unlocks multi-turn Cascading Failures.'
    },
    3: {
        'name': 'Solar Storm',
        'tier': 'Mission Specialist Tier (Ages 12+)',
        'target_sols': 20,
        'initial_power': 75,
        'initial_oxygen': 80,
        'initial_food': 75,
        'initial_shielding': 75,
        'initial_water': 85,
        'initial_integrity': 85,
        'base_drain': {'power': 7, 'oxygen': 7, 'food': 6, 'shielding': 6, 'water': 4, 'integrity': 2},
        'description': 'Simultaneous double-crises with real NASA telemetry units (kW, ppm O2, mSv).'
    },
    4: {
        'name': 'Apocalypse Protocol',
        'tier': 'Mars Base Commander Tier (Ages 14-16)',
        'target_sols': 30,
        'initial_power': 65,
        'initial_oxygen': 70,
        'initial_food': 65,
        'initial_shielding': 70,
        'initial_water': 75,
        'initial_integrity': 80,
        'base_drain': {'power': 9, 'oxygen': 8, 'food': 7, 'shielding': 7, 'water': 5, 'integrity': 3},
        'description': 'Extreme resource scarcity, full NASA telemetry math, and cascading chain reactions.'
    }
}

def compute_mars_cycle(sol):
    """Calculates diurnal cycle (Sun Elevation Angle, Sol progression)."""
    hour = (sol * 11) % 24
    if 6 <= hour < 18:
        phase = "DAY"
        elevation = round(math.sin((hour - 6) / 12 * math.pi) * 65, 1)
    else:
        phase = "NIGHT"
        elevation = -round(math.sin((hour - 18) / 12 * math.pi) * 45, 1) if hour >= 18 else -15.0

    return {
        'hour': hour,
        'phase': phase,
        'elevation_deg': elevation,
        'sol_progress': round((sol / 30.0) * 100, 1)
    }

def compute_nasa_telemetry(state):
    """Calculates live scientific NASA telemetry based on planetary and engineering models."""
    level = state.get('level', 1)
    base_tau = {1: 0.85, 2: 2.3, 3: 3.7, 4: 5.1}.get(level, 1.0)
    
    recent_logs = " ".join(state.get('log', [])[-3:])
    if "Dust Storm" in recent_logs or "Dust Squall" in recent_logs or "Vortex" in recent_logs:
        base_tau += 1.8
    
    # Solar Flux: Beer-Lambert atmospheric attenuation law: I = I_0 * exp(-tau / 2.3)
    solar_flux = round(590 * math.exp(-base_tau / 2.3), 1)
    
    # MOXIE Solid Oxide Electrolysis: Max 12.0 g/hr at 800°C
    moxie_rate = round((state.get('oxygen', 100) / 100.0) * 11.8, 2)
    o2_kpa = round(21.3 * (state.get('oxygen', 100) / 100.0), 2)
    
    # Hydroponics thermal regulation
    if state.get('temp_warning'):
        gh_temp = max(-55, 21.0 - (3 - state.get('cascade_counter', 0)) * 26.0)
    else:
        gh_temp = 21.4
        
    # Active Radiation Deflector: Background Mars GCR + SPE (~0.67 mSv/Sol)
    shield_pct = state.get('shielding', 100) / 100.0
    rad_msv = round(0.67 * (1.0 - shield_pct * 0.92), 3)
    
    # Battery reserve in kilowatt-hours
    battery_kwh = round((state.get('power', 100) / 100.0) * 1000, 1)

    return {
        'tau': round(base_tau, 2),
        'solar_flux': solar_flux,
        'moxie_rate': moxie_rate,
        'o2_kpa': o2_kpa,
        'gh_temp': round(gh_temp, 1),
        'rad_msv': rad_msv,
        'battery_kwh': battery_kwh,
        'water_liters': round((state.get('water', 100) / 100.0) * 850.0, 1),
        'integrity_pct': state.get('integrity', 100),
        'surface_temp': -63.5,
        'cycle': compute_mars_cycle(state.get('sol', 1))
    }

def compute_houston_advisor(state):
    """
    Intelligent AI Flight Copilot:
    Evaluates current telemetry and suggests optimal moves for beginners,
    with severity tags ('danger', 'warning', 'info', 'nominal').
    """
    p = state.get('power', 100)
    o = state.get('oxygen', 100)
    f = state.get('food', 100)
    s = state.get('shielding', 100)

    # 1. Thermal cascade priority
    if state.get('temp_warning'):
        counter = state.get('cascade_counter', 0)
        if counter <= 1:
            rtg_ready = not state.get('emergency_protocols', {}).get('rtg_burst', {}).get('used')
            return {
                'rec_action': 'emergency_rtg' if rtg_ready else 'boost_food',
                'title': '🚨 PIPE FREEZE IMMINENT',
                'message': 'Heaters remained off too long! Greenhouse water lines will burst NEXT SOL! Click RTG Core Overclock or avoid dimming heaters!',
                'severity': 'danger'
            }
        else:
            return {
                'rec_action': 'boost_food',
                'title': '⚠️ HEATER COOLDOWN DETECTED',
                'message': 'Heaters are dimmed. Greenhouse freezing in 2 Sols. Do not dim heaters consecutively!',
                'severity': 'warning'
            }

    # 2. Critical life-support emergencies (< 25%)
    min_val = min(p, o, f, s)
    if min_val <= 25:
        if p == min_val:
            rover_ready = state.get('rovers', {}).get('perseverance', {}).get('status') == 'READY'
            return {
                'rec_action': 'deploy_rover' if rover_ready else 'optimize_solar',
                'title': '⚡ POWER GRID CRITICAL',
                'message': 'Power below 25%! Risk of habitat blackout. Dispatch Perseverance Rover or execute OPTIMIZE SOLAR.',
                'severity': 'danger'
            }
        elif o == min_val:
            return {
                'rec_action': 'boost_oxygen',
                'title': '🫁 OXYGEN HYPOXIA RISK',
                'message': 'Oxygen below 25%! Crew SpO2 is dropping. Click 1. OVERCHARGE MOXIE to restore breathable air.',
                'severity': 'danger'
            }
        elif f == min_val:
            drill_ready = state.get('rovers', {}).get('drill', {}).get('status') == 'READY'
            return {
                'rec_action': 'deploy_drill' if drill_ready else 'boost_food',
                'title': '🌱 CROP STARVATION ALERT',
                'message': 'Food reserves below 25%! Click 2. HYDROPONIC UV or dispatch Subsurface Drill for water ice.',
                'severity': 'danger'
            }
        else:
            return {
                'rec_action': 'boost_shields',
                'title': '🛡️ RADIATION BREACH RISK',
                'message': 'Radiation shield below 25%! Cosmic rays penetrating hull. Click 3. CHARGE DEFLECTOR.',
                'severity': 'danger'
            }

    # 3. Moderate power warning (< 45%)
    if p < 45:
        rover_ready = state.get('rovers', {}).get('perseverance', {}).get('status') == 'READY'
        return {
            'rec_action': 'deploy_rover' if rover_ready else 'optimize_solar',
            'title': '⚡ LOW BATTERY RESERVES',
            'message': 'Power is under 45%. Execute OPTIMIZE SOLAR or dispatch Perseverance Rover to recharge safely.',
            'severity': 'warning'
        }

    # 4. Balanced nominal advice
    candidates = [('boost_oxygen', o, 'Oxygen'), ('boost_food', f, 'Food'), ('boost_shields', s, 'Shielding')]
    candidates.sort(key=lambda x: x[1])
    lowest_action, lowest_val, lowest_name = candidates[0]

    return {
        'rec_action': lowest_action,
        'title': '✅ SYSTEMS STABLE',
        'message': f'Base telemetry is nominal. Bolster your lowest resource ({lowest_name} at {lowest_val}%) to prepare for upcoming storms.',
        'severity': 'nominal'
    }

def update_crew_biometrics(state):
    """Calculates crew physiological vitals based on habitat environmental life support."""
    p = state.get('power', 100)
    o = state.get('oxygen', 100)
    f = state.get('food', 100)
    s = state.get('shielding', 100)

    base_spo2 = 99 if o >= 60 else (92 if o >= 30 else 82)
    base_bpm = 68 if o >= 60 else (95 if o >= 30 else 128)
    
    crew_list = state.get('crew', [])
    for member in crew_list:
        penalty = 0
        if o <= 25: penalty += 6
        if f <= 25: penalty += 5
        if s <= 25: penalty += 4
        if p <= 15: penalty += 3

        member['health'] = max(10, min(100, member['health'] - penalty + (2 if penalty == 0 else 0)))
        
        variance = hash(member['name'] + str(state.get('sol', 1))) % 7 - 3
        member['bpm'] = base_bpm + variance
        member['spo2'] = max(75, min(100, base_spo2 + (variance % 2)))
        
        if member['health'] < 40 or o <= 20:
            member['status'] = 'CRITICAL'
        elif member['health'] < 70 or o <= 45:
            member['status'] = 'STRESSED'
        else:
            member['status'] = 'NOMINAL'

    return crew_list

def get_initial_state(level=1, current_xp=0):
    """Initializes game state for a given level."""
    lvl_cfg = LEVEL_CONFIGS.get(level, LEVEL_CONFIGS[1])
    initial_st = {
        'level': level,
        'level_name': lvl_cfg['name'],
        'tier': lvl_cfg['tier'],
        'sol': 1,
        'target_sols': lvl_cfg['target_sols'],
        'power': lvl_cfg['initial_power'],
        'oxygen': lvl_cfg['initial_oxygen'],
        'food': lvl_cfg['initial_food'],
        'shielding': lvl_cfg['initial_shielding'],
        'water': lvl_cfg.get('initial_water', 100),
        'integrity': lvl_cfg.get('initial_integrity', 100),
        'role': 'COMMANDER',
        'modules': {
            'solar_arrays': {'id': 'solar_arrays', 'name': 'Solar Arrays & RTG', 'health': 100, 'status': 'NOMINAL', 'desc': 'Photovoltaic dual tracking wings and radioisotope thermoelectric generator.'},
            'central_hab': {'id': 'central_hab', 'name': 'Central Habitat Dome', 'health': 100, 'status': 'NOMINAL', 'desc': 'Crew living quarters, environmental avionics, and Whipple micrometeoroid shielding.'},
            'moxie': {'id': 'moxie', 'name': 'MOXIE Oxygen Plant', 'health': 100, 'status': 'NOMINAL', 'desc': 'High-temperature (800°C) solid-oxide electrolysis extracting O2 from Martian CO2.'},
            'hydroponics': {'id': 'hydroponics', 'name': 'Hydroponics Greenhouse', 'health': 100, 'status': 'NOMINAL', 'desc': 'Closed-loop nutrient film vertical bio-chambers cultivating caloric food.'},
            'water_recycler': {'id': 'water_recycler', 'name': 'Water Recycling System', 'health': 100, 'status': 'NOMINAL', 'desc': 'Catalytic oxidation & vapor compression distillation recycling greywater and condensate.'},
            'thermal_radiator': {'id': 'thermal_radiator', 'name': 'Thermal Radiator Loops', 'health': 100, 'status': 'NOMINAL', 'desc': 'Heat exchange fluid loops preventing nocturnal habitat hypothermia and pipe freezes.'},
            'radiation_shield': {'id': 'radiation_shield', 'name': 'Active Magnetic Deflector', 'health': 100, 'status': 'NOMINAL', 'desc': 'Superconducting coils generating artificial magnetosphere against cosmic rays.'},
        },
        'temp_warning': False,
        'cascade_counter': 0,
        'emergency_battery_tripped': False,
        'xp': current_xp,
        'badge': None,
        'latest_crisis': None,
        'status': 'ACTIVE',
        'fail_reason': '',
        'crises_handled': 0,
        'clutch_count': 0,
        'log': [
            "SYSTEM INIT: Sol Survivor Mission Control online.",
            f"DEPLOYMENT: Sol 1 of {lvl_cfg['target_sols']} on Mars surface ({lvl_cfg['name'].upper()}).",
            "Telemetry nominal. Awaiting Flight Director engineering commands."
        ],
        'history': [
            {
                'sol': 1,
                'power': lvl_cfg['initial_power'],
                'oxygen': lvl_cfg['initial_oxygen'],
                'food': lvl_cfg['initial_food'],
                'shielding': lvl_cfg['initial_shielding'],
                'water': lvl_cfg.get('initial_water', 100),
                'integrity': lvl_cfg.get('initial_integrity', 100)
            }
        ],
        'crew': [
            {'name': 'Commander Alex Vance', 'role': 'Mission Commander', 'health': 100, 'bpm': 68, 'spo2': 99, 'status': 'NOMINAL'},
            {'name': 'Dr. Maya Lin', 'role': 'Lead Astrobiologist', 'health': 100, 'bpm': 72, 'spo2': 98, 'status': 'NOMINAL'},
            {'name': 'Carlos Reyes', 'role': 'Flight Engineer', 'health': 100, 'bpm': 70, 'spo2': 99, 'status': 'NOMINAL'},
            {'name': 'Sarah Connor', 'role': 'Life Support Specialist', 'health': 100, 'bpm': 65, 'spo2': 100, 'status': 'NOMINAL'},
        ],
        'rovers': {
            'ingenuity': {'name': 'Ingenuity Drone', 'status': 'READY', 'cooldown': 0, 'desc': 'Recon aerial survey (predicts weather)'},
            'perseverance': {'name': 'Perseverance Rover', 'status': 'READY', 'cooldown': 0, 'desc': 'Dust-brush arrays (+18% Power)'},
            'drill': {'name': 'Subsurface Drill', 'status': 'READY', 'cooldown': 0, 'desc': 'Extracts permafrost ice (+15% Food, +10% O2)'}
        },
        'emergency_protocols': {
            'rtg_burst': {'name': 'RTG Thermal Overclock', 'used': False, 'desc': 'Instantly clear freeze risk'},
            'hyperbaric_purge': {'name': 'Hyperbaric O2 Purge', 'used': False, 'desc': 'Emergency injection of +30% O2'},
            'magnetic_pulse': {'name': 'Magnetosphere Pulse', 'used': False, 'desc': 'Emergency shield pulse +35%'}
        }
    }
    initial_st['telemetry'] = compute_nasa_telemetry(initial_st)
    initial_st['advisor'] = compute_houston_advisor(initial_st)
    return initial_st

MISSION_BADGES = {
    1: {
        'id': 'touchdown_pioneer',
        'badge': '🪐 Touchdown Pioneer',
        'rank': 'Junior Space Cadet',
        'level_name': 'Touchdown',
        'desc': 'Conquered first Martian Touchdown with sustainable baseline telemetry.'
    },
    2: {
        'id': 'dust_storm_navigator',
        'badge': '🌪️ Dust Storm Navigator',
        'rank': 'Martian Flight Engineer',
        'level_name': 'Red Dust',
        'desc': 'Navigated intense Martian dust storm cascades and thermal drops.'
    },
    3: {
        'id': 'solar_shield_tactician',
        'badge': '☀️ Solar Shield Tactician',
        'rank': 'Orbital Mission Specialist',
        'level_name': 'Solar Storm',
        'desc': 'Deflected hazardous Coronal Mass Ejections and balanced deep power deficits.'
    },
    4: {
        'id': 'colony_architect',
        'badge': '🚀 Colony Life-Support Architect',
        'rank': 'Mars Base Commander',
        'level_name': 'Apocalypse Protocol',
        'desc': 'Mastered closed-loop survival across all 30 Sols of the Apocalypse Protocol.'
    }
}

GRAND_RANK = "🏆 GRAND MARS FLEET ADMIRAL (APEX NASA SURVIVOR)"
SUPREME_BADGE = "🌟 SUPREME PLANETARY COMMANDER BADGE"
SUPREME_BADGE_DESC = "All 4 Martian sectors secured with supreme closed-loop engineering mastery."

def get_cadet_rank_and_badges(completed_missions, xp=0):
    """
    Computes current rank and list of earned badges based on cleared level IDs (1-4).
    If all 4 levels are completed, awards GRAND MARS FLEET ADMIRAL and SUPREME PLANETARY COMMANDER BADGE.
    """
    cleaned_levels = []
    for lvl in (completed_missions or []):
        try:
            val = int(lvl)
            if 1 <= val <= 4 and val not in cleaned_levels:
                cleaned_levels.append(val)
        except (ValueError, TypeError):
            continue

    cleared = set(cleaned_levels)
    badges = []
    badge_details = []
    for lvl in [1, 2, 3, 4]:
        if lvl in cleared:
            info = MISSION_BADGES[lvl]
            badges.append(info['badge'])
            badge_details.append(info)

    all_cleared = len(cleared.intersection({1, 2, 3, 4})) >= 4
    if all_cleared:
        badges.append(SUPREME_BADGE)
        badge_details.append({
            'id': 'supreme_commander',
            'badge': SUPREME_BADGE,
            'rank': GRAND_RANK,
            'level_name': 'All Martian Sectors',
            'desc': SUPREME_BADGE_DESC
        })
        current_rank = GRAND_RANK
    elif cleared:
        highest = max(cleared)
        current_rank = MISSION_BADGES[highest]['rank']
    else:
        current_rank = calculate_rank(xp)

    return current_rank, badges, all_cleared, badge_details

def calculate_rank(xp):
    """Calculates player title rank based on cumulative XP."""
    if xp >= 2500:
        return "Mars Base Commander"
    elif xp >= 1200:
        return "Mission Specialist"
    elif xp >= 500:
        return "Flight Engineer"
    return "Cadet"

def advance_turn(state, action):
    """
    Executes one Sol progression step:
    1. Handles Tactical Rover, Drone & Emergency Actions
    2. Applies player engineering action & trade-offs
    3. Applies ambient Sol baseline consumption
    4. Evaluates Cascading Failures (thermal cascade, voltage sag, radiation breach)
    5. Evaluates scripted & dynamic Martian crises
    6. Checks Clutch Survival & XP rewards
    7. Updates Crew Vitals, NASA Telemetry model, Strip-Chart & Houston Advisor
    """
    if state.get('status') != 'ACTIVE':
        return state

    level = state['level']
    lvl_cfg = LEVEL_CONFIGS.get(level, LEVEL_CONFIGS[1])
    state['badge'] = None
    state['latest_crisis'] = None
    sol = state['sol']

    # Update Rover cooldowns
    if 'rovers' in state:
        for rk, rover in state['rovers'].items():
            if rover.get('cooldown', 0) > 0:
                rover['cooldown'] -= 1
                if rover['cooldown'] == 0:
                    rover['status'] = 'READY'

    clutch_condition = min(state['power'], state['oxygen'], state['food'], state['shielding']) <= 15

    # --- 1. SPECIAL TACTICAL DISPATCHES & EMERGENCY OVERRIDES ---
    if action == 'deploy_drone':
        state['rovers']['ingenuity']['status'] = 'COOLDOWN'
        state['rovers']['ingenuity']['cooldown'] = 3
        state['xp'] += 75
        state['log'].append(f"SOL {sol} INGENUITY: Aerial scout airborne! Orbital cameras show Jezero Crater weather outlook clear for 48 hours.")
        state['power'] = max(0, state['power'] - 5)

    elif action == 'deploy_rover':
        state['rovers']['perseverance']['status'] = 'COOLDOWN'
        state['rovers']['perseverance']['cooldown'] = 4
        state['power'] = min(100, state['power'] + 18)
        state['xp'] += 100
        state['log'].append(f"SOL {sol} PERSEVERANCE: High-pressure gas jet dusted photovoltaic wings. (+18% Power restored)!")

    elif action == 'deploy_drill':
        state['rovers']['drill']['status'] = 'COOLDOWN'
        state['rovers']['drill']['cooldown'] = 5
        state['food'] = min(100, state['food'] + 15)
        state['oxygen'] = min(100, state['oxygen'] + 10)
        state['water'] = min(100, state.get('water', 100) + 20)
        state['xp'] += 120
        state['log'].append(f"SOL {sol} SUBSURFACE DRILL: Struck glaciated permafrost at 1.4m depth! Purified water shunted to life support (+15% Food, +10% O2, +20% Water).")

    elif action == 'emergency_rtg':
        if not state['emergency_protocols']['rtg_burst']['used']:
            state['emergency_protocols']['rtg_burst']['used'] = True
            state['temp_warning'] = False
            state['cascade_counter'] = 0
            state['power'] = max(0, state['power'] - 10)
            state['log'].append("🚨 EMERGENCY PROTOCOL EXECUTED: RTG core bypassed safety interlocks! Thermal surge defrosted hydroponic line immediately.")

    elif action == 'emergency_o2':
        if not state['emergency_protocols']['hyperbaric_purge']['used']:
            state['emergency_protocols']['hyperbaric_purge']['used'] = True
            state['oxygen'] = min(100, state['oxygen'] + 30)
            state['log'].append("🚨 EMERGENCY PROTOCOL EXECUTED: Cryogenic O2 emergency reserve dumped into habitat atmosphere (+30% O2)!")

    elif action == 'emergency_shield':
        if not state['emergency_protocols']['magnetic_pulse']['used']:
            state['emergency_protocols']['magnetic_pulse']['used'] = True
            state['shielding'] = min(100, state['shielding'] + 35)
            state['log'].append("🚨 EMERGENCY PROTOCOL EXECUTED: Superconducting deflector capacitor bank discharged (+35% Radiation Shield)!")

    # --- 2. STANDARD ENGINEERING ACTIONS ---
    elif action == 'optimize_solar':
        state['power'] = min(100, state['power'] + 22)
        state['log'].append(f"SOL {sol} ACTION: Solar Tracking Optimized (+22% Power). Sun-tracking gimbals & ultrasonic piezo dust vibrators cleared array wings.")
        if state['temp_warning']:
            state['cascade_counter'] -= 1

    elif action == 'boost_oxygen':
        state['oxygen'] = min(100, state['oxygen'] + 24)
        state['power'] = max(0, state['power'] - 8)
        state['log'].append(f"SOL {sol} ACTION: Boosted MOXIE O2 (+24% O2, -8% Power). Solid-oxide electrolysis operating at 800°C.")
        if state['temp_warning']:
            state['cascade_counter'] -= 1

    elif action == 'boost_food':
        state['food'] = min(100, state['food'] + 24)
        state['power'] = max(0, state['power'] - 8)
        state['log'].append(f"SOL {sol} ACTION: Hydroponic UV Overdrive (+24% Food, -8% Power). Blue/red LED grow cycle accelerated.")
        if state['temp_warning']:
            state['cascade_counter'] -= 1

    elif action == 'boost_shields':
        state['shielding'] = min(100, state['shielding'] + 26)
        state['power'] = max(0, state['power'] - 10)
        state['log'].append(f"SOL {sol} ACTION: Charged Magnetic Deflectors (+26% Shield, -10% Power). Hull deflector coils magnetized.")
        if state['temp_warning']:
            state['cascade_counter'] -= 1

    elif action == 'conserve_power':
        state['power'] = min(100, state['power'] + 25)
        state['food'] = max(0, state['food'] - 6)
        state['log'].append(f"SOL {sol} ACTION: Dimmed Habitat Heaters (+25% Power, -6% Food). Power shunted to primary bus.")

        if level >= 2:
            state['temp_warning'] = True
            state['cascade_counter'] = 3
            state['log'].append("⚠️ THERMAL WARNING: Heaters dimmed! Hydroponics greenhouse entering sub-zero freezing danger zone (3 Sols to freeze)!")

    elif action == 'recycle_water':
        state['water'] = min(100, state.get('water', 100) + 25)
        state['power'] = max(0, state['power'] - 6)
        state['log'].append(f"SOL {sol} ACTION: Catalytic Water Purification (+25% Water, -6% Power). Purged filtration membranes.")
        if state['temp_warning']:
            state['cascade_counter'] -= 1

    elif action == 'repair_seal':
        state['integrity'] = min(100, state.get('integrity', 100) + 25)
        state['power'] = max(0, state['power'] - 6)
        state['log'].append(f"SOL {sol} ACTION: Pressure Seal Reinforcement (+25% Integrity, -6% Power). Repaired airlock gasket micrometeoroid stress.")
        if state['temp_warning']:
            state['cascade_counter'] -= 1
    else:
        state['log'].append(f"SOL {sol}: Standing by telemetry with no direct command input.")
        if state['temp_warning']:
            state['cascade_counter'] -= 1

    # --- 3. AMBIENT RESOURCE DRAIN & SOLAR HARVEST ---
    drain = lvl_cfg['base_drain']
    state['oxygen'] = max(0, state['oxygen'] - drain['oxygen'])
    state['food'] = max(0, state['food'] - drain['food'])
    state['shielding'] = max(0, state['shielding'] - drain['shielding'])
    state['water'] = max(0, state.get('water', 100) - drain.get('water', 3))
    state['integrity'] = max(0, state.get('integrity', 100) - drain.get('integrity', 1))

    # Diurnal solar array generation
    cycle = compute_mars_cycle(sol)
    if cycle['phase'] == 'DAY':
        tau = compute_nasa_telemetry(state)['tau']
        daytime_solar = max(5, round(8.0 * math.exp(-tau / 4.0)))
        state['power'] = min(100, max(0, state['power'] + daytime_solar - drain['power']))
        state['log'].append(f"☀️ DIURNAL SOLAR HARVEST: Photovoltaic panels harvested +{daytime_solar}% solar energy during Martian daytime.")
    else:
        state['power'] = max(0, state['power'] - drain['power'])
        state['log'].append(f"🌙 MARTIAN NIGHT: Base sustained on battery reserves (-{drain['power']}% Power).")

    # --- 4. CASCADING FAILURES ENGINE ---
    if state['temp_warning'] and state['cascade_counter'] <= 0:
        freeze_damage = 35 if level >= 3 else 30
        state['food'] = max(0, state['food'] - freeze_damage)
        state['temp_warning'] = False
        state['cascade_counter'] = 0
        state['log'].append(f"💥 CASCADING FAILURE TRIGGERED: Thermal regulators remained offline too long! Water supply lines froze and burst! (-{freeze_damage}% Food ruined)!")
        state['latest_crisis'] = "CASCADING FAILURE: Hydroponic water pipes frozen and burst!"

    if level >= 3 and state['power'] <= 20 and state['power'] > 0:
        extra_o2_loss = 10
        state['oxygen'] = max(0, state['oxygen'] - extra_o2_loss)
        state['log'].append("⚠️ CASCADING BROWNOUT: Low bus voltage stalled MOXIE compressor (-10% O2 extra)!")
        if not state['latest_crisis']:
            state['latest_crisis'] = "CASCADING BROWNOUT: MOXIE compressor stalled by low voltage!"

    if level >= 3 and state['shielding'] <= 20 and state['shielding'] > 0:
        extra_pwr_loss = 10
        state['power'] = max(0, state['power'] - extra_pwr_loss)
        state['log'].append("⚠️ CASCADING IONIZATION: Unfiltered cosmic rays penetrated hab avionics, disrupting solar inverters (-10% Power extra)!")
        if not state['latest_crisis']:
            state['latest_crisis'] = "CASCADING IONIZATION: Cosmic radiation damaged solar inverters!"

    # --- 5. SCRIPTED & DYNAMIC MARTIAN CRISES ---
    crisis_occurred = False
    crisis_text = ""

    if level == 1:
        if sol == 4:
            state['power'] = max(0, state['power'] - 12)
            crisis_text = "CRISIS: Extended Martian Twilight. Solar array generation dropped (-12% Power)."
            crisis_occurred = True
        elif sol == 8:
            state['oxygen'] = max(0, state['oxygen'] - 14)
            crisis_text = "CRISIS: Regolith Dust Clog in MOXIE intake filter (-14% Oxygen)."
            crisis_occurred = True

    elif level == 2:
        if sol == 4:
            state['power'] = max(0, state['power'] - 20)
            crisis_text = "CRISIS: Regional Dust Storm! Atmospheric opacity (Tau=2.9) dropped solar yield (-20% Power)."
            crisis_occurred = True
        elif sol == 9:
            state['food'] = max(0, state['food'] - 20)
            crisis_text = "CRISIS: Permafrost Pressure Shift pinched Hydroponic nutrient delivery pipes (-20% Food)."
            crisis_occurred = True
        elif sol == 13:
            state['shielding'] = max(0, state['shielding'] - 22)
            crisis_text = "CRISIS: Micrometeoroid Shower degraded habitat deflector grid (-22% Shielding)."
            crisis_occurred = True

    elif level == 3:
        if sol == 5:
            state['shielding'] = max(0, state['shielding'] - 25)
            state['power'] = max(0, state['power'] - 15)
            crisis_text = "DUAL CRISIS: Coronal Mass Ejection (CME) + Battery Cell Overheat (-25% Shield, -15% Power)!"
            crisis_occurred = True
        elif sol == 11:
            state['oxygen'] = max(0, state['oxygen'] - 22)
            state['food'] = max(0, state['food'] - 18)
            crisis_text = "DUAL CRISIS: Scrubber Membrane Tear + Hydroponic UV ballast failure (-22% O2, -18% Food)!"
            crisis_occurred = True
        elif sol == 16:
            state['power'] = max(0, state['power'] - 22)
            state['shielding'] = max(0, state['shielding'] - 20)
            crisis_text = "DUAL CRISIS: Atmospheric Dust Vortex + Magnetic Field Harmonic Drift (-22% Power, -20% Shield)!"
            crisis_occurred = True

    elif level == 4:
        if sol == 6:
            state['power'] = max(0, state['power'] - 25)
            state['food'] = max(0, state['food'] - 20)
            crisis_text = "APOCALYPSE CRISIS: Polar vortex drops external temp to -125°C! (-25% Power, -20% Food)."
            crisis_occurred = True
        elif sol == 14:
            state['power'] = max(0, state['power'] - 25)
            state['oxygen'] = max(0, state['oxygen'] - 22)
            crisis_text = "APOCALYPSE CRISIS: Global Planet-Encircling Dust Storm! MOXIE starved & panels obscured (-25% Power, -22% O2)."
            crisis_occurred = True
        elif sol == 21:
            state['shielding'] = max(0, state['shielding'] - 30)
            state['power'] = max(0, state['power'] - 18)
            crisis_text = "APOCALYPSE CRISIS: Severe Class-X Solar Particle Storm! Magnetic coil overload (-30% Shield, -18% Power)."
            crisis_occurred = True
        elif sol == 27:
            state['power'] = max(0, state['power'] - 15)
            state['oxygen'] = max(0, state['oxygen'] - 15)
            state['food'] = max(0, state['food'] - 15)
            state['shielding'] = max(0, state['shielding'] - 15)
            crisis_text = "APOCALYPSE PROTOCOL: Life-support harmonic resonance breach! ALL SUBSYSTEMS STRESSED (-15% all)."
            crisis_occurred = True

    if crisis_occurred:
        state['crises_handled'] += 1
        state['latest_crisis'] = crisis_text
        state['log'].append(f"🚨 {crisis_text}")

    # Automated Emergency Battery Breaker (Cadet & Flight Engineer Tiers)
    if level <= 2 and state['power'] <= 5 and not state.get('emergency_battery_tripped'):
        state['power'] = 5
        state['emergency_battery_tripped'] = True
        state['log'].append("⚠️ AUTOMATIC LOAD SHEDDING: Emergency battery breaker tripped! Non-essential systems cut to prevent blackout (5% reserve preserved). RECHARGE IMMEDIATELY!")

    # --- 6. CHECK FAILURE (LOSS CONDITION) ---
    if state['power'] <= 0:
        state['status'] = 'LOST'
        state['fail_reason'] = (
            "HABITAT TOTAL BLACKOUT: Power grid depleted to 0%. Life support, communications, and primary heaters shut down. "
            "Martian night-time ambient temperature (-65°C) caused rapid habitat hypothermia."
        )
    elif state['oxygen'] <= 0:
        state['status'] = 'LOST'
        state['fail_reason'] = (
            "HYPOXIA CRISIS: MOXIE oxygen generation failed. Atmospheric partial pressure of O2 dropped below human viability (16 kPa). "
            "Crew suffered irreversible asphyxiation."
        )
    elif state['food'] <= 0:
        state['status'] = 'LOST'
        state['fail_reason'] = (
            "CALORIC SYSTEM COLLAPSE: Hydroponic closed-loop greenhouse suffered fatal biomass failure. "
            "Emergency caloric reserves depleted; mission abort required."
        )
    elif state['shielding'] <= 0:
        state['status'] = 'LOST'
        state['fail_reason'] = (
            "LETHAL RADIATION DOSAGE: Active magnetic radiation deflector depleted to 0%. "
            "Crew received unattenuated cosmic ray and solar energetic particle dosage exceeding NASA safety ceilings."
        )
    elif state.get('water', 100) <= 0:
        state['status'] = 'LOST'
        state['fail_reason'] = (
            "DEHYDRATION COLLAPSE: Closed-loop water reclamation depleted to 0%. "
            "Habitat life-support water reserves exhausted; crew unable to maintain metabolic hydration."
        )
    elif state.get('integrity', 100) <= 0:
        state['status'] = 'LOST'
        state['fail_reason'] = (
            "STRUCTURAL DECOMPRESSION: Habitat outer pressure hull suffered catastrophic structural breach. "
            "Atmospheric decompression required emergency mission abort."
        )

    # Sync module health
    if 'modules' in state:
        state['modules']['solar_arrays']['health'] = state['power']
        state['modules']['moxie']['health'] = state['oxygen']
        state['modules']['hydroponics']['health'] = state['food']
        state['modules']['water_recycler']['health'] = state.get('water', 100)
        state['modules']['radiation_shield']['health'] = state['shielding']
        state['modules']['central_hab']['health'] = state.get('integrity', 100)
        state['modules']['thermal_radiator']['health'] = 25 if state.get('temp_warning') else 100
        for mk, mod in state['modules'].items():
            h = mod['health']
            mod['status'] = 'CRITICAL' if h <= 25 else ('STRESSED' if h <= 50 else 'NOMINAL')

    # --- 7. CLUTCH SURVIVAL & XP ACCRUAL ---
    if state['status'] == 'ACTIVE':
        sol_xp = 40 + (level * 20)
        state['xp'] += sol_xp

        min_res = min(state['power'], state['oxygen'], state['food'], state['shielding'])
        if clutch_condition or min_res <= 15:
            state['clutch_count'] += 1
            state['xp'] += 250
            state['badge'] = "CLUTCH SURVIVOR! (+250 XP) Critical Life Support Recovery under Extreme Pressure!"
            state['log'].append("🏆 MISSION HIGHLIGHT: Base survived critical telemetry threshold (<15%)!")

        state['sol'] += 1

        if state['sol'] > state['target_sols']:
            state['status'] = 'WON'
            state['sol'] = state['target_sols']
            win_bonus = 500 * level
            state['xp'] += win_bonus
            badge_info = MISSION_BADGES.get(level, {})
            state['cleared_badge'] = badge_info.get('badge', '')
            state['cleared_rank'] = badge_info.get('rank', '')
            if level == 4:
                state['badge'] = f"{badge_info.get('badge', '')} - CONQUERED APOCALYPSE PROTOCOL!"
            else:
                state['badge'] = f"{badge_info.get('badge', '')} - {lvl_cfg['name'].upper()} CLEARED! (+{win_bonus} XP)"
            state['log'].append(f"🎉 MISSION ACCOMPLISHED: Survived all {state['target_sols']} Sols of {lvl_cfg['name']}! Awarded {badge_info.get('badge', '')}!")

    if 'history' not in state:
        state['history'] = []
    state['history'].append({
        'sol': state['sol'],
        'power': state['power'],
        'oxygen': state['oxygen'],
        'food': state['food'],
        'shielding': state['shielding'],
        'water': state.get('water', 100),
        'integrity': state.get('integrity', 100)
    })
    state['history'] = state['history'][-15:]

    state['crew'] = update_crew_biometrics(state)
    state['telemetry'] = compute_nasa_telemetry(state)
    state['advisor'] = compute_houston_advisor(state)

    return state
