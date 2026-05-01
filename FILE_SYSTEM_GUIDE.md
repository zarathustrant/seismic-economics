# File-Based Project System - User Guide

## Overview

Your Seismic Economics app now uses a **file-based storage system**. All projects are saved as folders with JSON files on your computer, making them easy to back up, share, and manage.

## How It Works

### Project Folder Structure

When you create a project, the app creates a folder with this structure:

```
SeismicProjects/             ← You choose this location
├── default_project_lz3k8p/  ← Project folder (auto-generated name)
│   ├── meta.json            ← Project metadata (name, date)
│   ├── inputs.json          ← Project inputs & parameters
│   ├── terms.json           ← Contract terms
│   ├── production.json      ← Production programs
│   ├── rates.json           ← Rate cards
│   └── costs.json           ← Cost lines
├── anambra_2d_lz3k9a/       ← Another project
│   ├── meta.json
│   ├── inputs.json
│   ├── terms.json
│   ├── production.json
│   ├── rates.json
│   └── costs.json
└── ...
```

## Getting Started

### First Time Use

1. **Open the app** ([app.html](app.html))
2. Browser will ask: **"Select folder where projects will be saved"**
3. **Create a new folder** or select existing folder (e.g., "SeismicProjects")
4. Click **"Select Folder"**
5. Browser asks for permission → Click **"View files"** and then **"Save changes"**
6. App creates "Default Project" automatically

### Selecting Projects Folder

Click the **📁 Folder** button in the header to:
- Select a different projects folder
- Change storage location
- Access projects after browser restart

**Note**: Browser security requires you to reselect the folder each time you reload the page.

## Creating Projects

1. Click **project name** in header to open project switcher
2. Type project name in "New project name..." field
3. Press **Enter** or click **+ Create**
4. App creates folder: `project_name_uniqueid/`
5. All files created automatically

## Editing Projects

**All changes auto-save** to the JSON files:
- Edit any input → saves to `inputs.json`
- Change rates → saves to `rates.json`
- Modify costs → saves to `costs.json`
- etc.

**Files are updated in real-time** as you work.

## Switching Projects

1. Click project name in header
2. Select different project from list
3. Current project saves automatically
4. New project loads from its folder

## File Details

### meta.json
```json
{
  "name": "NUPRC/FES ANAMBRA 2D",
  "createdAt": 1714475234567
}
```

### inputs.json
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

### terms.json
```json
{
  "turnkeyRate": 20000,
  "mobilisation": 2000000,
  "demobilisation": 500000,
  "upholeRate": 3500
}
```

### production.json
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
  "drilling": { ... },
  "recording": { ... },
  "upholes": { ... }
}
```

### rates.json
```json
{
  "survey": [
    {
      "name": "Survey rate per km",
      "value": 50000,
      "unit": "₦/km"
    },
    ...
  ],
  "drilling": [ ... ],
  ...
}
```

### costs.json
```json
[
  {
    "id": "c1",
    "category": "SURVEYING SUB.CONT. JOB",
    "item": "GPS Monumentation & Observation",
    "badge": "sub",
    "owner": "EnServ",
    "driverType": "manualMonthly",
    "driverRef": "",
    "rate": 0,
    "monthly": [0, 500000, 500000, 0, 0, 0, 0, 0, 0],
    "formula": {
      "enabled": false,
      "tokens": [],
      "applyTo": "all"
    },
    "monthFormulas": {}
  },
  ...
]
```

## Backing Up Projects

### Manual Backup
1. Close the app
2. Copy your entire projects folder (e.g., "SeismicProjects")
3. Paste to:
   - External drive
   - OneDrive
   - Network share
   - Cloud storage

### Automatic Backup
Set up folder sync:
- OneDrive: Put projects folder in OneDrive folder
- Google Drive: Use "Backup and Sync"
- Dropbox: Put in Dropbox folder

## Sharing Projects

### Share Single Project
1. Navigate to projects folder
2. Copy specific project folder (e.g., `anambra_2d_lz3k9a/`)
3. Send via:
   - Email (zip the folder first)
   - OneDrive share link
   - USB drive
   - Network share

### Recipient Instructions
1. Download/copy project folder
2. Place in their projects folder
3. Click **📁 Folder** button in app
4. Select their projects folder
5. Project appears in project list

### Share All Projects
1. Zip entire projects folder
2. Share the zip file
3. Recipient extracts and selects as projects folder

## Managing Projects

### Rename Project
1. Open project switcher
2. Hover over project → click **Rename**
3. Enter new name
4. Updates `meta.json` only (folder name unchanged)

### Duplicate Project
1. Open project switcher
2. Hover over project → click **Dup**
3. Enter new name
4. Creates new folder with copied data

### Delete Project
1. Open project switcher
2. Hover over project → click **Del**
3. Confirm deletion
4. **Folder is permanently deleted** (cannot undo)

## Troubleshooting

### "Failed to load projects"
- **Solution**: Click **📁 Folder** and reselect folder
- Browser lost permission (happens after closing browser)

### "Failed to create project folder"
- **Cause**: No folder selected or no write permission
- **Solution**: Click **📁 Folder** and select writable folder

### "Cannot find project files"
- **Cause**: JSON files missing or corrupted
- **Solution**: Check folder contents, restore from backup

### Changes not saving
- **Check**: Browser console for errors (F12 → Console)
- **Check**: Folder still accessible
- **Solution**: Reselect folder with **📁 Folder** button

### Project list empty after reload
- **Cause**: Browser security - folder permission expired
- **Solution**: Click **📁 Folder** and reselect (normal behavior)

## Browser Compatibility

### Supported Browsers
- ✅ **Chrome** 86+ (Recommended)
- ✅ **Edge** 86+
- ✅ **Opera** 72+
- ❌ **Firefox** (File System Access API not supported)
- ❌ **Safari** (File System Access API not supported)

### For Firefox/Safari Users
**Alternative**: Use old localStorage version (ask for FILE_SYSTEM_DISABLED build)

## Security & Privacy

### Permissions
App requests **two permissions**:
1. **Read files**: Load projects from folder
2. **Write files**: Save changes to files

### Data Location
- All data stored **locally on your computer**
- No cloud upload (unless you put folder in OneDrive/etc.)
- No data sent to servers
- No internet connection needed

### Browser Security
- Permission expires when browser closes
- Must reselect folder each time (security feature)
- Cannot access files outside selected folder

## Advanced Tips

### Version Control
Use Git to track changes:
```bash
cd SeismicProjects
git init
git add .
git commit -m "Initial projects"
```

### Batch Edit
Edit JSON files directly in text editor:
1. Close app
2. Open JSON file in VS Code/Notepad++
3. Make changes
4. Save
5. Reopen app and reselect folder

### Project Templates
Create template folder:
1. Create "Templates" folder in projects folder
2. Copy template project folders there
3. Duplicate in app when needed

### Integration with Excel
1. Export JSON files
2. Use Excel Power Query to import JSON
3. Analyze in Excel
4. Update JSON and reload in app

## Best Practices

1. **Regular Backups**: Copy projects folder weekly
2. **Descriptive Names**: Use clear project names
3. **Organize by Client**: Create subfolders per client (select as projects folder)
4. **Clean Up**: Delete old projects regularly
5. **Document Changes**: Keep notes in project folder (add README.txt)

## OneDrive Integration

### Setup
1. Create "SeismicProjects" folder in **OneDrive folder**
2. In app, click **📁 Folder**
3. Navigate to OneDrive folder
4. Select "SeismicProjects"
5. OneDrive syncs automatically

### Benefits
- Automatic cloud backup
- Access from multiple computers
- Share via OneDrive links
- Version history (OneDrive keeps old versions)

### Sharing via OneDrive
1. Right-click project folder in File Explorer
2. OneDrive → Share
3. Send link to colleague
4. They download folder
5. They select it in their app

---

**Last Updated**: 2026-04-30
