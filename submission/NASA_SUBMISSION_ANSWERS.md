# 🪐 SOL SURVIVOR: Complete NASA Space Apps Submission Package
**Challenge:** NASA International Space Apps Challenge 2026  
**Project Repository:** https://github.com/vickykumawat1221-bit/sol-survivor  
**Local Project Folder:** `/Users/vickykumawat/sol_survivor`

---

## 📋 1. Project Summary (50–200 Words)

**Sol Survivor** is an AI-powered Mars mission digital twin, closed-loop survival simulator, and interactive Space Academy engineered for students aged 8 to 16. Developing a full-stack flight control center with Python, Django, and HTML5 Canvas, we placed learners into the seat of a NASA Flight Director managing seven interdependent life-support subsystems—including MOXIE oxygen generation, hydroponics, and thermal grids—alongside eight physics-driven educational mini-games.

The platform directly addresses the challenge by transforming complex aerospace engineering, astrodynamics, and planetary science into an intuitive, cause-and-effect learning experience. Grounding its diurnal cycles and environmental crises in authentic NASA telemetry from the Perseverance MEDA, Curiosity REMS, and MOXIE missions, Sol Survivor demystifies space science through age-adaptive cognitive calibration and an onboard AI Flight Copilot.

Sol Survivor is important because it inspires the Artemis and Mars generation through "Stealth Learning." By navigating cascading thermodynamic failures and extreme resource scarcity on the Red Planet, young minds develop critical systems-thinking skills and a profound appreciation for closed-loop sustainability, renewable energy, and ecological stewardship on our home planet Earth.

---

## 📝 2. Project Details (1500 Words)

### Project Overview
Sol Survivor is an educational, turn-based Mars habitat simulator, interactive digital twin, and virtual space academy engineered specifically for students aged eight to sixteen. Created for the NASA International Space Apps Challenge, the project transforms complex aerospace engineering, planetary meteorology, orbital mechanics, and closed-loop life-support physics into an immersive, narrative-driven space exploration command center. Rather than approaching science education through passive reading or abstract problem sets, Sol Survivor immerses students directly into the high-stakes role of a Mars Mission Flight Director. Players assume command of an operational Martian surface outpost, navigating environmental hazards, balancing delicate life-support thermodynamics, deploying exploration rovers, and resolving compounding mechanical emergencies across four escalating mission tiers. The application integrates two seamlessly connected educational platforms within a unified software ecosystem: a turn-based Mars Mission Control digital twin and the NASA Space Academy, an interactive flight school featuring eight fully playable, physics-driven educational mini-games. Supported by an atmospheric outer-space aesthetic, authentic procedural audio synthesis, and real planetary telemetry from NASA robotic missions, Sol Survivor provides an engaging, scientifically rigorous entry point into humanity’s next giant leap.

### What Does It Do and How Does It Work?
Sol Survivor operates as a turn-based simulation engine where each turn corresponds to one Martian Sol. The core engine models seven interdependent environmental subsystems: the primary electrical power grid, solid-oxide electrolysis oxygen production, hydroponic food biomass, closed-loop water reclamation, thermal regulation, active magnetic radiation shielding, and structural habitat integrity. In the Martian environment, no subsystem functions in isolation; resource generation and consumption operate under strict physical trade-offs. For example, overcharging the Mars Oxygen ISRU Experiment (MOXIE) replenishes breathable air for the habitat crew, but demands a massive draw from the primary electrical bus that can leave thermal heating elements underpowered during the freezing Martian night.

The engine introduces realistic cascading failures to teach students the critical importance of systems engineering. If a cadet opts to dim habitat heaters to preserve battery storage during a regional dust squall, the immediate power surge prevents a total blackout; however, if heating coils remain unpowered for two consecutive Sols, sub-zero ambient temperatures cause water reclamation pipes to freeze, triggering a pipe rupture that immediately destroys thirty-five percent of the habitat's hydroponic crops. The game progresses across four escalating operational tiers: Level 1 (Touchdown) introduces basic diurnal energy cycles; Level 2 (Red Dust) incorporates atmospheric dust squalls modeled after empirical Martian optical depth dynamics; Level 3 (Solar Storm) unleashes Coronal Mass Ejections that bombard surface assets with dangerous radiation doses; and Level 4 (Apocalypse Protocol) challenges advanced students with multiple simultaneous system failures. An interactive Scalable Vector Graphics (SVG) digital twin of the habitat serves as the central visual schematic, dynamically pulsing amber and red as individual modules incur stress. By clicking on any habitat component, students can inspect live telemetry, power routing diagrams, and authentic engineering schematics of the underlying NASA hardware.

To assist young flight directors through these engineering crises, Sol Survivor incorporates the Houston AI Flight Copilot. Functioning as a virtual flight director, the Copilot analyzes current environmental parameters and active crises by executing a forward simulation tree. It evaluates all candidate actions one Sol in advance, calculating risk scores, highlighting trade-offs, and recommending the safest course of action accompanied by clear pros-and-cons comparisons. Crucially, the AI Copilot operates via a deterministic, rule-based expert system that runs entirely offline without requiring external API keys, while also supporting optional Large Language Model integrations for natural language flight advisory chats. Complementing this advisory system is a predictive survival analytics suite powered by Chart.js graphs, which visually projects resource depletion curves three to five Sols into the future, enabling cadets to identify life-support bottlenecks before they reach catastrophic failure thresholds.

Alongside Mission Control, the NASA Space Academy provides eight interactive physics mini-games: *Planet Explorer* (ordering the eight planets and comparing planetary atmospheres), *Zero Gravity Challenge* (navigating a spacewalking astronaut with nitrogen thrusters according to Newton’s First Law), *Rocket Builder* (balancing staging, engines, and Thrust-to-Weight Ratio to achieve orbital velocity), *Mars Rover Adventure* (driving the Perseverance rover across Jezero Crater to collect rock samples with authentic rocker-bogie suspension), *Asteroid Defender* (launching kinetic impactors to alter asteroid trajectories, inspired by NASA's DART mission), *Save The Astronaut* (solving environmental life-support emergencies involving CO2 scrubbers and hull breaches), *Gravity & Orbit Lab* (adjusting velocity and altitude to visualize circular, elliptical, and escape Keplerian orbits), and *Space Quiz Battle* (a timed trivia arena covering universe IQ and spaceflight history).

### What Benefits Does It Have?
Sol Survivor delivers deep educational value through "Stealth Learning"—the pedagogical principle that deep, lasting comprehension occurs when learners are actively immersed in problem-solving rather than memorizing isolated formulas. By placing scientific phenomena directly into the context of Mars exploration, abstract principles such as electrolysis, the Beer-Lambert law of atmospheric extinction, Keplerian orbital mechanics, and thermal dissipation become intuitive, practical tools for survival.

The platform provides a dynamic three-tier age calibration system: Junior Cadet (ages 8–10), Flight Specialist (ages 11–13), and Mission Commander (ages 14–16). Younger players receive simplified language, forgiving timers, and plain-English button subtitles like "Make Breathing Air" and "Save Battery Power." Older students experience full technical realism, quantitative equations, Astronomical Units, and unassisted life-support telemetry. This adaptive approach ensures that younger children are not intimidated, while older teenagers are intellectually challenged by genuine engineering trade-offs.

Furthermore, Sol Survivor features a comprehensive, exploit-resistant gamification architecture. Cadets earn experience points (XP) synchronized between Mission Control and the Space Academy, unlocking nine NASA STEM achievement badges, daily flight challenges, personal best tracking, and a printable Junior Commander Certificate of Completion complete with an automated cryptographic verification hash and a dynamic QR code. Built as a Progressive Web App (PWA) with zero mandatory installation or sign-up hurdles, it features an instant One-Click Guest Launch, making it accessible to any classroom or competition judge within seconds.

### What Is the Intended Impact of the Project?
The primary impact of Sol Survivor is democratizing hands-on aerospace and planetary science education for students worldwide. Many schools lack specialized aerospace curricula or laboratory equipment; Sol Survivor bridges this gap by turning any standard web browser, Chromebook, tablet, or smartphone into a functional NASA mission control terminal. It connects NASA’s flagship missions—such as Artemis, Perseverance, and DART—directly to everyday learners, demystifying space technology and inspiring underrepresented youth to pursue careers in STEM, computer science, and engineering.

Equally important is the project's contribution to environmental stewardship. Living on Mars requires an absolute circular economy where water is perpetually recycled, carbon dioxide is scrubbed, and every watt of solar power is accounted for. By experiencing firsthand how fragile closed-loop life support is on the Red Planet, students develop a profound respect for Earth's ecological systems, gaining an intuitive appreciation for renewable energy, resource conservation, and terrestrial climate resilience.

### Tools, Coding Languages, Hardware, and Software Used
Sol Survivor is built upon a robust, scalable full-stack software architecture engineered for cross-platform responsiveness and reliability. The backend is powered by Python 3.10+ and the Django 6.0 web framework, which enforces server-side game state integrity, handles session authentication, processes deterministic turn-based state machines, and manages a relational SQLite database. The database records comprehensive session profiles, student quiz attempts, and immutable step-by-step replay logs that store complete resource states before and after every single Sol action, providing students and educators with an exhaustive post-mission flight telemetry record for retrospectives.

The frontend presentation tier is crafted using semantic HTML5, CSS3, and Tailwind CSS, styled to evoke the sleek aesthetic of a modern space agency operations console. High-performance interactive elements—including the gravity sandbox, the lunar/Martian rover driving terrain, the microgravity spacewalk simulation, and the animated cosmic starfield—are rendered directly via the HTML5 2D Canvas API without reliance on heavy third-party gaming frameworks. Data visualization is powered by Chart.js, rendering multi-series forecasting graphs with dynamic color-coded safety thresholds.

Procedural auditory synthesis is accomplished through the browser-native Web Audio API, which generates real-time audio oscillations for Martian wind drones, two-tone emergency sirens, and Geiger counter clicks directly in memory without streaming heavy audio assets. The Web Speech API provides synthesized voice comms from Houston Flight Control, while Service Workers (`sw.js`) and a Web App Manifest (`manifest.json`) enable Progressive Web App offline caching. Rather than relying on static or synthetic background data, the system incorporates a dedicated NASA Data Center that integrates curated archives from the Mars Science Laboratory Curiosity Rover Environmental Monitoring Station (REMS), the Mars 2020 Perseverance Rover Environmental Dynamics Analyzer (MEDA), the NASA Space Weather Database Of Notifications, Knowledge, and Information (DONKI), and Planetary Data System (PDS) benchmarks for MOXIE. Deployment and public access are facilitated through automated Cloudflare edge tunnels, providing global SSL/TLS encryption.

### How Is Your Project Creative?
Sol Survivor demonstrates exceptional creativity through its dual-engine synergy, sensory immersion, and adaptive interface design:

First, it unites a serious closed-loop survival digital twin with an accessible physics arcade, sharing unified XP, ranks, and achievements between both worlds. Second, rather than relying on static, looping sound files, the application uses real-time Web Audio mathematical oscillators to synthesize procedural Martian wind that dynamically alters pitch based on atmospheric dust opacity (tau), alongside authentic emergency klaxons and synthesized voice radio communications from Houston. 

Third, crises emerge naturally through thermodynamics rather than arbitrary random penalties; neglecting thermal coils causes water pipes to physically freeze, and dust storms attenuate photovoltaic output according to the Beer-Lambert law ($I = I_0 e^{-\tau / \cos\theta}$), requiring robotic rover dust-brushing sorties. Fourth, the "Stealth Subtitles" system creatively bridges age demographics: an eight-year-old child and a sixteen-year-old high schooler can play the exact same simulation side-by-side, with the younger seeing intuitive labels like "Make Breathing Air" while the older sees "SOEC Electrolysis (12g/h)." Finally, the interactive SVG habitat turns passive graphics into an active technical blueprint, allowing students to click any module to inspect authentic NASA engineering schematics.

### What Factors Did Your Team Consider?
Throughout development, our team prioritized five core non-functional requirements to ensure the platform’s accessibility, robustness, and ethical integrity:

1. **Scientific Accuracy vs. Cognitive Playability:** A fundamental engineering challenge was balancing physical fidelity with child-friendly gameplay. Modeling exact partial differential equations for fluid dynamics or thermal radiation would quickly alienate an eight-year-old. Our team resolved this by preserving accurate scientific relationships under the hood—such as modeling solar flux attenuation via the Beer-Lambert law and orbital periods via Keplerian dynamics—while expressing these systems through intuitive visual gauges, percentage thresholds, and immediate cause-and-effect feedback.
2. **Universal Accessibility and Inclusivity:** We recognized that visual motion can trigger discomfort in users with vestibular sensitivity. To address this, Sol Survivor includes a prominent Reduced-Motion toggle (`✨ MOTION: [ON/OFF]`) that instantly halts starfield drifts, spinning galaxies, and pulsing glows, defaulting to a tranquil static starry backdrop while maintaining full functional readability. The color palette adheres to high-contrast WCAG guidelines, and all touch controls are optimized for mobile screens.
3. **Graceful Offline Fallback and Zero-Key Reliability:** Web-based hackathon applications frequently break during judging when third-party cloud APIs fail or exhaust billing quotas. Sol Survivor was engineered with zero external dependencies. The core game engine, the AI Flight Copilot, the predictive analytics, and all eight Space Academy mini-games operate completely autonomously offline on the local Django server, ensuring seamless reliability under any evaluation conditions.
4. **Data Privacy and Child Safety:** Designed for elementary and secondary school students, Sol Survivor strictly adheres to modern child data protection standards. No personally identifiable information (PII), email addresses, or social logins are collected. Cadets authenticate using lighthearted astronaut callsigns and simple four-digit clearance PINs stored in localized session tables, accompanied by an instant one-click guest bypass.
5. **Data Provenance Ethics:** We strictly adhered to NASA guidelines by never fabricating synthetic values as "real telemetry." Every piece of space weather data is labeled with its exact instrument, Martian Sol, terrestrial date, and source classification (**OBSERVED**, **DERIVED**, or **SIMULATED**).

---

## 🤖 3. Super Intelligence (SI) Options to Select

Check these options on the portal:
* ☑️ **Ideation or Brainstorming**
* ☑️ **Research or Information Gathering**
* ☑️ **Building SI/ML Into the Project**
* ☑️ **Coding, Debugging, or Troubleshooting**
* ☑️ **Writing, Editing, or Translation**

*(Leave unchecked: Visual Design / Image Creation, Presentation / Audio, Data Analysis, Other, None)*

---

## 🛰️ 4. NASA Data & Resources List

1. **NASA Mars 2020 Perseverance MEDA (Mars Environmental Dynamics Analyzer)**  
   `https://mars.nasa.gov/mars2020/mission/instruments/meda/`
2. **NASA MOXIE Mission & Planetary Data System (PDS) Oxygen Archive**  
   `https://mars.nasa.gov/technology/moxie/`
3. **NASA Curiosity Rover REMS (Rover Environmental Monitoring Station)**  
   `https://mars.nasa.gov/msl/mission/instruments/rems/`
4. **NASA DONKI (Space Weather Database Of Notifications, Knowledge, and Information)**  
   `https://kauai.ccmc.gsfc.nasa.gov/DONKI/`
5. **NASA Space Place (Educational STEM Curriculum & Planetary Science)**  
   `https://spaceplace.nasa.gov/`
6. **NASA DART (Double Asteroid Redirection Test) Planetary Defense Mission**  
   `https://science.nasa.gov/mission/dart/`
7. **NASA Jezero Crater Science & Perseverance Rover Sample Archive**  
   `https://mars.nasa.gov/mars2020/`

---

## 🌍 5. Space Agency Partner & Other Resources

1. **ESA (European Space Agency) Mars Exploration & Trace Gas Orbiter (TGO)**  
   `https://www.esa.int/Science_Exploration/Space_Science/Mars_Express`
2. **Django Web Framework (BSD-3-Clause Open Source)**  
   `https://www.djangoproject.com/`
3. **Tailwind CSS Framework (MIT License)**  
   `https://tailwindcss.com/`
4. **Chart.js Open Source Data Visualization Library (MIT License)**  
   `https://www.chartjs.org/`
5. **Google Fonts Open Source Font Library (SIL Open Font License)**  
   `https://fonts.google.com/`
6. **W3C Web Audio API & Web Speech API Standards**  
   `https://www.w3.org/TR/webaudio/`
7. **Cloudflare Tunnel Edge Network**  
   `https://www.cloudflare.com/products/tunnel/`

---

## 🔗 6. Public Links & Project Demonstration

* **Public GitHub Repository (Code, Docs, Tests):**  
  `https://github.com/vickykumawat1221-bit/sol-survivor`
* **7-Slide Project Demonstration:**  
  `https://github.com/vickykumawat1221-bit/sol-survivor/blob/main/DEMO_PRESENTATION.md`
