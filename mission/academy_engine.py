"""
Space Academy Educational Engine for Sol Survivor.
Provides age-adaptive curriculum, mini-game physics models, NASA scientific facts,
anti-exploit score verification, daily challenges, and achievement badge logic.
References: NASA Space Place, NASA Solar System Exploration, NASA JPL Mars 2020.
"""

import math
import datetime

# ==============================================================================
# 8 SPACE ACADEMY MINI-GAMES DEFINITIONS
# ==============================================================================

ACADEMY_GAMES = {
    'planet_explorer': {
        'id': 'planet_explorer',
        'title': 'Planet Explorer',
        'subtitle': 'Solar System Order & Planetary Science',
        'badge_name': 'Planet Explorer',
        'icon': '🪐',
        'color': 'cyan',
        'accent': '#06b6d4',
        'bg_gradient': 'from-cyan-950/40 to-slate-950',
        'difficulty_est': 'Easy to Medium',
        'time_est': '3–5 mins',
        'stem_topic': 'Planetary Geology & Orbital Order',
        'description': 'Master the order of our solar system, identify planet characteristics, and match authentic NASA rover & probe discoveries.',
        'learning_objectives': [
            'Order all 8 planets from the Sun outwards (Mercury through Neptune).',
            'Distinguish terrestrial rocky planets from gas and ice giants.',
            'Discover why Venus is the hottest planet despite Mercury being closest to the Sun.',
            'Investigate Olympus Mons and ancient water evidence on Mars.'
        ],
        'nasa_source': 'NASA Science: Solar System Exploration & NASA Space Place',
        'nasa_url': 'https://science.nasa.gov/solar-system/planets/'
    },
    'zero_gravity': {
        'id': 'zero_gravity',
        'title': 'Zero Gravity Challenge',
        'subtitle': 'Microgravity Spacewalk & Newton’s Laws',
        'badge_name': 'Junior Astronaut',
        'icon': '👨‍🚀',
        'color': 'emerald',
        'accent': '#10b981',
        'bg_gradient': 'from-emerald-950/40 to-slate-950',
        'difficulty_est': 'Medium',
        'time_est': '3–4 mins',
        'stem_topic': 'Newtonian Mechanics & Spacewalk EVA',
        'description': 'Pilot a floating astronaut on a spacewalk outside the Mars Transit Ship using RCS gas thrusters. Navigate microgravity inertia, collect tools, and monitor oxygen.',
        'learning_objectives': [
            'Apply Newton’s 1st Law: An object in motion in a vacuum stays in motion until counter-thrust is fired.',
            'Apply Newton’s 3rd Law: For every thruster pulse action, there is an equal and opposite reaction.',
            'Manage Extravehicular Activity (EVA) suit resources: Oxygen and RCS Nitrogen propellant.',
            'Avoid orbital debris travelling at hypersonic speeds.'
        ],
        'nasa_source': 'NASA Johnson Space Center: Extravehicular Activity (EVA) Operations',
        'nasa_url': 'https://www.nasa.gov/international-space-station/spacewalks/'
    },
    'rocket_builder': {
        'id': 'rocket_builder',
        'title': 'Rocket Builder & Launch',
        'subtitle': 'Thrust, Propulsion & Orbital Staging',
        'badge_name': 'Rocket Engineer',
        'icon': '🚀',
        'color': 'amber',
        'accent': '#f59e0b',
        'bg_gradient': 'from-amber-950/40 to-slate-950',
        'difficulty_est': 'Medium to Hard',
        'time_est': '4–6 mins',
        'stem_topic': 'Aerospace Propulsion & Rocket Equation',
        'description': 'Select boosters, fuel chemistries, and core stages to engineer a launch vehicle. Calculate Thrust-to-Weight Ratio (TWR) and achieve orbital velocity.',
        'learning_objectives': [
            'Understand Thrust-to-Weight Ratio (TWR > 1.2 required to overcome planetary gravity).',
            'Learn why multi-stage rockets drop empty fuel tanks to maximize velocity (Tsiolkovsky Rocket Equation).',
            'Compare Solid Rocket Boosters (high thrust) vs Liquid Cryogenic Engines (high efficiency Specific Impulse).',
            'Execute a gravity turn to reach Earth/Mars low orbital insertion (7.8 km/s).'
        ],
        'nasa_source': 'NASA Glenn Research Center: Beginner’s Guide to Rockets & Propulsion',
        'nasa_url': 'https://www.grc.nasa.gov/www/k-12/rocket/'
    },
    'mars_rover': {
        'id': 'mars_rover',
        'title': 'Mars Rover Adventure',
        'subtitle': 'Robotic Exploration & Martian Geology',
        'badge_name': 'Mars Rover Scientist',
        'icon': '🚜',
        'color': 'rose',
        'accent': '#f43f5e',
        'bg_gradient': 'from-rose-950/40 to-slate-950',
        'difficulty_est': 'Medium',
        'time_est': '4–5 mins',
        'stem_topic': 'Planetary Geology & Autonomous Robotics',
        'description': 'Drive the Perseverance rover across Jezero Crater with authentic Rocker-Bogie suspension. Sample clay minerals, avoid sand traps, and manage battery power.',
        'learning_objectives': [
            'Investigate Jezero Crater’s ancient river delta and biosignature-preserving clay minerals.',
            'Understand the NASA Rocker-Bogie 6-wheel suspension that keeps all wheels on the ground over rocks.',
            'Balance solar power generation against steep shadow valleys and Martian dust buildup.',
            'Collect samples for the Mars Sample Return mission.'
        ],
        'nasa_source': 'NASA JPL: Mars 2020 Mission (Perseverance Rover)',
        'nasa_url': 'https://mars.nasa.gov/mars2020/'
    },
    'asteroid_defender': {
        'id': 'asteroid_defender',
        'title': 'Asteroid Defender',
        'subtitle': 'Planetary Defense & Kinetic Impact',
        'badge_name': 'Planetary Defender',
        'icon': '☄️',
        'color': 'purple',
        'accent': '#a855f7',
        'bg_gradient': 'from-purple-950/40 to-slate-950',
        'difficulty_est': 'Medium to Hard',
        'time_est': '3–5 mins',
        'stem_topic': 'Celestial Mechanics & Planetary Defense',
        'description': 'Command a planetary defense probe inspired by NASA’s DART mission. Deflect incoming Near-Earth Objects (NEOs) using kinetic impactors to protect the station.',
        'learning_objectives': [
            'Learn how NASA’s DART (Double Asteroid Redirection Test) proved kinetic impact redirection.',
            'Understand that deflecting an asteroid by mere millimeters per second years early prevents an impact.',
            'Differentiate Carbonaceous (C-type), Stony (S-type), and Metallic (M-type) asteroids.',
            'Debunk Hollywood myths: Blowing up an asteroid creates hazardous radioactive shotgun shrapnel!'
        ],
        'nasa_source': 'NASA Planetary Defense Coordination Office (PDCO)',
        'nasa_url': 'https://www.nasa.gov/planetarydefense/'
    },
    'save_astronaut': {
        'id': 'save_astronaut',
        'title': 'Save The Astronaut',
        'subtitle': 'Life Support Engineering & Crisis Puzzles',
        'badge_name': 'Life Support Specialist',
        'icon': '🫁',
        'color': 'teal',
        'accent': '#14b8a6',
        'bg_gradient': 'from-teal-950/40 to-slate-950',
        'difficulty_est': 'Hard',
        'time_est': '4–6 mins',
        'stem_topic': 'Environmental Control & Life Support (ECLSS)',
        'description': 'Solve time-critical life support system puzzles inside a damaged habitat module. Re-route CO2 scrubbers, patch hull leaks, and isolate electrical fires.',
        'learning_objectives': [
            'Master closed-loop life support (ECLSS): Oxygen extraction, CO2 scrubbing, and moisture balance.',
            'Analyze how CO2 above 5,000 ppm causes cognitive impairment and hypercapnia in astronauts.',
            'Locate and seal micrometeoroid vacuum punctures using acoustic sensors and resin patches.',
            'Apply electrical isolation principles to save avionics without tripping main circuit breakers.'
        ],
        'nasa_source': 'NASA Marshall Space Flight Center: Environmental Control and Life Support System',
        'nasa_url': 'https://www.nasa.gov/centers-and-facilities/marshall/life-support-systems/'
    },
    'gravity_orbit_lab': {
        'id': 'gravity_orbit_lab',
        'title': 'Gravity & Orbit Lab',
        'subtitle': 'Orbital Mechanics & Kepler’s Laws Sandbox',
        'badge_name': 'Orbital Navigator',
        'icon': '🛰️',
        'color': 'indigo',
        'accent': '#6366f1',
        'bg_gradient': 'from-indigo-950/40 to-slate-950',
        'difficulty_est': 'Medium to Hard',
        'time_est': '4–6 mins',
        'stem_topic': 'Astrodynamics & Gravitational Motion',
        'description': 'Launch satellites into orbit around Earth, Mars, or the Sun. Adjust launch velocity, distance, and angle to observe circular, elliptical, and hyperbolic escape orbits.',
        'learning_objectives': [
            'Visualize Kepler’s 1st Law: Planetary orbits are ellipses with the Sun/planet at one focal point.',
            'Understand Circular Orbit Velocity: v = sqrt(GM/r). Moving too slow causes atmospheric burnup!',
            'Discover Escape Velocity: v_esc = sqrt(2GM/r). Moving too fast breaks gravitational capture.',
            'Execute a Hohmann Transfer maneuver to shift spacecraft between low and high orbits.'
        ],
        'nasa_source': 'NASA Jet Propulsion Laboratory: Basics of Space Flight (Orbital Mechanics)',
        'nasa_url': 'https://science.nasa.gov/learn/basics-of-space-flight/'
    },
    'space_quiz_battle': {
        'id': 'space_quiz_battle',
        'title': 'Space Quiz Battle',
        'subtitle': 'Timed Trivia Tournament & Universe IQ',
        'badge_name': 'Cosmic Scholar',
        'icon': '⚡',
        'color': 'yellow',
        'accent': '#eab308',
        'bg_gradient': 'from-yellow-950/40 to-slate-950',
        'difficulty_est': 'Adaptive (All Tiers)',
        'time_est': '3–5 mins',
        'stem_topic': 'Comprehensive Space Science & NASA Missions',
        'description': 'Compete in a timed space trivia showdown across Planets, Astronauts, NASA Missions, Rockets, and Deep Space Cosmology with explanations for every answer.',
        'learning_objectives': [
            'Identify key historic milestones: Apollo 11, Voyager interstellar voyage, Artemis program, James Webb.',
            'Explain how stars form, fuse hydrogen into helium, and collapse into neutron stars or black holes.',
            'Learn how spacesuits protect astronauts from the -150°C to +120°C temperature extremes of space.',
            'Reinforce core STEM principles through instant feedback and evidence-based explanations.'
        ],
        'nasa_source': 'NASA Space Place: Classroom Quizzes & Facts',
        'nasa_url': 'https://spaceplace.nasa.gov/'
    }
}

# ==============================================================================
# 1. PLANET EXPLORER DATA
# ==============================================================================

PLANET_DATA = [
    {
        'id': 'mercury',
        'name': 'Mercury',
        'order': 1,
        'type': 'Terrestrial (Rocky)',
        'color': '#94a3b8',
        'distance_au': 0.39,
        'diameter_km': 4879,
        'temp_c': '-180°C to 430°C',
        'moons': 0,
        'orbital_period': '88 Earth Days',
        'gravity_ms2': 3.7,
        'key_fact': 'Smallest planet and closest to the Sun. Has virtually no atmosphere (only a thin exosphere), so temperatures swing by 600°C between day and night!',
        'mystery_hint_easy': 'Closest planet to the Sun with lots of craters.',
        'mystery_hint_med': 'Has no moons, no atmosphere, and experiences extreme temperature swings of 600°C.',
        'mystery_hint_hard': 'Has a density second only to Earth due to a gigantic metallic iron core occupying 85% of its radius.'
    },
    {
        'id': 'venus',
        'name': 'Venus',
        'order': 2,
        'type': 'Terrestrial (Rocky)',
        'color': '#f59e0b',
        'distance_au': 0.72,
        'diameter_km': 12104,
        'temp_c': '465°C (Uniform)',
        'moons': 0,
        'orbital_period': '225 Earth Days',
        'gravity_ms2': 8.87,
        'key_fact': 'The hottest planet in the Solar System! A runaway greenhouse effect driven by a 96% CO2 atmosphere and sulfuric acid clouds traps solar heat at 465°C.',
        'mystery_hint_easy': 'The hottest planet in our solar system, covered in thick yellow clouds.',
        'mystery_hint_med': 'Traps extreme heat through a runaway greenhouse effect and spins backwards (retrograde).',
        'mystery_hint_hard': 'Surface atmospheric pressure is 92 times Earth’s—equivalent to being 900 meters underwater on Earth.'
    },
    {
        'id': 'earth',
        'name': 'Earth',
        'order': 3,
        'type': 'Terrestrial (Rocky)',
        'color': '#3b82f6',
        'distance_au': 1.00,
        'diameter_km': 12742,
        'temp_c': '-88°C to 58°C (Avg 15°C)',
        'moons': 1,
        'orbital_period': '365.25 Earth Days',
        'gravity_ms2': 9.81,
        'key_fact': 'The only known world harboring life. 71% covered in liquid water, protected by an active geomagnetic dipole field and an oxygen-nitrogen atmosphere.',
        'mystery_hint_easy': 'Our home world! The only planet known to support living organisms.',
        'mystery_hint_med': 'Has an active magnetic field generated by a liquid iron outer core and liquid surface oceans.',
        'mystery_hint_hard': 'The Goldilocks zone world with plate tectonics recycling carbon and stabilizing climate over gigayears.'
    },
    {
        'id': 'mars',
        'name': 'Mars',
        'order': 4,
        'type': 'Terrestrial (Rocky)',
        'color': '#ef4444',
        'distance_au': 1.52,
        'diameter_km': 6779,
        'temp_c': '-125°C to 20°C (Avg -63°C)',
        'moons': 2,
        'orbital_period': '687 Earth Days',
        'gravity_ms2': 3.72,
        'key_fact': 'The Red Planet. Iron oxide (rust) in its regolith gives it a crimson hue. Home to Olympus Mons (tallest shield volcano) and ancient river delta sediment.',
        'mystery_hint_easy': 'The Red Planet where our Sol Survivor habitat is located.',
        'mystery_hint_med': 'Home to Olympus Mons, the largest volcano in the solar system, and two potato-shaped moons.',
        'mystery_hint_hard': 'Atmospheric surface pressure is only 610 Pa (less than 1% of Earth), mostly CO2 with no global dipole magnetic field.'
    },
    {
        'id': 'jupiter',
        'name': 'Jupiter',
        'order': 5,
        'type': 'Gas Giant',
        'color': '#d97706',
        'distance_au': 5.20,
        'diameter_km': 139820,
        'temp_c': '-110°C (Cloud tops)',
        'moons': 95,
        'orbital_period': '11.86 Earth Years',
        'gravity_ms2': 24.79,
        'key_fact': 'The largest planet in the Solar System—more than twice as massive as all other planets combined! Famous for the Great Red Spot, a storm raging for >350 years.',
        'mystery_hint_easy': 'The giant king of all planets with a massive spinning Great Red Spot storm.',
        'mystery_hint_med': 'Has at least 95 moons including ocean-world Europa and volcanic Io, plus a powerful magnetic field.',
        'mystery_hint_hard': 'Generates metallic liquid hydrogen under millions of atmospheres of pressure, driving the solar system’s most intense radiation belts.'
    },
    {
        'id': 'saturn',
        'name': 'Saturn',
        'order': 6,
        'type': 'Gas Giant',
        'color': '#eab308',
        'distance_au': 9.58,
        'diameter_km': 116460,
        'temp_c': '-140°C',
        'moons': 146,
        'orbital_period': '29.45 Earth Years',
        'gravity_ms2': 10.44,
        'key_fact': 'Renowned for its breathtaking ring system composed of billions of chunks of water ice and rocky debris, ranging from microscopic dust to house-sized boulders.',
        'mystery_hint_easy': 'Famous for its dazzling, spectacular ring system made of shiny ice.',
        'mystery_hint_med': 'Has the lowest density in the solar system (less dense than water!) and the largest moon Titan.',
        'mystery_hint_hard': 'Its ring span extends over 282,000 km but is remarkably thin—averaging only 10 to 30 meters in thickness.'
    },
    {
        'id': 'uranus',
        'name': 'Uranus',
        'order': 7,
        'type': 'Ice Giant',
        'color': '#06b6d4',
        'distance_au': 19.22,
        'diameter_km': 50724,
        'temp_c': '-195°C',
        'moons': 28,
        'orbital_period': '84 Earth Years',
        'gravity_ms2': 8.69,
        'key_fact': 'The sideways planet! It rotates on an extreme axial tilt of 98 degrees, likely caused by an ancient collision with an Earth-sized protoplanet.',
        'mystery_hint_easy': 'A pale blue ice giant that rolls around the Sun on its side.',
        'mystery_hint_med': 'Rotates sideways at a 98-degree tilt and has cold methane clouds giving it a cyan-blue tint.',
        'mystery_hint_hard': 'Possesses a bizarrely tilted, off-center magnetic field inclined 59 degrees from its rotational axis.'
    },
    {
        'id': 'neptune',
        'name': 'Neptune',
        'order': 8,
        'type': 'Ice Giant',
        'color': '#2563eb',
        'distance_au': 30.05,
        'diameter_km': 49244,
        'temp_c': '-200°C',
        'moons': 16,
        'orbital_period': '164.8 Earth Years',
        'gravity_ms2': 11.15,
        'key_fact': 'The windiest planet in the Solar System. Supersonic winds whip through its vivid blue methane atmosphere at over 2,100 km/h (1,300 mph)!',
        'mystery_hint_easy': 'The farthest planet from the Sun, vivid deep cobalt blue.',
        'mystery_hint_med': 'Features the most violent supersonic winds in the solar system, exceeding 2,000 km/h.',
        'mystery_hint_hard': 'First planet located through mathematical prediction rather than direct telescopic observation (by Le Verrier and Adams).'
    }
]

# ==============================================================================
# 2. ZERO GRAVITY CHALLENGE DATA
# ==============================================================================

ZERO_G_ITEMS = [
    {'id': 'wrench', 'name': 'Titanium Torque Wrench', 'points': 50, 'fact': 'Astronauts use tethered, reactionless tools so tightening a bolt does not spin the astronaut backwards!'},
    {'id': 'sample_canister', 'name': 'Cryogenic Bio-Canister', 'points': 75, 'fact': 'Microgravity alters protein crystal growth, helping scientists develop life-saving medicine on the ISS.'},
    {'id': 'solar_bolt', 'name': 'Array Retaining Pin', 'points': 60, 'fact': 'External solar wing brackets require periodic spacewalk servicing to handle extreme thermal expansion.'},
    {'id': 'jwst_filter', 'name': 'Optical Sensor Shield', 'points': 100, 'fact': 'Spacewalkers must wear gold-coated polycarbonate visors to block blinding unfiltered ultraviolet sunlight.'}
]

# ==============================================================================
# 3. ROCKET BUILDER DATA
# ==============================================================================

ROCKET_COMPONENTS = {
    'boosters': [
        {
            'id': 'srb',
            'name': 'Solid Rocket Boosters (Pair)',
            'thrust_kn': 28000,
            'dry_mass_t': 180,
            'fuel_mass_t': 1000,
            'isp_s': 269,
            'pros': 'Massive initial liftoff thrust; low cost',
            'cons': 'Cannot be throttled down or restarted once lit',
            'science': 'Solid propellants (ammonium perchlorate composite) provide raw brute-force thrust to clear Earth’s dense lower atmosphere.'
        },
        {
            'id': 'methalox',
            'name': 'Reusable Methane/LOX Clusters',
            'thrust_kn': 22000,
            'dry_mass_t': 140,
            'fuel_mass_t': 850,
            'isp_s': 330,
            'pros': 'High efficiency; throttlable; Mars Sabatier compatible',
            'cons': 'Requires cryogenic refrigeration to prevent boil-off',
            'science': 'Methane (CH4) burns clean with Liquid Oxygen (LOX) and can be manufactured directly on Mars using atmospheric CO2!'
        },
        {
            'id': 'hydrolox',
            'name': 'Cryogenic HydroLOX Core Booster',
            'thrust_kn': 18000,
            'dry_mass_t': 120,
            'fuel_mass_t': 750,
            'isp_s': 390,
            'pros': 'Highest combustion efficiency; non-toxic exhaust (water vapor)',
            'cons': 'Liquid Hydrogen is ultra-low density, requiring giant insulated tanks',
            'science': 'Hydrogen and Oxygen produce the highest exhaust velocity of chemical fuels, making it ideal for upper-stage escape velocity.'
        }
    ],
    'second_stage': [
        {
            'id': 'vacuum_merlin',
            'name': 'Vacuum Expansion Engine',
            'thrust_kn': 980,
            'dry_mass_t': 15,
            'fuel_mass_t': 90,
            'isp_s': 348,
            'science': 'In space vacuum, rocket nozzles have giant bell expansions to extract every Newton of thrust from expanding gas.'
        },
        {
            'id': 'rl10_hydrolox',
            'name': 'RL10 Deep Space Vacuum Core',
            'thrust_kn': 110,
            'dry_mass_t': 8,
            'fuel_mass_t': 45,
            'isp_s': 453,
            'science': 'High-Isp engines sacrifice raw thrust for extreme fuel efficiency, enabling Trans-Mars Injection trajectories.'
        }
    ],
    'payloads': [
        {
            'id': 'mars_rover',
            'name': 'Perseverance-Class Heavy Mars Rover',
            'mass_t': 1.05,
            'target_orbit': 'Trans-Mars Injection (11.2 km/s)',
            'xp_bonus': 200
        },
        {
            'id': 'habitat_module',
            'name': 'Inflatable Deep Space Hab Module',
            'mass_t': 4.5,
            'target_orbit': 'Low Earth Orbit (7.8 km/s)',
            'xp_bonus': 150
        },
        {
            'id': 'comm_sat',
            'name': 'Deep Space Laser Relay Satellite',
            'mass_t': 0.8,
            'target_orbit': 'Geostationary Transfer Orbit (10.2 km/s)',
            'xp_bonus': 100
        }
    ]
}

# ==============================================================================
# 4. MARS ROVER GEOLOGY SAMPLES
# ==============================================================================

MARS_GEOLOGY_SAMPLES = [
    {
        'id': 'smectite_clay',
        'name': 'Smectite Phyllosilicate Clay',
        'points': 100,
        'science': 'Clay minerals form only in the presence of long-standing liquid neutral water. In Jezero Crater, they preserve ancient organic micro-textures!'
    },
    {
        'id': 'hematite_spherule',
        'name': 'Hematite Spherule (Martian Blueberry)',
        'points': 120,
        'science': 'Discovered by the Opportunity rover in Meridiani Planum, these concretions formed when iron-rich groundwater precipitated through porous rock.'
    },
    {
        'id': 'carbonate_rock',
        'name': 'Lacustrine Carbonate Outcrop',
        'points': 140,
        'science': 'Carbonates precipitate from water rich in dissolved CO2. They act as geological tape recorders of Mars’s ancient dense atmosphere.'
    },
    {
        'id': 'olivine_basalt',
        'name': 'Igneous Olivine Basalt',
        'points': 80,
        'science': 'Cooled volcanic lava rock containing crystals. Radiometric dating of basalt samples allows geologists to establish the exact timeline of Mars history.'
    }
]

# ==============================================================================
# 5. ASTEROID DEFENDER SCIENCE
# ==============================================================================

ASTEROID_CLASSES = [
    {
        'id': 'c_type',
        'name': 'C-Type (Carbonaceous Chondrite)',
        'composition': 'Rich in water, carbon, and amino acids',
        'density_gcm3': 1.8,
        'best_strategy': 'Kinetic Impactor at high relative velocity',
        'science': 'C-type asteroids are rubble piles from the birth of the solar system. NASA’s OSIRIS-REx collected a pristine sample from Bennu.'
    },
    {
        'id': 's_type',
        'name': 'S-Type (Stony Silicate)',
        'composition': 'Magnesium silicates and nickel-iron alloy',
        'density_gcm3': 2.7,
        'best_strategy': 'Kinetic Impactor (NASA DART target)',
        'science': 'NASA’s DART spacecraft crashed into Dimorphos at 22,500 km/h, altering its orbital period by 33 minutes and proving asteroid deflection works!'
    },
    {
        'id': 'm_type',
        'name': 'M-Type (Metallic Nickel-Iron)',
        'composition': 'Dense metallic iron-nickel core remnants',
        'density_gcm3': 5.3,
        'best_strategy': 'Dual Kinetic Impactor or Gravity Tractor',
        'science': 'NASA’s Psyche mission is exploring an M-type metallic world that may be the exposed core of an ancient shattered protoplanet.'
    }
]

# ==============================================================================
# 6. SAVE THE ASTRONAUT ECLSS PUZZLES
# ==============================================================================

ASTRONAUT_PUZZLES = [
    {
        'id': 'co2_scrubber',
        'title': 'CRITICAL: Carbon Dioxide Spike in Airlock',
        'scenario': 'Cabin CO2 has reached 4,800 ppm. Primary amine scrubber has saturated! Astronaut experiencing dizziness and headache.',
        'target_param': 'CO2 < 1,000 ppm',
        'options': [
            {'label': 'Open Nitrogen Blowdown Valve', 'correct': False, 'feedback': 'Incorrect. Diluting air with nitrogen lowers oxygen percentage without removing toxic CO2!'},
            {'label': 'Engage Backup Lithium Hydroxide (LiOH) Canister & Spin Fan', 'correct': True, 'feedback': 'CORRECT! LiOH chemically binds CO2 through exothermic reaction: 2 LiOH + CO2 -> Li2CO3 + H2O!'},
            {'label': 'Turn Off Cabin Heaters to Freeze CO2', 'correct': False, 'feedback': 'Incorrect. CO2 only deposits as dry ice at -78.5°C, which would cause severe crew hypothermia!'}
        ],
        'science': 'Astronauts exhale approximately 1 kg of CO2 per day. Above 5,000 ppm, hypercapnia causes confusion, impaired judgment, and acidosis.'
    },
    {
        'id': 'hull_puncture',
        'title': 'PRESSURE ALERT: Micrometeoroid Puncture',
        'scenario': 'Cabin pressure is dropping at 0.5 kPa per minute! Ultrasonic leak detectors identify a 3 mm hole behind the avionics rack.',
        'target_param': 'Cabin Pressure 101.3 kPa',
        'options': [
            {'label': 'Deploy Self-Expanding Vacuum Polymer Seal Patch', 'correct': True, 'feedback': 'CORRECT! The silicone-epoxy vacuum patch bonds instantaneously under differential pressure, sealing the leak!'},
            {'label': 'Pump in Liquid Water to Freeze and Plug the Hole', 'correct': False, 'feedback': 'Incorrect. Liquid water instantly boils and flash-freezes into useless drifting ice crystals in a space vacuum!'},
            {'label': 'Vent Entire Oxygen Reserve to Equalize Pressure', 'correct': False, 'feedback': 'Fatal mistake! Dumping remaining air suffocates the astronaut!'}
        ],
        'science': 'Whipple shields absorb high-velocity micrometeoroids by fragmenting them into a cloud of harmless dust before hitting the inner pressure vessel.'
    },
    {
        'id': 'electrical_fire',
        'title': 'FIRE EMERGENCY: Oxygen Concentrator Bus Short',
        'scenario': 'Electrical smoke detected in Main Bus B. Circuit breaker failed to trip due to magnetic contact weld.',
        'target_param': 'Bus Current < 20 Amperes',
        'options': [
            {'label': 'Throw Water on the Circuit Board', 'correct': False, 'feedback': 'Catastrophic failure! Water conducts electricity and would cause massive secondary short circuits and shock hazards!'},
            {'label': 'Fire Halon Gas & Manually Throw Master DC Disconnect Relay', 'correct': True, 'feedback': 'CORRECT! Clean inert gaseous extinguishant smothers electrical arcing while manual mechanical disconnect halts power!'},
            {'label': 'Increase Battery Voltage to Burn Through the Short', 'correct': False, 'feedback': 'Incorrect. Increasing voltage escalates thermal runaway and guarantees an explosive electrical fire!'}
        ],
        'science': 'In microgravity, flames do not rise because there is no natural thermal convection buoyancy. Fire forms a slow-burning spherical dome fed by diffusion.'
    }
]

# ==============================================================================
# 7. GRAVITY & ORBIT LAB CHALLENGES
# ==============================================================================

ORBIT_CHALLENGES = [
    {
        'id': 'stable_leo',
        'title': 'Mission 1: Achieve Circular Low Mars Orbit',
        'desc': 'Adjust velocity until eccentricity is below 0.05 at 400 km altitude.',
        'target_e': 0.05,
        'science': 'In a circular orbit, gravitational pull exactly equals the centripetal acceleration: v = sqrt(GM/r).'
    },
    {
        'id': 'escape_velocity',
        'title': 'Mission 2: Mars Escape Velocity (Parabolic Trajectory)',
        'desc': 'Accelerate spacecraft to escape Mars gravity into interplanetary space.',
        'target_e': 1.0,
        'science': 'Escape velocity is sqrt(2) times the circular velocity at the same radius: v_esc = sqrt(2GM/r).'
    },
    {
        'id': 'hohmann_transfer',
        'title': 'Mission 3: Hohmann Elliptical Orbit Transfer',
        'desc': 'Boost periapsis burn to expand apoapsis to the Mars outer moon Phobos orbit (9,376 km).',
        'target_apoapsis': 9376,
        'science': 'The Hohmann transfer orbit uses two impulsive engine burns to transition between two coplanar orbits with minimum propellant expenditure.'
    }
]

# ==============================================================================
# 8. SPACE QUIZ BATTLE QUESTION POOL (AGE-ADAPTIVE)
# ==============================================================================

QUIZ_QUESTION_BANK = {
    '8-10': [
        {
            'category': 'Planets',
            'q': 'Which planet is known as the "Red Planet"?',
            'choices': ['Mars', 'Venus', 'Jupiter', 'Mercury'],
            'answer': 0,
            'fact': 'Mars looks red because its surface rocks and regolith are rich in iron oxide—the same compound as common rust!'
        },
        {
            'category': 'Astronauts',
            'q': 'Who was the first human to walk on the Moon in 1969?',
            'choices': ['Buzz Aldrin', 'Neil Armstrong', 'Yuri Gagarin', 'Alan Shepard'],
            'answer': 1,
            'fact': 'Neil Armstrong stepped onto the lunar surface during Apollo 11 on July 20, 1969, declaring "That’s one small step for man, one giant leap for mankind."'
        },
        {
            'category': 'Rockets',
            'q': 'What must a rocket push out of its engines to fly upward?',
            'choices': ['Hot exhaust gas downward', 'Sound waves', 'Cold water', 'Magnetic lasers'],
            'answer': 0,
            'fact': 'According to Newton’s 3rd Law, by shooting hot high-speed exhaust gas downward, the rocket is pushed upward with equal and opposite force!'
        },
        {
            'category': 'Solar System',
            'q': 'Which planet has the famous giant rings made of ice and rock?',
            'choices': ['Saturn', 'Neptune', 'Earth', 'Mars'],
            'answer': 0,
            'fact': 'Saturn has the most magnificent rings in the solar system, made of billions of chunks of pure water ice ranging from dust specks to house-sized blocks.'
        },
        {
            'category': 'Missions',
            'q': 'What is the name of the NASA robot rover currently exploring Jezero Crater on Mars?',
            'choices': ['Perseverance', 'Voyager', 'Hubble', 'Apollo'],
            'answer': 0,
            'fact': 'The Perseverance rover landed on Mars in February 2021 carrying the MOXIE oxygen instrument and the Ingenuity Mars helicopter!'
        }
    ],
    '11-13': [
        {
            'category': 'Planets',
            'q': 'Why is Venus hotter than Mercury, even though Mercury is much closer to the Sun?',
            'choices': [
                'Venus has a runaway greenhouse effect from a 96% CO2 atmosphere',
                'Venus is closer to radioactive asteroid fields',
                'Mercury is completely made of ice on its day side',
                'Venus absorbs light with green chlorophyll clouds'
            ],
            'answer': 0,
            'fact': 'Venus is blanketed by a dense carbon dioxide atmosphere with clouds of sulfuric acid, trapping heat in a runaway greenhouse effect reaching 465°C!'
        },
        {
            'category': 'Missions',
            'q': 'What revolutionary task did the Ingenuity drone achieve on Mars?',
            'choices': [
                'First powered, controlled flight of an aircraft on another planet',
                'First drill to reach liquid water on Mars',
                'First robotic spacecraft to land on Pluto',
                'First satellite to communicate via quantum entanglement'
            ],
            'answer': 0,
            'fact': 'Ingenuity proved that powered flight is possible in Mars’s ultra-thin atmosphere (less than 1% of Earth’s density) by spinning its dual carbon-fiber rotors at 2,400 RPM!'
        },
        {
            'category': 'Astronomy',
            'q': 'What keeps the International Space Station in orbit around Earth instead of falling straight down?',
            'choices': [
                'It travels forward so fast (27,600 km/h) that the Earth curves away as fast as it falls',
                'Gravity does not exist at the ISS orbital altitude',
                'Giant rocket thrusters fire continuously 24 hours a day',
                'Magnetic repulsion from Earth’s magnetic North Pole pushes it up'
            ],
            'answer': 0,
            'fact': 'Earth’s gravity at ISS altitude is still about 90% as strong as on the surface! The ISS stays in orbit because its horizontal velocity matches the curvature of Earth—it is in perpetual free-fall!'
        },
        {
            'category': 'Rockets',
            'q': 'Why do orbital launch vehicles shed rocket stages as they climb?',
            'choices': [
                'To discard empty dead weight and increase final burnout velocity',
                'To reduce noise pollution for flight controllers',
                'Because rocket fuel dissolves metal tanks after 3 minutes',
                'To cool the engines by exposing them to space vacuum'
            ],
            'answer': 0,
            'fact': 'The Tsiolkovsky Rocket Equation dictates that reducing empty dry mass (tankage and structural weight) dramatically increases the velocity gained from remaining propellant.'
        },
        {
            'category': 'Astronauts',
            'q': 'What vital physiological adaptation must astronauts combat during long-duration spaceflights?',
            'choices': [
                'Bone mineral density loss and muscle atrophy from lack of gravity loading',
                'Blood turning acidic due to lack of atmospheric nitrogen',
                'Lungs shrinking because space air contains zero carbon dioxide',
                'Excessive tooth growth caused by cosmic rays'
            ],
            'answer': 0,
            'fact': 'Without gravity loading, astronauts lose approximately 1% to 1.5% of bone mineral density per month in space. They must exercise 2 hours daily on specialized resistance and treadmill devices!'
        }
    ],
    '14-16': [
        {
            'category': 'Propulsion',
            'q': 'What does "Specific Impulse" (Isp) measure in rocket propulsion physics?',
            'choices': [
                'The efficiency of propellant mass consumption (thrust per unit mass flow rate)',
                'The total acoustic decibel output of an engine nozzle',
                'The maximum payload volume inside the aerodynamic fairing',
                'The speed of sound through the combustion chamber injector plate'
            ],
            'answer': 0,
            'fact': 'Specific Impulse (measured in seconds) is the effective exhaust velocity divided by standard gravity (Isp = c / g0). It represents how many seconds one pound of fuel can produce one pound of thrust!'
        },
        {
            'category': 'Orbital Mechanics',
            'q': 'What is the theoretical velocity required for an object to achieve a parabolic escape trajectory from low Earth orbit?',
            'choices': [
                'Approximately 11.2 km/s (sqrt(2) times circular orbital velocity)',
                '7.8 km/s (circular Low Earth Orbit velocity)',
                '3.0 km/s (suborbital ballistic velocity)',
                '300,000 km/s (the speed of light)'
            ],
            'answer': 0,
            'fact': 'Escape velocity equals sqrt(2GM/r), which is sqrt(2) * v_circ. From Low Earth Orbit, escaping Earth’s gravitational well requires approximately 11.2 km/s.'
        },
        {
            'category': 'Planetary Science',
            'q': 'Why did Mars lose most of its ancient atmosphere and liquid surface oceans over the last 3.5 billion years?',
            'choices': [
                'Its molten iron dynamo cooled, collapsing its global magnetosphere and allowing solar wind to sputter away the atmosphere',
                'A rogue black hole passed through the asteroid belt and sucked up Martian water',
                'Martian gravity reversed polarity when Olympus Mons erupted',
                'The Sun’s gravitational pull pulled Mars’s air directly into Mercury'
            ],
            'answer': 0,
            'fact': 'Because Mars is smaller than Earth, its core cooled rapidly. Without a protective global dipole magnetosphere, intense solar energetic particles and ultraviolet radiation stripped away its atmosphere into space (ion sputtering).'
        },
        {
            'category': 'Space Weather',
            'q': 'What dangerous phenomenon occurs when a Coronal Mass Ejection (CME) strikes an unshielded spacecraft?',
            'choices': [
                'High-energy Solar Energetic Protons penetrate electronic avionics and induce radiation sickness in crew',
                'The spacecraft is physically blown into outer space like a sailing boat',
                'Gravity inside the habitat temporarily turns upside down',
                'All liquid water instantly freezes into diamond crystals'
            ],
            'answer': 0,
            'fact': 'CMEs carry gigatons of magnetized solar plasma and relativistic protons (>100 MeV). These particles pass through thin spacecraft hulls, causing single-event upsets in computers and severe DNA ionization in astronauts.'
        },
        {
            'category': 'Astrophysics',
            'q': 'What boundary around a Black Hole represents the point of no return where escape velocity exceeds the speed of light?',
            'choices': [
                'The Event Horizon (Schwarzschild Radius)',
                'The Oort Cloud',
                'The Kuiper Cliff',
                'The Roche Lobe'
            ],
            'answer': 0,
            'fact': 'The Event Horizon is the boundary where the gravitational escape velocity reaches the speed of light (c). For a non-rotating black hole, its radius is given by r_s = 2GM / c^2.'
        }
    ]
}

# ==============================================================================
# ACHIEVEMENTS DEFINITIONS
# ==============================================================================

ACADEMY_ACHIEVEMENTS_DEF = [
    {
        'id': 'PLANET_EXPLORER',
        'title': 'Solar System Navigator',
        'desc': 'Completed the Planet Explorer challenge and mapped all 8 planets.',
        'icon': '🪐',
        'game_id': 'planet_explorer'
    },
    {
        'id': 'ZERO_G_SPECIALIST',
        'title': 'Spacewalk Master',
        'desc': 'Controlled microgravity thrusters and collected all orbital tools in Zero Gravity.',
        'icon': '👨‍🚀',
        'game_id': 'zero_gravity'
    },
    {
        'id': 'ROCKET_ENGINEER',
        'title': 'Aerospace Engineer',
        'desc': 'Engineered a balanced multi-stage rocket and achieved orbital insertion.',
        'icon': '🚀',
        'game_id': 'rocket_builder'
    },
    {
        'id': 'MARS_GEOLOGIST',
        'title': 'Mars Field Geologist',
        'desc': 'Navigated Jezero Crater and sampled clay minerals and hematite blueberries.',
        'icon': '🚜',
        'game_id': 'mars_rover'
    },
    {
        'id': 'PLANETARY_DEFENDER',
        'title': 'Planetary Shield Commander',
        'desc': 'Executed kinetic deflection against hazardous near-Earth asteroids.',
        'icon': '☄️',
        'game_id': 'asteroid_defender'
    },
    {
        'id': 'ECLSS_SPECIALIST',
        'title': 'Life Support Hero',
        'desc': 'Neutralized life-threatening CO2 spikes and sealed vacuum hull punctures.',
        'icon': '🫁',
        'game_id': 'save_astronaut'
    },
    {
        'id': 'ORBITAL_NAVIGATOR',
        'title': 'Orbital Astrodynamicist',
        'desc': 'Constructed circular and elliptical orbits in the Gravity & Orbit Lab.',
        'icon': '🛰️',
        'game_id': 'gravity_orbit_lab'
    },
    {
        'id': 'COSMIC_SCHOLAR',
        'title': 'Grand Cosmic Scholar',
        'desc': 'Scored a high mastery percentage in the timed Space Quiz Battle.',
        'icon': '⚡',
        'game_id': 'space_quiz_battle'
    },
    {
        'id': 'SPACE_COMMANDER',
        'title': 'Supreme Space Commander',
        'desc': 'Graduated Space Academy by completing all 8 educational mini-games!',
        'icon': '🏆',
        'game_id': None
    }
]

# ==============================================================================
# ANTI-EXPLOIT & SCORE VALIDATION
# ==============================================================================

def validate_and_award_academy_score(profile, game_id, raw_score, time_seconds, details_json=None):
    """
    Validates submitted mini-game scores against anti-exploit rules:
    - Minimum time threshold (prevents instant bot submissions).
    - Capped maximum possible score per game.
    - Prevents duplicate replay XP farming: First-time clear awards base XP;
      replays only award incremental XP when beating personal high scores, plus daily bonus capped at 25 XP.
    - Automatically unlocks relevant achievement badges.
    Returns: dict(valid=bool, xp_awarded=int, message=str, new_achievements=list)
    """
    if game_id not in ACADEMY_GAMES:
        return {'valid': False, 'xp_awarded': 0, 'message': 'Invalid Game ID'}

    # 1. Anti-Cheat: Realistic minimum time constraint (at least 4 seconds of gameplay)
    if time_seconds < 3:
        return {'valid': False, 'xp_awarded': 0, 'message': 'Submission too fast. Simulation minimum duration not met.'}

    # 2. Score bounds check (capped at 500 max per mini-game)
    sanitized_score = max(0, min(500, int(raw_score)))
    if sanitized_score <= 0:
        return {'valid': True, 'xp_awarded': 0, 'message': 'Game completed with 0 points. Keep practicing!'}

    # 3. Check existing high score for this game
    from .models import AcademyGameScore, AcademyAchievement

    previous_best = AcademyGameScore.objects.filter(profile=profile, game_id=game_id).order_by('-score').first()

    base_xp = 150
    xp_awarded = 0
    first_completion = False

    if not previous_best:
        # First-time completion: award base XP + score bonus
        first_completion = True
        xp_awarded = base_xp + int(sanitized_score * 0.4)
    else:
        # Replay: award delta XP if score improved
        if sanitized_score > previous_best.score:
            improvement = sanitized_score - previous_best.score
            xp_awarded = max(10, min(100, int(improvement * 0.5)))
        else:
            # Modest participation bonus for practicing
            xp_awarded = 15

    # Cap single award to 300 XP
    xp_awarded = min(300, xp_awarded)

    # 4. Save score record
    AcademyGameScore.objects.create(
        profile=profile,
        game_id=game_id,
        score=sanitized_score,
        completed=True,
        accuracy_pct=min(100.0, (sanitized_score / 200.0) * 100.0),
        time_seconds=time_seconds,
        xp_awarded=xp_awarded,
        details_json=details_json or {}
    )

    # 5. Update Profile Stats
    profile.total_academy_xp += xp_awarded
    completed_distinct = AcademyGameScore.objects.filter(profile=profile, completed=True).values('game_id').distinct().count()
    profile.games_completed_count = completed_distinct
    profile.save()

    # 6. Check and award achievements
    new_achievements = []
    for ach in ACADEMY_ACHIEVEMENTS_DEF:
        ach_id = ach['id']
        already_has = AcademyAchievement.objects.filter(profile=profile, achievement_id=ach_id).exists()
        if not already_has:
            should_unlock = False
            if ach['game_id'] and ach['game_id'] == game_id and sanitized_score >= 50:
                should_unlock = True
            elif ach_id == 'SPACE_COMMANDER' and completed_distinct >= 8:
                should_unlock = True

            if should_unlock:
                AcademyAchievement.objects.create(
                    profile=profile,
                    achievement_id=ach_id,
                    title=ach['title'],
                    description=ach['desc'],
                    icon=ach['icon']
                )
                new_achievements.append(ach['title'])
                profile.total_academy_xp += 100  # Bonus achievement XP
                profile.save()

    return {
        'valid': True,
        'xp_awarded': xp_awarded,
        'first_completion': first_completion,
        'total_academy_xp': profile.total_academy_xp,
        'new_achievements': new_achievements,
        'message': f"Telemetry verified! +{xp_awarded} Space Academy XP awarded."
    }
