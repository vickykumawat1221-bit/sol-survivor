"""
STEM Educational Learning Center & NASA Curriculum Module.
Provides verified planetary science explanations, age-adaptive learning tracks (Ages 8-16),
and interactive quizzes with instant scientific feedback and XP rewards.
"""

STEM_CURRICULUM_MODULES = [
    {
        'id': 'mars_atmosphere',
        'title': 'Martian Atmosphere & Aerodynamics',
        'icon': '🪐',
        'summary': 'Why Mars is a harsh near-vacuum: 95.3% carbon dioxide and only 1% Earth surface pressure.',
        'learning_points': [
            'Mars atmospheric pressure is only 610 to 860 Pascals (less than 1% of Earth 101,325 Pa).',
            'Humans cannot breathe Martian air because it is 95% CO2 with trace nitrogen (2.6%) and argon (1.9%).',
            'Because the air is so thin, sound travels slower and loses high frequencies quickly.'
        ],
        'age_tiers': {
            'cadet': 'Mars has very little air—almost like being high up in space! You need a space suit to breathe.',
            'commander': 'The scale height of the Martian atmosphere is ~11.1 km. Low ambient density reduces aerodynamic drag on rovers but makes parachute deceleration difficult.'
        },
        'quiz': {
            'question': 'What is the primary gas found in the Martian atmosphere?',
            'options': ['Carbon Dioxide (CO2)', 'Oxygen (O2)', 'Nitrogen (N2)', 'Methane (CH4)'],
            'correct_index': 0,
            'explanation': 'Correct! Mars atmosphere is 95.3% Carbon Dioxide. NASA MOXIE uses this abundant gas to produce breathable oxygen!'
        }
    },
    {
        'id': 'solar_power_tau',
        'title': 'Photovoltaic Arrays & Dust Attenuation',
        'icon': '☀️',
        'summary': 'How Martian dust squalls cut solar power yield using the Beer-Lambert law.',
        'learning_points': [
            'Solar flux on Mars averages 590 W/m² (compared to 1,361 W/m² on Earth) due to Mars greater distance from the Sun.',
            'Atmospheric dust optical depth (Tau) attenuates sunlight: I = I_0 * exp(-Tau / cos(theta)).',
            'Dust settling on solar wings ended NASA Opportunity and InSight missions, demonstrating why dust-brushing is critical.'
        ],
        'age_tiers': {
            'cadet': 'Dust storms on Mars block the Sun just like dark clouds, turning off your solar power.',
            'commander': 'During regional storms (Tau > 3.0), solar flux drops below 100 W/m², necessitating RTG nuclear power or piezoelectric electrostatic dust mitigation.'
        },
        'quiz': {
            'question': 'What happened to NASA InSight and Opportunity landers when dust accumulated on their solar panels?',
            'options': ['Their batteries depleted and they shut down', 'They switched to jet fuel', 'Wind automatically kept them clean forever', 'They flew back to Earth'],
            'correct_index': 0,
            'explanation': 'Correct! Regolith dust blocked sunlight from reaching their photovoltaic cells, ultimately depleting battery reserves and ending their missions.'
        }
    },
    {
        'id': 'moxie_electrolysis',
        'title': 'NASA MOXIE: Making Oxygen on Mars',
        'icon': '🫁',
        'summary': 'Solid Oxide Electrolysis Cells converting Martian CO2 into breathable O2 at 800°C.',
        'learning_points': [
            'MOXIE stands for Mars Oxygen In-Situ Resource Utilization Experiment.',
            'It heats Martian CO2 to 800°C across scandia-stabilized zirconia (YSZ) membranes.',
            'The chemical reaction: 2 CO2 -> 2 CO (carbon monoxide) + O2 (pure breathable oxygen).'
        ],
        'age_tiers': {
            'cadet': 'MOXIE acts like a mechanical tree, taking Mars air and turning it into fresh oxygen!',
            'commander': 'Solid Oxide Electrolysis (SOEC) achieves 99.6% oxygen purity with a Faraday efficiency exceeding 95% at nominal 12.0 g/hr operational output.'
        },
        'quiz': {
            'question': 'What temperature does NASA MOXIE operate at to split CO2 molecules?',
            'options': ['800°C (1,470°F)', '0°C (Freezing)', '100°C (Boiling water)', '5,000°C (Sun surface)'],
            'correct_index': 0,
            'explanation': 'Correct! MOXIE operates at 800°C using specialized ceramic thermal insulation and nickel-mesh catalytic cells.'
        }
    },
    {
        'id': 'space_radiation',
        'title': 'Cosmic Radiation & Active Deflectors',
        'icon': '🛡️',
        'summary': 'Defending astronauts from Galactic Cosmic Rays and Solar Particle Events.',
        'learning_points': [
            'Mars lacks a global dipole magnetosphere like Earth, leaving the surface exposed to space radiation.',
            'Astronauts on Mars face ~0.67 mSv of radiation per day—equivalent to a chest X-ray every few days.',
            'Superconducting magnetic coils can create an artificial mini-magnetosphere to deflect charged ions.'
        ],
        'age_tiers': {
            'cadet': 'Invisible space rays can hurt astronauts. Magnetic shields work like an invisible umbrella to bounce them away!',
            'commander': 'Unattenuated GCR heavy ions (HZE particles) damage DNA and silicon avionics. Regolith berms (3m thickness) or 3-Tesla superconducting deflector coils provide the necessary mass/electromagnetic shielding.'
        },
        'quiz': {
            'question': 'Why is radiation higher on the surface of Mars than on Earth?',
            'options': ['Mars lacks a global protective magnetic field', 'Mars is closer to the sun', 'Martian rocks are all radioactive', 'Mars has too much oxygen'],
            'correct_index': 0,
            'explanation': 'Correct! Earth core generates a massive magnetosphere that deflects cosmic particles, while Mars lost its global magnetic dynamo billions of years ago.'
        }
    }
]

def get_all_curriculum_modules():
    return STEM_CURRICULUM_MODULES

def submit_quiz_answer(topic_id, selected_index):
    """
    Validates quiz answers server-side and awards XP.
    """
    module = next((m for m in STEM_CURRICULUM_MODULES if m['id'] == topic_id), None)
    if not module:
        return {'success': False, 'message': 'Topic not found'}

    quiz = module['quiz']
    is_correct = (selected_index == quiz['correct_index'])
    xp = 100 if is_correct else 25

    return {
        'success': True,
        'is_correct': is_correct,
        'xp_earned': xp,
        'explanation': quiz['explanation'] if is_correct else f"Incorrect. The correct answer was: {quiz['options'][quiz['correct_index']]}. {quiz['explanation']}"
    }
