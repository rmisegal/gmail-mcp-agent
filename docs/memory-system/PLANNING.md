# Project Planning & Architecture
## Gmail MCP Agent

**Version:** 1.0  
**Last Updated:** October 20, 2025  
**Status:** Production Ready

---

## Project Vision

The Gmail MCP Agent serves as a bridge between AI assistants (specifically Claude CLI) and Gmail, enabling secure, intelligent email data extraction through natural language commands. This project demonstrates the practical implementation of a specialized sub-agent within a multi-agent architecture.

---

## Technology Stack

### Core Technologies
- **Language:** Python 3.8+
- **Framework:** MCP Server (Model Context Protocol)
- **Communication:** stdio (standard input/output) for async operations
- **Testing:** pytest with comprehensive test coverage

### External APIs
- **Gmail API v1:** Email data access via OAuth 2.0
- **Gemini AI API:** Natural language processing and future enhancements
- **GitHub API:** Version control integration (via `gh` CLI)

### Key Libraries
```python
google-auth-oauthlib>=1.2.0      # OAuth 2.0 authentication
google-auth-httplib2>=0.2.0      # HTTP transport for Google APIs
google-api-python-client>=2.100.0 # Gmail API client
google-generativeai>=0.3.0       # Gemini AI integration
python-dotenv>=1.0.0             # Environment variable management
mcp>=0.1.0                       # Model Context Protocol server
pytest>=7.4.0                    # Testing framework
```

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                        Claude CLI                            │
│                    (Orchestrator/Conductor)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ MCP Protocol (stdio)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Gmail MCP Server                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Authentication Manager                              │  │
│  │  - OAuth 2.0 Flow                                    │  │
│  │  - Token Management (refresh, storage)               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Email Search Engine                                 │  │
│  │  - Label filtering                                   │  │
│  │  - Date range queries                                │  │
│  │  - Query builder                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Data Processor                                      │  │
│  │  - Email parsing                                     │  │
│  │  - UTF-8 encoding                                    │  │
│  │  - Content extraction                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CSV Exporter                                        │  │
│  │  - UTF-8 BOM encoding                                │  │
│  │  - Structured formatting                             │  │
│  │  - Filename generation                               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTPS
                         │
┌────────────────────────▼────────────────────────────────────┐
│                     Gmail API                                │
│                  (Google Cloud)                              │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Command:** User issues natural language command via Claude CLI
   ```
   /agent use gmail-extractor to fetch emails with label "Research_Data" from last month
   ```

2. **Claude Parsing:** Claude CLI interprets command and identifies gmail-extractor agent

3. **MCP Request:** Claude sends structured request to MCP server via stdio
   ```json
   {
     "tool": "search_and_export_emails",
     "arguments": {
       "label": "Research_Data",
       "start_date": "2025-09-20",
       "end_date": "2025-10-20"
     }
   }
   ```

4. **Authentication:** Server verifies OAuth token, refreshes if needed

5. **Gmail Query:** Server constructs and executes Gmail API query
   ```
   label:Research_Data after:2025/09/20 before:2025/10/20
   ```

6. **Data Processing:** Server parses emails, extracts metadata and content

7. **CSV Export:** Server generates CSV with UTF-8 BOM encoding

8. **Response:** Server returns success status and file path to Claude

9. **User Notification:** Claude presents results to user

---

## File Structure

```
gmail-mcp-agent/
├── docs/
│   ├── memory-system/              # Project management (4-file framework)
│   │   ├── PRD.md                  # Product Requirements Document
│   │   ├── CLAUDE.md               # Claude working instructions
│   │   ├── PLANNING.md             # This file - architecture
│   │   └── TASKS.md                # Task tracking
│   ├── Sub_Agent_Architecture_EN.md # Main book (academic style)
│   └── CLAUDE_CLI_INTEGRATION.md    # Integration guide
│
├── src/
│   ├── gmail_mcp_server.py         # Main MCP server implementation
│   ├── fetch_emails.py             # Standalone email extraction script
│   └── verify_encoding.py          # UTF-8 encoding verification tool
│
├── tests/
│   └── test_gmail_mcp_server.py    # Comprehensive test suite (15 tests)
│
├── examples/
│   └── gmail-extractor-agent.md    # Claude CLI agent definition
│
├── config/
│   └── claude-cli-config.json      # Template for Claude CLI configuration
│
├── private/                         # Git-ignored
│   ├── client_secret_*.json        # Gmail OAuth credentials
│   └── token.json                  # OAuth access token
│
├── csv/                             # Output directory (Git-ignored)
│   └── *.csv                       # Exported email data
│
├── .env                             # Environment variables (Git-ignored)
├── .env.example                     # Template for .env
├── .gitignore                       # Git exclusions
├── requirements.txt                 # Python dependencies
├── LICENSE                          # MIT License
└── README.md                        # User documentation
```

---

## Security Architecture

### Credential Management

**Three-Tier Security Model:**

1. **Gmail OAuth 2.0 Credentials**
   - Type: `client_secret_*.json` file
   - Location: `private/` directory (gitignored)
   - Purpose: User authorization for Gmail access
   - Scope: `gmail.readonly` (read-only)
   - Flow: User explicitly grants permission via browser

2. **Gemini API Key**
   - Type: String token
   - Location: `.env` file (gitignored)
   - Purpose: AI model access
   - Protection: Never hardcoded, loaded via `python-dotenv`

3. **GitHub PAT (Personal Access Token)**
   - Type: String token
   - Location: Environment variable or `gh` CLI config
   - Purpose: Repository operations
   - Scope: Minimal required permissions

### Security Principles

- **Separation of Concerns:** Credentials never in source code
- **Least Privilege:** Minimal API scopes requested
- **Explicit Consent:** OAuth 2.0 requires user approval
- **Token Refresh:** Automatic refresh of expired tokens
- **Audit Trail:** Logging of all API operations

---

## Integration Points

### Claude CLI Integration

**Configuration Location:** `~/.config/claude-cli/config.json`

```json
{
  "mcpServers": {
    "gmail-extractor": {
      "command": "python3",
      "args": ["/absolute/path/to/gmail-mcp-agent/src/gmail_mcp_server.py"]
    }
  }
}
```

**Agent Definition Location:** `~/.config/claude-cli/agents/gmail-extractor.md`

**Invocation Pattern:**
```
/agent use gmail-extractor to [natural language command]
```

### MCP Protocol

**Communication Method:** stdio (asynchronous)

**Tool Definition:**
```python
@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="search_and_export_emails",
            description="Search Gmail and export to CSV",
            inputSchema={...}
        )
    ]
```

**Tool Execution:**
```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    # Execute tool and return results
```

---

## Data Handling

### Email Parsing

**Input:** Gmail API message object (JSON)

**Processing Steps:**
1. Extract headers (From, To, Subject, Date)
2. Decode base64-encoded body
3. Handle multipart messages
4. Truncate body to 500 characters
5. Preserve Unicode characters (UTF-8)

**Output:** Structured dictionary
```python
{
    'id': 'msg123',
    'thread_id': 'thread123',
    'date': 'Mon, 20 Oct 2025 10:00:00 +0000',
    'from': 'sender@example.com',
    'to': 'recipient@example.com',
    'subject': 'Email Subject',
    'body': 'Email body preview...',
    'labels': ['INBOX', 'Research_Data']
}
```

### CSV Export Format

**Encoding:** UTF-8 with BOM (Byte Order Mark)
- **Why BOM:** Ensures Excel correctly detects UTF-8 encoding
- **Critical for:** Hebrew, Arabic, Chinese, and other non-ASCII characters

**Fields:**
- `date`: Full timestamp from email headers
- `from`: Sender email address
- `to`: Recipient email address
- `subject`: Email subject line
- `body`: First 500 characters of email body

**Filename Convention:**
```
[label]_emails_[YYYYMMDD]_[HHMMSS].csv
```

Example: `Research_Data_emails_20251020_153045.csv`

---

## Testing Strategy

### Test Coverage

**15 Test Cases Covering:**
- Server initialization
- Credential discovery
- OAuth authentication (valid, expired, refresh)
- Email parsing (simple, multipart, Hebrew)
- CSV export (creation, encoding, BOM)
- Search query building
- Error handling
- Unicode preservation

### Test Execution

```bash
# Run all tests
pytest -v

# Run specific test class
pytest tests/test_gmail_mcp_server.py::TestGmailMCPServer -v

# Run with coverage
pytest --cov=src --cov-report=html
```

### Mocking Strategy

- **Gmail API:** Mocked to avoid real API calls
- **OAuth Flow:** Mocked to simulate authentication
- **File System:** Uses `tmp_path` fixture for isolation
- **Gemini API:** Mocked (not yet fully utilized)

---

## Performance Considerations

### Optimization Targets

- **Response Time:** < 5 seconds for 100 emails
- **Memory Usage:** < 200MB during operation
- **Token Efficiency:** Minimal context in prompts
- **API Rate Limits:** Batch processing, respect Gmail quotas

### Scalability Limits

**Current Design (V1):**
- Single-user, local execution
- Synchronous email processing
- No caching layer
- Limited to 100 emails per request (configurable)

**Future Enhancements (V2+):**
- Multi-user support
- Async/parallel processing
- Redis caching
- Pagination for large result sets

---

## Deployment Model

### Current (V1): Local Execution

**Requirements:**
- Python 3.8+ installed locally
- User's machine with terminal access
- Internet connection for API calls

**Advantages:**
- Simple setup
- No server infrastructure
- User controls credentials
- Zero hosting costs

**Limitations:**
- Single-user only
- Requires local Python environment
- No remote access

### Future (V2): Hosted Service

**Potential Architecture:**
- Docker containerization
- Cloud deployment (AWS/GCP)
- Multi-tenant support
- API gateway for access control

---

## Error Handling

### Error Categories

1. **Authentication Errors**
   - Missing credentials file
   - Expired OAuth token
   - Invalid API key
   - Solution: Clear error messages, re-authentication flow

2. **API Errors**
   - Gmail API rate limiting
   - Network timeouts
   - Invalid queries
   - Solution: Retry logic, graceful degradation

3. **Data Processing Errors**
   - Malformed email content
   - Encoding issues
   - Empty result sets
   - Solution: Robust parsing, fallback encodings

4. **File System Errors**
   - Permission denied
   - Disk full
   - Invalid paths
   - Solution: Validation, informative error messages

### Logging Strategy

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Log Levels:**
- **INFO:** Normal operations (authentication, search, export)
- **WARNING:** Recoverable issues (token refresh, empty results)
- **ERROR:** Failures (API errors, file errors)
- **DEBUG:** Detailed debugging (disabled in production)

---

## Future Roadmap

### V1.1 (Immediate)
- [ ] Attachment download support
- [ ] Additional export formats (JSON, XML)
- [ ] Enhanced Gemini integration for NLP
- [ ] Performance profiling and optimization

### V2.0 (Next Quarter)
- [ ] Multi-account support
- [ ] Real-time email monitoring
- [ ] Advanced filtering (regex, sentiment)
- [ ] Web dashboard UI
- [ ] Cloud deployment option

### V3.0 (Long-term)
- [ ] Integration with other Google services (Calendar, Drive)
- [ ] Machine learning for email categorization
- [ ] Collaborative features (shared agents)
- [ ] Enterprise SSO support

---

## Dependencies & Compatibility

### Python Version
- **Minimum:** 3.8
- **Recommended:** 3.10+
- **Tested:** 3.11

### Operating Systems
- **Linux:** Fully supported (Ubuntu 22.04+)
- **macOS:** Fully supported (10.15+)
- **Windows:** Supported (Windows 10+, PowerShell)

### Claude CLI Version
- **Minimum:** 1.0
- **Recommended:** Latest stable
- **Compatibility:** MCP protocol standard

---

## Maintenance & Updates

### Regular Tasks
- **Weekly:** Monitor for security updates in dependencies
- **Monthly:** Review and update documentation
- **Quarterly:** Refactor based on user feedback
- **Annually:** Major version upgrades

### Dependency Updates
```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade google-api-python-client

# Update all packages (carefully)
pip install --upgrade -r requirements.txt
```

### Breaking Changes Policy
- Semantic versioning (MAJOR.MINOR.PATCH)
- Deprecation warnings before removal
- Migration guides for major versions
- Backward compatibility within major versions

---

## Related Documents

- [PRD.md](PRD.md) - Product requirements and success metrics
- [CLAUDE.md](CLAUDE.md) - Working instructions for Claude
- [TASKS.md](TASKS.md) - Task tracking and completion log
- [README.md](../../README.md) - User-facing documentation
- [CLAUDE_CLI_INTEGRATION.md](../CLAUDE_CLI_INTEGRATION.md) - Integration guide

---

**Last Architecture Review:** October 20, 2025  
**Next Review Due:** November 20, 2025  
**Architecture Owner:** Dr. Yoram Segal

