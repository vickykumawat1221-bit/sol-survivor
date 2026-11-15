# 🪐 SOL SURVIVOR: AI-Powered Mars Mission Digital Twin & NASA Space Academy

> **NASA International Space Apps Challenge 2026**  
> *Ages 8–16 STEM Curriculum, Closed-Loop Survival Simulator, 8 Space Academy Mini-Games & Real NASA Data Center*  
> Built with Python 3, Django, TailwindCSS, Chart.js, HTML5 Canvas & Interactive SVG Digital Twin

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![NASA Space Apps](https://img.shields.io/badge/NASA-Space%20Apps%202026-red.svg)](https://www.spaceappschallenge.org/)
[![Tests: 33 Passed](https://img.shields.io/badge/Tests-33%20Passed-emerald.svg)](mission/tests.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🏆 Hackathon Executive Summary

**Sol Survivor** is an educational, turn-based Mars habitat simulator, digital twin, and **NASA Space Academy** engineered for students aged **8 to 16 years** for the **NASA Space Apps Challenge**. Through "Stealth Learning," Sol Survivor transforms rigorous aerospace engineering, planetary meteorology, orbital mechanics, and closed-loop life-support physics into a high-stakes, dopamine-driven space exploration command center.

The application combines two seamlessly connected experiences:
1. **Mars Mission Control Survival Simulator:** Manage 7 interconnected life-support subsystems (Power, Oxygen, Food, Water, Temperature, Shielding, Structural Integrity) across 4 age-adaptive tiers, navigating dust storms, solar particle events, and cascading thermal failures with an **AI Mission Commander**.
2. **NASA Space Academy:** An interactive educational gaming hub featuring **eight fully playable, age-adapted mini-games**, teaching solar system astronomy, microgravity spacewalks, rocket propulsion, Mars geology, planetary defense, and orbital mechanics.

All wrapped in a **breath-taking outer-space visual experience** with deep navy cosmic nebula gradients, an interactive canvas starfield with twinkling stars, drifting micro-dust, occasional shooting stars, a 3D detailed Mars globe, and reduced-motion accessibility.

---

## 🌌 Part 1: Outer Space Visual Experience

* **Deep Cosmic Navy & Nebula Palette:** Atmospheric base (`#050816`) layered with purple nebula clouds (`#7e22ce`), deep space royal blue (`#1e3a8a`), and subtle cyan aurora highlights (`#06b6d4`).
* **Interactive Starfield Canvas:** 150+ twinkling stars with variable pulse frequencies, gentle inertia drift, and distant rotating spiral galaxies.
* **Shooting Stars:** Realistic meteor streaks with radiant cyan tails streaking across the sky every 10–18 seconds.
* **Detailed 3D Mars Planet:** High-resolution CSS/SVG sphere with realistic limb darkening, Olympus Mons caldera, Valles Marineris canyon features, and a polar ice cap.
* **Mars Surface Landscape Silhouette:** Atmospheric Martian horizon with crater rims and distant telemetry outposts.
* **Reduced-Motion Accessibility Toggle (`✨ MOTION: [ON/OFF]`):** One-click toggle in the header that pauses animations and falls back to a serene static starry nebula, respecting user accessibility and `prefers-reduced-motion`.

---

## 🚀 Part 2 & 3: The 8 Playable Space Academy Mini-Games

Each mini-game is **100% playable, responsive, and scientifically accurate**, with welcome screens, learning objectives, interactive gameplay, scoring, success/failure debriefs, and NASA scientific takeaways:

| Game | STEM Topic & Gameplay | Core Learning Objectives |
| :--- | :--- | :--- |
| **1. 🪐 Planet Explorer** | Solar System Order & Planetary Science | Order all 8 planets from the Sun outwards (Mercury to Neptune). Compare terrestrial rocky worlds to gas/ice giants. Learn why Venus is hottest (465°C) and explore Mars's Olympus Mons. |
| **2. 👨‍🚀 Zero Gravity Challenge** | Microgravity Spacewalk (EVA) & Newton's Laws | Pilot a floating astronaut in a 2D microgravity canvas simulation using RCS nitrogen gas thrusters. Apply Newton's 1st Law (inertia: you coast indefinitely until counter-thrust is fired!) and manage EVA suit oxygen and propellant. |
| **3. 🚀 Rocket Builder & Launch** | Aerospace Propulsion & Rocket Equation | Select Stage 1 Boosters (SRBs, MethaLOX, HydroLOX), Stage 2 Vacuum engines, and Payloads. Calculate Thrust-to-Weight Ratio ($TWR > 1.2$) and fly an atmospheric ascent with staging to achieve orbital velocity ($7.8 \text{ km/s}$). |
| **4. 🚜 Mars Rover Adventure** | Robotic Exploration & Jezero Geology | Drive the Perseverance rover across Jezero Crater with authentic Rocker-Bogie 6-wheel suspension. Collect 4 geological rock samples (smectite clay, hematite blueberries, carbonates, basalt) and manage battery recharge in sunlit patches. |
| **5. ☄️ Asteroid Defender** | Planetary Defense & Kinetic Deflection | Inspired by NASA's DART mission! Track incoming Near-Earth Objects (C-type, S-type, M-type). Launch kinetic impactors to alter asteroid velocity ($\Delta v$), proving why deflection is safer than Hollywood explosive myths. |
| **6. 🫁 Save The Astronaut** | Life Support Systems (ECLSS) Puzzles | Solve time-critical environmental emergencies: re-route CO2 scrubbers with Lithium Hydroxide (LiOH) canisters before hypercapnia occurs, patch micrometeoroid hull breaches with vacuum polymer seals, and isolate electrical fires. |
| **7. 🛰️ Gravity & Orbit Lab** | Astrodynamics & Keplerian Orbital Sandbox | Adjust launch altitude ($r$) and horizontal velocity ($v$) around Mars/Earth. Visualize Kepler's 1st Law: Circular orbits ($v = \sqrt{GM/r}$), Elliptical orbits with Periapsis/Apoapsis, and Hyperbolic escape trajectories ($v \ge v_{esc}$). |
| **8. ⚡ Space Quiz Battle** | Timed Trivia Tournament & Universe IQ | Fast-paced, timed NASA trivia showdown across Planets, Astronauts, Missions, Rockets, and Deep Space Cosmology with instant scientific explanations for every answer. |

---

## 🎓 Part 4: Age-Adaptive Learning (Ages 8–16)

Space Academy includes an interactive **Learning Tier Selector**:
* **Junior Cadet (Ages 8–10):** Visual guides, friendly hints, forgiving timings, intuitive orbital physics, and foundational planetary concepts.
* **Flight Specialist (Ages 11–13):** Balanced physics, authentic Astronomical Units (AU), Thrust-to-Weight ratios, geological rock analysis, and quantitative measurements.
* **Mission Commander (Ages 14–16):** Full scientific rigor, orbital mechanics equations ($v = \sqrt{GM/r}$, vis-viva), Tsiolkovsky delta-v calculations, closed-loop stoichiometry, and stoichiometry.
* **Difficulty Tiers:** Easy, Medium, and Hard options within mini-games.

---

## 🏆 Part 5: Gamification, Badges & Anti-Exploit XP

* **Space Academy XP System:** Complete mini-games to earn +150 to +300 XP.
* **Server-Side Anti-Exploit Validation:** Rejects submissions with unrealistic completion times (< 3 seconds). First-time clears award full XP; replays award delta XP when beating personal high scores, preventing duplicate XP farming.
* **XP Synchronization:** Space Academy XP automatically syncs with your active **Sol Survivor Mission Control XP**, elevating your rank from Cadet to Flight Engineer, Specialist, and Mars Base Commander!
* **9 NASA STEM Badges & Achievements:**
  1. 🪐 `Solar System Navigator` (Planet Explorer)
  2. 👨‍🚀 `Spacewalk Master` (Zero Gravity Challenge)
  3. 🚀 `Aerospace Engineer` (Rocket Builder)
  4. 🚜 `Mars Field Geologist` (Mars Rover Adventure)
  5. ☄️ `Planetary Shield Commander` (Asteroid Defender)
  6. 🫁 `Life Support Hero` (Save The Astronaut)
  7. 🛰️ `Orbital Astrodynamicist` (Gravity & Orbit Lab)
  8. ⚡ `Grand Cosmic Scholar` (Space Quiz Battle)
  9. 🏆 `Supreme Space Commander` (Complete all 8 Space Academy games!)
* **Daily Flight Challenge:** Daily rotating challenge awarding +150 bonus XP.

---

## 🕹️ How to Play & Win: Quick Walkthrough

### Mission Control (Mars Survival):
1. **Monitor 6 Vital Gauges:** Power (⚡), Oxygen (🫁), Food (🌱), Water (💧), Radiation Shield (🛡️), Hab Integrity (🏗️).
2. **Deploy Free Robotic Rovers:** Perseverance (Power restore), Ingenuity (Scout), Subsurface Drill (Water/Food).
3. **Beware the Thermal Cascade (Level 2+):** Dimming heaters saves power, but if kept dimmed for 2 consecutive Sols, greenhouse water pipes freeze and destroy 35% of crops! Overclock the RTG core or overdrive UV lights to defrost.
4. **Follow the AI Commander:** Check the Houston Flight Copilot bar for 1-Sol forward simulated risk predictions.

### Space Academy (Mini-Games):
1. Click **🚀 SPACE ACADEMY** in the top navigation bar.
2. Select your age tier (8–10, 11–13, 14–16).
3. Launch any of the 8 mini-games, review the NASA Learning Objectives, and hit **START MISSION 🚀**.
4. Use keyboard (WASD / Arrows), mouse, or on-screen touch controls.
5. Review the scientific takeaway at mission debrief and collect your NASA STEM badges!

---

## 🏗️ Project Architecture & Database Schema

```
sol_survivor/
├── manage.py                          # Django management CLI
├── sol_project/                       # Django project configuration
│   ├── settings.py                    # Database, sessions, templates configuration
│   ├── urls.py                        # Root URL dispatcher
│   └── wsgi.py                        # WSGI server entry point
├── mission/                           # Sol Survivor & Space Academy application
│   ├── academy_engine.py              # 8 mini-games physics models, NASA facts, scoring & achievements
│   ├── engine.py                      # 7-resource closed-loop physics, cascading engine, turn progression
│   ├── ai_advisor.py                  # Decision-tree simulator, risk scoring & AI chat advisor
│   ├── nasa_data.py                   # NASA PDS, REMS, MEDA & DONKI data center integration
│   ├── crisis_engine.py               # Deterministic seed-reproducible Martian emergency engine
│   ├── forecasting.py                 # 3-5 Sol predictive polynomial survival analytics
│   ├── learning_center.py             # 4 age-adaptive STEM modules & interactive quiz scoring
│   ├── models.py                      # SQLite models: MissionSession, AcademyProfile, AcademyGameScore, etc.
│   ├── views.py                       # Mission Control, Space Academy, reports, certificates & REST APIs
│   ├── urls.py                        # App routing (/academy/, /academy/<game_id>/, etc.)
│   ├── tests.py                       # 33 comprehensive automated unit and integration tests
│   └── templates/mission/
│       ├── dashboard.html             # Mars Mission Control 8-workstation retro-futuristic dashboard
│       ├── academy.html               # NASA Space Academy hub with 8 mini-game cards & achievements
│       ├── academy_game.html          # Dedicated interactive game theater with Web Audio SFX
│       ├── academy_minigames_script.html # 8 fully functional mini-game canvas & DOM engines
│       ├── space_background.html      # Outer space background, canvas starfield & 3D Mars globe
│       ├── report.html                # Printable post-flight debriefing & replay timeline
│       └── certificate.html           # Printable Junior Mars Mission Commander Certificate
└── README.md                          # Master project documentation & pitch deck
```

---

## ⚡ REST API Specifications

| Method | Endpoint | Description | Payload / Parameters |
| :--- | :--- | :--- | :--- |
| `GET` | `/academy/` | Space Academy hub with game cards, progress, and badges. | None |
| `GET` | `/academy/<game_id>/` | Dedicated interactive game theater for a specific mini-game. | URL param `game_id` |
| `POST` | `/api/academy/set_profile/` | Sets student age tier (`8-10`, `11-13`, `14-16`) and difficulty. | `{"age_group": "11-13", "difficulty": "medium"}` |
| `POST` | `/api/academy/submit_score/` | Validates score, awards XP, syncs with Sol Survivor, unlocks badges. | `{"game_id": "planet_explorer", "score": 200, "time_seconds": 15}` |
| `GET` | `/api/academy/progress/` | Returns JSON of academy scores, achievements, and completion. | None |
| `POST` | `/api/action/` | Executes a validated engineering action and advances 1 Sol. | `{"action": "optimize_solar"}` |
| `POST` | `/api/ai_chat/` | Submits a tactical query to the AI Mission Commander. | `{"query": "How do I survive a dust storm?"}` |
| `GET` | `/api/forecast/` | Returns 3–5 Sol predictive telemetry arrays for Chart.js. | None |
| `GET` | `/api/nasa_data/` | Fetches NASA PDS/DONKI telemetry (supports `mode=real\|sim`). | `?mode=real` |
| `GET` | `/report/` | Renders the complete printable mission debriefing audit. | None |
| `GET` | `/certificate/` | Renders the printable Junior Mars Commander Certificate. | `?name=Astronaut+Name` |

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
* Python 3.10, 3.11, 3.12, or 3.13
* `pip` package manager

### 2. Clone Repository
```bash
git clone https://github.com/vickykumawat1221-bit/sol-survivor.git
cd sol-survivor
```

### 3. Install Dependencies
```bash
pip install django
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Run the Automated Test Suite
Verify that all 33 automated tests pass:
```bash
python manage.py test
```
*Expected Output:*
```
Found 33 test(s).
Creating test database for alias 'default'...
.................................
Ran 33 tests in 0.090s

OK
```

### 6. Launch Sol Survivor & Space Academy
```bash
python manage.py runserver 127.0.0.1:8000
```
Open your browser and navigate to:
* **Mission Control (Mars Survival):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **NASA Space Academy (8 Mini-Games):** [http://127.0.0.1:8000/academy/](http://127.0.0.1:8000/academy/)

---

## 🔬 Educational Attribution & Non-Affiliation Disclaimer
* **NASA Educational References:** Sourced from public NASA learning programs including [NASA Space Place](https://spaceplace.nasa.gov/), [NASA Solar System Exploration](https://science.nasa.gov/solar-system/), the [NASA Mars 2020 Mission](https://mars.nasa.gov/mars2020/), and the [Planetary Defense Coordination Office (PDCO)](https://www.nasa.gov/planetarydefense/).
* **Disclaimer:** *Sol Survivor and Space Academy were developed as an educational project for the 2026 NASA International Space Apps Challenge. This application and its completion certificates are educational simulations and are not officially issued, endorsed, or certified by the National Aeronautics and Space Administration (NASA).*

---

## 📄 License
This project is open-source under the **[MIT License](LICENSE)**.
