# Demo Health Data for Reboot 2025 London Hackathon

## Overview
This folder contains synthetic smartwatch health datasets created for the Reboot 2025 London Hackathon. Each CSV represents hourly records for one of six personas over the period 1 Mar 2025 to 30 Mar 2025. Teams can use these realistic datasets to build and test wellbeing solutions tailored to diverse user needs.

## File List
1. `1_liwei_control_health_conscious_young_adult.csv`
2. `2_samira_young_adult_mild_anxiety.csv`
3. `3_javier_gen_z_student_academic_financial_stress.csv`
4. `4_aisha_young_adult_sleep_issues_low_activity.csv`
5. `5_kofi_young_professional_experiencing_burnout.csv`
6. `6_ahmed_night_shift_worker_circadian_disruption.csv`

## Personas

**Control: Health‑Conscious Young Adult**  
Li Wei, 27, is a data scientist in Edinburgh who owns a condo with her partner. She integrates every health platform, logs 7 500 steps daily, completes 30 minutes of mixed cardio and strength training, and never misses 15 minutes of mindfulness. She sleeps 7.5 hours nightly with a 20 percent deep / 25 percent REM split. On a stable salary and with an emergency fund, Li Wei simply seeks to explore advanced trend‑analysis features. She’ll know a demo succeeds when it surfaces insights she hasn’t already discovered.

**Young Adult with Mild Anxiety**  
Samira, 28, is a backend developer at a London fintech who shares a flat with three roommates. She tracks heart rate, steps, and breathing sessions—but looming release deadlines now trigger afternoon panic and sleepless nights. Although she plans a 10‑minute guided breathing session at 21:00 each evening, she never follows through, logging zero mindfulness minutes. Skipping lunch to hit sprint goals causes midday crashes. On a modest salary repaying a family loan, Samira needs tension‑alerts that nudge her into two‑minute guided breathing breaks and micro‑stretch prompts in her IDE. She’ll call success when her anxiety spikes drop by 50 percent and she reclaims a 30‑minute screen‑free lunch slot each workday.

**Gen Z Student under Academic & Financial Stress**  
Javier, 21, studies media in Manchester while juggling evening shifts at a convenience store to afford £350/month rent and textbooks. His smartwatch times Pomodoro sprints and logs sleep, but term‑end all‑nighters push his REM ratio below 15 percent. Guilt and fatigue blur lectures. Javier needs predictive stress forecasts tied to his timetable, peer‑group sleep challenges for accountability, and budget alerts before big purchases. He’ll judge success when REM stays above 20 percent and he limits all‑nighters to one per term.

**Young Adult with Sleep Issues & Low Activity**  
Aisha, 30, freelances as an illustrator in Bristol. She glances at her watch only when it buzzes—her steps linger at 3 000/day and exercise rarely exceeds ten minutes. Nights yield four–six hours of broken sleep with just 10 percent deep rest, leaving her foggy in client calls. With variable income, she resists premium subscriptions. Aisha needs low‑barrier micro‑challenges—“stand two minutes each hour”—and personalized audio bedtime routines. She’ll deem the solution successful when deep‑sleep rises above 20 percent and daytime focus measurably improves.

**Young Professional Experiencing Burnout**  
Kofi, 33, is a marketing strategist in Shoreditch who lives with his partner and rescue dog. He meticulously tracks VO₂ max, resting HR, and headphone volume, yet relentless meetings and weekend catch‑ups have driven his resting HR upward and HRV downward. Mindfulness minutes drop to zero on weekdays. With savings earmarked for a home deposit, he resists another subscription. Kofi needs bite‑sized recovery prompts woven into Slack and calendar invites. He’ll call success when his HRV trend remains upward for a week and he completes three five‑minute guided breaks each week.

**Night‑Shift Worker with Circadian Disruption**  
Ahmed, 26, is an ICU nurse on rotating nights in Manchester, sharing a house with fellow juniors. He grabs a single consolidated nap totaling around four hours on shift nights and about 4.9 hours on rest days—relying on his watch’s alarms to stay alert. Despite logging roughly 8 600 steps per shift night and only about 1 500 steps in daytime hours, minimal daylight exposure leaves him cognitively foggy. On a modest wage plus overtime, he fears data misuse and wants free, privacy‑preserving tools. Ahmed needs adaptive light‑and‑sound cues that match his roster and clear nap‑timing guides. He’ll call success when his rest‑day sleep reaches at least five hours and he reduces on‑shift errors.

## Column Definitions
1. **Date**: D‑MMM‑YYYY (e.g. 1‑Mar‑2025)
2. **Time**: HH:MM:SS (24h)
3. **Heart Rate (bpm)**: Beats per minute
4. **Heart Rate Variability (ms)**: Time between heartbeats
5. **Respiratory Rate (breaths/min)**: Breaths per minute
6. **Blood Oxygen (%)**: Oxygen saturation
7. **Step Count (steps)**: Steps taken per hour
8. **Walking Speed (km/h)**: Speed during movement
9. **Distance Walked/Run (km)**: Kilometers per hour
10. **Flights Climbed (flights)**: Stair flights per hour
11. **Active Energy Burned (kcal)**: Calories burned per hour
12. **Stand Hours (hours)**: Hours with ≥ 1 minute standing
13. **Sleep Duration (hours)**: Hours slept in nightly block
14. **Time Awake (minutes)**: Minutes awake during sleep block
15. **REM Sleep (%)**: REM proportion of nightly sleep
16. **Core Sleep (%)**: Light sleep proportion
17. **Deep Sleep (%)**: Deep sleep proportion
18. **Environmental Sound Level (dB)**: Ambient noise level
19. **Headphone Audio Exposure (dB)**: Audio exposure level
20. **VO2 Max (mL/kg/min)**: Max oxygen uptake
21. **ECG (ST Segment Elevation) (mm)**: ECG ST elevation
22. **Body Temperature (°C)**: Core temperature
23. **Exercise Minutes (minutes)**: Minutes of exercise per hour
24. **Elevation Gain (meters)**: Meters climbed per hour
25. **Running Pace (min/km)**: Pace in minutes per km
26. **Mindfulness Minutes (minutes)**: Minutes of mindfulness per hour

## Usage
1. Load any CSV into your analysis or demo pipeline.
2. Parse `Date` and `Time` for time‑series alignment.
3. Use column definitions to interpret metrics and triggers.
4. Apply persona narratives to drive scenario‑specific logic.
5. Validate results against success criteria in each narrative.
