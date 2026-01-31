# Script Analysis Guide

## New Feature: Analyze Existing Scripts 🎬

**Scriptoria** now supports two modes of operation:

### 1. Generate from Idea (Original Feature)
- Enter a short story idea or logline (20-500 characters)
- AI generates a complete screenplay structure from scratch
- Perfect for brainstorming new projects

### 2. Analyze Existing Script (NEW!)
- Paste your complete screenplay (100-100,000 characters)
- AI analyzes the structure and extracts:
  - Title and logline
  - 3-act structure breakdown
  - Character profiles
  - Scene breakdown
  - Sound design recommendations
- Perfect for pre-production planning on existing scripts

---

## How to Use Script Analysis

### Step 1: Switch to Analysis Mode
Click the **"🎬 Analyze Existing Script"** button at the top of the form.

### Step 2: Input Your Script
You have two options:

**Option A: Upload a File**
- Click the "Upload Script" box
- Select a `.pdf` or `.docx` file containing your screenplay
- The text will be extracted automatically

**Option B: Paste Directly**
- Copy your screenplay text
- Paste it into the large text area
- Include:
  - Title
  - Character names
  - Dialogue
  - Action lines
  - Scene headings (INT/EXT, location, time)

### Step 3: Select Genre (Optional)
Choose the genre that best matches your script:
- Drama
- Thriller
- Comedy
- Sci-Fi
- Horror

### Step 4: Generate Analysis
Click **"Analyze & Generate"** and wait 10-15 seconds.

The AI will:
1. ✅ Extract the screenplay structure
2. ✅ Identify main characters
3. ✅ Create character profiles with arcs and traits
4. ✅ Break down scenes with locations and cast
5. ✅ Suggest sound design (music, SFX, ambience)

---

## What Script Formats Work Best?

### ✅ Good Formats:
- Standard screenplay format (Courier 12pt)
- Clear scene headings (INT. HOUSE - DAY)
- Character names in CAPS before dialogue
- Action lines between dialogue

### Example:
```
FADE IN:

INT. COFFEE SHOP - DAY

SARAH, 30s, nervous but determined, sits across from MARCUS, 40s, calm and calculating.

SARAH
I know what you did.

MARCUS
(smiling)
You have no proof.

Sarah slides a folder across the table.
```

### ⚠️ Formats That May Need Cleaning:
- Novel-style prose
- Treatment documents (too high-level)
- Outline-only documents (no dialogue)

---

## API Endpoint Details

### `POST /analyze_script`

**Request:**
```json
{
  "scriptText": "Full screenplay text here...",
  "genre": "Thriller"
}
```

**Response:**
```json
{
  "success": true,
  "screenplay": {
    "title": "Extracted or inferred title",
    "logline": "AI-generated logline based on script",
    "genre": "Thriller",
    "mainCharacters": ["Sarah", "Marcus", "Detective Jones"],
    "threeActStructure": { ... }
  },
  "characters": [ ... ],
  "scenes": [ ... ],
  "soundDesign": { ... }
}
```

---

## Technical Implementation

### Backend Changes:
- **New File:** `backend/generators/script_analyzer.py`
  - Analyzes existing scripts using AI
  - Extracts structure, characters, and plot points
  
- **New Endpoint:** `/analyze_script`
  - Validates script text (100-50,000 chars)
  - Calls script analyzer
  - Runs full generation pipeline (characters, scenes, sound)

### Frontend Changes:
- **Mode Toggle:** Switch between "Generate" and "Analyze"
- **Conditional Inputs:** Different text areas for ideas vs scripts
- **Validation:** Different character limits based on mode

---

## Use Cases

### 1. Pre-Production Planning
You've written a screenplay and need to create:
- Character breakdowns for actors
- Scene lists for scheduling
- Sound design notes for composers

### 2. Script Analysis
Understand the structure of your screenplay:
- How your 3-act structure is working
- Character arc identification
- Plot point mapping

### 3. Pitch Deck Creation
Generate professional materials from your script:
- Compelling logline
- Character profiles
- Scene-by-scene breakdown
- Export to PDF for pitch meetings

---

## Limitations

- **Max Length:** 100,000 characters (~100 pages)
- **Processing Time:** 10-20 seconds (longer than idea generation)
- **AI Interpretation:** Results depend on script clarity
- **Format Sensitivity:** Better results with standard screenplay format

---

## Tips for Best Results

1. **Use Clear Character Names**
   - Consistent capitalization (SARAH, not Sarah/sarah)
   - Full names help AI distinguish characters

2. **Include Scene Headings**
   - Helps AI identify scene boundaries
   - Use standard format (INT/EXT. LOCATION - TIME)

3. **Provide Complete Scenes**
   - Include dialogue and action
   - Not just outlines or beat sheets

4. **Clean Your Text**
   - Remove page numbers and headers if copying from PDF
   - Ensure proper line breaks

---

## Troubleshooting

### "Script text is too short"
- Minimum: 100 characters
- Make sure you pasted the full script, not just a snippet

### "Script text is too long"
- Maximum: 100,000 characters
- Consider analyzing one act at a time
- Or submit a condensed version

### "Failed to analyze script"
- Check that script has clear character names
- Ensure dialogue is present
- Try reformatting to standard screenplay format

### AI extracted wrong information
- Use the "Edit" button to correct any mistakes
- The more standard your screenplay format, the better the AI accuracy

---

## Example Workflow

1. ✅ Finish writing your screenplay
2. ✅ Switch to "Analyze Existing Script" mode
3. ✅ Upload or paste your script
4. ✅ Click "Analyze & Generate"
5. ✅ Review the generated materials
6. ✅ Use "Edit" to refine any details
7. ✅ Export to PDF for your production team

---

**Ready to analyze your script?** Start using Scriptoria today! 🎬
