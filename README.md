# F1 Race Strategist — ML-Powered Race Strategy Simulator

## Project Objective

The goal of this project is to develop a machine learning-powered Formula 1 race strategy simulator that evaluates different racing scenarios and helps identify optimal race strategies.

By combining historical Formula 1 data, lap-time prediction, and race simulation, the system aims to estimate how strategic decisions affect overall race performance.

The project is designed to eventually allow users to:

- **Predict lap times** based on driver, circuit, tyre compound, tyre degradation, and race conditions.
- **Simulate race strategies**, including different tyre selections, stint lengths, and pit-stop timings.
- **Compare strategies**, such as one-stop versus two-stop approaches, to estimate total race time.
- **Evaluate race scenarios**, including Safety Cars, Virtual Safety Cars, weather changes, and race interruptions.
- **Identify promising strategies** by comparing simulated outcomes and evaluating trade-offs.

## Current Development Stage

The project is currently in **Phase 1: Lap-Time Prediction**.

A supervised machine learning model has been developed using FastF1 data from the 2022–2024 Formula 1 seasons.

The model is trained on 2022–2023 data and evaluated on the 2024 season, achieving a mean absolute error (MAE) of **2.78 seconds**.

This model will serve as the predictive component of the future race strategy simulator.

## Development Roadmap

**Phase 1 — Lap-Time Prediction (Current)**

- Collect and clean historical F1 race data.
- Identify and filter race-interruption-affected laps.
- Train and evaluate a lap-time prediction model.
- Improve prediction accuracy using additional race and car-performance features.

**Phase 2 — Race Strategy Simulation**

- Simulate tyre degradation throughout a stint.
- Model pit-stop timing and pit-lane time loss.
- Estimate total race time for different strategies.
- Compare one-stop, two-stop, and alternative tyre strategies.

**Phase 3 — Dynamic Race Scenarios**

- Incorporate Safety Car and Virtual Safety Car conditions.
- Model weather changes and race interruptions.
- Evaluate how unexpected events influence strategy decisions.

**Phase 4 — Interactive Application**

- Develop an interface for selecting drivers, circuits, and race conditions.
- Visualize predicted lap times, stint performance, and strategy comparisons.
- Allow users to experiment with different strategies and view simulated outcomes.
