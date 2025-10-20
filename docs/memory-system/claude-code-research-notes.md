# Claude Code Research Notes

## Key Findings from Official Documentation

### CLAUDE.md File
- **Special file** that Claude automatically pulls into context when starting a conversation
- Can be placed in multiple locations:
  - Root of repo (most common): `CLAUDE.md` (checked into git) or `CLAUDE.local.md` (gitignored)
  - Parent directories (useful for monorepos)
  - Child directories (pulled on demand)
  - Home folder: `~/.claude/CLAUDE.md` (applies to all sessions)
- Should contain:
  - Common bash commands
  - Core files and utility functions
  - Code style guidelines
  - Testing instructions
  - Repository etiquette
  - Developer environment setup
  - Unexpected behaviors or warnings
- No required format - keep concise and human-readable
- Can be generated automatically with `/init` command
- Can be updated during session by pressing `#` key

### Plan Mode
- Activated by pressing **Shift+Tab twice**
- When activated, Claude will NOT edit files, run commands, or change anything until you approve the plan
- Useful for:
  - Brainstorming different solutions
  - Getting feedback on approaches
  - Complex code changes that need review
- Claude creates a plan first, you review, then approve execution

### Project Context
- Claude automatically pulls context from project files
- Use `@` symbol to manually add files as context
- Context gathering consumes time and tokens
- Can be optimized through environment tuning

### Permissions System
- Conservative by default - requests permission for system modifications
- Four ways to manage allowed tools:
  1. Select "Always allow" when prompted
  2. Use `/permissions` command
  3. Manually edit `.claude/settings.json` or `~/.claude.json`
  4. Use `--allowedTools` CLI flag

### Key Commands
- `/init` - Generate CLAUDE.md automatically
- `/permissions` - Manage allowed tools
- `#` - Add instruction to CLAUDE.md
- `@` - Add files to context manually

### Integration with GitHub
- Supports `gh` CLI for GitHub operations
- Can create issues, open PRs, read comments
- Falls back to GitHub API or MCP server

## Implications for Gmail MCP Agent Project

1. **Create comprehensive CLAUDE.md** with:
   - Project structure
   - Common commands (pytest, python3 src/gmail_mcp_server.py)
   - Security reminders (never commit .env)
   - Testing instructions
   - Integration steps

2. **Use Plan Mode** for:
   - Architectural changes
   - New feature planning
   - Complex refactoring

3. **Document in book**:
   - Explain CLAUDE.md philosophy
   - Show Plan Mode workflow
   - Demonstrate @ for context
   - Include permission management

4. **Memory System Files**:
   - PRD.md - Product requirements
   - CLAUDE.md - Working instructions
   - PLANNING.md - Architecture
   - TASKS.md - Task tracking

