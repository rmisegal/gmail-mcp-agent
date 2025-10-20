# Product Requirements Document (PRD)
## Gmail MCP Agent: Intelligent Email Automation Sub-Agent

**Author:** Dr. Yoram Segal  
**Version:** 1.0  
**Last Updated:** October 20, 2025  
**Status:** Completed & Deployed

---

## Executive Summary

The Gmail MCP Agent is a specialized AI sub-agent that provides secure, programmatic access to Gmail data through the Model Context Protocol (MCP). It enables AI assistants like Claude CLI to extract, process, and export email data based on natural language commands, with full support for multilingual content including Hebrew.

---

## Problem Statement

### Current Challenges

1. **Manual Email Management:** Users spend significant time manually searching, filtering, and organizing emails
2. **Data Extraction Complexity:** Extracting structured data from emails requires technical knowledge of Gmail API
3. **Encoding Issues:** Non-ASCII characters (Hebrew, Arabic, Chinese) often become garbled in exports
4. **Security Concerns:** Direct API access requires careful credential management
5. **Integration Gaps:** No standardized way for AI assistants to access personal email data

### Target Users

- **Researchers:** Need to extract and analyze email correspondence for studies
- **Business Professionals:** Require automated invoice/receipt collection
- **Data Analysts:** Want to process email data for insights
- **Developers:** Building AI-powered email automation workflows

---

## Product Vision

Create a secure, intelligent bridge between AI assistants and Gmail that:
- Understands natural language queries
- Respects user privacy through OAuth 2.0
- Handles multilingual content flawlessly
- Integrates seamlessly with Claude CLI
- Provides structured, analysis-ready output

---

## Core Features

### 1. Secure Authentication
- **OAuth 2.0 Flow:** User explicitly grants permissions
- **Token Management:** Automatic refresh and secure storage
- **Minimal Scope:** Read-only access (`gmail.readonly`)
- **Credential Isolation:** Secrets stored in `.env`, never in code

### 2. Intelligent Email Search
- **Label Filtering:** Search by Gmail labels (e.g., "Invoices", "Research_Data")
- **Date Range Queries:** Filter by start and end dates (YYYY-MM-DD format)
- **Flexible Queries:** Support for natural language via Gemini AI
- **Batch Processing:** Handle up to 100+ emails per request

### 3. Data Export
- **CSV Format:** Universal compatibility with Excel, Google Sheets
- **UTF-8 BOM Encoding:** Ensures Hebrew/Unicode characters display correctly
- **Structured Fields:** Date, From, To, Subject, Body (truncated)
- **Auto-Naming:** Timestamp-based filenames for easy organization

### 4. MCP Integration
- **Standard Protocol:** Implements MCP server specification
- **Tool Discovery:** Claude CLI can automatically detect capabilities
- **Async Communication:** Non-blocking operations via stdio
- **Error Handling:** Graceful failures with informative messages

### 5. Developer Experience
- **Comprehensive Tests:** 15+ pytest test cases covering all functionality
- **Clear Documentation:** README, integration guide, code comments
- **Example Configurations:** Ready-to-use templates for Claude CLI
- **Extensibility:** Modular design for adding new features

---

## Technical Requirements

### Platform
- **Language:** Python 3.8+
- **Framework:** MCP Server (stdio-based)
- **APIs:** Gmail API v1, Gemini AI API
- **Deployment:** Local execution, user's machine

### Dependencies
```
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.100.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
mcp>=0.1.0
pytest>=7.4.0
```

### Security
- Environment variable-based credential management
- `.gitignore` protection for sensitive files
- OAuth 2.0 with explicit user consent
- No hardcoded secrets in codebase

### Performance
- Response time: < 5 seconds for 100 emails
- Memory usage: < 200MB during operation
- Concurrent requests: 1 (single-user design)

---

## User Stories

### Story 1: Research Data Collection
**As a** researcher  
**I want to** extract all emails with the label "Research_Data" from the last quarter  
**So that** I can analyze correspondence patterns for my study

**Acceptance Criteria:**
- User can specify label and date range
- All matching emails are exported to CSV
- Hebrew content in emails is preserved correctly
- Output includes sender, date, subject, and body preview

### Story 2: Invoice Management
**As a** small business owner  
**I want to** automatically collect all invoices from my email  
**So that** I can import them into my accounting software

**Acceptance Criteria:**
- User can filter by "Invoices" label
- CSV export is Excel-compatible
- Filenames include timestamps for versioning
- Process completes in under 30 seconds

### Story 3: AI-Assisted Email Analysis
**As a** Claude CLI user  
**I want to** ask Claude to "find emails from my accountant last month"  
**So that** Claude can extract and summarize them for me

**Acceptance Criteria:**
- Natural language command is understood
- Agent automatically determines date range
- Results are returned in structured format
- Claude can chain this with other agents

---

## Success Metrics

### Functionality
- ✅ 100% test coverage for core functions
- ✅ Zero encoding errors for Hebrew/Unicode
- ✅ < 1% failure rate for OAuth authentication
- ✅ Support for 10+ Gmail labels simultaneously

### Usability
- ✅ Setup time < 15 minutes for new users
- ✅ Documentation clarity score > 4.5/5
- ✅ Zero-configuration CSV export

### Integration
- ✅ Compatible with Claude CLI v1.x
- ✅ Discoverable via MCP protocol
- ✅ Works with Gemini 2.0+ models

---

## Out of Scope (V1)

- ❌ Email sending/composing
- ❌ Email deletion/modification
- ❌ Attachment download
- ❌ Multi-user/server deployment
- ❌ Real-time email monitoring
- ❌ GUI interface

---

## Future Enhancements (V2+)

1. **Attachment Handling:** Download and process attachments
2. **Advanced NLP:** Sentiment analysis, entity extraction
3. **Multi-Account Support:** Manage multiple Gmail accounts
4. **Real-Time Sync:** Monitor inbox for new emails
5. **Additional Formats:** JSON, XML, Parquet export options
6. **Cloud Deployment:** Hosted MCP server option

---

## Risk Assessment

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| OAuth token expiry | Medium | Low | Automatic refresh logic |
| API rate limiting | Low | Medium | Batch processing, caching |
| Encoding errors | Low | High | UTF-8 BOM, comprehensive tests |
| Gemini API downtime | Low | Medium | Fallback to explicit queries |

### Security Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Credential exposure | Medium | Critical | `.gitignore`, env vars, docs |
| Unauthorized access | Low | Critical | OAuth 2.0, read-only scope |
| Token theft | Low | High | Secure storage, user education |

---

## Timeline & Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Core server implementation | Oct 15, 2025 | ✅ Complete |
| Authentication flow | Oct 16, 2025 | ✅ Complete |
| CSV export with UTF-8 BOM | Oct 17, 2025 | ✅ Complete |
| MCP protocol integration | Oct 18, 2025 | ✅ Complete |
| Test suite (15+ tests) | Oct 19, 2025 | ✅ Complete |
| Documentation & README | Oct 20, 2025 | ✅ Complete |
| GitHub repository creation | Oct 20, 2025 | ✅ Complete |

---

## Stakeholders

- **Primary Developer:** Dr. Yoram Segal
- **Target Users:** Researchers, business professionals, developers
- **Integration Partner:** Anthropic (Claude CLI)
- **API Providers:** Google (Gmail API, Gemini AI)

---

## Appendix

### Related Documents
- [CLAUDE.MD](CLAUDE.md) - Claude CLI working instructions
- [PLANNING.MD](PLANNING.md) - Architecture and technical design
- [TASKS.MD](TASKS.md) - Task tracking and completion log
- [README.md](../README.md) - User-facing documentation
- [CLAUDE_CLI_INTEGRATION.md](CLAUDE_CLI_INTEGRATION.md) - Integration guide

### References
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [OAuth 2.0 Best Practices](https://oauth.net/2/)

