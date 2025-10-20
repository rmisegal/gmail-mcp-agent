# New Sections for README.md

## Insert after "Installation" section and before "Configuration and Authentication"

---

## Configuration Methods: Two Approaches

The Gmail MCP Agent can be configured and integrated with Claude CLI using **two distinct approaches**. Each has its own advantages depending on your workflow and team collaboration needs.

### Approach A: Interactive CLI (Quick Setup)

**Best for:** Individual developers, rapid prototyping, one-time setup

**Advantages:**
- ✅ Fast and simple
- ✅ Automatic validation
- ✅ Immediate feedback
- ✅ No manual file editing

**Process:**
```bash
# Add MCP server
claude mcp add --transport stdio gmail-extractor python3 src/gmail_mcp_server.py

# Verify
claude mcp list
```

**Configuration stored in:** `~/.claude.json` (auto-generated)

---

### Approach B: Configuration Files (Declarative Setup)

**Best for:** Team collaboration, version control, reproducible environments

**Advantages:**
- ✅ Version controlled (commit to Git)
- ✅ Team sharing (everyone gets same config)
- ✅ Portable across machines
- ✅ Self-documenting
- ✅ Infrastructure as Code philosophy

**Process:**
```bash
# Option 1: Project-level configuration
cp config-examples/mcp-project-config-example.json .mcp.json

# Option 2: Global configuration
cp config-examples/claude-global-config-example.json ~/.claude.json
# Edit to replace paths

# Verify
claude mcp list
```

**Configuration stored in:** 
- Project: `.mcp.json` (can be committed)
- Global: `~/.claude.json` (per-machine)

---

### Comparison Table

| Feature | Interactive CLI | Configuration Files |
|---------|----------------|---------------------|
| Setup Speed | ⚡ Fastest | 🐢 Slower (manual editing) |
| Version Control | ❌ No | ✅ Yes (.mcp.json) |
| Team Sharing | ❌ Manual replication | ✅ Automatic (via Git) |
| Portability | ❌ Per-machine | ✅ Cross-machine |
| Documentation | ❌ Implicit | ✅ Explicit |
| Validation | ✅ Automatic | ⚠️ Manual |

**Recommendation:** Use **Configuration Files (Approach B)** for production and team projects. Use **Interactive CLI (Approach A)** for quick experiments.

---

## Memory System Setup

The Gmail MCP Agent uses a **4-file memory architecture** to provide persistent context across Claude CLI sessions. This eliminates the "amnesia problem" where AI assistants forget project details between sessions.

### The Four Memory Files

Located in `docs/memory-system/`:

1. **PRD.md** - Product Requirements Document
   - Defines WHAT we're building and WHY
   - User stories, success metrics, scope

2. **CLAUDE.md** - Working Instructions
   - Defines HOW to work on this project
   - Coding conventions, commands, file structure
   - **Special:** Claude CLI automatically reads this file

3. **PLANNING.md** - Architecture & Design
   - Defines the TECHNICAL blueprint
   - Technology stack, data flow, security model

4. **TASKS.md** - Task Tracking
   - Defines WHAT'S DONE and WHAT REMAINS
   - Organized by milestones, marked with completion dates

### Setup Options

#### Option A: Use Existing Memory Files (Recommended)

The project already includes complete memory files:

```bash
# Files are ready to use in docs/memory-system/
ls docs/memory-system/
# PRD.md  CLAUDE.md  PLANNING.md  TASKS.md
```

**No action needed!** Claude CLI will automatically read `CLAUDE.md` when you start a session in this project directory.

#### Option B: Customize for Your Fork

If you've forked this project and want to customize:

```bash
# Edit the memory files
nano docs/memory-system/CLAUDE.md
nano docs/memory-system/PLANNING.md
nano docs/memory-system/TASKS.md

# Update paths and project-specific details
```

### How to Use the Memory System

#### Starting a Session

```bash
cd /path/to/gmail-mcp-agent
claude

# In Claude CLI, activate Plan Mode (Shift+Tab twice)
# Then type:
```

```
Please read PLANNING.md, CLAUDE.md, and TASKS.md to understand the project.
Then continue from where we left off.
```

Claude will load all memory files and present a plan based on the current project state.

#### During a Session

- **Add context:** Use `@` to reference specific files
  ```
  @src/gmail_mcp_server.py
  Can you add error handling for network timeouts?
  ```

- **Update memory:** Press `#` to add instructions to CLAUDE.md
  ```
  # Always run pytest with -v flag for verbose output
  ```

#### Ending a Session

Before closing Claude CLI:

```
Please add a session summary to CLAUDE.md summarizing what we accomplished.
Update TASKS.md with completed items and any new discoveries.
```

This ensures the next session has full context.

### Memory File Locations

```
gmail-mcp-agent/
├── docs/
│   └── memory-system/          # Memory architecture files
│       ├── PRD.md              # Product requirements
│       ├── CLAUDE.md           # Working instructions (auto-read)
│       ├── PLANNING.md         # Architecture blueprint
│       └── TASKS.md            # Task tracking
├── config-examples/            # Configuration templates
│   ├── CONFIGURATION_GUIDE.md  # Detailed config guide
│   ├── claude-global-config-example.json
│   └── mcp-project-config-example.json
└── .mcp.json                   # Project MCP config (optional)
```

---

## Detailed Setup: Step-by-Step

### Setup Workflow A: Interactive CLI

**Step 1: Install Claude CLI**

```bash
npm install -g @anthropic-ai/claude-code
claude --version  # Verify installation
```

**Step 2: Navigate to Project**

```bash
cd /path/to/gmail-mcp-agent
```

**Step 3: Add MCP Server**

```bash
claude mcp add --transport stdio gmail-extractor python3 src/gmail_mcp_server.py
```

**Step 4: Verify Configuration**

```bash
claude mcp list
# Expected output:
# gmail-extractor: python3 src/gmail_mcp_server.py - ✓ Connected
```

**Step 5: Start Using**

```bash
claude

# In Claude CLI:
# > Please use the gmail-extractor to fetch emails with label "Invoices" from last month
```

---

### Setup Workflow B: Configuration Files

**Step 1: Install Claude CLI**

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

**Step 2: Choose Configuration Level**

**Option B1: Project-Level (Recommended for Teams)**

```bash
cd /path/to/gmail-mcp-agent

# Copy the example configuration
cp config-examples/mcp-project-config-example.json .mcp.json

# No editing needed - uses relative paths
```

**Option B2: Global Configuration (Recommended for Personal Use)**

```bash
# Copy the example
cp config-examples/claude-global-config-example.json ~/.claude.json

# Edit to replace placeholder paths
nano ~/.claude.json

# Replace "/absolute/path/to/gmail-mcp-agent" with actual path
# Get actual path:
cd /path/to/gmail-mcp-agent && pwd
```

**Step 3: Verify Configuration**

```bash
cd /path/to/gmail-mcp-agent
claude mcp list
# Expected output:
# gmail-extractor: python3 src/gmail_mcp_server.py - ✓ Connected
```

**Step 4: Set Up Memory System**

Memory files are already in place! Verify:

```bash
ls docs/memory-system/
# PRD.md  CLAUDE.md  PLANNING.md  TASKS.md
```

**Step 5: Start Using with Memory**

```bash
claude

# Activate Plan Mode: Press Shift+Tab twice
# Then type:
```

```
Please read PLANNING.md, CLAUDE.md, and TASKS.md to understand the project.
Then continue from where we left off.
```

Claude will load the memory and present a contextualized plan.

---

## Configuration File Reference

### Project-Level: `.mcp.json`

**Location:** Project root (`/path/to/gmail-mcp-agent/.mcp.json`)

**Content:**
```json
{
  "mcpServers": {
    "gmail-extractor": {
      "command": "python3",
      "args": ["src/gmail_mcp_server.py"],
      "env": {"PYTHONPATH": "src"},
      "transport": "stdio"
    }
  }
}
```

**Advantages:**
- Uses relative paths (portable)
- Can be committed to Git
- Team members get same config automatically

---

### Global Configuration: `~/.claude.json`

**Location:** Home directory (`~/.claude.json`)

**Content:**
```json
{
  "projects": {
    "/absolute/path/to/gmail-mcp-agent": {
      "mcpServers": {
        "gmail-extractor": {
          "type": "stdio",
          "command": "python3",
          "args": ["/absolute/path/to/gmail-mcp-agent/src/gmail_mcp_server.py"],
          "env": {"PYTHONPATH": "/absolute/path/to/gmail-mcp-agent/src"}
        }
      },
      "allowedTools": ["Bash(git:*)", "Edit", "Write"],
      "hasTrustDialogAccepted": true
    }
  }
}
```

**Advantages:**
- Centralized configuration for all projects
- Can set `allowedTools` and trust settings
- Survives project deletion

---

## Troubleshooting Configuration

### MCP Server Not Found

**Problem:** `claude mcp list` shows "No MCP servers configured"

**Solutions:**
1. Verify you're in the correct directory
2. Check `.mcp.json` exists: `ls -la .mcp.json`
3. Validate JSON syntax: `python3 -m json.tool .mcp.json`
4. Check `~/.claude.json` for project-specific config

### Connection Failed

**Problem:** `claude mcp list` shows "✗ Connection failed"

**Solutions:**
1. Test the server directly:
   ```bash
   python3 src/gmail_mcp_server.py
   # Should start without errors
   ```
2. Check dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Verify Python version:
   ```bash
   python3 --version  # Should be 3.8+
   ```
4. Check logs:
   ```bash
   claude --debug mcp
   ```

### Memory Files Not Loaded

**Problem:** Claude doesn't seem to remember project context

**Solutions:**
1. Verify files exist:
   ```bash
   ls docs/memory-system/
   ```
2. Explicitly load them:
   ```
   Please read docs/memory-system/CLAUDE.md, PLANNING.md, and TASKS.md
   ```
3. Check you're in project root:
   ```bash
   pwd  # Should show /path/to/gmail-mcp-agent
   ```
4. Use Plan Mode (Shift+Tab twice) for better memory loading

---

## Further Configuration Resources

- **Detailed Guide:** See `config-examples/CONFIGURATION_GUIDE.md` for comprehensive documentation
- **Memory System:** See `docs/memory-system/CLAUDE.md` for working instructions
- **Architecture:** See `docs/memory-system/PLANNING.md` for technical design
- **Book:** See `docs/Sub_Agent_Architecture_EN.md` for academic treatment

---

## Quick Reference

### Essential Commands

```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude-code

# Add MCP server (CLI method)
claude mcp add --transport stdio gmail-extractor python3 src/gmail_mcp_server.py

# List configured servers
claude mcp list

# Remove MCP server
claude mcp remove gmail-extractor

# Start Claude CLI
claude

# Start with memory loading
claude
# Then: Shift+Tab+Tab (Plan Mode)
# Then: "Please read CLAUDE.md, PLANNING.md, and TASKS.md..."
```

### Essential Files

```
~/.claude.json                  # Global configuration
.mcp.json                       # Project MCP configuration
docs/memory-system/CLAUDE.md    # Auto-read by Claude CLI
docs/memory-system/PLANNING.md  # Architecture
docs/memory-system/TASKS.md     # Task tracking
docs/memory-system/PRD.md       # Requirements
```

### Essential Keyboard Shortcuts

- **Shift+Tab+Tab:** Activate Plan Mode
- **@:** Add file to context (`@src/file.py`)
- **#:** Add instruction to CLAUDE.md
- **/:** Command mode (e.g., `/compact` to compress context)

---

