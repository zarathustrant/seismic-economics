# Technical Documentation

Developer-focused documentation for the Seismic Project Economics Management System.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Code Structure](#code-structure)
3. [Data Flow](#data-flow)
4. [Storage System](#storage-system)
5. [Core Modules](#core-modules)
6. [Calculation Engine](#calculation-engine)
7. [Rendering System](#rendering-system)
8. [Formula System](#formula-system)
9. [API Reference](#api-reference)
10. [Extending the Application](#extending-the-application)

---

## Architecture Overview

### Technology Stack

- **HTML5**: Single-page structure
- **CSS3**: Custom properties (CSS variables), Flexbox, Grid
- **JavaScript (ES6+)**: Vanilla JS, no frameworks
- **Storage**: Browser localStorage API

### Design Patterns

1. **Module Pattern**: Projects module encapsulates project management
2. **Observer Pattern**: Event listeners for UI interactions
3. **MVC-like**: Separation of data (model), rendering (view), and logic (controller)
4. **Functional**: Heavy use of pure functions for calculations

### Key Principles

- **No External Dependencies**: Zero npm packages, CDNs, or libraries
- **Single File**: Entire app in one HTML file (~1815 lines)
- **Client-Side Only**: No server-side code or API calls
- **Auto-Save**: Every mutation triggers save to localStorage
- **Reactive**: Model changes trigger full re-render

---

## Code Structure

### File Layout

```
app.html
├── <head>
│   ├── Metadata & Title
│   ├── Google Fonts (IBM Plex Sans, IBM Plex Mono)
│   └── <style> (lines 9-117)
│       ├── CSS Reset
│       ├── CSS Custom Properties
│       ├── Layout Styles (header, tabs, panes)
│       ├── Component Styles (cards, tables, forms)
│       └── Responsive Breakpoints
├── <body>
│   ├── Header (lines 120-139)
│   ├── Project Switcher Panel (lines 141-147)
│   ├── Tab Navigation (lines 149-157)
│   └── Main Content Panes (lines 159-221)
│       ├── Executive Summary
│       ├── Inputs
│       ├── Crew & Rates
│       ├── Production Schedule
│       ├── Cost Model
│       ├── Revenue & Funding
│       └── Cash Flow
└── <script> (lines 223-1812)
    ├── Default Data (PROJECT_DATA)
    ├── Projects Module
    ├── Storage Functions
    ├── Model Initialization
    ├── Calculation Engine
    ├── Rendering Functions
    ├── Formula System
    ├── Event Handlers
    └── Application Bootstrap
```

### Code Sections

| Lines | Section | Purpose |
|-------|---------|---------|
| 1-117 | Styles | All CSS styling |
| 120-221 | HTML | DOM structure |
| 224-337 | Default Data | PROJECT_DATA constant |
| 339-477 | Projects Module | Multi-project management |
| 479-511 | Project UI | Panel rendering and interaction |
| 513-571 | Initialization | Boot sequence and model init |
| 572-581 | Utilities | Helper functions (fmt, sum, etc.) |
| 582-663 | Production | Production phasing logic |
| 664-713 | Calculation | Main calculate() function |
| 715-735 | Rendering Core | render() and renderHeader() |
| 737-768 | Summary Render | Executive summary rendering |
| 770-831 | Inputs Render | Inputs tab rendering |
| 832-915 | Production Render | Production schedule rendering |
| 917-978 | Rates Render | Crew & rates rendering |
| 981-1066 | Costs Render | Cost model rendering |
| 1068-1452 | Monthly Edit | Monthly value editing UI |
| 1463-1535 | Rate CRUD | Rate card management functions |
| 1537-1668 | Formula Engine | Formula evaluation and management |
| 1670-1752 | Cost CRUD | Cost category and line management |
| 1754-1777 | Funding Render | Revenue & funding rendering |
| 1770-1802 | Cash Flow Render | Cash flow rendering and charts |
| 1804-1812 | Event Listeners | Tab switching and bootstrap |

---

## Data Flow

### Application Lifecycle

```
1. Page Load
   ↓
2. Projects.init()
   - Load project list from localStorage
   - Migrate legacy data if needed
   - Ensure at least one project exists
   - Set current project ID
   ↓
3. Load Current Project
   - Retrieve project data from localStorage
   - Parse JSON to model object
   - Initialize model properties (formulas, etc.)
   ↓
4. render()
   - Calculate all derived values
   - Update all UI sections
   - Save to localStorage
   ↓
5. User Interaction
   - User edits value
   - Event handler updates model
   - render() called
   - Loop back to step 4
```

### Render Cycle

```
render()
├── latest = calculate()
│   ├── Build production series
│   ├── Calculate revenue in USD
│   ├── Convert to NGN
│   ├── Calculate costs per line
│   ├── Aggregate by category
│   ├── Calculate cash flow
│   └── Calculate KPIs
├── saveModel() → localStorage
├── renderHeader()
├── renderSummary()
├── renderInputs()
├── renderRates()
├── renderProduction()
├── renderCosts()
├── renderFunding()
└── renderCashFlow()
```

---

## Storage System

### localStorage Keys

| Key Pattern | Purpose | Example |
|-------------|---------|---------|
| `seismic_projects_list` | Array of all projects | `[{id, name, createdAt}]` |
| `seismic_current_project` | ID of current project | `"abc123xyz"` |
| `seismic_project_{id}` | Individual project data | Full model JSON |
| `seismic_economics_model_v1` | Legacy single-project key | Migrated on first load |

### Storage Functions

```javascript
// In Projects module
function list() // Get all projects
function saveList(l) // Save project list
function currentId() // Get current project ID
function setCurrentId(id) // Set current project ID
function loadModel(id) // Load project data by ID
function saveModel(id, data) // Save project data
```

### Data Persistence

**Auto-Save Mechanism**:
- Every `render()` call triggers `saveModel()`
- No manual save required
- All mutations → render() → auto-save

**Storage Limits**:
- localStorage quota: ~5-10MB (browser-dependent)
- Each project: ~50-500KB depending on:
  - Number of cost lines
  - Number of months
  - Formula complexity
  - Rate card size

---

## Core Modules

### Projects Module

**Purpose**: Manages multiple projects and their lifecycle.

**Pattern**: IIFE (Immediately Invoked Function Expression) returning public API.

```javascript
const Projects = (() => {
  // Private variables
  const LIST_KEY = 'seismic_projects_list';
  const CUR_KEY = 'seismic_current_project';

  // Private functions
  function uid() { ... }
  function list() { ... }
  function saveList(l) { ... }

  // Public API
  return {
    init,
    loadModel,
    saveModel,
    save,
    create,
    switchTo,
    rename,
    duplicate,
    remove,
    resetCurrent,
    currentId,
    list,
    currentName
  };
})();
```

**Key Functions**:

- `init()`: Bootstrap, migrate legacy data, ensure valid state
- `create()`: Create new project with unique ID
- `switchTo(id)`: Save current, load target, render
- `loadModel(id)`: Retrieve and parse project data
- `saveModel(id, data)`: Stringify and store project data

### Global State

**Variables**:

```javascript
let model = { ... }; // Current project data
let expandedCats = new Set(); // Expanded cost categories
let expandedLines = new Set(); // Expanded cost lines
let latest = null; // Latest calculation results
let nextCostLineId = 47; // Auto-increment ID
let showAddCatForm = false; // UI state
let activeAddItemCategory = null; // UI state
let showAddRateSectionForm = false; // UI state
let activeAddRateSection = null; // UI state
let openMonthFormula = null; // {lineIdx, monthIdx}
```

---

## Calculation Engine

### calculate() Function

**Purpose**: Derives all financial metrics from input data.

**Input**: Reads global `model` object.

**Output**: Object with all calculated series and metrics.

**Structure**:

```javascript
function calculate() {
  // 1. Build production series
  const prod = buildProduction();

  // 2. Calculate USD revenue components
  const revenueProdUsd = prod.recording.map(v => v * terms.turnkeyRate);
  const mobUsd = [mobilisation, 0, 0, ...];
  const upholeUsd = prod.upholes.map(v => v * terms.upholeRate);
  const demobUsd = [..., demobilisation];

  // 3. Aggregate and convert to NGN
  const revenue100Usd = sum(all components);
  const revenueEnservUsd = revenue100Usd × revenueShare;
  const revenueNgn = revenueEnservUsd × fx;

  // 4. Calculate costs
  const lineSeriesMap = {};
  model.costLines.forEach(line => {
    lineSeriesMap[line.id] = lineSeries(line, prod);
  });

  // 5. Aggregate by category
  const categorySeries = {};
  // ... group by category

  // 6. Calculate cash flow
  const funding = sum(all categories);
  const cash = revenueNgn - funding;

  // 7. Calculate KPIs
  const totalRevenue = sum(revenueNgn);
  const totalCost = sum(funding);
  const netCashFlow = sum(cash);
  const crr = totalCost / totalRevenue;
  const roic = (netCashFlow * 0.7) / (500000000 + totalCost);

  return { prod, revenue*, funding, cash, total*, crr, roic, ... };
}
```

### buildProduction()

**Purpose**: Generate monthly production volumes.

**Logic**:

```javascript
function buildProduction() {
  // For each program (survey, drilling, recording, upholes)
  const series = phasedSeries(program);

  return { survey, drilling, recording, shots, upholes };
}
```

### phasedSeries()

**Purpose**: Distribute total volume across months based on profile.

**Profiles**:

1. **Manual**: Return stored values as-is
2. **Uniform**: Equal distribution
3. **S-Curve**: Ramp up, plateau, ramp down
4. **Front-Loaded**: Linear decrease
5. **Back-Loaded**: Linear increase
6. **Bell Curve**: Gaussian-like distribution

**Algorithm** (S-Curve example):

```javascript
function phasedSeries(program) {
  if (program.profile === 'Manual') {
    return program.manualMonthly;
  }

  const activeSlots = []; // Months that are active
  const weights = []; // Relative weight per month

  for (let m = start; m < start + active; m++) {
    const pos = m - start + 1;
    weights.push(profileWeight(profile, pos, active, ramp));
    activeSlots.push(m);
  }

  // Distribute total proportionally
  const totalWeight = sum(weights);
  activeSlots.forEach((idx, i) => {
    out[idx] = Math.round(total * weights[i] / totalWeight);
  });

  return out;
}
```

### lineSeries()

**Purpose**: Calculate monthly costs for a single line item.

**Logic**:

```javascript
function lineSeries(line, prod) {
  let base;

  if (line.driverType === 'productionLinked') {
    // Multiply production by rate
    base = driverSeries(line, prod).map(v => v * line.rate);
  } else if (line.driverType === 'fixedMonthly') {
    // Use fixed rate or manual monthly
    base = line.monthly.some(v => v !== 0)
      ? normalizedSeries(line.monthly)
      : Array(len).fill(line.rate);
  } else {
    // Manual monthly values
    base = normalizedSeries(line.monthly);
  }

  // Apply owner factor (EnServ, JV, Reimbursable)
  const f = ownerFactor(line.owner);
  return base.map(v => v * f);
}
```

---

## Rendering System

### Reactive Rendering

**Principle**: Any model change triggers full re-render.

**Pattern**:

```javascript
function onUserEdit(newValue) {
  model.someProperty = newValue;
  render(); // Re-renders everything
}
```

**Performance**: Acceptable for small-to-medium datasets (<100 line items).

### Render Functions

Each render function updates a specific section:

| Function | Target | Description |
|----------|--------|-------------|
| `renderHeader()` | Header metrics | Updates KPIs in header |
| `renderSummary()` | Summary cards | Updates cards and charts |
| `renderInputs()` | Inputs tab | Rebuilds input form |
| `renderRates()` | Rates tab | Rebuilds rate card table |
| `renderProduction()` | Production tab | Rebuilds production table |
| `renderCosts()` | Cost Model tab | Rebuilds cost tree |
| `renderFunding()` | Funding tab | Rebuilds funding tables |
| `renderCashFlow()` | Cash Flow tab | Rebuilds cash flow table |

### Rendering Helpers

**HTML Generation**:

```javascript
// Generate table row
function row(label, vals, cls='', labelCls='', formatter=fmtN) {
  const total = sum(vals);
  return `<tr class="${cls}">
    <td class="lbl ${labelCls}">${label}</td>
    ${vals.map(v => `<td class="${v<0?'neg':v>0?'pos':''}">${formatter(v)}</td>`).join('')}
    <td class="tc">${formatter(total)}</td>
  </tr>`;
}

// Generate table headers
function headers() {
  return '<thead><tr><th>Line Item</th>'
    + labels().map(m => `<th>${m}</th>`).join('')
    + '<th class="tc">Total</th></tr></thead>';
}
```

**Formatters**:

```javascript
const fmt = (n, d=0) => /* Format number with commas */
const fmtN = n => '₦' + fmt(n); // Naira
const fmtU = n => '$' + fmt(n); // USD
const fmtB = n => '₦' + (n/1e9).toFixed(2) + 'B'; // Billions
const fmtM = n => '₦' + (n/1e6).toFixed(0) + 'M'; // Millions
const fmtPct = n => (n*100).toFixed(1) + '%'; // Percentage
```

### Chart Rendering

**Bar Chart** (Cash Flow):

```javascript
function renderBarChart(id, vals) {
  const max = Math.max(...vals.map(v => Math.abs(v)), 1);
  const hasNeg = vals.some(v => v < 0);

  let html = '';
  if (hasNeg) {
    // Add zero line
    html += `<div class="zero" style="bottom:${zeroPos}px"></div>`;
  }

  vals.forEach((v, i) => {
    const h = Math.round(Math.abs(v) / max * 128);
    html += `<div class="bar-col">
      <div class="bar ${v >= 0 ? 'pos' : 'neg'}" style="height:${h}px"></div>
      <span class="bar-lbl">${labels()[i]}</span>
    </div>`;
  });

  $(id).innerHTML = html;
}
```

**Sparkline** (Trend):

```javascript
function renderSparkline(vals) {
  const max = Math.max(...vals, 1);
  const min = Math.min(...vals, 0);
  const range = max - min || 1;
  const points = vals.map((v, i) =>
    `${i * stepX},${height - (v - min) / range * height}`
  ).join(' ');

  return `<svg class="sparkline" viewBox="0 0 68 18">
    <polyline points="${points}" fill="none" stroke="var(--accent)" stroke-width="1.5" />
  </svg>`;
}
```

---

## Formula System

### Formula Structure

**Line-Level Formula**:

```javascript
{
  enabled: true,
  applyTo: 'all' | [monthIdx, ...],
  tokens: [
    {type: 'rate', section: 'survey', idx: 0},
    {type: 'op', value: '×'},
    {type: 'prod', series: 'recording'},
    {type: 'op', value: '+'},
    {type: 'num', value: 1000}
  ]
}
```

**Per-Month Formula**:

```javascript
line.monthFormulas = {
  0: { tokens: [...] }, // M01 override
  3: { tokens: [...] }, // M04 override
  // ...
}
```

### Token Types

| Type | Fields | Description |
|------|--------|-------------|
| `rate` | `section`, `idx` | Reference to rate card |
| `prod` | `series` | Reference to production series |
| `op` | `value` | Operator: ×, +, −, ÷ |
| `num` | `value` | Custom number |

### Formula Evaluation

```javascript
function evaluateFormula(formula, monthIdx) {
  if (!formula || !formula.tokens.length) return 0;

  let expr = '';
  formula.tokens.forEach(token => {
    if (token.type === 'rate') {
      expr += model.rateCards[token.section]?.[token.idx]?.value || 0;
    } else if (token.type === 'prod') {
      expr += latest.prod[token.series]?.[monthIdx] || 0;
    } else if (token.type === 'op') {
      expr += token.value.replace('×', '*').replace('÷', '/').replace('−', '-');
    } else if (token.type === 'num') {
      expr += token.value;
    }
  });

  try {
    return eval(expr); // Safe in this context (no user input)
  } catch (e) {
    return 0;
  }
}
```

**Security Note**: `eval()` is used here, but the formula is built from controlled UI elements, not free-text input, so it's safe.

### Formula Application

**Apply to Months**:

```javascript
function applyFormulaResult(lineIdx) {
  const line = model.costLines[lineIdx];
  const len = labels().length;

  if (line.formula.applyTo === 'all') {
    for (let i = 0; i < len; i++) {
      line.monthly[i] = Math.round(evaluateFormula(line.formula, i));
    }
  } else if (Array.isArray(line.formula.applyTo)) {
    line.formula.applyTo.forEach(monthIdx => {
      line.monthly[monthIdx] = Math.round(evaluateFormula(line.formula, monthIdx));
    });
  }

  line.formula.enabled = true;
  render();
}
```

**Recalculate All**:

Called when rates change:

```javascript
function recalculateAllFormulas() {
  model.costLines.forEach((line, idx) => {
    // Line-level formulas
    if (line.formula?.enabled) {
      applyFormulaResult(idx);
    }

    // Per-month formulas (override line-level)
    if (line.monthFormulas) {
      Object.keys(line.monthFormulas).forEach(mi => {
        const mf = line.monthFormulas[mi];
        if (mf?.tokens?.length > 0) {
          line.monthly[+mi] = Math.round(evaluateFormula(mf, +mi));
        }
      });
    }
  });
}
```

---

## API Reference

### Global Functions

#### Utility Functions

```javascript
const $(id) // Shorthand for document.getElementById(id)
const sum(arr) // Sum array values
const clampInt(v, min, max) // Clamp and round to integer
const fmt(n, d=0) // Format number with commas
const fmtN(n) // Format as Naira
const fmtU(n) // Format as USD
const fmtB(n) // Format as billions
const fmtM(n) // Format as millions
const fmtPct(n) // Format as percentage
```

#### Model Functions

```javascript
function initModel() // Initialize model properties (formulas, arrays)
function saveModel() // Save current model to localStorage
function render() // Calculate and re-render all
```

#### Production Functions

```javascript
function labels() // Generate month labels: ['M01', 'M02', ..., 'Demob']
function profileWeight(profile, pos, active, ramp) // Calculate weight for position
function phasedSeries(program) // Generate monthly volumes
function buildProduction() // Build all production series
```

#### Calculation Functions

```javascript
function calculate() // Main calculation engine
function lineSeries(line, prod) // Calculate line item costs
function driverSeries(line, prod) // Get production driver series
function ownerFactor(owner) // Get cost share factor
function normalizedSeries(values) // Normalize array to month count
```

#### Input Handlers

```javascript
function setPath(path, value, type) // Set nested model property
function setLine(idx, key, value, type) // Set line item property
function setLineMonth(idx, month, value) // Set line monthly value
function setRateValue(section, idx, value) // Set rate card value
function setForecastType(key, profile) // Set production profile
function setManualProduction(key, monthIdx, value) // Set manual production value
```

#### UI Handlers

```javascript
function toggleCat(cat) // Expand/collapse category
function toggleLine(id) // Expand/collapse line item
function toggleAddCategoryForm() // Show/hide add category form
function toggleAddItemForm(category) // Show/hide add item form
function toggleAddRateForm(section) // Show/hide add rate form
function toggleMonthFormula(lineIdx, monthIdx) // Open per-month formula editor
```

#### CRUD Functions

**Cost Lines**:
```javascript
function addCategorySubmit() // Create new category
function removeCategory(categoryName) // Delete category and items
function addItemSubmit(category) // Create new line item
function removeLineItem(idx) // Delete line item
```

**Rate Cards**:
```javascript
function addRateSectionSubmit() // Create new rate section
function removeRateSection(section) // Delete rate section
function addRateItemSubmit(section) // Create new rate item
function removeRateItem(section, idx) // Delete rate item
```

**Formulas**:
```javascript
function addFormulaToken(lineIdx, token) // Add token to line formula
function removeFormulaToken(lineIdx, tokenIdx) // Remove token from line formula
function clearFormula(lineIdx) // Clear line formula
function applyFormulaResult(lineIdx) // Apply formula to months
function addMonthFormulaToken(lineIdx, monthIdx, token) // Add to per-month formula
function removeMonthFormulaToken(lineIdx, monthIdx, tokenIdx) // Remove from per-month
function clearMonthFormula(lineIdx, monthIdx) // Clear per-month formula
function evaluateFormula(formula, monthIdx) // Evaluate formula to number
function recalculateAllFormulas() // Recalc all formulas (after rate changes)
```

#### Bulk Operations

```javascript
function bulkCopyFirst(idx) // Copy M01 to all months
function bulkCopyLast(idx) // Copy last month to all
function bulkLinearFill(idx) // Linear interpolation
function bulkFillForward(idx) // Fill forward from non-zero values
function bulkClearAll(idx) // Clear all monthly values
```

### Projects API

```javascript
Projects.init() // Initialize project system
Projects.loadModel(id) // Load project by ID
Projects.saveModel(id, data) // Save project by ID
Projects.save() // Save current project
Projects.create() // Create new project
Projects.switchTo(id) // Switch to project
Projects.rename(id) // Rename project
Projects.duplicate(id) // Duplicate project
Projects.remove(id) // Delete project
Projects.resetCurrent() // Reset current project to defaults
Projects.currentId() // Get current project ID
Projects.list() // Get all projects
Projects.currentName() // Get current project name
```

---

## Extending the Application

### Adding a New Input Field

1. **Add to model**:
   ```javascript
   // In PROJECT_DATA
   projectInputs: {
     ...,
     newField: defaultValue
   }
   ```

2. **Add to EMPTY_PROJECT**:
   ```javascript
   projectInputs: {
     ...,
     newField: defaultValue
   }
   ```

3. **Add to renderInputs()**:
   ```javascript
   ${inputRow('New Field Label', 'projectInputs.newField', p.newField, 'number', 'med', 'unit')}
   ```

4. **Use in calculations**:
   ```javascript
   function calculate() {
     const newValue = model.projectInputs.newField;
     // Use in calculations
   }
   ```

### Adding a New Production Program

1. **Add to model**:
   ```javascript
   productionPrograms: {
     ...,
     newProgram: {
       label: 'New Program',
       unit: 'units',
       total: 0,
       startMonth: 1,
       activeMonths: 4,
       rampMonths: 1,
       profile: 'S-Curve',
       manualMonthly: []
     }
   }
   ```

2. **Update buildProduction()**:
   ```javascript
   const newProgram = phasedSeries(model.productionPrograms.newProgram);
   return { survey, drilling, recording, shots, upholes, newProgram };
   ```

3. **Add to renderInputs()**:
   ```javascript
   ${programControls('newProgram')}
   ```

4. **Add to renderProduction()**:
   ```javascript
   + prodRow('New Program', 'newProgram', 'newProgram', 2)
   ```

5. **Add to PROD_LABELS**:
   ```javascript
   const PROD_LABELS = {
     ...,
     newProgram: 'New Program Label'
   };
   ```

### Adding a New Cost Badge Type

1. **Update renderCosts()** badge select:
   ```javascript
   <select class="sel small" id="new-item-badge">
     ...
     <option value="newbadge">newbadge</option>
   </select>
   ```

2. **Add CSS style**:
   ```css
   .badge.newbadge { background:#color; color:#text; }
   ```

3. **Update badge map in renderCosts()**:
   ```javascript
   const badgeMap = {
     ...,
     newbadge: 'newbadge'
   };
   ```

### Adding a New Tab

1. **Add tab button**:
   ```html
   <div class="tab" data-tab="newtab">New Tab</div>
   ```

2. **Add pane**:
   ```html
   <section class="pane" id="pane-newtab">
     <!-- Content -->
   </section>
   ```

3. **Add render function**:
   ```javascript
   function renderNewTab() {
     $('newtab-content').innerHTML = '...';
   }
   ```

4. **Call in render()**:
   ```javascript
   function render() {
     ...
     renderNewTab();
   }
   ```

### Adding Export Functionality

**Example: Export to JSON**

```javascript
function exportProject() {
  const data = JSON.stringify(model, null, 2);
  const blob = new Blob([data], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${model.projectInputs.projectName}.json`;
  a.click();
  URL.revokeObjectURL(url);
}
```

**Example: Export to CSV**

```javascript
function exportToCsv() {
  const rows = [];

  // Header
  rows.push(['Line Item', ...labels(), 'Total']);

  // Data rows
  model.costLines.forEach(line => {
    const vals = normalizedSeries(line.monthly);
    rows.push([line.item, ...vals, sum(vals)]);
  });

  const csv = rows.map(r => r.join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${model.projectInputs.projectName}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}
```

### Optimizing Performance

**1. Debounce Render**:

```javascript
let renderTimeout;
function debouncedRender() {
  clearTimeout(renderTimeout);
  renderTimeout = setTimeout(render, 100);
}

// Use debouncedRender() instead of render() for frequent updates
```

**2. Partial Render**:

```javascript
// Instead of full render(), update specific sections
function onInputChange(path, value) {
  setPath(path, value, 'number');
  latest = calculate();
  saveModel();
  renderHeader(); // Only update header
  renderSummary(); // Only update summary
  // Skip re-rendering tabs that haven't changed
}
```

**3. Virtual Scrolling** (for large datasets):

Consider implementing virtual scrolling for cost lines table if >100 items.

---

## Development Workflow

### Local Development

1. Edit `app.html` in your preferred editor
2. Refresh browser to see changes
3. Use browser DevTools for debugging
4. Test in multiple browsers

### Debugging

**Console Logging**:
```javascript
console.log('Model:', model);
console.log('Latest calculations:', latest);
```

**Breakpoints**:
- Set breakpoints in browser DevTools
- Step through calculate() function
- Inspect intermediate values

**localStorage Inspection**:
```javascript
// View all projects
JSON.parse(localStorage.getItem('seismic_projects_list'))

// View current project
const id = localStorage.getItem('seismic_current_project');
JSON.parse(localStorage.getItem(`seismic_project_${id}`))
```

### Testing

**Manual Test Checklist**:
- [ ] Create new project
- [ ] Edit inputs and verify calculations
- [ ] Add/edit/delete rate cards
- [ ] Add/edit/delete cost categories and items
- [ ] Build formulas and verify results
- [ ] Switch projects and verify data isolation
- [ ] Refresh page and verify persistence
- [ ] Reset project and verify defaults
- [ ] Test all production profiles
- [ ] Test manual production editing
- [ ] Test per-month formulas
- [ ] Test bulk operations
- [ ] Test responsive layout (mobile)

---

## Known Limitations

1. **No Undo/Redo**: Changes are immediate and auto-saved
2. **No Collaboration**: Single-user, local-only
3. **Storage Quota**: Limited by browser localStorage
4. **No Versioning**: No history or change tracking
5. **Security**: eval() used in formulas (controlled, but worth noting)
6. **Performance**: Full re-render on every change (acceptable for current scale)
7. **Browser Dependency**: Requires localStorage support

---

## Future Enhancement Ideas

1. **Export/Import**: JSON, CSV, Excel export
2. **Print Optimization**: Better print layouts for reports
3. **Undo/Redo**: Implement command pattern for undo
4. **Version History**: Snapshot projects at intervals
5. **Templates**: Save and reuse project templates
6. **Advanced Charts**: More visualization options (Highcharts, Chart.js)
7. **Offline Support**: Service Worker for true offline use
8. **Data Validation**: More robust input validation
9. **Formula Syntax Highlighting**: Better formula editor UX
10. **Comparison Mode**: Compare multiple projects side-by-side

---

**Last Updated**: 2026-04-30
