# Data Model Reference

Complete reference for all data structures in the Seismic Project Economics Management System.

## Table of Contents

1. [Overview](#overview)
2. [Project Model](#project-model)
3. [Project Inputs](#project-inputs)
4. [Contract Terms](#contract-terms)
5. [Production Programs](#production-programs)
6. [Rate Cards](#rate-cards)
7. [Cost Lines](#cost-lines)
8. [Formula Structure](#formula-structure)
9. [Calculated Results](#calculated-results)
10. [Storage Schema](#storage-schema)
11. [Example Data](#example-data)

---

## Overview

The application uses a JavaScript object model stored in the global `model` variable. This model is serialized to JSON and stored in browser localStorage.

### Top-Level Structure

```javascript
{
  projectInputs: { /* Project identity and parameters */ },
  contractTerms: { /* Financial terms */ },
  productionPrograms: { /* Production schedules */ },
  rateCards: { /* Rate dictionary */ },
  costLines: [ /* Cost line items */ ],
  upholes: [ /* Legacy uphole array */ ]
}
```

---

## Project Model

### Complete Model Schema

```typescript
interface ProjectModel {
  projectInputs: ProjectInputs;
  contractTerms: ContractTerms;
  productionPrograms: {
    survey: ProductionProgram;
    drilling: ProductionProgram;
    recording: ProductionProgram;
    upholes: ProductionProgram;
  };
  rateCards: {
    [sectionName: string]: RateItem[];
  };
  costLines: CostLine[];
  upholes: number[]; // Legacy, kept for backwards compatibility
}
```

---

## Project Inputs

### Schema

```typescript
interface ProjectInputs {
  projectName: string;
  omlNumber: string;
  client: string;
  contractor: string;
  projectArea: number;      // km
  shotFactor: number;       // km/shot
  redrillFactor: number;    // multiplier
  duration: number;         // months (1-14)
  revenueShare: number;     // 0-1 multiplier
  costShare: number;        // 0-1 multiplier
  fx: number;               // ₦/$ exchange rate
}
```

### Field Descriptions

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `projectName` | string | - | Full project name/title |
| `omlNumber` | string | - | OML number or basin identifier |
| `client` | string | - | Client/operator name |
| `contractor` | string | - | Contractor name |
| `projectArea` | number | km | Total project area |
| `shotFactor` | number | km/shot | Recording km per shot point |
| `redrillFactor` | number | x | Redrill multiplier (typically 1.0-1.2) |
| `duration` | number | months | Project duration (1-14) |
| `revenueShare` | number | 0-1 | Contractor's revenue share (1 = 100%) |
| `costShare` | number | 0-1 | Contractor's cost share (1 = 100%) |
| `fx` | number | ₦/$ | USD to NGN exchange rate |

### Example

```json
{
  "projectName": "NUPRC/FES ANAMBRA 2D SEISMIC ACQUISITION",
  "omlNumber": "NUPRC/FES ANAMBRA BASIN",
  "client": "NUPRC/FES",
  "contractor": "EnServ",
  "projectArea": 541.593,
  "shotFactor": 0.0276794095,
  "redrillFactor": 1.1,
  "duration": 8,
  "revenueShare": 1,
  "costShare": 1,
  "fx": 1360
}
```

---

## Contract Terms

### Schema

```typescript
interface ContractTerms {
  turnkeyRate: number;      // $/km
  mobilisation: number;     // $
  demobilisation: number;   // $
  upholeRate: number;       // $/uphole
}
```

### Field Descriptions

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `turnkeyRate` | number | $/km | Rate per kilometer of recording |
| `mobilisation` | number | $ | One-time mobilization fee |
| `demobilisation` | number | $ | One-time demobilization fee |
| `upholeRate` | number | $/uphole | Rate per uphole drilled |

### Example

```json
{
  "turnkeyRate": 20000,
  "mobilisation": 2000000,
  "demobilisation": 500000,
  "upholeRate": 3500
}
```

### Revenue Calculation

```
Production Revenue = Recording km × Turnkey Rate
Uphole Revenue = Upholes × Uphole Rate
Total Revenue = Production + Mobilisation + Uphole + Demobilisation
```

---

## Production Programs

### Schema

```typescript
interface ProductionProgram {
  label: string;              // Display name
  unit: string;               // Unit of measurement
  total: number;              // Total volume to distribute
  startMonth: number;         // 1-based month index
  activeMonths: number;       // Number of active months
  rampMonths: number;         // Ramp period duration
  profile: ProductionProfile; // Distribution algorithm
  manualMonthly?: number[];   // Manual values (if profile = 'Manual')
}

type ProductionProfile =
  | 'S-Curve'
  | 'Uniform'
  | 'Front-Loaded'
  | 'Back-Loaded'
  | 'Bell Curve'
  | 'Manual';
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `label` | string | Human-readable name |
| `unit` | string | Measurement unit (km, SDH, holes) |
| `total` | number | Total volume to distribute across months |
| `startMonth` | number | First active month (1 = M01) |
| `activeMonths` | number | Number of months with activity |
| `rampMonths` | number | Ramp-up/down period length |
| `profile` | enum | Distribution algorithm |
| `manualMonthly` | array | Manual values (when profile = 'Manual') |

### Production Profiles

#### S-Curve
- Slow ramp-up over `rampMonths`
- Plateau in middle
- Slow ramp-down over `rampMonths`
- Most realistic for field operations

#### Uniform
- Equal distribution across all `activeMonths`
- Simple linear schedule

#### Front-Loaded
- Highest volume in first month
- Linear decrease to last month
- Aggressive schedule

#### Back-Loaded
- Lowest volume in first month
- Linear increase to last month
- Cautious schedule

#### Bell Curve
- Gradual increase to peak in middle
- Gradual decrease after peak
- Gaussian-like distribution

#### Manual
- User specifies exact values per month
- Stored in `manualMonthly` array
- No automatic calculation

### Example

```json
{
  "survey": {
    "label": "Survey",
    "unit": "km",
    "total": 541.593,
    "startMonth": 2,
    "activeMonths": 5,
    "rampMonths": 2,
    "profile": "S-Curve"
  },
  "drilling": {
    "label": "Drilling",
    "unit": "SDH",
    "total": 18054,
    "startMonth": 4,
    "activeMonths": 4,
    "rampMonths": 2,
    "profile": "S-Curve"
  },
  "recording": {
    "label": "Recording",
    "unit": "km",
    "total": 499.713,
    "startMonth": 5,
    "activeMonths": 4,
    "rampMonths": 2,
    "profile": "Uniform"
  },
  "upholes": {
    "label": "Upholes",
    "unit": "holes",
    "total": 16,
    "startMonth": 2,
    "activeMonths": 3,
    "rampMonths": 1,
    "profile": "Manual",
    "manualMonthly": [0, 4, 4, 4, 0, 0, 0, 0, 0]
  }
}
```

---

## Rate Cards

### Schema

```typescript
interface RateCards {
  [sectionName: string]: RateItem[];
}

interface RateItem {
  name: string;   // Rate description
  value: number;  // Rate value in ₦
  unit: string;   // Unit of measurement
}
```

### Default Sections

- `survey`: Survey-related rates
- `drilling`: Drilling-related rates
- `preloading`: Preloading crew rates
- `recording`: Recording equipment rates
- `baseCamp`: Base camp and medical rates

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Descriptive name for the rate |
| `value` | number | Numeric value (in Naira) |
| `unit` | string | Unit notation (e.g., "₦/km", "₦/mo") |

### Example

```json
{
  "survey": [
    {
      "name": "Survey rate per km",
      "value": 50000,
      "unit": "₦/km"
    },
    {
      "name": "Survey supervisor salary",
      "value": 450000,
      "unit": "₦/mo"
    }
  ],
  "drilling": [
    {
      "name": "Drilling rate per SDH",
      "value": 1200,
      "unit": "₦/SDH"
    },
    {
      "name": "Standby rate",
      "value": 150000,
      "unit": "₦/day"
    }
  ]
}
```

### Usage

Rate cards are referenced in:
1. **Line-level formulas**: Calculate costs dynamically
2. **Per-month formulas**: Override specific months
3. **Documentation**: Reference values for manual calculations

---

## Cost Lines

### Schema

```typescript
interface CostLine {
  id: string;                  // Unique identifier (e.g., "c1", "c2")
  category: string;            // Category name (e.g., "SURVEYING")
  item: string;                // Line item description
  badge: CostBadge;            // Type indicator
  owner: CostOwner;            // Cost responsibility
  driverType: DriverType;      // How cost is calculated
  driverRef: string;           // Reference to driver (if applicable)
  rate: number;                // Rate value (if applicable)
  monthly: number[];           // Monthly cost values
  formula?: Formula;           // Line-level formula (optional)
  monthFormulas?: {            // Per-month formulas (optional)
    [monthIdx: number]: Formula;
  };
}

type CostBadge = 'fixed' | 'var' | 'sub' | 'lease' | 'owned' | 'labor';

type CostOwner = 'EnServ' | 'JV' | 'Reimbursable';

type DriverType =
  | 'manualMonthly'      // User enters monthly values
  | 'productionLinked'   // Linked to production series
  | 'crewLinked'         // Linked to crew count
  | 'fixedMonthly'       // Fixed monthly rate
  | 'oneTime';           // One-time cost in specific month
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique ID (auto-generated, e.g., "c47") |
| `category` | string | Category grouping (uppercase) |
| `item` | string | Line item name/description |
| `badge` | enum | Visual badge type |
| `owner` | enum | Who bears the cost |
| `driverType` | enum | Calculation method |
| `driverRef` | string | Reference key for driver |
| `rate` | number | Associated rate value |
| `monthly` | array | Monthly cost values (₦) |
| `formula` | object | Line-level formula config |
| `monthFormulas` | object | Per-month formula overrides |

### Badge Types

| Badge | Meaning | Color |
|-------|---------|-------|
| `fixed` | Fixed cost | Default |
| `var` | Variable cost | Green |
| `sub` | Subcontractor | Amber |
| `lease` | Leased equipment | Blue |
| `owned` | Owned equipment | Green |
| `labor` | Labor cost | Purple |

### Owner Types

| Owner | Factor Applied |
|-------|----------------|
| `EnServ` | 1.0 (100%) |
| `JV` | `costShare` (from projectInputs) |
| `Reimbursable` | 0.0 (0%, not included in funding) |

### Driver Types

| Type | Description | Uses `rate` | Uses `driverRef` |
|------|-------------|-------------|------------------|
| `manualMonthly` | User enters values | No | No |
| `productionLinked` | Cost = Production × Rate | Yes | Yes (surveyKm, drillSdh, etc.) |
| `crewLinked` | Cost = Crew count × Rate | Yes | Yes |
| `fixedMonthly` | Fixed rate per month | Yes | No |
| `oneTime` | One-time cost | Yes | Yes (month: "m1", "m2", etc.) |

### Example

```json
{
  "id": "c1",
  "category": "SURVEYING SUB.CONT. JOB",
  "item": "GPS Monumentation & Observation",
  "badge": "sub",
  "owner": "EnServ",
  "driverType": "manualMonthly",
  "driverRef": "",
  "rate": 0,
  "monthly": [0, 500000, 500000, 500000, 0, 0, 0, 0, 0],
  "formula": {
    "enabled": false,
    "tokens": [],
    "applyTo": "all"
  },
  "monthFormulas": {}
}
```

### With Formula

```json
{
  "id": "c22",
  "category": "FUEL & LUBRICANTS",
  "item": "Diesel (AGO)",
  "badge": "var",
  "owner": "EnServ",
  "driverType": "manualMonthly",
  "driverRef": "",
  "rate": 0,
  "monthly": [0, 0, 0, 0, 0, 0, 0, 0, 0],
  "formula": {
    "enabled": true,
    "tokens": [
      {"type": "prod", "series": "drilling"},
      {"type": "op", "value": "×"},
      {"type": "rate", "section": "drilling", "idx": 2},
      {"type": "op", "value": "×"},
      {"type": "num", "value": 15}
    ],
    "applyTo": "all"
  },
  "monthFormulas": {
    "3": {
      "tokens": [
        {"type": "num", "value": 2000000}
      ]
    }
  }
}
```

**Explanation**:
- Formula: `Drilling SDH × Drilling Rate × 15`
- Applied to all months
- Month 4 (index 3) overridden with fixed value: 2,000,000

---

## Formula Structure

### Schema

```typescript
interface Formula {
  enabled?: boolean;         // Formula is active (for line-level)
  tokens: FormulaToken[];   // Array of formula components
  applyTo?: 'all' | number[]; // Which months to apply to
}

type FormulaToken =
  | { type: 'rate', section: string, idx: number }
  | { type: 'prod', series: string }
  | { type: 'op', value: string }
  | { type: 'num', value: number };
```

### Token Types

#### Rate Token

References a rate from rate cards.

```typescript
{
  type: 'rate',
  section: 'survey',  // Section name in rateCards
  idx: 0              // Index in section array
}
```

**Value**: `model.rateCards[section][idx].value`

#### Production Token

References a production series.

```typescript
{
  type: 'prod',
  series: 'drilling'  // One of: survey, drilling, recording, shots, upholes
}
```

**Value**: `latest.prod[series][monthIdx]`

#### Operator Token

Mathematical operator.

```typescript
{
  type: 'op',
  value: '×'  // One of: ×, +, −, ÷
}
```

**Conversion**: `×` → `*`, `÷` → `/`, `−` → `-`

#### Number Token

Custom numeric value.

```typescript
{
  type: 'num',
  value: 1000
}
```

**Value**: Direct numeric value

### Apply To

**All Months**:
```json
{
  "applyTo": "all"
}
```

**Selected Months**:
```json
{
  "applyTo": [0, 1, 2, 5]  // M01, M02, M03, M06
}
```

### Evaluation

Formulas are evaluated using JavaScript `eval()`:

```javascript
// Formula: Drilling × Rate × 15
// Tokens: [prod:drilling, op:×, rate:drilling:0, op:×, num:15]

// For month 3:
expr = "1500 * 1200 * 15"  // 1500 SDH, rate ₦1200
result = eval(expr)         // 27,000,000
```

### Example Formulas

**Simple Rate × Production**:
```json
{
  "tokens": [
    {"type": "rate", "section": "survey", "idx": 0},
    {"type": "op", "value": "×"},
    {"type": "prod", "series": "survey"}
  ]
}
```
Result: `Survey Rate × Survey km` (varies by month)

**Complex Calculation**:
```json
{
  "tokens": [
    {"type": "rate", "section": "drilling", "idx": 0},
    {"type": "op", "value": "×"},
    {"type": "num", "value": 3},
    {"type": "op", "value": "+"},
    {"type": "rate", "section": "baseCamp", "idx": 1}
  ]
}
```
Result: `(Drilling Rate × 3) + Base Camp Rate` (static)

---

## Calculated Results

### Latest Object

The `calculate()` function returns a comprehensive object:

```typescript
interface CalculatedResults {
  // Production series (monthly arrays)
  prod: {
    survey: number[];
    drilling: number[];
    recording: number[];
    shots: number[];
    upholes: number[];
  };

  // Revenue in USD
  revenueProdUsd: number[];     // Recording revenue
  mobUsd: number[];             // Mobilisation
  upholeUsd: number[];          // Uphole revenue
  demobUsd: number[];           // Demobilisation
  revenue100Usd: number[];      // Total 100% revenue
  revenueEnservUsd: number[];   // Contractor share in USD

  // Revenue in NGN
  revenueNgn: number[];         // Contractor share in NGN

  // Costs
  categories: string[];         // List of cost categories
  categorySeries: {             // Costs by category
    [category: string]: number[];
  };
  lineSeriesMap: {              // Costs by line ID
    [lineId: string]: number[];
  };
  funding: number[];            // Total funding per month

  // Cash flow
  cash: number[];               // Monthly cash flow (revenue - funding)

  // KPIs
  totalRevenue: number;         // Sum of revenueNgn
  totalCost: number;            // Sum of funding
  netCashFlow: number;          // Sum of cash
  crr: number;                  // Cost recovery ratio
  roic: number;                 // Return on invested capital
}
```

### KPI Calculations

**CRR (Cost Recovery Ratio)**:
```
CRR = Total Funding / Total Revenue
```
Lower is better. Target: <0.8 (80%)

**ROIC (Return on Invested Capital)**:
```
ROIC = (Net Cash Flow × 0.7) / (500,000,000 + Total Funding)
```
Higher is better. Target: >0.15 (15%)

---

## Storage Schema

### localStorage Keys

| Key | Type | Description |
|-----|------|-------------|
| `seismic_projects_list` | JSON array | List of all projects |
| `seismic_current_project` | string | Current project ID |
| `seismic_project_{id}` | JSON object | Individual project data |
| `seismic_economics_model_v1` | JSON object | Legacy key (migrated) |

### Project List Entry

```typescript
interface ProjectListItem {
  id: string;         // Unique ID (timestamp-based)
  name: string;       // Project name
  createdAt: number;  // Unix timestamp (ms)
}
```

**Example**:
```json
[
  {
    "id": "lz3k8p9x2a",
    "name": "NUPRC/FES ANAMBRA 2D",
    "createdAt": 1714475234567
  },
  {
    "id": "lz3k9a4b7c",
    "name": "Niger Delta Exploration",
    "createdAt": 1714475567890
  }
]
```

### Stored Project Data

Stored at key: `seismic_project_{id}`

**Structure**: Entire `ProjectModel` serialized as JSON.

**Example**: See complete model in [Example Data](#example-data) section below.

---

## Example Data

### Complete Project Example

```json
{
  "projectInputs": {
    "projectName": "NUPRC/FES ANAMBRA 2D SEISMIC ACQUISITION",
    "omlNumber": "NUPRC/FES ANAMBRA BASIN",
    "client": "NUPRC/FES",
    "contractor": "EnServ",
    "projectArea": 541.593,
    "shotFactor": 0.0276794095,
    "redrillFactor": 1.1,
    "duration": 8,
    "revenueShare": 1,
    "costShare": 1,
    "fx": 1360
  },
  "contractTerms": {
    "turnkeyRate": 20000,
    "mobilisation": 2000000,
    "demobilisation": 500000,
    "upholeRate": 3500
  },
  "productionPrograms": {
    "survey": {
      "label": "Survey",
      "unit": "km",
      "total": 541.593,
      "startMonth": 2,
      "activeMonths": 5,
      "rampMonths": 2,
      "profile": "S-Curve",
      "manualMonthly": []
    },
    "drilling": {
      "label": "Drilling",
      "unit": "SDH",
      "total": 18054,
      "startMonth": 4,
      "activeMonths": 4,
      "rampMonths": 2,
      "profile": "S-Curve",
      "manualMonthly": []
    },
    "recording": {
      "label": "Recording",
      "unit": "km",
      "total": 499.713,
      "startMonth": 5,
      "activeMonths": 4,
      "rampMonths": 2,
      "profile": "Uniform",
      "manualMonthly": []
    },
    "upholes": {
      "label": "Upholes",
      "unit": "holes",
      "total": 16,
      "startMonth": 2,
      "activeMonths": 3,
      "rampMonths": 1,
      "profile": "Manual",
      "manualMonthly": [0, 4, 4, 4, 0, 0, 0, 0, 0]
    }
  },
  "rateCards": {
    "survey": [
      {"name": "Survey rate per km", "value": 0, "unit": "₦/km"},
      {"name": "Offset rate", "value": 0, "unit": "₦"},
      {"name": "Number of survey crew", "value": 0, "unit": "crews"}
    ],
    "drilling": [
      {"name": "Drilling rate per SDH", "value": 0, "unit": "₦/SDH"},
      {"name": "Uphole drilling rate", "value": 0, "unit": "₦/hole"},
      {"name": "Standby rate", "value": 0, "unit": "₦/day"}
    ]
  },
  "costLines": [
    {
      "id": "c1",
      "category": "SURVEYING SUB.CONT. JOB",
      "item": "GPS Monumentation & Observation",
      "badge": "sub",
      "owner": "EnServ",
      "driverType": "manualMonthly",
      "driverRef": "",
      "rate": 0,
      "monthly": [0, 0, 0, 0, 0, 0, 0, 0, 0],
      "formula": {
        "enabled": false,
        "tokens": [],
        "applyTo": "all"
      },
      "monthFormulas": {}
    },
    {
      "id": "c22",
      "category": "FUEL & LUBRICANTS",
      "item": "Diesel (AGO)",
      "badge": "var",
      "owner": "EnServ",
      "driverType": "manualMonthly",
      "driverRef": "",
      "rate": 0,
      "monthly": [0, 0, 0, 0, 0, 0, 0, 0, 0],
      "formula": {
        "enabled": false,
        "tokens": [],
        "applyTo": "all"
      },
      "monthFormulas": {}
    }
  ],
  "upholes": [0, 4, 4, 4, 0, 0, 0, 0, 0]
}
```

---

## Migration & Versioning

### Legacy Migration

On first load, the application checks for legacy data:

**Legacy Key**: `seismic_economics_model_v1`

**Migration Process**:
1. Check if projects list is empty
2. Check if legacy key exists
3. Create new project with legacy data
4. Extract project name from legacy data
5. Save to new structure
6. Delete legacy key

**Code**:
```javascript
const legacy = localStorage.getItem('seismic_economics_model_v1');
if (legacy && projects.length === 0) {
  const id = uid();
  const data = JSON.parse(legacy);
  const name = data.projectInputs?.projectName || 'Default Project';

  projects = [{id, name, createdAt: Date.now()}];
  saveList(projects);
  localStorage.setItem(dataKey(id), legacy);
  localStorage.removeItem('seismic_economics_model_v1');
}
```

### Data Versioning

Currently no explicit version field. Future enhancement:

```json
{
  "_version": 2,
  "_lastModified": 1714475234567,
  "projectInputs": { ... },
  ...
}
```

---

## Validation Rules

### Constraints

| Field | Min | Max | Type |
|-------|-----|-----|------|
| `duration` | 1 | 14 | integer |
| `revenueShare` | 0 | unlimited | number |
| `costShare` | 0 | unlimited | number |
| `fx` | 0 | unlimited | number |
| `startMonth` | 1 | duration | integer |
| `activeMonths` | 1 | duration | integer |
| `rampMonths` | 1 | activeMonths | integer |
| `monthly` array | - | duration + 1 | array |

### Business Rules

1. **Ramp Months**: Should not exceed `activeMonths / 2` (warning shown)
2. **Manual Total**: Sum of `manualMonthly` should equal `total` (warning shown)
3. **Month Count**: All monthly arrays normalized to `duration + 1` (including demob)
4. **Unique IDs**: Cost line IDs must be unique (enforced by generator)
5. **Owner Factor**: EnServ = 1.0, JV = costShare, Reimbursable = 0.0

---

## Best Practices

### Data Entry

1. **Duration First**: Set duration before configuring production
2. **Normalize Totals**: Ensure production totals are realistic
3. **Rate Cards Early**: Define all rates before using formulas
4. **Formula Testing**: Test formulas on one month before "apply to all"
5. **Backup Projects**: Duplicate before major changes

### Performance

1. **Limit Line Items**: Keep under 100 for optimal performance
2. **Minimize Formulas**: Use manual entry for static values
3. **Avoid Deep Nesting**: Don't create overly complex categories
4. **Clean Up**: Delete unused projects regularly

### Data Integrity

1. **Consistent Units**: Use same units across related fields
2. **Validate Formulas**: Ensure all referenced rates exist
3. **Check Totals**: Verify calculations make sense
4. **Test Scenarios**: Use duplicate projects for what-if analysis

---

**Last Updated**: 2026-04-30
