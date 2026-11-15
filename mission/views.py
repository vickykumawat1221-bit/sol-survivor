"""
Views for Sol Survivor: AI-Powered Mars Mission Digital Twin & Survival Simulator.
Provides server-side action validation, database persistence, replay logging,
predictive analytics, NASA Data Center provenance, AI chat, and STEM quizzes.
"""

import json
import copy
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    MissionSession, MissionStepLog, RepairMission, STEMQuizRecord,
    AcademyProfile, AcademyGameScore, AcademyAchievement, AcademyDailyChallenge
)
from .engine import (
    LEVEL_CONFIGS, get_initial_state, advance_turn, calculate_rank,
    compute_nasa_telemetry, update_crew_biometrics, compute_houston_advisor,
    MISSION_BADGES, GRAND_RANK, SUPREME_BADGE, get_cadet_rank_and_badges
)
from .nasa_data import get_nasa_data_center_telemetry
from .ai_advisor import evaluate_decision_tree, answer_mission_chat
from .crisis_engine import generate_crisis_for_sol
from .forecasting import generate_predictive_forecast
from .learning_center import get_all_curriculum_modules, submit_quiz_answer
from .academy_engine import (
    ACADEMY_GAMES, ACADEMY_ACHIEVEMENTS_DEF, validate_and_award_academy_score
)

LEGAL_ACTIONS = {
    'optimize_solar', 'boost_oxygen', 'boost_food', 'boost_shields', 'conserve_power',
    'recycle_water', 'repair_seal', 'deploy_rover', 'deploy_drone', 'deploy_drill',
    'emergency_rtg', 'emergency_o2', 'emergency_shield', 'restart', 'next_level'
}

def get_crew_status(state):
    min_stat = min(
        state.get('power', 100),
        state.get('oxygen', 100),
        state.get('food', 100),
        state.get('shielding', 100),
        state.get('water', 100),
        state.get('integrity', 100)
    )
    if min_stat <= 20:
        return "CRITICAL", "rose-500"
    elif min_stat <= 45:
        return "WARNING", "amber-400"
    return "NOMINAL", "emerald-400"

def ensure_state_structure(state):
    """Ensures state dictionary has all required keys for closed-loop simulation."""
    initial = get_initial_state(state.get('level', 1), state.get('xp', 0))
    for key in ['crew', 'rovers', 'emergency_protocols', 'history', 'telemetry', 'advisor', 'modules', 'water', 'integrity', 'role']:
        if key not in state:
            state[key] = initial[key]
    return state

def get_or_create_db_session(request, state=None):
    """Syncs state with persistent Django database model."""
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key

    try:
        ms = MissionSession.objects.filter(session_key=session_key).first()
        if not ms:
            ms = MissionSession.objects.create(
                session_key=session_key,
                commander_name=request.session.get('commander_name', 'Junior Commander'),
                role=request.session.get('player_role', 'COMMANDER'),
                level=state.get('level', 1) if state else 1,
                unlocked_level=request.session.get('unlocked_level', 1),
                sol=state.get('sol', 1) if state else 1,
                status=state.get('status', 'ACTIVE') if state else 'ACTIVE',
                xp=state.get('xp', 0) if state else 0,
                state_json=state or {}
            )
        elif state:
            ms.level = state.get('level', ms.level)
            ms.sol = state.get('sol', ms.sol)
            ms.status = state.get('status', ms.status)
            ms.fail_reason = state.get('fail_reason', '')
            ms.xp = state.get('xp', ms.xp)
            ms.crises_handled = state.get('crises_handled', ms.crises_handled)
            ms.clutch_count = state.get('clutch_count', ms.clutch_count)
            ms.state_json = state
            ms.save()
        return ms
    except Exception:
        return None

def log_step_to_db(mission_session, sol, action, before_state, after_state):
    """Saves a turn step snapshot to the database for replay timeline."""
    if not mission_session:
        return
    try:
        MissionStepLog.objects.create(
            mission=mission_session,
            sol=sol,
            action_taken=action,
            action_label=action.replace('_', ' ').upper(),
            resources_before={
                'power': before_state.get('power'),
                'oxygen': before_state.get('oxygen'),
                'food': before_state.get('food'),
                'shielding': before_state.get('shielding'),
                'water': before_state.get('water', 100),
                'integrity': before_state.get('integrity', 100)
            },
            resources_after={
                'power': after_state.get('power'),
                'oxygen': after_state.get('oxygen'),
                'food': after_state.get('food'),
                'shielding': after_state.get('shielding'),
                'water': after_state.get('water', 100),
                'integrity': after_state.get('integrity', 100)
            },
            active_crises=[after_state['latest_crisis']] if after_state.get('latest_crisis') else [],
            ai_recommendation=after_state.get('advisor', {}),
            log_messages=after_state.get('log', [])[-3:]
        )
    except Exception:
        pass


def login_view(request):
    """
    Cadet Login & Access Clearance Gateway:
    - Cadet Callsign Input (e.g. Cadet Aarav)
    - 4-Digit Security Clearance PIN (e.g. 2026)
    - Astronaut Character Avatar Selector (👨‍🚀 Orion, 👩‍🚀 Nova, ⚡ Volt, 🤖 Rover, 🛸 Orbit)
    - Age Selector (8 to 16 Years) with Starting Difficulty Level calibration
    - Station Role Selection (COMMANDER, ENGINEER, SCIENTIST)
    - Plain-English kid-friendly subtitles toggle
    - 1-Click Instant Guest Launch for quick evaluation
    - Synchronizes request.session and Space Academy profile
    """
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'guest_launch' or 'guest' in request.POST:
            cadet_name = "Cadet Guest"
            cadet_pin = "2026"
            cadet_avatar = "👨‍🚀"
            cadet_age_bracket = "8–9 yrs"
            cadet_age = 9
            starting_level = 1
            show_subtitles = True
            player_role = "COMMANDER"
        else:
            cadet_name = request.POST.get('cadet_name', '').strip()
            if not cadet_name:
                cadet_name = "Cadet Aarav"
            cadet_pin = request.POST.get('cadet_pin', '2026').strip() or '2026'
            cadet_avatar = request.POST.get('cadet_avatar', '👨‍🚀')
            cadet_age_bracket = request.POST.get('cadet_age', '8–9 yrs')
            player_role = request.POST.get('role', request.POST.get('player_role', 'COMMANDER'))

            if '8' in cadet_age_bracket or '9' in cadet_age_bracket:
                starting_level = 1
                cadet_age = 9
                show_subtitles = True
            elif '10' in cadet_age_bracket or '11' in cadet_age_bracket:
                starting_level = 2
                cadet_age = 11
                show_subtitles = True
            elif '12' in cadet_age_bracket or '13' in cadet_age_bracket:
                starting_level = 3
                cadet_age = 13
                show_subtitles = False
            else:
                starting_level = 4
                cadet_age = 15
                show_subtitles = False

            if 'show_subtitles' in request.POST:
                show_subtitles = request.POST.get('show_subtitles') in ['true', 'True', '1', 'on']

        # Save authenticated cadet identity to session
        request.session['is_authenticated_cadet'] = True
        request.session['cadet_name'] = cadet_name
        request.session['commander_name'] = cadet_name
        request.session['cadet_pin'] = cadet_pin
        request.session['cadet_avatar'] = cadet_avatar
        request.session['cadet_age_bracket'] = cadet_age_bracket
        request.session['cadet_age'] = cadet_age
        request.session['show_subtitles'] = show_subtitles
        request.session['player_role'] = player_role

        if 'completed_missions' not in request.session:
            request.session['completed_missions'] = []
        if 'earned_badges' not in request.session:
            request.session['earned_badges'] = []

        unlocked_level = max(request.session.get('unlocked_level', 1), starting_level)
        request.session['unlocked_level'] = unlocked_level

        # Initialize fresh state calibrated to starting level
        state = get_initial_state(level=starting_level, current_xp=0)
        state['role'] = player_role
        request.session['sol_survivor_state'] = state
        request.session.modified = True

        # Synchronize with Space Academy AcademyProfile
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key

        if cadet_age <= 10:
            age_group_choice = '8-10'
            diff_choice = 'easy'
        elif cadet_age <= 13:
            age_group_choice = '11-13'
            diff_choice = 'medium'
        else:
            age_group_choice = '14-16'
            diff_choice = 'hard'

        profile, _ = AcademyProfile.objects.get_or_create(
            session_key=session_key,
            defaults={
                'callsign': cadet_name,
                'age_group': age_group_choice,
                'difficulty': diff_choice,
                'total_academy_xp': 0,
                'games_completed_count': 0
            }
        )
        profile.callsign = cadet_name
        profile.age_group = age_group_choice
        profile.difficulty = diff_choice
        profile.save()

        get_or_create_db_session(request, state)
        return redirect('dashboard')

    is_authenticated = bool(request.session.get('is_authenticated_cadet') and request.session.get('cadet_name'))
    cadet_name = request.session.get('cadet_name', 'Cadet Aarav')
    cadet_avatar = request.session.get('cadet_avatar', '👨‍🚀')
    cadet_age_bracket = request.session.get('cadet_age_bracket', '8–9 yrs')
    completed_missions = request.session.get('completed_missions', [])
    rank, earned_badges, all_cleared, _ = get_cadet_rank_and_badges(completed_missions)

    context = {
        'is_authenticated_cadet': is_authenticated,
        'current_cadet_name': cadet_name if is_authenticated else '',
        'current_avatar': cadet_avatar,
        'cadet_age_bracket': cadet_age_bracket,
        'completed_missions': completed_missions,
        'earned_badges': earned_badges,
        'rank': rank,
        'unlocked_level': request.session.get('unlocked_level', 1),
    }
    return render(request, 'mission/login.html', context)


def logout_view(request):
    """Logs out active cadet, flushes session, and redirects to login gateway."""
    request.session.flush()
    return redirect('login')


def dashboard_view(request):
    """Primary Mission Control Telemetry Dashboard & Digital Twin Workstation."""
    # Enforce mandatory cadet authentication
    if not request.session.get('is_authenticated_cadet') or 'cadet_name' not in request.session:
        return redirect('login')

    if 'unlocked_level' not in request.session:
        request.session['unlocked_level'] = 1
    if 'commander_name' not in request.session:
        request.session['commander_name'] = request.session.get('cadet_name', 'Junior Commander')
    if 'player_role' not in request.session:
        request.session['player_role'] = 'COMMANDER'
    if 'completed_missions' not in request.session:
        request.session['completed_missions'] = []
    if 'earned_badges' not in request.session:
        request.session['earned_badges'] = []

    state = request.session.get('sol_survivor_state')
    if not state or 'telemetry' not in state:
        state = get_initial_state(level=request.session.get('unlocked_level', 1), current_xp=0)
    else:
        state = ensure_state_structure(state)

    request.session['sol_survivor_state'] = state
    unlocked_level = request.session.get('unlocked_level', 1)

    # Sync with database
    db_session = get_or_create_db_session(request, state)

    if request.method == 'POST':
        action = request.POST.get('action')
        target_level_str = request.POST.get('level')
        role_select = request.POST.get('role')

        if role_select:
            request.session['player_role'] = role_select
            state['role'] = role_select

        if action == 'restart':
            try:
                target_lvl = int(target_level_str) if target_level_str else state.get('level', 1)
            except (ValueError, TypeError):
                target_lvl = 1
            if target_lvl > unlocked_level:
                target_lvl = unlocked_level
            current_xp = state.get('xp', 0)
            state = get_initial_state(level=target_lvl, current_xp=current_xp)
            state['role'] = request.session.get('player_role', 'COMMANDER')

        elif action == 'next_level':
            current_lvl = state.get('level', 1)
            if state.get('status') == 'WON' and current_lvl < 4:
                next_lvl = current_lvl + 1
                unlocked_level = max(unlocked_level, next_lvl)
                request.session['unlocked_level'] = unlocked_level
                state = get_initial_state(level=next_lvl, current_xp=state.get('xp', 0))
                state['role'] = request.session.get('player_role', 'COMMANDER')

        elif action in LEGAL_ACTIONS or (action and action.startswith('repair_module_')):
            if state.get('status') == 'ACTIVE':
                before_state = copy.deepcopy(state)
                state = advance_turn(state, action)
                if state.get('status') == 'WON':
                    current_lvl = state.get('level', 1)
                    unlocked_level = max(unlocked_level, min(4, current_lvl + 1))
                    request.session['unlocked_level'] = unlocked_level
                    completed_missions = request.session.get('completed_missions', [])
                    if current_lvl not in completed_missions:
                        completed_missions.append(current_lvl)
                    completed_missions = sorted(list(set(completed_missions)))
                    request.session['completed_missions'] = completed_missions
                    r, b, all_c, _ = get_cadet_rank_and_badges(completed_missions, state.get('xp', 0))
                    request.session['earned_badges'] = b

                log_step_to_db(db_session, before_state.get('sol', 1), action, before_state, state)

        request.session['sol_survivor_state'] = state
        request.session['unlocked_level'] = unlocked_level
        request.session.modified = True
        get_or_create_db_session(request, state)
        return redirect('dashboard')

    completed_missions = request.session.get('completed_missions', [])
    rank, earned_badges, all_missions_completed, badge_details = get_cadet_rank_and_badges(
        completed_missions, state.get('xp', 0)
    )
    request.session['earned_badges'] = earned_badges
    crew_status, crew_status_color = get_crew_status(state)

    # Analytics forecast & NASA Data telemetry
    forecast_data = generate_predictive_forecast(state, horizon_sols=5)
    nasa_telemetry = get_nasa_data_center_telemetry(mode="real", sol_index=state.get('sol', 1))
    curriculum = get_all_curriculum_modules()

    # Step logs for replay timeline
    step_logs = []
    if db_session:
        step_logs = list(db_session.steps.all().order_by('-sol')[:15])

    context = {
        'state': state,
        'rank': rank,
        'levels': LEVEL_CONFIGS,
        'unlocked_level': unlocked_level,
        'crew_status': crew_status,
        'crew_status_color': crew_status_color,
        'telemetry': state.get('telemetry', compute_nasa_telemetry(state)),
        'advisor': state.get('advisor', compute_houston_advisor(state)),
        'crew': state.get('crew', []),
        'rovers': state.get('rovers', {}),
        'emergency_protocols': state.get('emergency_protocols', {}),
        'modules': state.get('modules', {}),
        'forecast_data': forecast_data,
        'nasa_data': nasa_telemetry,
        'curriculum': curriculum,
        'step_logs': step_logs,
        'commander_name': request.session.get('commander_name', request.session.get('cadet_name', 'Junior Commander')),
        'cadet_name': request.session.get('cadet_name', 'Junior Commander'),
        'cadet_avatar': request.session.get('cadet_avatar', '👨‍🚀'),
        'cadet_pin': request.session.get('cadet_pin', '2026'),
        'cadet_age': request.session.get('cadet_age', 10),
        'cadet_age_bracket': request.session.get('cadet_age_bracket', '8–9 yrs'),
        'show_subtitles': request.session.get('show_subtitles', True),
        'player_role': request.session.get('player_role', 'COMMANDER'),
        'completed_missions': completed_missions,
        'earned_badges': earned_badges,
        'badge_details': badge_details,
        'all_missions_completed': all_missions_completed,
        'grand_rank': GRAND_RANK,
        'supreme_badge': SUPREME_BADGE,
    }
    return render(request, 'mission/dashboard.html', context)


@csrf_exempt
def api_action(request):
    """
    Seamless AJAX JSON API endpoint for real-time turn execution.
    Validates actions server-side, prevents replay exploits, logs to DB, and returns updated state.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    if 'unlocked_level' not in request.session:
        request.session['unlocked_level'] = 1

    state = request.session.get('sol_survivor_state')
    if not state or 'telemetry' not in state:
        state = get_initial_state(level=1, current_xp=0)
    else:
        state = ensure_state_structure(state)

    unlocked_level = request.session.get('unlocked_level', 1)
    db_session = get_or_create_db_session(request, state)

    try:
        body = json.loads(request.body.decode('utf-8'))
    except Exception:
        body = request.POST

    action = body.get('action', '').strip()
    target_lvl_val = body.get('level')
    role_val = body.get('role')

    if role_val in ['COMMANDER', 'ENGINEER', 'SCIENTIST']:
        request.session['player_role'] = role_val
        state['role'] = role_val

    # Server-side validation
    if action == 'restart':
        try:
            target_lvl = int(target_lvl_val) if target_lvl_val else state.get('level', 1)
        except (ValueError, TypeError):
            target_lvl = 1
        if target_lvl > unlocked_level:
            target_lvl = unlocked_level
        current_xp = state.get('xp', 0)
        state = get_initial_state(level=target_lvl, current_xp=current_xp)
        state['role'] = request.session.get('player_role', 'COMMANDER')

    elif action == 'next_level':
        current_lvl = state.get('level', 1)
        if state.get('status') == 'WON' and current_lvl < 4:
            next_lvl = current_lvl + 1
            unlocked_level = max(unlocked_level, next_lvl)
            request.session['unlocked_level'] = unlocked_level
            state = get_initial_state(level=next_lvl, current_xp=state.get('xp', 0))
            state['role'] = request.session.get('player_role', 'COMMANDER')

    elif action in LEGAL_ACTIONS or action.startswith('repair_module_'):
        # Replay exploit protection: cannot execute standard turns on terminated mission
        if state.get('status') != 'ACTIVE':
            return JsonResponse({
                'success': False,
                'error': f"Mission has ended with status: {state.get('status')}. Please restart or advance tier.",
                'state': state
            })

        before_state = copy.deepcopy(state)

        # Handle specific module repair action
        if action.startswith('repair_module_'):
            mod_id = action.replace('repair_module_', '')
            if 'modules' in state and mod_id in state['modules']:
                state['modules'][mod_id]['health'] = 100
                state['modules'][mod_id]['status'] = 'NOMINAL'
                state['power'] = max(0, state['power'] - 8)
                state['xp'] += 100
                state['log'].append(f"SOL {state['sol']} REPAIR: {state['modules'][mod_id]['name']} fully overhauled and re-certified!")
        else:
            state = advance_turn(state, action)

        if state.get('status') == 'WON':
            current_lvl = state.get('level', 1)
            unlocked_level = max(unlocked_level, min(4, current_lvl + 1))
            request.session['unlocked_level'] = unlocked_level
            completed_missions = request.session.get('completed_missions', [])
            if current_lvl not in completed_missions:
                completed_missions.append(current_lvl)
            completed_missions = sorted(list(set(completed_missions)))
            request.session['completed_missions'] = completed_missions
            r, b, all_c, _ = get_cadet_rank_and_badges(completed_missions, state.get('xp', 0))
            request.session['earned_badges'] = b

        log_step_to_db(db_session, before_state.get('sol', 1), action, before_state, state)

    else:
        return JsonResponse({
            'success': False,
            'error': f"Invalid engineering action: '{action}'. Command rejected by Mission Control."
        }, status=400)

    request.session['sol_survivor_state'] = state
    request.session['unlocked_level'] = unlocked_level
    request.session.modified = True
    get_or_create_db_session(request, state)

    completed_missions = request.session.get('completed_missions', [])
    rank, earned_badges, all_missions_completed, badge_details = get_cadet_rank_and_badges(
        completed_missions, state.get('xp', 0)
    )
    request.session['earned_badges'] = earned_badges

    announcement = ""
    if state.get('status') == 'WON':
        cadet_callsign = request.session.get('cadet_name', 'Commander')
        if all_missions_completed:
            announcement = f"Congratulations Cadet {cadet_callsign}. All four Martian sectors secured. Grand Mars Fleet Admiral rank and Supreme Planetary Commander badge unlocked."
        else:
            lvl_info = MISSION_BADGES.get(state.get('level', 1), {})
            announcement = f"Congratulations Cadet {cadet_callsign}! {lvl_info.get('badge', '')} unlocked and promoted to {lvl_info.get('rank', 'Cadet')}!"

    crew_status, crew_status_color = get_crew_status(state)
    forecast = generate_predictive_forecast(state, horizon_sols=5)

    return JsonResponse({
        'success': True,
        'state': state,
        'rank': rank,
        'crew_status': crew_status,
        'crew_status_color': crew_status_color,
        'unlocked_level': unlocked_level,
        'telemetry': state.get('telemetry', compute_nasa_telemetry(state)),
        'advisor': state.get('advisor', compute_houston_advisor(state)),
        'crew': state.get('crew', []),
        'rovers': state.get('rovers', {}),
        'emergency_protocols': state.get('emergency_protocols', {}),
        'modules': state.get('modules', {}),
        'forecast': forecast,
        'completed_missions': completed_missions,
        'earned_badges': earned_badges,
        'badge_details': badge_details,
        'all_missions_completed': all_missions_completed,
        'grand_rank': GRAND_RANK,
        'supreme_badge': SUPREME_BADGE,
        'announcement': announcement
    })


@csrf_exempt
def api_cli_command(request):
    """Processes interactive CLI terminal commands with server validation."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        raw_cmd = data.get('command', '').strip().lower()
    except Exception:
        raw_cmd = request.POST.get('command', '').strip().lower()

    state = request.session.get('sol_survivor_state', get_initial_state(1))
    state = ensure_state_structure(state)
    db_session = get_or_create_db_session(request, state)

    response_text = ""
    triggered_action = None

    if raw_cmd in ['help', '?']:
        response_text = (
            "AVAILABLE COMMANDS:\n"
            "> status, diag, vitals, modules, forecast\n"
            "> 1 (moxie), 2 (food), 3 (shields), 4 (solar), 5 (dim heaters), 6 (water), 7 (seals)\n"
            "> rover, drone, drill\n"
            "> emergency rtg, emergency o2, emergency shield\n"
            "> role commander, role engineer, role scientist\n"
            "> hint, advisor, abort"
        )
    elif raw_cmd in ['hint', 'advisor', 'advice', 'guide']:
        adv = state.get('advisor', compute_houston_advisor(state))
        response_text = f"HOUSTON ADVISORY: {adv['title']} - {adv['message']} (Rec: {adv['rec_action'].upper()})"
    elif raw_cmd in ['status', 'diag', 'diagnostics']:
        p, o, f, s, w, integ = (
            state['power'], state['oxygen'], state['food'], state['shielding'],
            state.get('water', 100), state.get('integrity', 100)
        )
        response_text = f"TELEMETRY -> PWR:{p}% | O2:{o}% | FOOD:{f}% | SHLD:{s}% | H2O:{w}% | HULL:{integ}% | SOL:{state['sol']}/{state['target_sols']}"
    elif raw_cmd in ['modules', 'habitat', 'subsystems']:
        mod_report = " | ".join([f"{m['name']}: {m['health']}% ({m['status']})" for m in state.get('modules', {}).values()])
        response_text = f"HABITAT SUBSYSTEMS: {mod_report}"
    elif raw_cmd in ['crew', 'vitals']:
        crew_summary = " | ".join([f"{c['role']}: {c['health']}% HP ({c['bpm']} BPM, {c['spo2']}% SpO2)" for c in state.get('crew', [])])
        response_text = f"CREW BIOMETRICS: {crew_summary}"
    elif raw_cmd in ['drone', 'ingenuity']:
        triggered_action = 'deploy_drone'
    elif raw_cmd in ['rover', 'perseverance']:
        triggered_action = 'deploy_rover'
    elif raw_cmd in ['drill', 'ice']:
        triggered_action = 'deploy_drill'
    elif raw_cmd in ['emergency rtg', 'rtg']:
        triggered_action = 'emergency_rtg'
    elif raw_cmd in ['emergency o2', 'hyperbaric']:
        triggered_action = 'emergency_o2'
    elif raw_cmd in ['emergency shield', 'pulse']:
        triggered_action = 'emergency_shield'
    elif raw_cmd in ['1', 'boost moxie', 'moxie', 'boost oxygen']:
        triggered_action = 'boost_oxygen'
    elif raw_cmd in ['2', 'boost food', 'food', 'hydroponics', 'uv']:
        triggered_action = 'boost_food'
    elif raw_cmd in ['3', 'boost shields', 'shields', 'deflector']:
        triggered_action = 'boost_shields'
    elif raw_cmd in ['4', 'solar', 'optimize solar', 'boost solar', 'sun']:
        triggered_action = 'optimize_solar'
    elif raw_cmd in ['5', 'dim heaters', 'conserve', 'conserve power', 'heaters']:
        triggered_action = 'conserve_power'
    elif raw_cmd in ['6', 'water', 'recycle water', 'purify']:
        triggered_action = 'recycle_water'
    elif raw_cmd in ['7', 'hull', 'seal', 'repair seal', 'integrity']:
        triggered_action = 'repair_seal'
    elif raw_cmd in ['role commander', 'role engineer', 'role scientist']:
        new_role = raw_cmd.split()[1].upper()
        request.session['player_role'] = new_role
        state['role'] = new_role
        response_text = f"CREW ROLE RECONFIGURED: Switched primary station to {new_role}."
    elif raw_cmd in ['abort', 'reset', 'restart']:
        triggered_action = 'restart'
    else:
        response_text = f"UNKNOWN COMMAND '{raw_cmd}'. TYPE 'help' OR 'hint' FOR MISSION COMMANDS."

    if triggered_action:
        before_state = copy.deepcopy(state)
        state = advance_turn(state, triggered_action) if triggered_action != 'restart' else get_initial_state(state.get('level', 1), state.get('xp', 0))
        if state.get('status') == 'WON':
            current_lvl = state.get('level', 1)
            unlocked_level = max(request.session.get('unlocked_level', 1), min(4, current_lvl + 1))
            request.session['unlocked_level'] = unlocked_level
            completed_missions = request.session.get('completed_missions', [])
            if current_lvl not in completed_missions:
                completed_missions.append(current_lvl)
            completed_missions = sorted(list(set(completed_missions)))
            request.session['completed_missions'] = completed_missions
            r, b, all_c, _ = get_cadet_rank_and_badges(completed_missions, state.get('xp', 0))
            request.session['earned_badges'] = b

        request.session['sol_survivor_state'] = state
        request.session.modified = True
        get_or_create_db_session(request, state)
        log_step_to_db(db_session, before_state.get('sol', 1), triggered_action, before_state, state)
        response_text = f"EXECUTED: {triggered_action.upper()} on Sol {state['sol']}"

    completed_missions = request.session.get('completed_missions', [])
    rank, earned_badges, all_missions_completed, badge_details = get_cadet_rank_and_badges(
        completed_missions, state.get('xp', 0)
    )
    request.session['earned_badges'] = earned_badges
    crew_status, crew_status_color = get_crew_status(state)

    return JsonResponse({
        'response': response_text,
        'state': state,
        'rank': rank,
        'crew_status': crew_status,
        'crew_status_color': crew_status_color,
        'telemetry': state.get('telemetry', compute_nasa_telemetry(state)),
        'advisor': state.get('advisor', compute_houston_advisor(state)),
        'crew': state.get('crew', []),
        'rovers': state.get('rovers', {}),
        'emergency_protocols': state.get('emergency_protocols', {}),
        'modules': state.get('modules', {}),
        'completed_missions': completed_missions,
        'earned_badges': earned_badges,
        'all_missions_completed': all_missions_completed,
        'grand_rank': GRAND_RANK,
        'supreme_badge': SUPREME_BADGE,
    })


@csrf_exempt
def api_ai_chat(request):
    """Interactive AI Mission Commander Chat endpoint."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8'))
        user_query = body.get('message', '').strip()
    except Exception:
        user_query = request.POST.get('message', '').strip()

    if not user_query:
        return JsonResponse({'reply': 'Awaiting flight question or systems inquiry.'})

    state = request.session.get('sol_survivor_state', get_initial_state(1))
    reply = answer_mission_chat(state, user_query)
    return JsonResponse({'reply': reply})


@csrf_exempt
def api_forecast(request):
    """Returns predictive resource forecasting with optional candidate action comparison."""
    state = request.session.get('sol_survivor_state', get_initial_state(1))
    candidate = request.GET.get('action') or None
    forecast = generate_predictive_forecast(state, candidate_action=candidate, horizon_sols=5)
    return JsonResponse(forecast)


@csrf_exempt
def api_nasa_data(request):
    """Provides verified NASA PDS & DONKI telemetry with Real vs Simulation mode toggle."""
    mode = request.GET.get('mode', 'real').lower()
    state = request.session.get('sol_survivor_state', get_initial_state(1))
    sol_idx = state.get('sol', 1)
    data = get_nasa_data_center_telemetry(mode=mode, sol_index=sol_idx)
    return JsonResponse(data)


@csrf_exempt
def api_submit_quiz(request):
    """Validates student STEM curriculum quizzes and records learning achievements."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8'))
        topic_id = body.get('topic_id')
        selected_idx = int(body.get('selected_index', 0))
    except Exception:
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    result = submit_quiz_answer(topic_id, selected_idx)
    if result.get('success'):
        state = request.session.get('sol_survivor_state', get_initial_state(1))
        state['xp'] = state.get('xp', 0) + result['xp_earned']
        request.session['sol_survivor_state'] = state
        request.session.modified = True

        # Save to database
        db_session = get_or_create_db_session(request, state)
        if db_session:
            try:
                STEMQuizRecord.objects.create(
                    session=db_session,
                    topic=topic_id,
                    question=f"Module {topic_id} Quiz",
                    user_answer=str(selected_idx),
                    correct_answer="Checked",
                    is_correct=result['is_correct'],
                    xp_earned=result['xp_earned']
                )
            except Exception:
                pass

        result['total_xp'] = state['xp']
        result['rank'] = calculate_rank(state['xp'])

    return JsonResponse(result)


def mission_report_view(request):
    """Comprehensive Mission Debriefing Report & Post-Flight Analytics."""
    if not request.session.get('is_authenticated_cadet') or 'cadet_name' not in request.session:
        return redirect('login')
    state = request.session.get('sol_survivor_state', get_initial_state(1))
    xp = state.get('xp', 500)
    level = state.get('level', 1)
    rank = calculate_rank(xp)
    commander_name = request.session.get('commander_name', 'Junior Commander')

    total_res = (
        state.get('power', 60) + state.get('oxygen', 70) + state.get('food', 65) +
        state.get('shielding', 75) + state.get('water', 80) + state.get('integrity', 85)
    )
    efficiency = round((total_res / 600.0) * 100, 1)

    db_session = get_or_create_db_session(request, state)
    steps = []
    if db_session:
        steps = list(db_session.steps.all().order_by('sol'))

    context = {
        'state': state,
        'commander_name': commander_name,
        'role': request.session.get('player_role', 'COMMANDER'),
        'rank': rank,
        'xp': xp,
        'level': level,
        'efficiency': efficiency,
        'crises_handled': state.get('crises_handled', 0),
        'clutch_count': state.get('clutch_count', 0),
        'steps': steps,
        'date': datetime.now().strftime("%B %d, %Y"),
    }
    return render(request, 'mission/report.html', context)


def certificate_view(request):
    """Downloadable / Printable Junior Mars Mission Commander Certificate."""
    if not request.session.get('is_authenticated_cadet') or 'cadet_name' not in request.session:
        return redirect('login')
    state = request.session.get('sol_survivor_state', {})
    mission_xp = state.get('xp', 2500)
    level = state.get('level', 4)
    cadet_name = request.GET.get('name') or request.session.get('cadet_name') or request.session.get('commander_name', 'Cadet Aarav')
    cadet_age_bracket = request.session.get('cadet_age_bracket', '10–11 yrs')
    completed_missions = request.session.get('completed_missions', [1, 2, 3, 4] if level == 4 else [1])

    # Calculate cumulative Space Academy XP from AcademyProfile
    academy_xp = 0
    if request.session.session_key:
        profile = AcademyProfile.objects.filter(session_key=request.session.session_key).first()
        if profile:
            academy_xp = profile.total_academy_xp

    total_cumulative_xp = mission_xp + academy_xp

    rank, earned_badges, all_missions_completed, badge_details = get_cadet_rank_and_badges(
        completed_missions, total_cumulative_xp
    )

    total_res = (
        state.get('power', 60) + state.get('oxygen', 70) + state.get('food', 65) +
        state.get('shielding', 75) + state.get('water', 80) + state.get('integrity', 85)
    )
    efficiency = round((total_res / 600.0) * 100, 1)

    verification_hash = f"SOLSURVIVOR-MARS-{hex(abs(hash(cadet_name + str(total_cumulative_xp) + str(level))))[2:10].upper()}-2026"

    context = {
        'commander_name': cadet_name,
        'cadet_name': cadet_name,
        'cadet_age_bracket': cadet_age_bracket,
        'rank': rank,
        'xp': total_cumulative_xp,
        'mission_xp': mission_xp,
        'academy_xp': academy_xp,
        'level': level,
        'efficiency': efficiency,
        'crises_handled': state.get('crises_handled', 6),
        'clutch_count': state.get('clutch_count', 2),
        'date': datetime.now().strftime("%B %d, %Y"),
        'verification_hash': verification_hash,
        'completed_missions': completed_missions,
        'earned_badges': earned_badges,
        'badge_details': badge_details,
        'all_missions_completed': all_missions_completed,
        'grand_rank': GRAND_RANK,
        'supreme_badge': SUPREME_BADGE,
    }
    return render(request, 'mission/certificate.html', context)


# ==============================================================================
# SPACE ACADEMY VIEWS & API CONTROLLERS
# ==============================================================================

def get_or_create_academy_profile(request):
    """Retrieves or initializes the Space Academy learner profile for this session."""
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key

    profile, _ = AcademyProfile.objects.get_or_create(
        session_key=session_key,
        defaults={
            'callsign': request.session.get('commander_name', 'Space Explorer'),
            'age_group': '11-13',
            'difficulty': 'medium',
            'total_academy_xp': 0,
            'games_completed_count': 0
        }
    )
    return profile


def academy_view(request):
    """
    Space Academy Hub: 8 educational mini-games, age selection,
    NASA learning achievements, daily challenges, and personal best scores.
    """
    if not request.session.get('is_authenticated_cadet') or 'cadet_name' not in request.session:
        return redirect('login')
    profile = get_or_create_academy_profile(request)

    # Calculate high scores map
    scores_map = {}
    completed_distinct = set()
    for sc in AcademyGameScore.objects.filter(profile=profile):
        if sc.game_id not in scores_map or sc.score > scores_map[sc.game_id]:
            scores_map[sc.game_id] = sc.score
        if sc.completed:
            completed_distinct.add(sc.game_id)

    profile.games_completed_count = len(completed_distinct)
    profile.save()

    completion_pct = int(round((len(completed_distinct) / 8.0) * 100))

    # Unlocked achievements
    unlocked_ach_ids = set(
        AcademyAchievement.objects.filter(profile=profile).values_list('achievement_id', flat=True)
    )

    # Daily challenge
    today = datetime.now().date()
    daily, _ = AcademyDailyChallenge.objects.get_or_create(
        profile=profile,
        challenge_date=today,
        challenge_key='daily_2_games',
        defaults={
            'title': 'Junior Explorer Daily: Complete 2 Mini-Games',
            'description': 'Play and complete at least two Space Academy missions today to earn bonus XP.',
            'target_count': 2,
            'current_count': 0,
            'is_completed': False,
            'xp_reward': 150
        }
    )

    games_list = []
    for gid, gdata in ACADEMY_GAMES.items():
        g_copy = copy.deepcopy(gdata)
        g_copy['high_score'] = scores_map.get(gid)
        g_copy['is_completed'] = gid in completed_distinct
        games_list.append(g_copy)

    completed_missions = request.session.get('completed_missions', [])
    cadet_rank, earned_badges, all_missions_completed, badge_details = get_cadet_rank_and_badges(
        completed_missions, profile.total_academy_xp
    )

    context = {
        'profile': profile,
        'cadet_name': request.session.get('cadet_name', profile.callsign),
        'cadet_avatar': request.session.get('cadet_avatar', '👨‍🚀'),
        'cadet_age_bracket': request.session.get('cadet_age_bracket', '10–11 yrs'),
        'completed_missions': completed_missions,
        'earned_badges': earned_badges,
        'badge_details': badge_details,
        'all_missions_completed': all_missions_completed,
        'grand_rank': GRAND_RANK,
        'cadet_rank': cadet_rank,
        'games': games_list,
        'scores_map': scores_map,
        'completion_pct': completion_pct,
        'achievements_def': ACADEMY_ACHIEVEMENTS_DEF,
        'unlocked_ach_ids': unlocked_ach_ids,
        'achievements_unlocked_count': len(unlocked_ach_ids),
        'daily_challenge': daily,
    }
    return render(request, 'mission/academy.html', context)


def academy_game_view(request, game_id):
    """Dedicated interactive game theater for an individual Space Academy mini-game."""
    if not request.session.get('is_authenticated_cadet') or 'cadet_name' not in request.session:
        return redirect('login')
    if game_id not in ACADEMY_GAMES:
        return redirect('academy')

    profile = get_or_create_academy_profile(request)
    game_data = ACADEMY_GAMES[game_id]

    context = {
        'profile': profile,
        'game': game_data,
        'game_id': game_id,
    }
    return render(request, 'mission/academy_game.html', context)


def api_academy_set_profile(request):
    """Updates learner age tier (8-10, 11-13, 14-16) and difficulty (easy, medium, hard)."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8'))
        age_group = body.get('age_group', '11-13')
        difficulty = body.get('difficulty', 'medium')

        profile = get_or_create_academy_profile(request)
        profile.age_group = age_group
        profile.difficulty = difficulty
        profile.save()

        age_labels = {
            '8-10': 'Junior Cadet (Ages 8-10)',
            '11-13': 'Flight Specialist (Ages 11-13)',
            '14-16': 'Mission Commander (Ages 14-16)'
        }

        return JsonResponse({
            'status': 'ok',
            'age_group': profile.age_group,
            'difficulty': profile.difficulty,
            'age_label': age_labels.get(profile.age_group, profile.age_group)
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def api_academy_submit_score(request):
    """
    Submits, validates, and awards XP for a mini-game completion.
    Synchronizes rewards to both AcademyProfile and the active Sol Survivor MissionSession!
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8'))
        game_id = body.get('game_id')
        score = int(body.get('score', 0))
        time_seconds = int(body.get('time_seconds', 0))
        details = body.get('details', {})

        profile = get_or_create_academy_profile(request)
        result = validate_and_award_academy_score(profile, game_id, score, time_seconds, details)

        if not result['valid']:
            return JsonResponse({'status': 'invalid', 'message': result['message']})

        xp_awarded = result['xp_awarded']

        # Synchronize awarded XP with active Sol Survivor game state
        state = request.session.get('sol_survivor_state', get_initial_state(1))
        state['xp'] = state.get('xp', 0) + xp_awarded
        request.session['sol_survivor_state'] = state
        request.session.modified = True

        # Synchronize with MissionSession database model
        db_session = get_or_create_db_session(request, state)
        if db_session:
            db_session.xp = state['xp']
            db_session.save()

        # Update Daily Challenge
        today = datetime.now().date()
        daily = AcademyDailyChallenge.objects.filter(profile=profile, challenge_date=today, challenge_key='daily_2_games').first()
        if daily and not daily.is_completed:
            daily.current_count += 1
            if daily.current_count >= daily.target_count:
                daily.is_completed = True
                profile.total_academy_xp += daily.xp_reward
                profile.save()
                state['xp'] += daily.xp_reward
                request.session['sol_survivor_state'] = state
                request.session.modified = True
            daily.save()

        return JsonResponse({
            'status': 'ok',
            'xp_awarded': xp_awarded,
            'total_academy_xp': profile.total_academy_xp,
            'sol_survivor_xp': state['xp'],
            'new_achievements': result.get('new_achievements', []),
            'message': result['message']
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def api_academy_progress(request):
    """Returns JSON progress payload for learner dashboard."""
    profile = get_or_create_academy_profile(request)
    achievements = list(AcademyAchievement.objects.filter(profile=profile).values('achievement_id', 'title', 'unlocked_at'))
    scores = list(AcademyGameScore.objects.filter(profile=profile).values('game_id', 'score', 'completed', 'timestamp')[:20])

    return JsonResponse({
        'status': 'ok',
        'callsign': profile.callsign,
        'age_group': profile.age_group,
        'difficulty': profile.difficulty,
        'total_academy_xp': profile.total_academy_xp,
        'games_completed': profile.games_completed_count,
        'achievements': achievements,
        'recent_scores': scores
    })

