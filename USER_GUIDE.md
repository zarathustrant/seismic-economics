# Seismic Project Economics - User Guide

Complete guide for using the Seismic Project Economics Management System.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Management](#project-management)
3. [Executive Summary Tab](#executive-summary-tab)
4. [Inputs Tab](#inputs-tab)
5. [Crew & Rates Tab](#crew--rates-tab)
6. [Production Schedule Tab](#production-schedule-tab)
7. [Cost Model Tab](#cost-model-tab)
8. [Revenue & Funding Tab](#revenue--funding-tab)
9. [Cash Flow Tab](#cash-flow-tab)
10. [Advanced Features](#advanced-features)
11. [Best Practices](#best-practices)

---

## Getting Started

### Opening the Application

1. Locate the `app.html` file
2. Double-click to open in your default browser, or
3. Right-click and choose "Open with" to select a specific browser

### First Launch

On first launch, the application will:
- Create a default project named "Default Project"
- Initialize with sample data (NUPRC/FES ANAMBRA 2D SEISMIC ACQUISITION)
- Auto-save to browser localStorage

### Navigation

The application has a **sticky header** showing:
- Project switcher (left)
- Key metrics (Revenue, Funding, Net CF, CRR, ROIC)
- Reset button

Below the header is a **tab bar** with seven tabs:
- Executive Summary
- Inputs
- Crew & Rates
- Production Schedule
- Cost Model
- Revenue & Funding
- Cash Flow

---

## Project Management

### Project Switcher

Located in the top-left corner of the header.

#### Creating a New Project

1. Click the **project switcher button** (shows current project name)
2. Type a name in the "New project name..." field
3. Click **+ Create** or press Enter
4. The new project will be created with default values

#### Switching Projects

1. Click the **project switcher button**
2. Click any project in the list
3. Current project data is auto-saved before switching

#### Renaming a Project

1. Open the project switcher
2. Hover over a project to reveal actions
3. Click **Rename**
4. Enter new name and click OK

#### Duplicating a Project

1. Open the project switcher
2. Hover over a project to reveal actions
3. Click **Dup** (Duplicate)
4. A copy will be created with "(copy)" suffix

#### Deleting a Project

1. Open the project switcher
2. Hover over a project to reveal actions
3. Click **Del**
4. Confirm deletion (cannot delete the only project)

#### Resetting Current Project

1. Click **Reset** button in the header
2. Confirm reset
3. Project will revert to factory defaults (sample data)

---

## Executive Summary Tab

### Overview

Dashboard view showing high-level metrics and visualizations.

### Summary Cards

Five cards displaying:
1. **Total Revenue**: NGN converted from USD revenue
2. **Funding Requirement**: Excluding CA/security reimbursables
3. **Net Cash Flow**: Revenue less funding (green if positive, red if negative)
4. **CRR**: Funding requirement / revenue ratio
5. **ROIC**: Return on invested capital percentage

### Monthly Cash Flow Chart

- Bar chart showing cash flow by month
- Green bars: Positive cash flow
- Red bars: Negative cash flow
- Zero line shown if negative values present
- Hover to see month labels

### Top Funding Drivers

- Grid showing top 8 cost categories
- Shows category name and total value
- Progress bar indicates relative size
- Sorted by descending value

---

## Inputs Tab

### Project Identity Panel

Configure basic project information:

- **Project Name**: Full project name (text)
- **OML / Basin**: Location identifier (text)
- **Client / Operator**: Client name (text)
- **Contractor**: Contractor name (text)
- **Project Area**: Total area in km (number)
- **Duration**: Project duration in months, 1-14 (number)

### Commercial Terms Panel

Financial parameters:

- **Turnkey Rate**: Rate per km in USD ($/km)
- **Mobilisation**: One-time mobilization fee in USD
- **Demobilisation**: One-time demobilization fee in USD
- **Uphole Rate**: Rate per uphole in USD ($/uphole)
- **Revenue Share**: Contractor's revenue share multiplier (0-1)
- **Cost Share**: Contractor's cost share multiplier (0-1)
- **NNPC FX Rate**: USD to NGN exchange rate (₦/$)

### Production Drivers Panel

Configure four production programs:

#### Survey
- **Total km**: Total survey kilometers
- **Start Month**: Month to begin (1 = M01)
- **Active Months**: Number of active months
- **Ramp Months**: Ramp-up/down period
- **Forecast Type**: Distribution profile (see Production Schedule)

#### Drilling
- **Total SDH**: Total shot-depth-holes
- **Start Month, Active Months, Ramp Months**: Same as Survey
- **Forecast Type**: Distribution profile

#### Recording
- **Total km**: Total recording kilometers
- **Start Month, Active Months, Ramp Months**: Same as Survey
- **Forecast Type**: Distribution profile

#### Upholes
- **Total holes**: Total upholes
- **Start Month, Active Months, Ramp Months**: Same as Survey
- **Forecast Type**: Distribution profile (often Manual)

**Note**: When Forecast Type is "Manual", the start/active/ramp fields are hidden. Use the Production Schedule tab to edit values directly.

---

## Crew & Rates Tab

### Purpose

Define reusable rate values for cost calculations and formulas.

### Rate Sections

Default sections:
- **Survey Rates**
- **Drilling Rates**
- **Preloading Rates**
- **Recording Rates**
- **Base Camp & Medical Rates**

### Managing Rate Items

#### Adding a Rate Item

1. Click **+** button next to section name
2. Enter rate name (e.g., "GPS Monumentation")
3. Enter unit (e.g., "₦/km" or "₦/mo")
4. Click **Add**

#### Editing Rate Values

- Click directly in the value column
- Type new value
- Press Enter or click outside to save
- All formulas using this rate will auto-recalculate

#### Removing a Rate Item

1. Click **Remove** next to the rate
2. Confirm deletion
3. Warning: Formulas referencing this rate may break

### Managing Rate Sections

#### Adding a New Section

1. Click **+ Add Section** at bottom
2. Enter section name (will be lowercase, no spaces)
3. Click **Add**

#### Removing a Section

1. Click **−** button next to section name
2. Confirm deletion
3. All rate items in section will be deleted

---

## Production Schedule Tab

### Overview

View and edit monthly production values for all programs.

### Production Rows

Four main rows:
1. **Survey production (km)**: Decimal values, 3 decimals
2. **Drilling production (SDH)**: Whole numbers
3. **Upholes**: Whole numbers
4. **Recording production (km)**: Decimal values, 3 decimals

Plus one calculated row:
5. **Recording shots**: Auto-calculated from recording km and shot factor

### Auto vs Manual Mode

**Auto Mode** (S-Curve, Uniform, etc.):
- Values are calculated based on Inputs tab settings
- Display-only (cannot edit in table)
- Modify via Inputs tab

**Manual Mode**:
- Row shows "MANUAL" badge
- Each month has editable input field
- Type values directly
- **Auto-balancing**: When you change one month, the system adjusts other months to maintain the total
- Warning shown if total doesn't match configured total

### Editing Manual Production

1. Set Forecast Type to "Manual" in Inputs tab
2. Return to Production Schedule tab
3. Type values in each month's input field
4. Total column shows current total vs. target total
5. If totals don't match, column turns red

### Warnings

If configuration issues detected:
- Yellow warning banner appears
- Example: "Survey: ramp months exceed half of active months"

---

## Cost Model Tab

### Overview

Comprehensive cost breakdown by category and line item.

### Structure

- **Categories**: Top-level groupings (e.g., "SURVEYING SUB.CONT. JOB")
- **Line Items**: Individual cost entries within categories
- **Badges**: Type indicators (sub, labor, var, lease, owned, fixed)

### Managing Categories

#### Adding a Category

1. Click **+ Add Category** at bottom
2. Enter category name (auto-uppercase)
3. Click **Add**
4. New category created with one default item

#### Removing a Category

1. Click **−** button next to category name
2. Confirm deletion
3. All items in category will be deleted

### Managing Line Items

#### Adding a Line Item

1. Click **+** button next to category name
2. Enter item name
3. Select badge type:
   - **fixed**: Fixed cost
   - **var**: Variable cost
   - **sub**: Subcontractor
   - **lease**: Leased equipment
   - **owned**: Owned equipment
   - **labor**: Labor cost
4. Click **Add**

#### Viewing Line Item Details

1. Click **Monthly** button next to line item
2. Monthly breakdown panel expands
3. Shows:
   - Formula builder
   - Monthly summary statistics
   - Monthly value grid with heat maps
   - Bulk action buttons

#### Removing a Line Item

1. Click **Remove** button
2. Confirm deletion

### Monthly Values

#### Viewing Monthly Breakdown

Click **Monthly** button to expand the line item.

**Monthly Summary Section** shows:
- **Total**: Sum of all months
- **Average**: Mean value
- **Min**: Minimum value (and month)
- **Max**: Maximum value (and month)
- **Variance**: Percentage variance (amber if >30%, yellow if >15%)

#### Editing Monthly Values

**Grid Layout**:
- Each month has an input field
- Type value and press Enter to save
- Auto-saves and recalculates

**Visual Indicators**:
- **Heat Map**: Color intensity shows relative magnitude
  - Light yellow: Low (0-33%)
  - Medium yellow: Med (33-67%)
  - Orange: High (67-100%)
- **Progress Bar**: Visual bar under each value
- **Spike Warning**: Red border if value spikes >50% from previous month

#### Bulk Actions

Six bulk operation buttons:

1. **Copy First**: Copy M01 value to all months
2. **Copy Last**: Copy last month value to all months
3. **Linear Fill**: Linear interpolation from M01 to last month
4. **Fill Forward**: Copy each non-zero value forward until next non-zero
5. **Clear All**: Set all months to zero (with confirmation)
6. **Close**: Collapse the panel

---

## Revenue & Funding Tab

### Revenue Bridge Table

Shows USD to NGN revenue conversion:

1. **Production revenue (USD)**: Recording km × Turnkey rate
2. **Mobilisation (USD)**: One-time mobilization
3. **Uphole revenue (USD)**: Upholes × Uphole rate
4. **Demobilisation (USD)**: One-time demobilization
5. **100% Revenue (USD)**: Sum of above
6. **EnServ Revenue Share (USD)**: 100% × Revenue share
7. **EnServ Revenue (NGN)**: USD × FX rate (final row)

### Monthly Funding Requirement Table

Shows funding by cost category:
- One row per category from Cost Model
- Shows monthly breakdown
- **Total Funding Requirement** row at bottom

---

## Cash Flow Tab

### Cash Flow Statement Table

Monthly breakdown:

1. **EnServ Revenue (NGN)**: Revenue from Revenue Bridge
2. **Funding Requirement (NGN)**: Total costs (shown as negative)
3. **Monthly Cash Flow**: Revenue - Funding
4. **Cumulative Cash Flow**: Running total

### Revenue, Funding, and Net Cash Flow Chart

Dual-bar chart:
- **Blue bars**: Revenue per month
- **Amber bars**: Funding per month
- Compare visually to see surplus/deficit months

---

## Advanced Features

### Formula Calculator

Build dynamic cost calculations using rates and production data.

#### Types of Formulas

1. **Line-Level Formula**: Applies to entire line item (all months or selected months)
2. **Per-Month Formula**: Overrides specific months only

#### Building a Line-Level Formula

1. Expand a line item (click **Monthly**)
2. In the Formula Calculator section:
   - Select rates or production from dropdown
   - Add operators (×, +, −, ÷)
   - Add custom numbers
3. Select "Apply To":
   - **All months**: Formula applies to every month
   - **Select months**: Check specific months
4. Click **Apply Formula**
5. Formula calculates and populates monthly values

**Example**: Labor cost = Number of workers × Daily rate × Days in month
- Select "Number of workers" rate
- Click × operator
- Select "Daily rate" rate
- Click × operator
- Add custom number (e.g., 30 for days)

#### Building a Per-Month Formula

Use when a specific month needs different calculation logic.

1. Expand a line item
2. Click **fx** button on the month you want to override
3. Green formula panel opens for that month
4. Build formula same as line-level
5. Formula auto-applies (no "Apply" button needed)
6. Month shows "fx" indicator

**Per-month formulas always override line-level formulas.**

#### Production-Linked Formulas

When formula includes production data (Survey, Drilling, Recording, Shots, Upholes):
- Formula evaluates separately for each month
- Uses that month's production volume
- Result varies month to month

**Example**: Fuel cost = Drilling SDH × Rate per SDH
- M01: 500 SDH × ₦1000 = ₦500,000
- M02: 800 SDH × ₦1000 = ₦800,000

#### Formula Display

- Formula shows as human-readable text
- Rate values shown in parentheses
- If production-linked: "varies by month"
- If static: calculated result shown

#### Clearing Formulas

**Line-Level**:
- Click **Clear Formula** in formula builder
- Confirms and removes formula

**Per-Month**:
- Click **Clear** in per-month formula panel
- Removes formula for that month only

### Visual Indicators

#### Sparklines

- Mini line charts next to total values in Cost Model
- Shows trend across months
- Helps identify patterns quickly

#### Heat Maps

In monthly value grids:
- Color intensity indicates magnitude
- Helps spot high-cost months visually

#### Badges

Color-coded badges on line items:
- **green (owned)**: Owned equipment
- **blue (lease)**: Leased equipment
- **amber (sub)**: Subcontractor
- **purple (labor)**: Labor
- **default (fixed)**: Fixed cost
- **green (var)**: Variable cost

---

## Best Practices

### Project Setup Workflow

1. **Create Project**: Start with descriptive name
2. **Configure Inputs**: Set all project identity and terms
3. **Define Rates**: Add all relevant rates in Crew & Rates tab
4. **Set Production**: Configure production programs
5. **Build Costs**: Add categories and line items
6. **Use Formulas**: Link costs to rates and production where possible
7. **Review Summary**: Check Executive Summary for sanity

### Data Entry Tips

1. **Use Formulas**: Prefer formulas over manual entry for consistency
2. **Rate Cards First**: Define all rates before building cost formulas
3. **Start Simple**: Use auto profiles (S-Curve) before switching to Manual
4. **Regular Saves**: Application auto-saves, but duplicate projects before major changes
5. **Validate Totals**: In Manual mode, ensure totals match expected values

### Formula Best Practices

1. **Name Rates Clearly**: Use descriptive names like "Survey Crew Daily Rate"
2. **Document Units**: Include units in rate names (₦/day, ₦/km)
3. **Test Formulas**: Verify results in a few months before applying to all
4. **Use Per-Month Sparingly**: Only override months when truly exceptional
5. **Recalculate After Rate Changes**: Rate changes auto-recalculate, but verify results

### Performance Considerations

1. **Limit Projects**: 10-20 projects should perform well
2. **Browser Storage**: Each project ~50-500KB depending on complexity
3. **Backup Data**: Export localStorage periodically using browser dev tools
4. **Clear Old Projects**: Delete unused projects to free space

### Multi-Project Management

1. **Naming Convention**: Use clear, consistent names (Client - Basin - Year)
2. **Duplicate for Scenarios**: Use duplicate feature for what-if analysis
3. **Track Dates**: Project creation date shown in switcher
4. **Active Project Indicator**: Active project highlighted in green

### Troubleshooting

**Values Not Saving**:
- Check browser localStorage is enabled
- Ensure not in private/incognito mode
- Check storage quota not exceeded

**Formulas Not Calculating**:
- Verify all referenced rates exist
- Check formula syntax (no missing operators)
- Ensure monthly array initialized

**Production Totals Don't Match**:
- In Manual mode, manually adjust until totals align
- Check auto-balancing worked correctly
- Verify no rounding errors in source data

**Performance Slow**:
- Reduce number of cost line items
- Minimize use of per-month formulas
- Clear browser cache and reload

### Exporting Data

**Browser Print**:
1. Navigate to desired tab
2. Browser → Print (Ctrl/Cmd + P)
3. Adjust print settings
4. Save as PDF or print

**localStorage Export** (Advanced):
1. Open browser Developer Tools (F12)
2. Go to Application/Storage tab
3. Find localStorage for the file
4. Copy JSON data
5. Save to text file for backup

---

## Keyboard Shortcuts

- **Enter**: In input fields, confirms change
- **Tab**: Navigate between fields
- **Esc**: Close project switcher (if open)
- **Ctrl/Cmd + P**: Print current view

---

## Appendix: Production Profiles

### S-Curve
- Slow start (ramp-up)
- Peak in middle
- Slow end (ramp-down)
- Typical for most operations

### Uniform
- Equal distribution across all active months
- Simple, predictable

### Front-Loaded
- Highest volumes at start
- Decreases linearly to end
- Good for aggressive schedules

### Back-Loaded
- Lowest volumes at start
- Increases linearly to end
- Good for ramping operations

### Bell Curve
- Gradual increase to peak in middle
- Gradual decrease after peak
- Smooth, natural distribution

### Manual
- Complete control
- Enter exact values per month
- Use when none of the above fit

---

## Appendix: Formula Tokens

### Rate Token
- References a rate from Crew & Rates tab
- Format: Section:Index
- Example: survey:0 (first rate in survey section)
- Value: Current rate value

### Production Token
- References production volume for a month
- Options: survey, drilling, recording, shots, upholes
- Value: Volume for that month

### Operator Token
- Arithmetic operators
- Options: × (multiply), + (add), − (subtract), ÷ (divide)

### Number Token
- Custom numeric value
- Enter any number
- Static across all months

---

## Support

For additional help:
- Review sample data (Reset project to see examples)
- Examine default formulas in sample project
- Consult TECHNICAL_DOCUMENTATION.md for internal workings

**Last Updated**: 2026-04-30
