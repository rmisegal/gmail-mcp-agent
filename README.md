

> # Gmail MCP Agent: An Intelligent Sub-Agent for Email Automation
> 
> **Author:** Dr. Yoram Segal
> 
> **License:** MIT
> 
> ---
> 
> ## Overview
> 
> The Gmail MCP Agent is a sophisticated, self-contained sub-agent designed to bridge the gap between large language models and personal email data. It functions as a Model-Context-Policy (MCP) server that provides a secure, programmatic interface to a user's Gmail account. By leveraging the cognitive power of Google's Gemini AI, this agent can understand natural language commands, search for emails based on complex criteria, and export the results into a structured CSV format, with full support for Hebrew and other Unicode characters.
> 
> This project serves as a practical and academic reference for building specialized AI agents that can be orchestrated within larger systems like Claude Code. It demonstrates a robust architecture for handling authentication, processing data, and ensuring security, all while providing a powerful tool for email automation and data extraction.
> 
> ### Table of Contents
> 1.  [Architecture](#architecture)
> 2.  [Key Features](#key-features)
> 3.  [Getting Started](#getting-started)
>     *   [Prerequisites](#prerequisites)
>     *   [Installation](#installation)
> 4.  [Configuration and Authentication](#configuration-and-authentication)
>     *   [1. Gmail API Credentials](#1-gmail-api-credentials)
>     *   [2. Gemini API Key](#2-gemini-api-key)
>     *   [3. Environment Setup](#3-environment-setup)
>     *   [4. First-Time Authentication (OAuth 2.0)](#4-first-time-authentication-oauth-20)
> 5.  [Usage](#usage)
>     *   [Running the Server](#running-the-server)
>     *   [Integration with Claude CLI](#integration-with-claude-cli)
> 6.  [Running the Tests](#running-the-tests)
> 7.  [Security Considerations](#security-considerations)
> 8.  [License](#license)
> 
> ---


> ## Architecture
> 
> The agent is built as a Python-based server that adheres to the Model-Context-Policy (MCP) protocol. This allows it to be seamlessly integrated as a "tool" by higher-level AI assistants.
> 
> The core components are:
> 
> *   **MCP Server (Flask & MCP Library):** A lightweight web server that exposes the agent's capabilities (e.g., `search_and_export_emails`) through a standardized protocol.
> *   **Gmail API Client:** Securely interacts with the Gmail API using OAuth 2.0 to perform actions on behalf of the user. It handles token generation, refresh, and storage.
> *   **Gemini AI Model:** Used as the cognitive engine to parse natural language, although the current implementation primarily uses it for future extension possibilities. The core logic for query building is handled explicitly.
> *   **Authentication Manager:** Manages the OAuth 2.0 flow for Gmail and the secure handling of API keys for Gemini.
> *   **CSV Exporter:** Formats the extracted email data into a CSV file, ensuring correct encoding (UTF-8 with BOM) for compatibility with spreadsheet software like Microsoft Excel, especially for languages like Hebrew.
> 
> ## Key Features
> 
> *   **Secure Authentication:** Uses the official Google OAuth 2.0 flow to ensure the user grants explicit, revocable access to their Gmail account.
> *   **Natural Language Queries (via Claude CLI):** Allows users to make requests in plain English, such as "find emails with the label 'invoices' from the last 30 days."
> *   **Advanced Search:** Supports filtering by Gmail labels, start dates, and end dates.
> *   **Structured Data Export:** Automatically exports search results to a clean, well-formatted CSV file.
> *   **Full Unicode & Hebrew Support:** Correctly handles and encodes non-ASCII characters in both email content and CSV output, preventing garbled text.
> *   **Comprehensive Testing:** Includes a full suite of `pytest` tests to ensure reliability and correctness.
> *   **Standalone & Integratable:** Can be run as a standalone server or integrated as a sub-agent in platforms like Claude Code.
> 
> ---


> ## Getting Started
> 
> Follow these steps to get the Gmail MCP Agent up and running.
> 
> ### Prerequisites
> 
> *   Python 3.8+
> *   `pip` and `virtualenv`
> *   A Google Account with Gmail enabled
> *   Access to the Google Cloud Console
> *   A Gemini API Key from Google AI Studio
> 
> ### Installation
> 
> 1.  **Clone the repository:**
> 
>     ```bash
>     git clone <repository-url>
>     cd gmail-mcp-agent
>     ```
> 
> 2.  **Create and activate a virtual environment:**
> 
>     ```bash
>     python3 -m venv venv
>     source venv/bin/activate
>     ```
> 
> 3.  **Install the required dependencies:**
> 
>     ```bash
>     pip install -r requirements.txt
>     ```
> 
> ---


> ## Configuration and Authentication
> 
> This agent requires secure credentials to access Google services. Follow these steps carefully.
> 
> ### 1. Gmail API Credentials
> 
> You need to authorize the application to access Gmail data by creating an OAuth 2.0 Client ID.
> 
> 1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
> 2.  Create a new project or select an existing one.
> 3.  Navigate to **APIs & Services > Enabled APIs & Services** and click **+ ENABLE APIS AND SERVICES**. Search for "Gmail API" and enable it.
> 4.  Go to **APIs & Services > Credentials**.
> 5.  Click **+ CREATE CREDENTIALS** and select **OAuth client ID**.
> 6.  Choose **Desktop app** as the application type.
> 7.  Give it a name (e.g., "Gmail MCP Agent").
> 8.  Click **Create**. A window will appear with your Client ID and Client Secret. Click **DOWNLOAD JSON**.
> 9.  **Crucially**, rename the downloaded file to `client_secret.json` and move it into the `private/` directory within this project.
> 
> ### 2. Gemini API Key
> 
> The agent uses the Gemini model for its cognitive abilities.
> 
> 1.  Go to [Google AI Studio](https://aistudio.google.com/apikey).
> 2.  Click **Create API key**.
> 3.  Copy the generated API key.
> 
> ### 3. Environment Setup
> 
> The project uses a `.env` file to manage secret keys securely. **This file should never be committed to version control.**
> 
> 1.  Make a copy of the example file:
> 
>     ```bash
>     cp .env.example .env
>     ```
> 
> 2.  Open the `.env` file and paste your Gemini API key:
> 
>     ```env
>     # .env
>     GEMINI_API_KEY="your_gemini_api_key_here"
>     ```
> 
> ### 4. First-Time Authentication (OAuth 2.0)
> 
> The first time you run the server, it will need to get your permission to access your Gmail account.
> 
> 1.  Run the server (see [Usage](#usage) below).
> 2.  A message will appear in your console with a URL.
> 3.  Copy this URL and paste it into your web browser.
> 4.  Log in to the Google account you want the agent to access.
> 5.  You will be shown a consent screen asking for permission to "View your email messages and settings." Click **Allow**.
> 6.  If you see a warning that "Google hasn't verified this app," click **Advanced** and then **Go to (unsafe)**. This is expected for local desktop applications.
> 7.  After you approve, the authentication flow will complete, and the server will create a `private/token.json` file. This file will be used for all future authentications, so you will only need to do this once.
> 
> ---


> ## Usage
> 
> ### Running the Server
> 
> To start the agent, run the main server script from the project root:
> 
> ```bash
> python3 src/gmail_mcp_server.py
> ```
> 
> The server will initialize, and if it's the first run, it will guide you through the authentication process. Once running, it will listen for requests from a connected client, such as the Claude CLI.
> 
> ### Integration with Claude CLI
> 
> This agent is designed to be used as a sub-agent within Claude CLI/Code. Follow these detailed steps to integrate it.
> 
> #### Step 1: Install Claude CLI
> 
> **For macOS/Linux:**
> ```bash
> npm install -g @anthropic-ai/claude-cli
> # Or via Homebrew (macOS)
> brew install anthropic-ai/tap/claude-cli
> ```
> 
> **For Windows:**
> ```powershell
> npm install -g @anthropic-ai/claude-cli
> ```
> 
> **Verify installation:**
> ```bash
> claude --version
> ```
> 
> #### Step 2: Configure Claude CLI for MCP
> 
> 1. **Create or edit the Claude CLI configuration file:**
> 
>    ```bash
>    mkdir -p ~/.config/claude-cli
>    nano ~/.config/claude-cli/config.json
>    ```
> 
> 2. **Add the MCP server configuration:**
> 
>    ```json
>    {
>      "apiKey": "your_anthropic_api_key",
>      "mcpServers": {
>        "gmail-extractor": {
>          "command": "python3",
>          "args": [
>            "/absolute/path/to/gmail-mcp-agent/src/gmail_mcp_server.py"
>          ]
>        }
>      }
>    }
>    ```
> 
>    **Important:** Replace `/absolute/path/to/gmail-mcp-agent/` with the actual full path to your project directory.
> 
>    **To get the absolute path:**
>    ```bash
>    cd ~/gmail-mcp-agent && pwd
>    ```
> 
> 3. **Alternative: Use the provided configuration template:**
> 
>    ```bash
>    cp config/claude-cli-config.json ~/.config/claude-cli/config.json
>    # Then edit the file to replace placeholder paths
>    ```
> 
> #### Step 3: Create the Agent Definition
> 
> 1. **Create the agents directory:**
> 
>    ```bash
>    mkdir -p ~/.config/claude-cli/agents
>    ```
> 
> 2. **Copy the agent definition file:**
> 
>    ```bash
>    cp examples/gmail-extractor-agent.md ~/.config/claude-cli/agents/
>    ```
> 
>    Or create it manually:
> 
>    ```bash
>    nano ~/.config/claude-cli/agents/gmail-extractor.md
>    ```
> 
>    And paste the contents from `examples/gmail-extractor-agent.md`.
> 
> #### Step 4: Verify Agent Registration
> 
> ```bash
> claude agents list
> ```
> 
> You should see `gmail-extractor` in the list of available agents.
> 
> #### Step 5: Use the Agent
> 
> Start a Claude CLI session:
> 
> ```bash
> claude
> ```
> 
> Then invoke the agent with natural language commands:
> 
> **Example 1: Extract by label**
> ```
> /agent use gmail-extractor to fetch emails with the label "work-reports" from the last 7 days
> ```
> 
> **Example 2: Extract by date range**
> ```
> /agent use gmail-extractor to fetch emails from 2025-09-01 to 2025-10-20
> ```
> 
> **Example 3: Extract with custom filename**
> ```
> /agent use gmail-extractor to fetch emails with the label "Invoices" and save to invoices_q3.csv
> ```
> 
> **Example Output:**
> 
> ```json
> {
>   "success": true,
>   "count": 15,
>   "message": "Successfully exported 15 emails",
>   "output_file": "csv/work-reports_emails_20251020_153000.csv"
> }
> ```
> 
> #### Troubleshooting
> 
> **Issue: "Agent not found"**
> - Verify the agent definition file exists: `ls ~/.config/claude-cli/agents/gmail-extractor.md`
> - Check file permissions: `chmod 644 ~/.config/claude-cli/agents/gmail-extractor.md`
> - Restart Claude CLI
> 
> **Issue: "MCP server failed to start"**
> - Verify Python path: `which python3`
> - Test the server manually: `python3 src/gmail_mcp_server.py`
> - Check that all environment variables are set in `.env`
> 
> **Issue: "Authentication failed"**
> - Delete old token: `rm private/token.json`
> - Run the server manually to complete OAuth flow
> - Verify Gmail API credentials exist: `ls private/client_secret_*.json`
> 
> **For complete integration guide, see:** [docs/CLAUDE_CLI_INTEGRATION.md](docs/CLAUDE_CLI_INTEGRATION.md)
> 
> ---


> ## Running the Tests
> 
> A comprehensive test suite is included to ensure the agent functions correctly. The tests cover authentication logic, email parsing, CSV generation, and Unicode character handling.
> 
> To run the tests, execute `pytest` from the root of the project:
> 
> ```bash
> pytest -v
> ```
> 
> All tests should pass, confirming that your environment is set up correctly and the agent is behaving as expected.
> 
> ---
> 
> ## Security Considerations
> 
> *   **API Keys:** Your `GEMINI_API_KEY` is highly sensitive. The `.env` file is included in `.gitignore` to prevent it from being accidentally committed to version control. **Never share this file or commit it to a public repository.**
> *   **OAuth Tokens:** The `private/token.json` file contains the OAuth 2.0 token that grants access to your Gmail account. It is also included in `.gitignore`. Treat this file like a password.
> *   **Scopes:** The agent requests only `gmail.readonly` scope. This means it can read your emails but **cannot** send, delete, or modify them, minimizing potential risks.
> 
> ---
> 
> ## License
> 
> This project is licensed under the MIT License. See the `LICENSE` file for details.

