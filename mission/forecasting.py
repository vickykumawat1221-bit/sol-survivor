"""
Predictive Survival Analytics & 3-5 Sol Resource Forecasting Engine.
Calculates closed-loop trajectories for Power, Oxygen, Food, Water, and Shielding,
identifying future depletion bottlenecks, cascading risks, and survival probabilities.
"""

from .engine import compute_mars_cycle, LEVEL_CONFIGS

def generate_predictive_forecast(state, candidate_action=None, horizon_sols=5):
    """
    Simulates forward resource trajectories across horizon_sols.
    Returns:
    - chart_data: labels and datasets for Chart.js
    - warnings: list of impending bottlenecks
    - risk_assessment: survival risk score and explanation
    """
    level = state.get('level', 1)
    lvl_cfg = LEVEL_CONFIGS.get(level, LEVEL_CONFIGS[1])
    base_drain = lvl_cfg['base_drain']
    current_sol = state.get('sol', 1)

    labels = []
    pwr_series = []
    o2_series = []
    food_series = []
    water_series = []
    shield_series = []

    p = state.get('power', 100)
    o = state.get('oxygen', 100)
    f = state.get('food', 100)
    s = state.get('shielding', 100)
    w = state.get('water', 100)
    temp_warn = state.get('temp_warning', False)
    cascade_cnt = state.get('cascade_counter', 0)

    # If previewing an action, apply turn 1 effects
    if candidate_action == 'optimize_solar':
        p = min(100, p + 22)
    elif candidate_action == 'boost_oxygen':
        o = min(100, o + 24)
        p = max(0, p - 8)
    elif candidate_action == 'boost_food':
        f = min(100, f + 24)
        p = max(0, p - 8)
    elif candidate_action == 'boost_shields':
        s = min(100, s + 26)
        p = max(0, p - 10)
    elif candidate_action == 'conserve_power':
        p = min(100, p + 25)
        f = max(0, f - 6)
        temp_warn = True
        cascade_cnt = 3
    elif candidate_action == 'deploy_rover':
        p = min(100, p + 18)
    elif candidate_action == 'deploy_drill':
        f = min(100, f + 15)
        o = min(100, o + 10)
        w = min(100, w + 20)

    depletion_warnings = []
    first_depleted_sol = None

    for step in range(1, horizon_sols + 1):
        sim_sol = current_sol + step
        labels.append(f"Sol {sim_sol}")

        cycle = compute_mars_cycle(sim_sol)
        # Daytime solar vs nocturnal battery drain
        if cycle['phase'] == 'DAY':
            daytime_solar = 8
            p = min(100, max(0, p + daytime_solar - base_drain['power']))
        else:
            p = max(0, p - base_drain['power'])

        o = max(0, o - base_drain['oxygen'])
        f = max(0, f - base_drain['food'])
        s = max(0, s - base_drain['shielding'])
        w = max(0, w - 4)  # Closed-loop water baseline evaporation

        # Thermal cascade evaluation
        if temp_warn:
            cascade_cnt -= 1
            if cascade_cnt <= 0:
                f = max(0, f - 30)
                temp_warn = False
                depletion_warnings.append(f"Sol {sim_sol}: Freezing pipe rupture burst! -30% Hydroponics loss!")

        # Check for zero breaches
        if p == 0 and not first_depleted_sol:
            first_depleted_sol = f"Power blackout on Sol {sim_sol}"
        if o == 0 and not first_depleted_sol:
            first_depleted_sol = f"Hypoxia breach on Sol {sim_sol}"
        if f == 0 and not first_depleted_sol:
            first_depleted_sol = f"Caloric exhaustion on Sol {sim_sol}"
        if s == 0 and not first_depleted_sol:
            first_depleted_sol = f"Radiation shield collapse on Sol {sim_sol}"
        if w == 0 and not first_depleted_sol:
            first_depleted_sol = f"Water reservoir empty on Sol {sim_sol}"

        pwr_series.append(round(p, 1))
        o2_series.append(round(o, 1))
        food_series.append(round(f, 1))
        water_series.append(round(w, 1))
        shield_series.append(round(s, 1))

    # Overall survival risk calculation
    min_final = min(pwr_series[-1], o2_series[-1], food_series[-1], water_series[-1], shield_series[-1])
    if first_depleted_sol:
        risk_score = 95
        risk_tier = "CRITICAL RISK"
        risk_color = "rose-500"
        summary = f"Impending subsystem failure: {first_depleted_sol}. Immediate countermeasure required!"
    elif min_final <= 20:
        risk_score = 65
        risk_tier = "ELEVATED RISK"
        risk_color = "amber-400"
        summary = f"Resource depletion predicted within {horizon_sols} Sols. Subsystems dropping into emergency reserve threshold."
    else:
        risk_score = 15
        risk_tier = "LOW RISK"
        risk_color = "emerald-400"
        summary = f"Predictive model shows stable closed-loop equilibrium across next {horizon_sols} Sols."

    return {
        'labels': labels,
        'datasets': [
            {'label': 'Power (%)', 'data': pwr_series, 'borderColor': '#f59e0b', 'backgroundColor': 'rgba(245, 158, 11, 0.1)'},
            {'label': 'Oxygen (%)', 'data': o2_series, 'borderColor': '#34d399', 'backgroundColor': 'rgba(52, 211, 153, 0.1)'},
            {'label': 'Food (%)', 'data': food_series, 'borderColor': '#10b981', 'backgroundColor': 'rgba(16, 185, 129, 0.1)'},
            {'label': 'Water (%)', 'data': water_series, 'borderColor': '#06b6d4', 'backgroundColor': 'rgba(6, 182, 212, 0.1)'},
            {'label': 'Shielding (%)', 'data': shield_series, 'borderColor': '#818cf8', 'backgroundColor': 'rgba(129, 140, 248, 0.1)'},
        ],
        'warnings': depletion_warnings,
        'risk_score': risk_score,
        'risk_tier': risk_tier,
        'risk_color': risk_color,
        'summary': summary,
        'candidate_action': candidate_action
    }
