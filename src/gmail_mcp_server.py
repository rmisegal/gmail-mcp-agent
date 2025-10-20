#!/usr/bin/env python3
"""
Gmail MCP Server - Model Context Protocol Server for Gmail Integration
Author: Dr. Yoram Segal
License: MIT

This server provides Gmail access through MCP protocol, enabling AI agents
to extract and process email data with proper authentication and security.
"""

import os
import json
import logging
import base64
import webbrowser
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import google.generativeai as genai
from dotenv import load_dotenv

# MCP Server imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailMCPServer:
    """MCP Server for Gmail integration with Gemini AI assistance."""
    
    def __init__(self):
        """Initialize the Gmail MCP Server."""
        self.credentials_path = self._find_credentials_path()
        self.token_path = os.getenv('GMAIL_TOKEN_PATH', './private/token.json')
        self.csv_output_dir = os.getenv('CSV_OUTPUT_DIR', './csv')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Ensure output directory exists
        Path(self.csv_output_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini AI initialized successfully")
        else:
            logger.warning("GEMINI_API_KEY not found - AI features disabled")
            self.gemini_model = None
        
        # Gmail service will be initialized on first use
        self.gmail_service = None
        
        logger.info("Gmail MCP Server initialized")
    
    def _find_credentials_path(self) -> str:
        """Find the Gmail credentials JSON file."""
        creds_path = os.getenv('GMAIL_CREDENTIALS_PATH', './private/client_secret_*.json')
        
        # If wildcard, find the actual file
        if '*' in creds_path:
            private_dir = Path('./private')
            json_files = list(private_dir.glob('client_secret_*.json'))
            if json_files:
                return str(json_files[0])
            else:
                raise FileNotFoundError(
                    "No Gmail credentials file found in ./private/\n"
                    "Please download credentials from Google Cloud Console"
                )
        
        return creds_path
    
    def authenticate(self) -> Credentials:
        """
        Authenticate with Gmail API using OAuth 2.0.

        Returns:
            Credentials object for Gmail API access
        """
        creds = None

        # Load existing token if available
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
                logger.info("Loaded existing credentials from token.json")
            except Exception as e:
                logger.warning(f"Failed to load token: {e}")

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("Refreshed expired credentials")
                except Exception as e:
                    logger.warning(f"Failed to refresh token: {e}")
                    creds = None

            if not creds:
                # Configure browser for the environment
                self._configure_browser()

                # Run OAuth flow with console fallback for better reliability
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )

                try:
                    # Try to run with local server first (automatic)
                    creds = flow.run_local_server(port=0)
                    logger.info("Completed OAuth authentication flow via automatic browser")
                except Exception as e:
                    logger.warning(f"Automatic browser flow failed: {e}")
                    logger.info("Falling back to console-based authentication")

                    # Fallback to console-based flow
                    creds = flow.run_console()
                    logger.info("Completed OAuth authentication flow via console")

            # Save credentials for future use
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
                logger.info(f"Saved credentials to {self.token_path}")

        return creds

    def _is_wsl(self) -> bool:
        """Check if running in Windows Subsystem for Linux."""
        try:
            with open('/proc/version', 'r') as f:
                version_info = f.read().lower()
                return 'microsoft' in version_info or 'wsl' in version_info
        except:
            return False

    def _configure_browser(self):
        """Configure browser based on the environment (WSL or native Linux)."""
        try:
            if self._is_wsl():
                logger.info("WSL detected, configuring Windows browser integration")
                self._configure_wsl_browser()
            else:
                logger.info("Native Linux detected, configuring Linux browser")
                self._configure_linux_browser()
        except Exception as e:
            logger.warning(f"Failed to configure browser: {e}")
            # Universal fallback
            logger.info("Using fallback browser configuration")
            self._configure_fallback_browser()

    def _configure_wsl_browser(self):
        """Configure browser for WSL environment to use Windows browser."""
        try:
            # Create a custom browser class that uses Windows PowerShell to open URLs
            class WindowsChromeBrowser:
                def open(self, url, new=0, autoraise=True):
                    try:
                        # Use PowerShell to open URL in default Windows browser
                        import subprocess
                        subprocess.run(['powershell.exe', '-Command', f'Start-Process "{url}"'],
                                     check=True, capture_output=True)
                        return True
                    except Exception as e:
                        logger.error(f"Failed to open URL with PowerShell: {e}")
                        return False

                def open_new(self, url):
                    return self.open(url, new=1)

                def open_new_tab(self, url):
                    return self.open(url, new=2)

            # Register our custom browser
            webbrowser.register('windows-chrome', WindowsChromeBrowser, WindowsChromeBrowser())
            os.environ['BROWSER'] = 'windows-chrome'
            logger.info("Configured to use Windows browser via PowerShell")

        except Exception as e:
            logger.warning(f"Failed to configure Windows browser: {e}")
            raise

    def _configure_linux_browser(self):
        """Configure browser for native Linux environment."""
        try:
            # Try common Linux browsers in order of preference
            linux_browsers = [
                'firefox',
                'google-chrome',
                'chrome',
                'chromium',
                'chromium-browser',
                'opera',
                'edge'
            ]

            configured = False
            for browser in linux_browsers:
                try:
                    # Check if browser exists and is executable
                    subprocess.run(['which', browser], check=True, capture_output=True)
                    os.environ['BROWSER'] = browser
                    logger.info(f"Configured to use Linux browser: {browser}")
                    configured = True
                    break
                except subprocess.CalledProcessError:
                    continue

            if not configured:
                # Try using xdg-open as fallback
                try:
                    subprocess.run(['which', 'xdg-open'], check=True, capture_output=True)
                    os.environ['BROWSER'] = 'xdg-open'
                    logger.info("Configured to use xdg-open for Linux browser")
                    configured = True
                except subprocess.CalledProcessError:
                    pass

            if not configured:
                raise Exception("No suitable Linux browser found")

        except Exception as e:
            logger.warning(f"Failed to configure Linux browser: {e}")
            raise

    def _configure_fallback_browser(self):
        """Configure universal fallback browser that works in most environments."""
        try:
            if self._is_wsl():
                # WSL fallback: try multiple methods
                fallback_methods = [
                    'powershell.exe -Command "Start-Process \\"%s\\""',
                    '/mnt/c/Windows/System32/cmd.exe /c start %s',
                    'explorer.exe %s'
                ]
            else:
                # Linux fallback
                fallback_methods = [
                    'xdg-open %s',
                    'firefox %s',
                    'google-chrome %s'
                ]

            for method in fallback_methods:
                try:
                    # Test if the method works by trying to parse it
                    if '%s' in method:
                        os.environ['BROWSER'] = method
                        logger.info(f"Configured fallback browser method: {method}")
                        return
                except:
                    continue

            # Last resort: set a simple method that might work
            os.environ['BROWSER'] = 'echo "Please open manually: %s"'
            logger.warning("Using manual fallback - you'll need to open the URL manually")

        except Exception as e:
            logger.warning(f"Failed to configure fallback browser: {e}")

    def _configure_windows_chrome(self):
        """Legacy method - now delegates to _configure_browser()."""
        self._configure_browser()
    
    def get_gmail_service(self):
        """Get or create Gmail API service."""
        if not self.gmail_service:
            creds = self.authenticate()
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API service initialized")
        
        return self.gmail_service
    
    def search_emails(
        self,
        label: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search for emails matching criteria.
        
        Args:
            label: Gmail label to filter by
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            max_results: Maximum number of emails to retrieve
        
        Returns:
            List of email dictionaries with metadata and content
        """
        service = self.get_gmail_service()
        
        # Build search query
        query_parts = []
        
        if label:
            query_parts.append(f'label:{label}')
        
        if start_date:
            query_parts.append(f'after:{start_date}')
        
        if end_date:
            query_parts.append(f'before:{end_date}')
        
        query = ' '.join(query_parts) if query_parts else None
        
        logger.info(f"Searching emails with query: {query}")
        
        try:
            # Search for messages
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            logger.info(f"Found {len(messages)} messages")
            
            # Fetch full message details
            emails = []
            for msg in messages:
                try:
                    message = service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='full'
                    ).execute()
                    
                    email_data = self._parse_message(message)
                    emails.append(email_data)
                    
                except HttpError as e:
                    logger.error(f"Error fetching message {msg['id']}: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(emails)} emails")
            return emails
            
        except HttpError as e:
            logger.error(f"Gmail API error: {e}")
            raise
    
    def _parse_message(self, message: Dict) -> Dict[str, Any]:
        """
        Parse Gmail message into structured format.
        
        Args:
            message: Raw Gmail message object
        
        Returns:
            Parsed email dictionary
        """
        headers = {h['name']: h['value'] for h in message['payload']['headers']}
        
        # Extract body
        body = self._get_message_body(message['payload'])
        
        return {
            'id': message['id'],
            'thread_id': message['threadId'],
            'date': headers.get('Date', ''),
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'body': body[:500] if body else '',  # Limit body length
            'labels': message.get('labelIds', [])
        }
    
    def _get_message_body(self, payload: Dict) -> str:
        """Extract message body from payload."""
        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        else:
            # Simple message
            data = payload['body'].get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        return ''
    
    def export_to_csv(
        self,
        emails: List[Dict[str, Any]],
        output_filename: str
    ) -> str:
        """
        Export emails to CSV with UTF-8 BOM encoding for Hebrew support.
        
        Args:
            emails: List of email dictionaries
            output_filename: Output CSV filename
        
        Returns:
            Full path to created CSV file
        """
        import csv
        
        output_path = os.path.join(self.csv_output_dir, output_filename)
        
        # Ensure .csv extension
        if not output_path.endswith('.csv'):
            output_path += '.csv'
        
        logger.info(f"Exporting {len(emails)} emails to {output_path}")
        
        # Write CSV with UTF-8 BOM for Excel compatibility
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['date', 'from', 'to', 'subject', 'body'],
                quoting=csv.QUOTE_ALL
            )
            
            writer.writeheader()
            
            for email in emails:
                writer.writerow({
                    'date': email['date'],
                    'from': email['from'],
                    'to': email['to'],
                    'subject': email['subject'],
                    'body': email['body']
                })
        
        logger.info(f"CSV export completed: {output_path}")
        return output_path
    
    def search_and_export(
        self,
        label: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        output_filename: Optional[str] = None,
        max_results: int = 100
    ) -> Dict[str, Any]:
        """
        Search emails and export to CSV in one operation.
        
        Args:
            label: Gmail label to filter by
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            output_filename: Output CSV filename (auto-generated if not provided)
            max_results: Maximum number of emails to retrieve
        
        Returns:
            Dictionary with results summary
        """
        # Generate filename if not provided
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            label_part = f"{label}_" if label else ""
            output_filename = f"{label_part}emails_{timestamp}.csv"
        
        # Search emails
        emails = self.search_emails(
            label=label,
            start_date=start_date,
            end_date=end_date,
            max_results=max_results
        )
        
        if not emails:
            return {
                'success': True,
                'count': 0,
                'message': 'No emails found matching criteria',
                'output_file': None
            }
        
        # Export to CSV
        output_path = self.export_to_csv(emails, output_filename)
        
        return {
            'success': True,
            'count': len(emails),
            'message': f'Successfully exported {len(emails)} emails',
            'output_file': output_path
        }


# MCP Server setup
app = Server("gmail-mcp-server")
gmail_server = GmailMCPServer()


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="search_and_export_emails",
            description=(
                "Search Gmail for emails matching criteria (label, date range) "
                "and export results to CSV with full Hebrew/Unicode support. "
                "Perfect for data extraction and analysis."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "label": {
                        "type": "string",
                        "description": "Gmail label to filter by (e.g., 'Research_Data')"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format"
                    },
                    "output_filename": {
                        "type": "string",
                        "description": "Output CSV filename (auto-generated if not provided)"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of emails to retrieve (default: 100)"
                    }
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls."""
    if name == "search_and_export_emails":
        try:
            result = gmail_server.search_and_export(
                label=arguments.get('label'),
                start_date=arguments.get('start_date'),
                end_date=arguments.get('end_date'),
                output_filename=arguments.get('output_filename'),
                max_results=arguments.get('max_results', 100)
            )
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
            
        except Exception as e:
            logger.error(f"Tool execution error: {e}", exc_info=True)
            return [TextContent(
                type="text",
                text=json.dumps({
                    'success': False,
                    'error': str(e)
                }, indent=2)
            )]
    
    return [TextContent(
        type="text",
        text=json.dumps({'error': f'Unknown tool: {name}'})
    )]


async def main():
    """Run the MCP server."""
    logger.info("Starting Gmail MCP Server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

