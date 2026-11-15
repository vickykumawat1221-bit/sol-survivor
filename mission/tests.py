"""
Comprehensive automated test suite for Sol Survivor: AI-Powered Mars Mission Digital Twin.
Tests:
- Scientific resource calculations (Power, O2, Food, Water, Shielding, Integrity)
- Server-side action validation and replay exploit protection
- Level unlocking and unauthorized tier access prevention
- Multi-turn cascading failures & thermal pipe freeze
- Deterministic seed crisis generation
- AI Mission Commander decision tree & chat
- Predictive survival forecasting (3-5 Sols)
- NASA Data Center provenance & real/simulated mode toggle
- SQLite database persistence & replay step logging
- STEM educational quizzes & scoring
- Mission report and Junior Commander Certificate generation
- Complete mission progression through all 4 levels
"""

import json
from django.test import TestCase, Client
from django.urls import reverse

from mission.models import MissionSession, MissionStepLog, STEMQuizRecord
from mission.engine import (
    get_initial_state, advance_turn, LEVEL_CONFIGS, calculate_rank, compute_nasa_telemetry
)
from mission.nasa_data import get_nasa_data_center_telemetry
from mission.crisis_engine import generate_crisis_for_sol
from mission.ai_advisor import evaluate_decision_tree, answer_mission_chat
from mission.forecasting import generate_predictive_forecast
from mission.learning_center import submit_quiz_answer, get_all_curriculum_modules

class SolSurvivorCoreEngineTests(TestCase):
    def test_initial_state_closed_loop(self):
        state = get_initial_state(level=1)
        self.assertEqual(state['level'], 1)
        self.assertEqual(state['sol'], 1)
        self.assertEqual(state['power'], 100)
        self.assertEqual(state['oxygen'], 100)
        self.assertEqual(state['food'], 100)
        self.assertEqual(state['shielding'], 100)
        self.assertEqual(state['water'], 100)
        self.assertEqual(state['integrity'], 100)
        self.assertEqual(state['status'], 'ACTIVE')
        self.assertIn('modules', state)
        self.assertEqual(len(state['modules']), 7)
        self.assertIn('solar_arrays', state['modules'])
        self.assertIn('water_recycler', state['modules'])
        self.assertIn('telemetry', state)
        self.assertIn('advisor', state)

    def test_actions_tradeoffs(self):
        state = get_initial_state(level=1)
        new_state = advance_turn(state, 'boost_oxygen')
        self.assertEqual(new_state['power'], 93)
        self.assertEqual(new_state['sol'], 2)
        # Verify optimize_solar adds safe clean power
        solar_state = advance_turn(new_state, 'optimize_solar')
        self.assertEqual(solar_state['power'], 95)
        self.assertEqual(solar_state['sol'], 3)

    def test_water_and_integrity_actions(self):
        state = get_initial_state(level=1)
        state['water'] = 50
        state['integrity'] = 50
        state = advance_turn(state, 'recycle_water')
        self.assertGreater(state['water'], 50)
        state = advance_turn(state, 'repair_seal')
        self.assertGreater(state['integrity'], 50)

    def test_rover_dispatches(self):
        state = get_initial_state(level=1)
        state['power'] = 50
        new_state = advance_turn(state, 'deploy_rover')
        self.assertGreater(new_state['power'], 50)
        self.assertEqual(new_state['rovers']['perseverance']['status'], 'COOLDOWN')

    def test_subsurface_drill_ice_extraction(self):
        state = get_initial_state(level=1)
        state['water'] = 60
        state = advance_turn(state, 'deploy_drill')
        self.assertGreater(state['water'], 60)
        self.assertEqual(state['rovers']['drill']['status'], 'COOLDOWN')

    def test_emergency_override_rtg(self):
        state = get_initial_state(level=2)
        state['temp_warning'] = True
        state['cascade_counter'] = 1
        new_state = advance_turn(state, 'emergency_rtg')
        self.assertFalse(new_state['temp_warning'])
        self.assertTrue(new_state['emergency_protocols']['rtg_burst']['used'])

    def test_cascading_thermal_failure_level_2(self):
        state = get_initial_state(level=2)
        state = advance_turn(state, 'conserve_power')
        self.assertTrue(state['temp_warning'])
        self.assertEqual(state['cascade_counter'], 3)

        state = advance_turn(state, 'boost_shields')
        self.assertEqual(state['cascade_counter'], 2)
        state = advance_turn(state, 'boost_shields')
        self.assertEqual(state['cascade_counter'], 1)
        state = advance_turn(state, 'boost_shields')
        self.assertFalse(state['temp_warning'])
        self.assertTrue(any("CASCADING FAILURE TRIGGERED" in log for log in state['log']))

    def test_clutch_survival_bonus(self):
        state = get_initial_state(level=1)
        state['power'] = 14
        initial_xp = state['xp']
        new_state = advance_turn(state, 'conserve_power')
        self.assertEqual(new_state['status'], 'ACTIVE')
        self.assertGreater(new_state['xp'], initial_xp + 50)
        self.assertIn("CLUTCH SURVIVOR", new_state['badge'])

    def test_emergency_battery_breaker_cadet(self):
        state = get_initial_state(level=1)
        state['power'] = 2
        new_state = advance_turn(state, 'boost_oxygen')
        self.assertEqual(new_state['status'], 'ACTIVE')
        self.assertEqual(new_state['power'], 5)
        self.assertTrue(new_state['emergency_battery_tripped'])
        final_state = advance_turn(new_state, 'boost_oxygen')
        self.assertEqual(final_state['status'], 'LOST')
        self.assertIn("BLACKOUT", final_state['fail_reason'])

    def test_water_loss_condition(self):
        state = get_initial_state(level=3)
        state['water'] = 1
        new_state = advance_turn(state, 'conserve_power')
        self.assertEqual(new_state['status'], 'LOST')
        self.assertIn("DEHYDRATION", new_state['fail_reason'])

    def test_rank_calculation(self):
        self.assertEqual(calculate_rank(200), "Cadet")
        self.assertEqual(calculate_rank(700), "Flight Engineer")
        self.assertEqual(calculate_rank(1500), "Mission Specialist")
        self.assertEqual(calculate_rank(2600), "Mars Base Commander")


class SolSurvivorScientificModuleTests(TestCase):
    def test_nasa_data_center_provenance(self):
        real_data = get_nasa_data_center_telemetry(mode="real", sol_index=1)
        self.assertTrue(real_data['is_real_data'])
        self.assertEqual(real_data['weather']['data_status'], 'OBSERVED')
        self.assertIn("NASA", real_data['citation'])

        sim_data = get_nasa_data_center_telemetry(mode="simulated", sol_index=1)
        self.assertFalse(sim_data['is_real_data'])
        self.assertEqual(sim_data['weather']['data_status'], 'SIMULATED DIGITAL TWIN')

    def test_deterministic_crisis_generator(self):
        crises_sol_4 = generate_crisis_for_sol(level=1, sol=4, seed=42)
        self.assertEqual(len(crises_sol_4), 1)
        self.assertEqual(crises_sol_4[0]['id'], 'dust_storm')

        # Level 3 features simultaneous double crises
        crises_sol_5 = generate_crisis_for_sol(level=3, sol=5, seed=42)
        self.assertEqual(len(crises_sol_5), 2)
        crisis_ids = [c['id'] for c in crises_sol_5]
        self.assertIn('solar_particle_event', crisis_ids)
        self.assertIn('dust_storm', crisis_ids)

    def test_ai_advisor_decision_tree(self):
        state = get_initial_state(level=1)
        state['power'] = 15
        eval_result = evaluate_decision_tree(state, advance_turn)
        self.assertIn('rec_action', eval_result)
        self.assertIn('comparison', eval_result)
        self.assertGreater(len(eval_result['comparison']), 0)

    def test_ai_chat_response(self):
        state = get_initial_state(level=1)
        reply = answer_mission_chat(state, "How does MOXIE make oxygen?")
        self.assertIn("MOXIE", reply)
        self.assertIn("electrolysis", reply)

    def test_predictive_survival_forecast(self):
        state = get_initial_state(level=1)
        forecast = generate_predictive_forecast(state, horizon_sols=5)
        self.assertEqual(len(forecast['labels']), 5)
        self.assertEqual(len(forecast['datasets']), 5)
        self.assertIn('risk_score', forecast)
        self.assertIn('risk_tier', forecast)

    def test_stem_curriculum_and_quiz_scoring(self):
        modules = get_all_curriculum_modules()
        self.assertGreater(len(modules), 2)
        res = submit_quiz_answer('moxie_electrolysis', selected_index=0)
        self.assertTrue(res['success'])
        self.assertTrue(res['is_correct'])
        self.assertEqual(res['xp_earned'], 100)


class SolSurvivorViewAndAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['is_authenticated_cadet'] = True
        session['cadet_name'] = 'Junior Commander'
        session['cadet_age_bracket'] = '10–11 yrs'
        session['completed_missions'] = []
        session['earned_badges'] = []
        session.save()

    def test_unauthenticated_dashboard_redirect(self):
        anon_client = Client()
        response = anon_client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_unauthenticated_academy_redirect(self):
        anon_client = Client()
        response = anon_client.get(reverse('academy'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_unauthenticated_report_redirect(self):
        anon_client = Client()
        response = anon_client.get(reverse('mission_report'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_unauthenticated_certificate_redirect(self):
        anon_client = Client()
        response = anon_client.get(reverse('certificate'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_unauthenticated_academy_game_redirect(self):
        anon_client = Client()
        response = anon_client.get(reverse('academy_game', kwargs={'game_id': 'game_solar'}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_dashboard_get(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SOL SURVIVOR")
        self.assertContains(response, "POWER")
        self.assertContains(response, "WATER")

    def test_api_action_valid(self):
        response = self.client.post(
            reverse('api_action'),
            data=json.dumps({'action': 'optimize_solar'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['state']['sol'], 2)
        # Verify saved to database
        self.assertGreater(MissionSession.objects.count(), 0)
        self.assertGreater(MissionStepLog.objects.count(), 0)

    def test_api_action_invalid_rejected(self):
        response = self.client.post(
            reverse('api_action'),
            data=json.dumps({'action': 'infinite_cheat_power'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])

    def test_api_cli_endpoint(self):
        response = self.client.post(
            reverse('api_cli'),
            data=json.dumps({'command': 'status'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("TELEMETRY", data['response'])

    def test_api_ai_chat_endpoint(self):
        response = self.client.post(
            reverse('api_ai_chat'),
            data=json.dumps({'message': 'Explain solar power'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("POWER", data['reply'])

    def test_api_forecast_endpoint(self):
        response = self.client.get(reverse('api_forecast'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('datasets', data)

    def test_api_nasa_data_endpoint(self):
        response = self.client.get(reverse('api_nasa_data') + '?mode=real')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['is_real_data'])

    def test_api_submit_quiz_endpoint(self):
        response = self.client.post(
            reverse('api_submit_quiz'),
            data=json.dumps({'topic_id': 'mars_atmosphere', 'selected_index': 0}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['is_correct'])
        self.assertEqual(STEMQuizRecord.objects.count(), 1)

    def test_mission_report_view(self):
        response = self.client.get(reverse('mission_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "POST-FLIGHT DEBRIEFING REPORT")

    def test_certificate_view(self):
        response = self.client.get(reverse('certificate') + '?name=Astronaut+Vicky')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Astronaut Vicky")
        self.assertContains(response, "JUNIOR MARS MISSION COMMANDER CERTIFICATE")
        self.assertContains(response, "SOLSURVIVOR-MARS-")

    def test_end_to_end_level1_to_level4_unlock_progression(self):
        # Level 1 Touchdown (10 Sols)
        state = get_initial_state(level=1)
        for _ in range(10):
            adv = evaluate_decision_tree(state, advance_turn)
            state = advance_turn(state, adv['rec_action'])
        self.assertEqual(state['status'], 'WON')

        # Advance to Level 2
        state = get_initial_state(level=2, current_xp=state['xp'])
        for _ in range(15):
            adv = evaluate_decision_tree(state, advance_turn)
            state = advance_turn(state, adv['rec_action'])
        self.assertEqual(state['status'], 'WON')

        # Advance to Level 3
        state = get_initial_state(level=3, current_xp=state['xp'])
        for _ in range(20):
            adv = evaluate_decision_tree(state, advance_turn)
            state = advance_turn(state, adv['rec_action'])
        self.assertEqual(state['status'], 'WON')

        # Advance to Level 4 Apocalypse Protocol
        state = get_initial_state(level=4, current_xp=state['xp'])
        self.assertEqual(state['level'], 4)
        self.assertEqual(state['target_sols'], 30)


class SpaceAcademyTests(TestCase):
    """
    Comprehensive test suite for Space Academy educational mini-games,
    age adaptation, anti-cheat score validation, XP syncing, and achievement badges.
    """
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['is_authenticated_cadet'] = True
        session['cadet_name'] = 'Cadet Test'
        session['cadet_avatar'] = '👨‍🚀'
        session['cadet_age_bracket'] = '11-13 yrs'
        session.save()

    def test_academy_hub_view(self):
        response = self.client.get(reverse('academy'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SPACE ACADEMY")
        self.assertContains(response, "Planet Explorer")
        self.assertContains(response, "Zero Gravity Challenge")
        self.assertContains(response, "Rocket Builder")
        self.assertContains(response, "Mars Rover Adventure")
        self.assertContains(response, "Asteroid Defender")
        self.assertContains(response, "Save The Astronaut")
        self.assertContains(response, "Orbit Lab")
        self.assertContains(response, "Space Quiz Battle")

    def test_all_8_mini_game_screens(self):
        game_ids = [
            'planet_explorer', 'zero_gravity', 'rocket_builder', 'mars_rover',
            'asteroid_defender', 'save_astronaut', 'gravity_orbit_lab', 'space_quiz_battle'
        ]
        for gid in game_ids:
            response = self.client.get(reverse('academy_game', args=[gid]))
            self.assertEqual(response.status_code, 200, f"Mini-game {gid} failed to load.")
            self.assertContains(response, "NASA LEARNING OBJECTIVES")
            self.assertContains(response, "START MISSION")

    def test_set_age_tier_and_difficulty(self):
        response = self.client.post(
            reverse('api_academy_set_profile'),
            data=json.dumps({'age_group': '14-16', 'difficulty': 'hard'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['age_group'], '14-16')
        self.assertEqual(data['difficulty'], 'hard')

    def test_submit_score_and_xp_sync(self):
        # 1. Anti-Cheat: Reject submission if duration too short (< 3 seconds)
        resp_fast = self.client.post(
            reverse('api_academy_submit_score'),
            data=json.dumps({
                'game_id': 'planet_explorer',
                'score': 200,
                'time_seconds': 1
            }),
            content_type='application/json'
        )
        data_fast = resp_fast.json()
        self.assertEqual(data_fast['status'], 'invalid')

        # 2. Valid submission: awards XP and unlocks badge
        resp_valid = self.client.post(
            reverse('api_academy_submit_score'),
            data=json.dumps({
                'game_id': 'planet_explorer',
                'score': 200,
                'time_seconds': 15,
                'details': {'accuracy': 100}
            }),
            content_type='application/json'
        )
        self.assertEqual(resp_valid.status_code, 200)
        data_valid = resp_valid.json()
        self.assertEqual(data_valid['status'], 'ok')
        self.assertGreater(data_valid['xp_awarded'], 0)
        self.assertIn('Solar System Navigator', data_valid['new_achievements'])

        # 3. Verify sync with Sol Survivor main XP
        session = self.client.session
        state = session.get('sol_survivor_state', {})
        self.assertGreater(state.get('xp', 0), 0)

    def test_academy_progress_api(self):
        # First play a game
        self.client.post(
            reverse('api_academy_submit_score'),
            data=json.dumps({
                'game_id': 'mars_rover',
                'score': 150,
                'time_seconds': 20
            }),
            content_type='application/json'
        )
        response = self.client.get(reverse('api_academy_progress'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertGreaterEqual(data['games_completed'], 1)
        self.assertGreaterEqual(len(data['achievements']), 1)


class CadetLoginCalibrationAndGrandBadgeTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CADET MISSION CALIBRATION")
        self.assertContains(response, "INSTANT LAUNCH (GUEST CADET)")
        self.assertContains(response, "8–9 YRS")
        self.assertContains(response, "10–11 YRS")
        self.assertContains(response, "12–13 YRS")
        self.assertContains(response, "14–16 YRS")

    def test_instant_guest_launch(self):
        response = self.client.post(reverse('login'), data={'action': 'guest_launch'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
        session = self.client.session
        self.assertEqual(session.get('cadet_name'), 'Cadet Guest')
        self.assertTrue(session.get('is_authenticated_cadet'))
        self.assertEqual(session.get('unlocked_level'), 1)
        self.assertTrue(session.get('show_subtitles'))

    def test_cadet_login_with_avatar_and_pin(self):
        response = self.client.post(reverse('login'), data={
            'cadet_name': 'Cadet Rohan',
            'cadet_pin': '2026',
            'cadet_avatar': '⚡',
            'cadet_age': '10–11 yrs',
            'role': 'ENGINEER'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
        session = self.client.session
        self.assertTrue(session.get('is_authenticated_cadet'))
        self.assertEqual(session.get('cadet_name'), 'Cadet Rohan')
        self.assertEqual(session.get('cadet_avatar'), '⚡')
        self.assertEqual(session.get('player_role'), 'ENGINEER')
        self.assertEqual(session.get('unlocked_level'), 2)

    def test_age_calibration_and_profile_sync(self):
        # 1. Age 8-9 yrs -> Level 1, subtitles True
        resp1 = self.client.post(reverse('login'), data={
            'cadet_name': 'Cadet Maya',
            'cadet_age': '8–9 yrs'
        })
        self.assertEqual(resp1.status_code, 302)
        s1 = self.client.session
        self.assertEqual(s1.get('cadet_name'), 'Cadet Maya')
        self.assertEqual(s1.get('unlocked_level'), 1)
        self.assertTrue(s1.get('show_subtitles'))

        # Verify AcademyProfile synced
        from mission.models import AcademyProfile
        profile = AcademyProfile.objects.filter(session_key=self.client.session.session_key).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.callsign, 'Cadet Maya')
        self.assertEqual(profile.age_group, '8-10')
        self.assertEqual(profile.difficulty, 'easy')

        # 2. Age 14-16 yrs -> Level 4, subtitles False
        resp2 = self.client.post(reverse('login'), data={
            'cadet_name': 'Cadet Leo',
            'cadet_age': '14–16 yrs'
        })
        self.assertEqual(resp2.status_code, 302)
        s2 = self.client.session
        self.assertEqual(s2.get('cadet_name'), 'Cadet Leo')
        self.assertEqual(s2.get('unlocked_level'), 4)
        self.assertFalse(s2.get('show_subtitles'))

    def test_logout_and_switch_cadet(self):
        self.client.post(reverse('login'), data={'action': 'guest_launch'})
        self.assertIn('cadet_name', self.client.session)
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('login'))
        self.assertNotIn('cadet_name', self.client.session)

    def test_per_mission_badge_awards_and_grand_rank(self):
        # Log in first
        self.client.post(reverse('login'), data={
            'cadet_name': 'Cadet Aarav',
            'cadet_age': '10–11 yrs'
        })

        from mission.engine import get_cadet_rank_and_badges, GRAND_RANK, SUPREME_BADGE

        # Level 1 only
        rank1, badges1, all_c1, _ = get_cadet_rank_and_badges([1])
        self.assertEqual(rank1, 'Junior Space Cadet')
        self.assertIn('🪐 Touchdown Pioneer', badges1)
        self.assertFalse(all_c1)

        # Level 2 added
        rank2, badges2, all_c2, _ = get_cadet_rank_and_badges([1, 2])
        self.assertEqual(rank2, 'Martian Flight Engineer')
        self.assertIn('🌪️ Dust Storm Navigator', badges2)
        self.assertFalse(all_c2)

        # Level 3 added
        rank3, badges3, all_c3, _ = get_cadet_rank_and_badges([1, 2, 3])
        self.assertEqual(rank3, 'Orbital Mission Specialist')
        self.assertIn('☀️ Solar Shield Tactician', badges3)
        self.assertFalse(all_c3)

        # Level 4 added -> All 4 cleared!
        rank4, badges4, all_c4, _ = get_cadet_rank_and_badges([1, 2, 3, 4])
        self.assertEqual(rank4, GRAND_RANK)
        self.assertIn('🚀 Colony Life-Support Architect', badges4)
        self.assertIn(SUPREME_BADGE, badges4)
        self.assertTrue(all_c4)
        self.assertEqual(len(badges4), 5)

    def test_reboot_form_post_on_failure(self):
        # 1. Login
        self.client.post(reverse('login'), data={'action': 'guest_launch'})
        # 2. Simulate Habitat Failure
        session = self.client.session
        st = session['sol_survivor_state']
        st['status'] = 'LOST'
        st['sol'] = 5
        st['fail_reason'] = 'CRITICAL VOLTAGE COLLAPSE'
        session['sol_survivor_state'] = st
        session.save()

        # 3. Submit reboot form to dashboard
        response = self.client.post(reverse('dashboard'), data={'action': 'restart', 'level': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

        # 4. Check state reset to ACTIVE and Sol 1
        reloaded_session = self.client.session
        reloaded_st = reloaded_session['sol_survivor_state']
        self.assertEqual(reloaded_st['status'], 'ACTIVE')
        self.assertEqual(reloaded_st['sol'], 1)
        self.assertEqual(reloaded_st['power'], 100)

    def test_reboot_api_action_on_failure(self):
        # 1. Login
        self.client.post(reverse('login'), data={'action': 'guest_launch'})
        # 2. Simulate Habitat Failure
        session = self.client.session
        st = session['sol_survivor_state']
        st['status'] = 'LOST'
        st['sol'] = 5
        st['fail_reason'] = 'OXYGEN STARVATION'
        session['sol_survivor_state'] = st
        session.save()

        # 3. Call API restart
        response = self.client.post(
            reverse('api_action'),
            data=json.dumps({'action': 'restart', 'level': 1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['state']['status'], 'ACTIVE')
        self.assertEqual(data['state']['sol'], 1)
        self.assertEqual(data['state']['oxygen'], 100)

    def test_pwa_manifest_and_sw(self):
        resp_m = self.client.get(reverse('pwa_manifest'))
        self.assertEqual(resp_m.status_code, 200)
        self.assertEqual(resp_m['Content-Type'], 'application/json')
        data = json.loads(resp_m.content.decode('utf-8'))
        self.assertEqual(data['short_name'], 'Sol Survivor')
        self.assertEqual(data['start_url'], '/')

        resp_sw = self.client.get(reverse('pwa_sw'))
        self.assertEqual(resp_sw.status_code, 200)
        self.assertEqual(resp_sw['Content-Type'], 'application/javascript')
        self.assertIn('CACHE_NAME', resp_sw.content.decode('utf-8'))

    def test_certificate_with_cumulative_xp_and_all_badges(self):
        # Login and award academy score
        self.client.post(reverse('login'), data={
            'cadet_name': 'Cadet Aarav',
            'cadet_age': '10–11 yrs'
        })
        session = self.client.session
        session['completed_missions'] = [1, 2, 3, 4]
        session.save()

        # Submit academy score to create Academy XP
        self.client.post(
            reverse('api_academy_submit_score'),
            data=json.dumps({
                'game_id': 'planet_explorer',
                'score': 150,
                'time_seconds': 20
            }),
            content_type='application/json'
        )

        response = self.client.get(reverse('certificate'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cadet Aarav")
        self.assertContains(response, "10–11 yrs")
        self.assertContains(response, "GRAND MARS FLEET ADMIRAL")
        self.assertContains(response, "SUPREME PLANETARY COMMANDER BADGE")
        self.assertContains(response, "Touchdown Pioneer")
        self.assertContains(response, "Print Official NASA Cadet Certificate")

