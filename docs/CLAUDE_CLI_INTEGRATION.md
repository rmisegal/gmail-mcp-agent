# Complete Guide: Integrating Gmail MCP Agent with Claude CLI

**Author:** Dr. Yoram Segal

**Last Updated:** October 20, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Install Claude CLI](#step-1-install-claude-cli)
4. [Step 2: Configure the MCP Server](#step-2-configure-the-mcp-server)
5. [Step 3: Create the Agent Definition](#step-3-create-the-agent-definition)
6. [Step 4: Register the Agent with Claude CLI](#step-4-register-the-agent-with-claude-cli)
7. [Step 5: Test the Integration](#step-5-test-the-integration)
8. [Usage Examples](#usage-examples)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides a complete, step-by-step walkthrough for integrating the Gmail MCP Agent with Anthropic's Claude CLI. By the end of this guide, you will have a fully functional sub-agent that can be invoked from within Claude Code to extract and process your Gmail data.

The integration follows the **Model Context Protocol (MCP)** standard, which allows AI assistants to discover and use external tools through a standardized interface.

---

## Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.8+ installed
- ✅ The Gmail MCP Agent installed and configured (see main README.md)
- ✅ Valid Gmail API credentials in `private/client_secret_*.json`
- ✅ Gemini API key configured in `.env`
- ✅ Claude CLI installed (we'll cover this in Step 1)

---

## Step 1: Install Claude CLI

### For macOS/Linux:

```bash
# Install via npm (Node.js required)
npm install -g @anthropic-ai/claude-cli

# Or install via Homebrew (macOS)
brew install anthropic-ai/tap/claude-cli
```

### For Windows:

```powershell
# Install via npm
npm install -g @anthropic-ai/claude-cli
```

### Verify Installation:

```bash
claude --version
```

You should see output like: `claude-cli version 1.x.x`

---

## Step 2: Configure the MCP Server

The MCP server needs to be running for Claude CLI to communicate with it. We'll configure it to run as a background service.

### 2.1 Create a Server Configuration File

Create a file named `mcp-server-config.json` in the project root:

```json
{
  "mcpServers": {
    "gmail-extractor": {
      "command": "python3",
      "args": [
        "/absolute/path/to/gmail-mcp-agent/src/gmail_mcp_server.py"
      ],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key_here",
        "GMAIL_CREDENTIALS_PATH": "/absolute/path/to/gmail-mcp-agent/private/client_secret_*.json",
        "GMAIL_TOKEN_PATH": "/absolute/path/to/gmail-mcp-agent/private/token.json",
        "CSV_OUTPUT_DIR": "/absolute/path/to/gmail-mcp-agent/csv"
      }
    }
  }
}
```

**Important:** Replace all `/absolute/path/to/gmail-mcp-agent/` with the actual full path to your project directory.

### 2.2 Set Up Environment Variables

Alternatively, you can use the `.env` file approach (recommended for security):

```bash
# In your project root
cp .env.example .env
nano .env  # Edit with your actual keys
```

---

## Step 3: Create the Agent Definition

Agent definitions tell Claude CLI what your agent can do and how to communicate with it.

### 3.1 Create the Agents Directory

```bash
mkdir -p ~/.config/claude-cli/agents
```

### 3.2 Create the Agent Definition File

Create a file named `gmail-extractor.md` in the agents directory:

```bash
nano ~/.config/claude-cli/agents/gmail-extractor.md
```

### 3.3 Add the Following Content:

```markdown
# Gmail Extractor Agent

## Description
An intelligent agent that extracts emails from Gmail based on labels and date ranges, exporting them to CSV format with full Unicode support.

## Capabilities
- Search emails by Gmail label
- Filter emails by date range (start and end dates)
- Export results to CSV with UTF-8 BOM encoding
- Full support for Hebrew and other Unicode characters
- Automatic filename generation with timestamps

## MCP Server
- **Server Name:** gmail-extractor
- **Protocol:** stdio
- **Command:** python3 /absolute/path/to/gmail-mcp-agent/src/gmail_mcp_server.py

## Tools

### search_and_export_emails

**Description:** Search Gmail for emails matching criteria and export to CSV.

**Parameters:**
- `label` (string, optional): Gmail label to filter by (e.g., "Research_Data", "Invoices")
- `start_date` (string, optional): Start date in YYYY-MM-DD format (e.g., "2025-09-01")
- `end_date` (string, optional): End date in YYYY-MM-DD format (e.g., "2025-10-20")
- `output_filename` (string, optional): Custom output filename (auto-generated if not provided)
- `max_results` (integer, optional): Maximum number of emails to retrieve (default: 100)

**Returns:**
```json
{
  "success": true,
  "count": 15,
  "message": "Successfully exported 15 emails",
  "output_file": "csv/Research_Data_emails_20251020_153000.csv"
}
```

## Usage Examples

### Example 1: Extract emails by label
```
/agent use gmail-extractor to fetch emails with the label "Research_Data"
```

### Example 2: Extract emails by date range
```
/agent use gmail-extractor to fetch emails from the last 30 days
```

### Example 3: Extract emails with specific criteria
```
/agent use gmail-extractor to fetch emails with the label "Invoices" from 2025-09-01 to 2025-10-20
```

## Notes
- First run will require OAuth 2.0 authentication via browser
- Output files are saved in the `csv/` directory
- CSV files use UTF-8 BOM encoding for Excel compatibility
```

**Remember:** Replace `/absolute/path/to/gmail-mcp-agent/` with your actual path.

---

## Step 4: Register the Agent with Claude CLI

### 4.1 Configure Claude CLI to Use MCP Servers

Edit the Claude CLI configuration file:

```bash
nano ~/.config/claude-cli/config.json
```

Add or update the `mcpServers` section:

```json
{
  "apiKey": "your_anthropic_api_key",
  "mcpServers": {
    "gmail-extractor": {
      "command": "python3",
      "args": [
        "/absolute/path/to/gmail-mcp-agent/src/gmail_mcp_server.py"
      ]
    }
  }
}
```

### 4.2 Verify Agent Registration

```bash
claude agents list
```

You should see `gmail-extractor` in the list of available agents.

---

## Step 5: Test the Integration

### 5.1 Start a Claude CLI Session

```bash
claude
```

### 5.2 Invoke the Agent

Try a simple command:

```
/agent use gmail-extractor to fetch emails with the label "INBOX" from the last 7 days
```

### 5.3 Expected Output

You should see:
1. The agent initializing
2. OAuth authentication (first time only)
3. Email search progress
4. A JSON response with the results:

```json
{
  "success": true,
  "count": 12,
  "message": "Successfully exported 12 emails",
  "output_file": "csv/INBOX_emails_20251020_154530.csv"
}
```

---

## Usage Examples

### Example 1: Research Data Extraction

**Command:**
```
/agent use gmail-extractor to fetch all emails with the label "Research_Data" from the last quarter
```

**What happens:**
- Agent calculates the date range (last 90 days)
- Searches Gmail for emails with the "Research_Data" label
- Exports to `csv/Research_Data_emails_[timestamp].csv`

### Example 2: Invoice Collection

**Command:**
```
/agent use gmail-extractor to fetch emails with the label "Invoices" from 2025-01-01 to 2025-10-20
```

**What happens:**
- Agent searches for emails in the "Invoices" label
- Filters by the specified date range
- Exports to CSV with automatic filename

### Example 3: Recent Communications

**Command:**
```
/agent use gmail-extractor to fetch the last 50 emails from yesterday
```

**What happens:**
- Agent interprets "yesterday" as the previous day's date
- Retrieves up to 50 emails
- Exports with timestamp-based filename

---

## Troubleshooting

### Issue 1: "Agent not found"

**Solution:**
- Verify the agent definition file exists: `ls ~/.config/claude-cli/agents/gmail-extractor.md`
- Check the file has correct permissions: `chmod 644 ~/.config/claude-cli/agents/gmail-extractor.md`
- Restart Claude CLI

### Issue 2: "MCP server failed to start"

**Solution:**
- Verify Python path: `which python3`
- Check the absolute path in the configuration is correct
- Test the server manually: `python3 /path/to/gmail_mcp_server.py`
- Check environment variables are set correctly

### Issue 3: "Authentication failed"

**Solution:**
- Verify Gmail API credentials exist: `ls private/client_secret_*.json`
- Delete old token and re-authenticate: `rm private/token.json`
- Run the server manually to complete OAuth flow

### Issue 4: "No emails found"

**Solution:**
- Verify the label name is correct (case-sensitive)
- Check the date range is valid
- Test with a broader search (e.g., just "INBOX")

### Issue 5: "Hebrew characters are garbled"

**Solution:**
- This should not happen with our UTF-8 BOM encoding
- If it does, verify the CSV is opened with UTF-8 encoding
- In Excel: Data → Get Data → From Text/CSV → File Origin: UTF-8

---

## Advanced Configuration

### Running Multiple Agents

You can define multiple agents in the same configuration:

```json
{
  "mcpServers": {
    "gmail-extractor": {
      "command": "python3",
      "args": ["/path/to/gmail_mcp_server.py"]
    },
    "calendar-agent": {
      "command": "python3",
      "args": ["/path/to/calendar_agent.py"]
    }
  }
}
```

### Custom Output Directory

Modify the `CSV_OUTPUT_DIR` environment variable:

```json
"env": {
  "CSV_OUTPUT_DIR": "/Users/yourname/Documents/EmailExports"
}
```

---

## Security Best Practices

1. **Never commit credentials:** Ensure `.env` and `private/` are in `.gitignore`
2. **Use environment variables:** Store API keys in `.env`, not in configuration files
3. **Limit OAuth scopes:** The agent only requests `gmail.readonly` scope
4. **Rotate tokens regularly:** Delete `private/token.json` periodically to force re-authentication
5. **Monitor access:** Check Google Account activity for unexpected API usage

---

## Next Steps

- Explore chaining multiple agents together for complex workflows
- Customize the agent's behavior by modifying `gmail_mcp_server.py`
- Build additional MCP servers for other Google services (Calendar, Drive, etc.)
- Contribute improvements back to the repository

---

**For more information, see:**
- Main README: [README.md](../README.md)
- Sub-Agent Architecture Book: [Sub_Agent_Architecture_EN.md](Sub_Agent_Architecture_EN.md)
- GitHub Repository: https://github.com/rmisegal/gmail-mcp-agent

