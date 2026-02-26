#import "@preview/basic-resume:0.2.9": *

#let name = "Jean Doux"
#let location = "Geneva, Switzerland"
#let email = "jean.doux@email.com"
#let linkedin = "linkedin.com/in/jeandoux"
#let github = "github.com/jeandoux"

#show: resume.with(
  author: name,
  location: location,
  email: email,
  linkedin: linkedin,
  github: github,
  accent-color: "#26428b",
  font: "New Computer Modern",
  paper: "us-letter",
  author-position: left,
  personal-info-position: left,
)

== Professional Experience

#work(
  title: "Quantitative Researcher",
  location: "Geneva, Switzerland",
  company: "SquarePoint Capital",
  dates: dates-helper(start-date: "July 2024", end-date: "Present"),
)
- Developed statistical arbitrage strategies on equity futures using factor decomposition and regime detection, contributing to a book with \$200M+ AUM.
- Built end-to-end alpha research pipeline in Python and C++ covering data ingestion, signal generation, backtesting, and live deployment.
- Applied gradient boosting and LSTM models to predict short-term price dislocations from order flow and alternative data sources.
- Collaborated with portfolio managers to size and risk-manage positions using mean-variance optimization with custom turnover and capacity constraints.

#work(
  title: "Quantitative Analyst",
  location: "London, United Kingdom",
  company: "Vitol",
  dates: dates-helper(start-date: "July 2023", end-date: "June 2024"),
)
- Built quantitative models for energy commodity markets (crude oil, natural gas) supporting proprietary trading and hedging decisions.
- Designed a time-series forecasting framework for supply/demand imbalances using ARIMA, Kalman filters, and regime-switching models.
- Automated daily P&L attribution and Greeks reporting, reducing manual effort by 80% and enabling faster risk decisions.
- Conducted statistical analysis of physical market spreads (Brent/WTI, Henry Hub/TTF) to identify systematic trading opportunities.

#work(
  title: "Quantitative Research Intern",
  location: "Paris, France",
  company: "Société Générale CIB",
  dates: dates-helper(start-date: "May 2022", end-date: "August 2022"),
)
- Researched equity factor models (momentum, value, low-volatility) for the structured products desk; backtested strategies over a 10-year horizon.
- Implemented a volatility surface interpolation model using SVI parametrization for options pricing and hedging workflows.

== Education

#edu(
  institution: "École Polytechnique",
  location: "Palaiseau, France",
  dates: dates-helper(start-date: "September 2019", end-date: "June 2023"),
  degree: "Diplôme d'Ingénieur — Applied Mathematics & Finance",
)

== Skills
*Programming*: Python (expert), C++ (proficient), R, SQL, Bash \
*Libraries*: NumPy, Pandas, Polars, SciPy, scikit-learn, PyTorch, statsmodels \
*Quantitative*: Factor models, time-series analysis, Monte Carlo simulation, stochastic calculus, Bayesian inference \
*Tools*: Git, Docker, Bloomberg Terminal, Jupyter, Linux \
*Languages*: French (Native), English (Fluent)
