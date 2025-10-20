# Claude CLI Configuration Guide
## Gmail MCP Agent

**Version:** 1.0  
**Last Updated:** October 20, 2025

---

## Overview

Claude CLI supports three methods for configuring MCP servers:

1. **Interactive CLI Commands** - Quick setup via `claude mcp add`
2. **Manual Configuration Files** - Direct editing of JSON configuration
3. **Project-Level Configuration** - Per-project `.mcp.json` files

This guide covers all three methods, with emphasis on the declarative, file-based approach that enables version control and team collaboration.

---

## Method 1: Interactive CLI (Quickest)

### Adding an MCP Server

```bash
cd /path/to/gmail-mcp-agent

# Add stdio MCP server
claude mcp add --transport stdio gmail-extractor python3 src/gmail_mcp_server.py
```

### Verification

```bash
# List configured servers
claude mcp list

# Expected output:
# gmail-extractor: python3 src/gmail_mcp_server.py - ✓ Connected
```

### Removing an MCP Server

```bash
claude mcp remove gmail-extractor
```

### Advantages
- ✅ Fast and simple
- ✅ Automatic validation
- ✅ Immediate feedback

### Disadvantages
- ❌ Not version-controlled
- ❌ Difficult to share with team
- ❌ Manual replication across machines

---

## Method 2: Global Configuration File (Recommended for Personal Use)

### Location

```
~/.claude.json
```

### Structure

The global configuration file stores settings for all projects. It is organized by project path:

```json
{
  "installMethod": "npm",
  "autoUpdates": true,
  "projects": {
    "/absolute/path/to/project1": {
      "mcpServers": { ... },
      "allowedTools": [ ... ]
    },
    "/absolute/path/to/project2": {
      "mcpServers": { ... }
    }
  }
}
```

### Gmail MCP Agent Configuration

Add this to the `projects` section:

```json
"/absolute/path/to/gmail-mcp-agent": {
  "allowedTools": [
    "Bash(git:*)",
    "Edit",
    "Write"
  ],
  "mcpServers": {
    "gmail-extractor": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/absolute/path/to/gmail-mcp-agent/src/gmail_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/gmail-mcp-agent/src"
      }
    }
  },
  "hasTrustDialogAccepted": true
}
```

### Important Notes

- **Absolute Paths:** Use full paths, not relative or `~` shortcuts
- **Environment Variables:** The `env` object sets environment variables for the MCP server process
- **Trust Dialog:** Set `hasTrustDialogAccepted: true` to skip the trust prompt (use only in trusted environments)

### Editing the File

```bash
# Open in your preferred editor
nano ~/.claude.json
# or
code ~/.claude.json
```

### Verification

```bash
cd /path/to/gmail-mcp-agent
claude mcp list
```

### Advantages
- ✅ Centralized configuration
- ✅ Survives project deletion
- ✅ Can configure multiple projects at once

### Disadvantages
- ❌ Not shared with team
- ❌ Requires manual replication across machines
- ❌ Not version-controlled

---

## Method 3: Project-Level Configuration (Recommended for Teams)

### Location

```
/path/to/gmail-mcp-agent/.mcp.json
```

### Structure

A simplified configuration file that lives in the project directory:

```json
{
  "mcpServers": {
    "gmail-extractor": {
      "command": "python3",
      "args": [
        "src/gmail_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "src"
      },
      "description": "Gmail MCP Agent - Extract and export emails",
      "transport": "stdio"
    }
  }
}
```

### Key Differences from Global Config

- **Relative Paths:** Paths are relative to the project root
- **Simpler Structure:** No `projects` wrapper
- **Version Controlled:** Can be committed to Git
- **Team Sharing:** Everyone on the team gets the same configuration

### Creating the File

```bash
cd /path/to/gmail-mcp-agent

# Copy the example
cp config-examples/mcp-project-config-example.json .mcp.json

# Or create manually
cat > .mcp.json << 'EOF'
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
EOF
```

### Verification

```bash
# Claude CLI automatically detects .mcp.json in the current directory
claude mcp list
```

### Advantages
- ✅ Version controlled (commit to Git)
- ✅ Team collaboration (everyone gets same config)
- ✅ Portable (works on any machine)
- ✅ Self-documenting (lives with the code)

### Disadvantages
- ❌ Requires approval on first use (security feature)
- ❌ Per-project only (not global)

---

## Configuration Hierarchy

Claude CLI loads configuration in this order (later sources override earlier ones):

1. **Global Config:** `~/.claude.json`
2. **Project Config:** `.mcp.json` in project root
3. **CLI Flags:** `--mcp-config` flag at runtime

### Example: Override at Runtime

```bash
claude --mcp-config custom-config.json
```

---

## Security Considerations

### Trust Dialogs

When Claude CLI encounters a new MCP server, it prompts for approval. This is a security feature to prevent malicious code execution.

**Options:**
- **Interactive Approval:** Review and approve each time (safest)
- **Persistent Approval:** Set `hasTrustDialogAccepted: true` in config
- **Bypass All:** Use `--dangerously-skip-permissions` flag (sandboxes only)

### Environment Variables

MCP servers can access environment variables. Be cautious about:
- API keys (use `.env` files, not hardcoded in config)
- Credentials (never commit to Git)
- Sensitive paths

### Allowed Tools

Restrict what Claude can do by setting `allowedTools`:

```json
"allowedTools": [
  "Bash(git:*)",      // Only git commands
  "Edit",             // File editing
  "Write"             // File writing
]
```

---

## Troubleshooting

### MCP Server Not Listed

**Problem:** `claude mcp list` shows "No MCP servers configured"

**Solutions:**
1. Check you're in the correct directory
2. Verify `.mcp.json` exists and is valid JSON
3. Check `~/.claude.json` for project-specific config
4. Run `claude mcp add` to add manually

### Connection Failed

**Problem:** `claude mcp list` shows "✗ Connection failed"

**Solutions:**
1. Verify Python is installed: `python3 --version`
2. Check the script path is correct
3. Test the script directly: `python3 src/gmail_mcp_server.py`
4. Check for missing dependencies: `pip3 install -r requirements.txt`
5. Review logs: `claude --debug mcp`

### Permission Denied

**Problem:** Claude CLI asks for permission repeatedly

**Solutions:**
1. Accept the trust dialog and select "Always allow"
2. Set `hasTrustDialogAccepted: true` in config
3. Use `--dangerously-skip-permissions` (trusted environments only)

### Environment Variables Not Loaded

**Problem:** MCP server can't find credentials

**Solutions:**
1. Check `.env` file exists in project root
2. Verify `python-dotenv` is installed
3. Add `PYTHONPATH` to `env` in MCP config
4. Test manually: `cd /path/to/project && python3 src/gmail_mcp_server.py`

---

## Best Practices

### For Individual Developers

1. **Use Global Config** for personal projects
2. **Keep Absolute Paths** in `~/.claude.json`
3. **Don't Commit** `~/.claude.json` to Git
4. **Document** setup steps in README

### For Teams

1. **Use Project Config** (`.mcp.json`)
2. **Commit to Git** so everyone benefits
3. **Use Relative Paths** for portability
4. **Document** in README and CLAUDE.md
5. **Test** on multiple machines before merging

### For Both

1. **Version Control** configuration examples
2. **Document** environment variable requirements
3. **Test** after every config change
4. **Backup** `~/.claude.json` regularly

---

## Example Workflow

### Initial Setup (One-Time)

```bash
# Clone the repository
git clone https://github.com/rmisegal/gmail-mcp-agent.git
cd gmail-mcp-agent

# Install dependencies
pip3 install -r requirements.txt

# Set up credentials
cp .env.example .env
# Edit .env and add your API keys

# Configure MCP server (choose one method)

# Method A: Interactive CLI
claude mcp add --transport stdio gmail-extractor python3 src/gmail_mcp_server.py

# Method B: Copy project config
cp config-examples/mcp-project-config-example.json .mcp.json

# Method C: Edit global config
nano ~/.claude.json
# Add configuration from config-examples/claude-global-config-example.json
```

### Verification

```bash
# List configured servers
claude mcp list

# Expected output:
# gmail-extractor: python3 src/gmail_mcp_server.py - ✓ Connected
```

### Daily Use

```bash
# Navigate to project
cd /path/to/gmail-mcp-agent

# Start Claude CLI
claude

# Use the agent
# (In Claude CLI)
# > Please use the gmail-extractor to fetch emails with label "Invoices" from last month
```

---

## Configuration Files in This Project

```
gmail-mcp-agent/
├── config-examples/
│   ├── CONFIGURATION_GUIDE.md                    # This file
│   ├── claude-global-config-example.json         # Global config template
│   └── mcp-project-config-example.json           # Project config template
├── .mcp.json                                     # Actual project config (optional)
└── .env                                          # Environment variables (git-ignored)
```

---

## Further Reading

- [Claude CLI Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Gmail MCP Agent README](../README.md)
- [CLAUDE.md Working Instructions](../docs/memory-system/CLAUDE.md)

---

**Questions or Issues?**

- Check the [Troubleshooting](#troubleshooting) section above
- Review the [README](../README.md)
- Open an issue on [GitHub](https://github.com/rmisegal/gmail-mcp-agent/issues)

