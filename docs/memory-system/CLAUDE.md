# Claude Working Instructions
## Gmail MCP Agent Project

**Project:** Gmail MCP Agent - Intelligent Email Automation Sub-Agent  
**Version:** 1.0  
**Last Updated:** October 20, 2025

---

## Project Overview

You are working on the Gmail MCP Agent, a specialized AI sub-agent that provides secure, programmatic access to Gmail data through the Model Context Protocol (MCP). This agent enables AI assistants like Claude CLI to extract, process, and export email data based on natural language commands.

---

## Core Principles

### 1. Always Start Here
At the beginning of **every new conversation**, you must:
1. Read `PLANNING.md` to understand the architecture
2. Check `TASKS.md` to see what's been completed
3. Review `PRD.md` for product requirements
4. Understand the current project state before taking action

### 2. Task Management
- **Before starting work:** Check `TASKS.md` for the next incomplete task
- **After completing a task:** Mark it as `✅ [DONE - YYYY-MM-DD]`
- **When discovering new tasks:** Add them to `TASKS.md` under the appropriate milestone
- **Never duplicate work:** If a task is marked done, don't redo it

### 3. Code Quality Standards
- **Security First:** Never hardcode API keys or credentials
- **UTF-8 BOM:** All CSV exports must use UTF-8 with BOM for Hebrew support
- **Type Hints:** All Python functions must have type annotations
- **Docstrings:** Every function needs a clear docstring
- **Error Handling:** Use try/except with informative logging
- **Testing:** Every new feature needs corresponding pytest tests

### 4. File Organization
```
gmail-mcp-agent/
├── docs/
│   ├── memory-system/      # Project management files
│   │   ├── PRD.md
│   │   ├── CLAUDE.md       # This file
│   │   ├── PLANNING.md
│   │   └── TASKS.md
│   ├── Sub_Agent_Architecture_EN.md  # Main book
│   └── CLAUDE_CLI_INTEGRATION.md     # Integration guide
├── src/
│   ├── gmail_mcp_server.py  # Main server
│   ├── fetch_emails.py      # Standalone script
│   └── verify_encoding.py   # UTF-8 verification
├── tests/
│   └── test_gmail_mcp_server.py
├── examples/
│   └── gmail-extractor-agent.md
├── config/
│   └── claude-cli-config.json
├── private/                 # Git-ignored
│   ├── client_secret_*.json
│   └── token.json
├── csv/                     # Output directory
├── .env                     # Git-ignored
├── .env.example
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Coding Guidelines

### Python Style
- Follow PEP 8 conventions
- Use descriptive variable names
- Maximum line length: 100 characters
- Use f-strings for formatting

### Security
- All credentials in `.env` or environment variables
- Never commit `.env`, `private/`, or `csv/` to Git
- Use OAuth 2.0 for Gmail authentication
- Minimal API scopes (read-only when possible)

### Testing
- Run `pytest -v` before committing
- All tests must pass
- Add tests for new features
- Mock external API calls

### Documentation
- Update README.md for user-facing changes
- Update PLANNING.md for architectural changes
- Add code comments for complex logic
- Keep examples/ directory current

---

## Common Tasks

### Adding a New Feature
1. Check if it's in `TASKS.md`, if not, add it
2. Review `PLANNING.md` for architectural fit
3. Implement with tests
4. Update documentation
5. Mark task as done in `TASKS.md`

### Fixing a Bug
1. Write a failing test that reproduces the bug
2. Fix the bug
3. Verify the test now passes
4. Update `TASKS.md` with fix details

### Updating Documentation
1. Identify which files need updates (README, book, guides)
2. Maintain consistent style (academic for book, practical for README)
3. Include code examples where helpful
4. Update table of contents if needed

---

## Integration Points

### Gmail API
- Uses `google-api-python-client`
- OAuth 2.0 flow via `google-auth-oauthlib`
- Scope: `https://www.googleapis.com/auth/gmail.readonly`
- Token stored in `private/token.json`

### Gemini AI
- Uses `google-generativeai` library
- API key from environment variable `GEMINI_API_KEY`
- Model: `gemini-pro`
- Used for future NLP enhancements

### MCP Protocol
- Uses `mcp` library
- Communication via stdio (standard input/output)
- Async operations with `asyncio`
- Tool definition in `@app.list_tools()`

### Claude CLI
- Agent definition in `examples/gmail-extractor-agent.md`
- Configuration in `~/.config/claude-cli/config.json`
- Invoked via `/agent use gmail-extractor ...`

---

## Session Management

### Starting a New Session
Use this prompt:
```
Please read PLANNING.md, CLAUDE.md, and TASKS.md to understand the project. 
Then continue from where we left off.
```

### Ending a Session
Before closing, run:
```
Please add a session summary to CLAUDE.md summarizing what we accomplished.
Update TASKS.md with completed items and any new discoveries.
```

### Clearing Context
When context is getting full:
1. Use `/compact` command
2. Or manually: "Please summarize our progress and update CLAUDE.md"
3. Ensure all important decisions are captured in PLANNING.md

---

## Session Summaries

### Session 1 - October 20, 2025
**Completed:**
- ✅ Created complete Gmail MCP server implementation
- ✅ Implemented OAuth 2.0 authentication flow
- ✅ Built email search with label and date filtering
- ✅ Created CSV export with UTF-8 BOM encoding
- ✅ Wrote comprehensive test suite (15 tests, all passing)
- ✅ Generated full documentation (README, integration guide, book)
- ✅ Created GitHub repository: https://github.com/rmisegal/gmail-mcp-agent
- ✅ Established memory system (PRD, CLAUDE.md, PLANNING.md, TASKS.md)

**Key Decisions:**
- Used Python 3.8+ for broad compatibility
- Chose MCP protocol for Claude CLI integration
- Implemented UTF-8 BOM for Excel/Hebrew compatibility
- Stored credentials in `.env` for security
- Wrote book in academic style (Professor Yuval Noah Harari)

**Next Steps:**
- Monitor for user feedback
- Consider V2 features (attachments, multi-account)
- Expand test coverage for edge cases

---

## Troubleshooting

### Common Issues

**"Module not found" errors:**
- Ensure virtual environment is activated: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

**OAuth authentication fails:**
- Delete `private/token.json` and re-authenticate
- Verify `client_secret_*.json` exists in `private/`
- Check Gmail API is enabled in Google Cloud Console

**Hebrew characters garbled:**
- Verify CSV uses UTF-8 BOM encoding
- Check `encoding='utf-8-sig'` in file write operations
- Test with `src/verify_encoding.py`

**Tests failing:**
- Run `pytest -v` to see detailed errors
- Check that mocks are properly configured
- Ensure test environment variables are set

---

## Contact & Resources

- **Repository:** https://github.com/rmisegal/gmail-mcp-agent
- **Gmail API Docs:** https://developers.google.com/gmail/api
- **MCP Specification:** https://modelcontextprotocol.io
- **Claude CLI Docs:** https://docs.anthropic.com/claude/docs/claude-cli

---

## Remember

> "The best code is code that doesn't need to be written twice. Check TASKS.md, follow PLANNING.md, and update documentation as you go. Every session should leave the project better than you found it."

**Always read this file at the start of every conversation.**

