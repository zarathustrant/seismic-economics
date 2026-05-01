# Seismic Project Economics Management System

A comprehensive single-page web application for managing seismic acquisition project economics, cost modeling, and financial analysis.

## Overview

This application provides a complete financial management solution for 2D seismic acquisition projects, with support for:
- Multi-project management with local storage persistence
- Revenue and funding requirement modeling
- Production scheduling and phasing
- Cost structure analysis with dynamic formulas
- Currency conversion (USD to NGN)
- Cash flow analysis and reporting
- Key performance indicators (CRR, ROIC)

## Features

### Project Management
- **Multi-Project Support**: Create, switch, rename, duplicate, and delete projects
- **Auto-Save**: All changes automatically saved to browser localStorage
- **Project Migration**: Seamless migration from legacy single-project data

### Financial Modeling
- **Revenue Modeling**: Turnkey rates, mobilization/demobilization, uphole revenue
- **Cost Structure**: Categorized cost lines with monthly breakdown
- **Currency Conversion**: Automatic USD to NGN conversion at configured FX rates
- **Funding Requirements**: Comprehensive funding calculations by category

### Production Scheduling
- **Multiple Programs**: Survey, Drilling, Recording, Upholes
- **Flexible Profiles**: S-Curve, Uniform, Front-Loaded, Back-Loaded, Bell Curve, Manual
- **Phase Management**: Configure start month, active months, and ramp periods
- **Real-time Validation**: Warnings for configuration issues

### Advanced Formula Calculator
- **Line-Level Formulas**: Create dynamic calculations using rates and production data
- **Per-Month Formulas**: Override specific months with custom formulas
- **Production-Linked**: Link costs to production volumes automatically
- **Rate Cards**: Define and reference reusable rates across formulas

### Analytics & Reporting
- **Executive Summary**: Key metrics and visualizations at a glance
- **Cash Flow Charts**: Monthly and cumulative cash flow visualization
- **Cost Drivers**: Top funding drivers with visual progress bars
- **Variance Analysis**: Track cost variance across months

### User Experience
- **Tabbed Interface**: Seven organized tabs for different aspects
- **Inline Editing**: Edit values directly in tables
- **Bulk Operations**: Copy, fill, and clear operations for efficiency
- **Heat Maps**: Visual indicators for cost intensity
- **Sparklines**: Mini charts showing cost trends

## Quick Start

### Installation

1. **No Installation Required**: This is a standalone HTML file
2. Simply open `app.html` in a modern web browser

### Supported Browsers
- Chrome/Edge (recommended)
- Firefox
- Safari
- Any modern browser with JavaScript and localStorage support

### First Time Use

1. Open `app.html` in your browser
2. The application will create a default project
3. Navigate through the tabs to configure your project:
   - **Inputs**: Set project details and commercial terms
   - **Crew & Rates**: Define rate cards for calculations
   - **Production Schedule**: Configure production programs
   - **Cost Model**: Add and manage cost lines
   - **Revenue & Funding**: Review revenue bridge
   - **Cash Flow**: Analyze cash flow statements

## Key Metrics

### CRR (Cost Recovery Ratio)
```
CRR = Total Funding Requirement / Total Revenue
```
Indicates the percentage of revenue consumed by costs.

### ROIC (Return on Invested Capital)
```
ROIC = (Net Cash Flow × 70%) / (500M + Total Funding)
```
Measures return efficiency on invested capital.

## Data Persistence

- All project data is stored in browser localStorage
- Each project has a unique ID and timestamp
- Data persists across browser sessions
- Export/backup: Use browser developer tools to export localStorage

## Tabs Overview

1. **Executive Summary**: KPIs, charts, and top cost drivers
2. **Inputs**: Project identity, commercial terms, production drivers
3. **Crew & Rates**: Rate card dictionary for calculations
4. **Production Schedule**: Configure production programs with forecasting
5. **Cost Model**: Detailed cost structure with categories and line items
6. **Revenue & Funding**: Revenue bridge and funding requirements
7. **Cash Flow**: Monthly and cumulative cash flow analysis

## Project Context

This application is specifically designed for:
- NUPRC/FES seismic acquisition projects
- Contractors like EnServ
- Anambra Basin and similar regions
- Multi-month field operations (1-14 months)

## Technical Details

- **Technology**: Vanilla HTML, CSS, JavaScript (no dependencies)
- **Storage**: Browser localStorage
- **Size**: Single ~90KB file
- **Architecture**: Client-side only, no server required

## Security & Privacy

- All data stored locally in your browser
- No data sent to external servers
- No network connectivity required after initial load
- Clear browser data to remove all projects

## Limitations

- Maximum 14 months per project
- Storage limited by browser localStorage quota (~5-10MB)
- No cloud sync or collaboration features
- No export to Excel/PDF (browser print only)

## Support

For issues, questions, or feature requests related to this application, please consult:
- The USER_GUIDE.md for detailed usage instructions
- The TECHNICAL_DOCUMENTATION.md for development details
- The DATA_MODEL.md for data structure reference

## Version

Current implementation: Standalone version with project management capabilities

## License

Proprietary - For authorized use only

---

**Last Updated**: 2026-04-30
