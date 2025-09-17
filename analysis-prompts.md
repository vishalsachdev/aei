# AI Analysis Prompts for Anthropic Economic Index Data

## Dataset Context for AI Agents

**Primary Sources**:
- Claude.ai consumer usage (100K+ rows, 150+ countries)
- Enterprise API usage (33K+ rows, global business patterns)
- Time period: August 4-11, 2025
- Geographic coverage: All countries with >200 conversations, all US states with >100

**Key Variables Available**:
- Geographic identifiers (ISO country codes, US state codes)
- Task classifications (O*NET occupational taxonomy)
- Collaboration patterns (automation vs augmentation)
- Usage metrics (counts, percentages, per-capita indices)

## Structured Analysis Prompts

### 1. Geographic Inequality Analysis
```
Analyze the geographic distribution of AI adoption using the AEI data. Focus on:
- Calculate Gini coefficient for global AI usage distribution
- Identify correlation between GDP per capita and AI Usage Index
- Map high/low adoption clusters and their economic characteristics
- Project implications for global economic convergence/divergence

Key metrics: AUI values by country, GDP correlations, adoption tiers
```

### 2. Task Automation Feasibility Assessment
```
Using O*NET task data, determine which occupational tasks show highest automation potential:
- Rank tasks by automation rate (directive + feedback loop patterns)
- Cross-reference with enterprise vs consumer usage patterns
- Identify tasks with growing automation rates over time (V1→V3)
- Map to SOC occupation groups for labor market impact assessment

Key metrics: Task-level automation percentages, enterprise adoption rates
```

### 3. Regional Economic Specialization Patterns
```
Analyze how AI usage patterns reflect regional economic advantages:
- Map task specialization by US state/country (AUI by task category)
- Identify comparative advantages in AI deployment
- Correlate with existing industry clusters (tech, finance, government)
- Assess potential for AI-driven regional competitiveness

Key metrics: Task specialization indices, regional usage patterns
```

### 4. Technology Diffusion Curve Analysis
```
Model AI adoption following Rogers' diffusion curve framework:
- Classify countries/states into adopter categories (innovators, early adopters, etc.)
- Calculate adoption velocity by comparing V1, V2, V3 data
- Predict when lagging regions will reach adoption thresholds
- Identify barriers to adoption in low-AUI regions

Key metrics: Temporal adoption rates, geographic adoption rankings
```

### 5. Enterprise Deployment Strategy Analysis
```
Examine how businesses strategically deploy AI through API usage:
- Analyze cost-sensitivity in task selection (cost vs usage correlation)
- Identify high-value automation targets (cost-efficient + high-usage)
- Map enterprise vs consumer task preferences
- Assess scalability patterns in business AI deployment

Key metrics: API cost indices, task usage rates, automation dominance
```

### 6. Human-AI Collaboration Evolution
```
Track the evolution of human-AI interaction patterns:
- Measure shift from augmentation to automation over time
- Identify tasks transitioning from collaborative to automated
- Analyze geographic differences in collaboration preferences
- Project future collaboration pattern trends

Key metrics: Collaboration mode percentages, temporal trends V1→V3
```

### 7. Digital Divide Impact Assessment
```
Quantify the emerging AI divide and its economic implications:
- Calculate usage gaps between high/low adoption regions
- Model productivity differentials from AI adoption
- Assess whether current patterns will increase global inequality
- Identify intervention points to reduce AI access disparities

Key metrics: Usage concentration ratios, economic correlation coefficients
```

### 8. Occupational Disruption Risk Analysis
```
Identify which occupations face highest AI disruption risk:
- Map SOC occupation groups to automation rates
- Correlate with wage levels and employment volumes
- Identify vulnerable worker populations by geography
- Assess speed of automation adoption by occupation

Key metrics: SOC-level automation rates, geographic employment data
```

## Analysis Output Specifications

### For Geographic Analysis
- Include country/state rankings with specific AUI values
- Provide correlation coefficients (GDP vs usage)
- Map clustering patterns (high/medium/low adoption regions)

### For Economic Analysis
- Calculate elasticity coefficients (economic factors vs adoption)
- Provide concentration indices (Gini, Herfindahl)
- Include confidence intervals for projections

### For Temporal Analysis
- Show V1→V2→V3 trend data with growth rates
- Calculate momentum indicators for adoption acceleration
- Project future adoption curves based on historical patterns

### For Task Analysis
- Rank tasks by automation potential with confidence scores
- Cross-reference enterprise vs consumer adoption patterns
- Map to occupational impact assessments

## Key Analytical Frameworks to Apply

1. **Technology Adoption Models**: Rogers diffusion, S-curves, network effects
2. **Economic Geography**: Agglomeration effects, core-periphery patterns
3. **Labor Economics**: Skill-biased technological change, task-based models
4. **Development Economics**: Convergence theory, technology leapfrogging
5. **Innovation Diffusion**: Geographic spillovers, knowledge networks

## Expected Insights Categories

**Confirmed Patterns**: Geographic concentration, income correlation, task specialization
**Emerging Trends**: Automation acceleration, education sector growth, enterprise deployment
**Surprising Findings**: Regional specialization patterns, collaboration mode shifts
**Policy Implications**: Digital divide interventions, education adaptation needs
**Economic Forecasts**: Productivity distribution, labor market impacts, global competitiveness

These prompts are designed to generate actionable insights from the AEI data while maintaining analytical rigor and economic interpretation frameworks.