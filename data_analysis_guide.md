# Anthropic Economic Index (AEI) Data Analysis Guide

## Overview
You have access to rich datasets from Anthropic's Economic Index V3 report covering AI usage patterns from August 4-11, 2025. This data reveals geographic, task-based, and collaboration patterns in AI adoption across both consumer (Claude.ai) and enterprise (1P API) segments.

## Datasets Available

### 1. Claude.ai Consumer Data (`aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv`)
- **Size**: 100,063 rows
- **Coverage**: 150+ countries and all US states
- **Key Dimensions**:
  - **Geographic**: Country-level and US state-level usage patterns
  - **Tasks**: O*NET occupational tasks showing what people use Claude for
  - **Collaboration**: How users interact with Claude (automation vs augmentation)
  - **Requests**: Bottom-up categorization of request types

### 2. Enterprise API Data (`aei_raw_1p_api_2025-08-04_to_2025-08-11.csv`)
- **Size**: 33,795 rows
- **Coverage**: Global enterprise/developer usage via API
- **Unique Features**: Cost analysis, token usage, programmatic deployment patterns

## Key Analysis Opportunities

### 🌍 Geographic AI Adoption Analysis
- **AI Usage Index (AUI)**: Compare expected vs actual usage by population
- **Economic correlation**: Usage patterns vs GDP per capita
- **Regional specialization**: Different task preferences by geography
- **Digital divide**: High vs low adoption countries/states

**Sample Questions**:
- Which countries/states punch above their weight in AI adoption?
- How does usage pattern differ between Silicon Valley and rural states?
- Are emerging economies using AI differently than developed ones?

### 💼 Task & Occupation Analysis
- **O*NET Task Mapping**: See which occupational tasks Claude is being used for
- **SOC Major Groups**: Education, Science, Management, Computer/Math, etc.
- **Task Evolution**: Compare with previous reports to see trends

**Sample Questions**:
- Which occupational categories are adopting AI fastest?
- Are certain tasks more "automatable" via AI than others?
- How do task preferences differ between consumers vs enterprises?

### 🤝 Human-AI Collaboration Patterns
- **Automation**: Directive (66% API vs 39% consumer), Feedback Loops
- **Augmentation**: Learning, Task Iteration, Validation
- **Geographic variation**: Do high-income regions use AI differently?

**Sample Questions**:
- Why is enterprise usage more automated than consumer usage?
- Which regions favor automation vs augmentation approaches?
- How do collaboration patterns vary by task type?

### 💰 Economic Impact Analysis
- **Cost sensitivity**: Do businesses optimize for cheaper tasks?
- **Productivity implications**: High-directive usage patterns
- **Regional competitiveness**: Economic advantages of early adoption

## Key Findings to Explore Further

### 1. Geographic Concentration
- Singapore (4.6x expected usage), Canada (2.9x), DC (3.8x), Utah (3.78x)
- Low adoption: India (0.27x), Nigeria (0.2x), Indonesia (0.36x)

### 2. Task Specialization by Region
- **California**: IT tasks elevated
- **Florida**: Financial services focus
- **DC**: Document editing, career assistance
- **India**: >50% coding vs ~33% global average

### 3. Enterprise vs Consumer Differences
- **API**: 77% automation, heavy coding/admin focus
- **Consumer**: 50% automation, more education/writing

## Getting Started - Recommended First Analyses

### 1. Geographic AI Usage Mapping
```python
# Filter for country-level usage data
country_usage = df[df['facet'] == 'country'].copy()
# Calculate usage concentration indices
# Visualize on world map
```

### 2. Task Category Trends
```python
# Analyze O*NET task distribution
onet_tasks = df[df['facet'] == 'onet_task'].copy()
# Group by SOC major categories
# Compare consumer vs enterprise patterns
```

### 3. Collaboration Mode Analysis
```python
# Extract collaboration patterns
collab_data = df[df['facet'] == 'collaboration'].copy()
# Calculate automation vs augmentation ratios
# Analyze by geography and task type
```

## Data Schema Quick Reference

**Core Columns**:
- `geo_id`: Country (ISO-2) or US state code
- `facet`: Analysis dimension (country, onet_task, collaboration, etc.)
- `variable`: Metric type (count, percentage, index)
- `cluster_name`: Specific entity (task name, collaboration type)
- `value`: Numeric value

**Key Variables**:
- `usage_count`: Total conversations
- `usage_pct`: Percentage of total usage
- `onet_task_count/pct`: Task-specific usage
- `collaboration_count/pct`: Interaction pattern usage

## Next Steps

1. **Load and explore** the data structure
2. **Geographic analysis**: Create usage maps and identify patterns
3. **Task analysis**: Understand occupational adoption patterns
4. **Collaboration analysis**: Automation vs augmentation trends
5. **Cross-analysis**: Geographic + task + collaboration intersections
6. **Economic correlation**: Usage vs GDP, population, development indicators

The data is rich enough to support multiple research papers - focus on the questions that most interest you about AI adoption patterns and economic impacts.