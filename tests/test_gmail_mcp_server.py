#!/usr/bin/env python3
"""
Test Suite for Gmail MCP Server
Comprehensive tests for authentication, email extraction, and CSV export.
"""

import os
import sys
import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from gmail_mcp_server import GmailMCPServer


class TestGmailMCPServer:
    """Test cases for GmailMCPServer class."""
    
    @pytest.fixture
    def server(self):
        """Create a test server instance."""
        with patch.dict(os.environ, {
            'GEMINI_API_KEY': 'test_key',
            'GMAIL_CREDENTIALS_PATH': './private/test_credentials.json',
            'GMAIL_TOKEN_PATH': './private/test_token.json',
            'CSV_OUTPUT_DIR': './test_csv'
        }):
            with patch.object(GmailMCPServer, '_find_credentials_path', return_value='./private/test_credentials.json'):
                server = GmailMCPServer()
                return server
    
    def test_initialization(self, server):
        """Test server initialization."""
        assert server is not None
        assert server.csv_output_dir == './test_csv'
        assert server.gemini_api_key == 'test_key'
    
    def test_find_credentials_path_with_wildcard(self):
        """Test finding credentials file with wildcard."""
        with patch('pathlib.Path.glob') as mock_glob:
            mock_glob.return_value = [Path('./private/client_secret_123.json')]
            
            with patch.dict(os.environ, {'GMAIL_CREDENTIALS_PATH': './private/client_secret_*.json'}):
                server = GmailMCPServer()
                assert 'client_secret_123.json' in server.credentials_path
    
    def test_find_credentials_path_not_found(self):
        """Test error when credentials file not found."""
        with patch('pathlib.Path.glob', return_value=[]):
            with patch.dict(os.environ, {'GMAIL_CREDENTIALS_PATH': './private/client_secret_*.json'}):
                with pytest.raises(FileNotFoundError):
                    GmailMCPServer()
    
    def test_parse_message_simple(self, server):
        """Test parsing a simple email message."""
        message = {
            'id': 'msg123',
            'threadId': 'thread123',
            'payload': {
                'headers': [
                    {'name': 'Date', 'value': 'Mon, 20 Oct 2025 10:00:00 +0000'},
                    {'name': 'From', 'value': 'sender@example.com'},
                    {'name': 'To', 'value': 'recipient@example.com'},
                    {'name': 'Subject', 'value': 'Test Email'}
                ],
                'body': {
                    'data': 'VGVzdCBib2R5'  # Base64 for "Test body"
                }
            },
            'labelIds': ['INBOX']
        }
        
        parsed = server._parse_message(message)
        
        assert parsed['id'] == 'msg123'
        assert parsed['thread_id'] == 'thread123'
        assert parsed['subject'] == 'Test Email'
        assert parsed['from'] == 'sender@example.com'
        assert parsed['to'] == 'recipient@example.com'
        assert 'Test body' in parsed['body']
    
    def test_parse_message_with_hebrew(self, server):
        """Test parsing email with Hebrew content."""
        import base64
        
        hebrew_text = "שלום עולם"
        encoded = base64.urlsafe_b64encode(hebrew_text.encode('utf-8')).decode('ascii')
        
        message = {
            'id': 'msg456',
            'threadId': 'thread456',
            'payload': {
                'headers': [
                    {'name': 'Date', 'value': 'Mon, 20 Oct 2025 10:00:00 +0000'},
                    {'name': 'From', 'value': 'sender@example.com'},
                    {'name': 'To', 'value': 'recipient@example.com'},
                    {'name': 'Subject', 'value': 'בדיקה'}
                ],
                'body': {
                    'data': encoded
                }
            },
            'labelIds': ['INBOX']
        }
        
        parsed = server._parse_message(message)
        
        assert parsed['subject'] == 'בדיקה'
        assert hebrew_text in parsed['body']
    
    def test_export_to_csv_creates_file(self, server, tmp_path):
        """Test CSV export creates file with correct encoding."""
        server.csv_output_dir = str(tmp_path)
        
        emails = [
            {
                'date': 'Mon, 20 Oct 2025 10:00:00 +0000',
                'from': 'sender@example.com',
                'to': 'recipient@example.com',
                'subject': 'Test Email',
                'body': 'Test body content'
            }
        ]
        
        output_path = server.export_to_csv(emails, 'test_output.csv')
        
        assert os.path.exists(output_path)
        
        # Check UTF-8 BOM
        with open(output_path, 'rb') as f:
            bom = f.read(3)
            assert bom == b'\xef\xbb\xbf'  # UTF-8 BOM
    
    def test_export_to_csv_with_hebrew(self, server, tmp_path):
        """Test CSV export with Hebrew characters."""
        server.csv_output_dir = str(tmp_path)
        
        emails = [
            {
                'date': 'Mon, 20 Oct 2025 10:00:00 +0000',
                'from': 'sender@example.com',
                'to': 'recipient@example.com',
                'subject': 'בדיקה עברית',
                'body': 'תוכן בעברית'
            }
        ]
        
        output_path = server.export_to_csv(emails, 'hebrew_test.csv')
        
        # Read and verify Hebrew content
        with open(output_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            assert 'בדיקה עברית' in content
            assert 'תוכן בעברית' in content
    
    def test_search_and_export_no_results(self, server):
        """Test search and export with no results."""
        with patch.object(server, 'search_emails', return_value=[]):
            result = server.search_and_export(label='NonExistent')
            
            assert result['success'] is True
            assert result['count'] == 0
            assert result['output_file'] is None
            assert 'No emails found' in result['message']
    
    def test_search_and_export_with_results(self, server, tmp_path):
        """Test search and export with results."""
        server.csv_output_dir = str(tmp_path)
        
        mock_emails = [
            {
                'date': 'Mon, 20 Oct 2025 10:00:00 +0000',
                'from': 'sender@example.com',
                'to': 'recipient@example.com',
                'subject': 'Test',
                'body': 'Body'
            }
        ]
        
        with patch.object(server, 'search_emails', return_value=mock_emails):
            result = server.search_and_export(
                label='TestLabel',
                output_filename='test.csv'
            )
            
            assert result['success'] is True
            assert result['count'] == 1
            assert result['output_file'] is not None
            assert os.path.exists(result['output_file'])
    
    def test_auto_filename_generation(self, server, tmp_path):
        """Test automatic filename generation."""
        server.csv_output_dir = str(tmp_path)
        
        mock_emails = [
            {
                'date': 'Mon, 20 Oct 2025 10:00:00 +0000',
                'from': 'sender@example.com',
                'to': 'recipient@example.com',
                'subject': 'Test',
                'body': 'Body'
            }
        ]
        
        with patch.object(server, 'search_emails', return_value=mock_emails):
            result = server.search_and_export(label='Research_Data')
            
            assert result['success'] is True
            assert 'Research_Data' in result['output_file']
            assert '.csv' in result['output_file']


class TestAuthentication:
    """Test cases for Gmail authentication."""
    
    def test_authenticate_with_existing_valid_token(self):
        """Test authentication with existing valid token."""
        mock_creds = Mock()
        mock_creds.valid = True
        
        with patch('os.path.exists', return_value=True):
            with patch('google.oauth2.credentials.Credentials.from_authorized_user_file', return_value=mock_creds):
                with patch.dict(os.environ, {'GMAIL_CREDENTIALS_PATH': './test.json'}):
                    with patch.object(GmailMCPServer, '_find_credentials_path', return_value='./test.json'):
                        server = GmailMCPServer()
                        creds = server.authenticate()
                        
                        assert creds.valid is True
    
    def test_authenticate_with_expired_token(self):
        """Test authentication with expired token that needs refresh."""
        mock_creds = Mock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = 'refresh_token'
        
        with patch('os.path.exists', return_value=True):
            with patch('google.oauth2.credentials.Credentials.from_authorized_user_file', return_value=mock_creds):
                with patch.object(mock_creds, 'refresh'):
                    mock_creds.valid = True  # After refresh
                    
                    with patch.dict(os.environ, {'GMAIL_CREDENTIALS_PATH': './test.json'}):
                        with patch.object(GmailMCPServer, '_find_credentials_path', return_value='./test.json'):
                            server = GmailMCPServer()
                            
                            with patch('builtins.open', create=True):
                                creds = server.authenticate()
                                assert creds.valid is True


class TestEmailSearch:
    """Test cases for email search functionality."""
    
    def test_search_query_building(self, tmp_path):
        """Test search query construction."""
        with patch.dict(os.environ, {'GMAIL_CREDENTIALS_PATH': './test.json'}):
            with patch.object(GmailMCPServer, '_find_credentials_path', return_value='./test.json'):
                server = GmailMCPServer()
                
                mock_service = Mock()
                mock_list = Mock()
                mock_list.execute.return_value = {'messages': []}
                mock_service.users().messages().list.return_value = mock_list
                
                server.gmail_service = mock_service
                
                # Test with label and date range
                server.search_emails(
                    label='Research_Data',
                    start_date='2025-10-01',
                    end_date='2025-10-20'
                )
                
                # Verify query was built correctly
                call_args = mock_service.users().messages().list.call_args
                assert 'label:Research_Data' in call_args[1]['q']
                assert 'after:2025-10-01' in call_args[1]['q']
                assert 'before:2025-10-20' in call_args[1]['q']


class TestCSVEncoding:
    """Test cases for CSV encoding and Hebrew support."""
    
    def test_utf8_bom_encoding(self, tmp_path):
        """Test that CSV files have UTF-8 BOM."""
        with patch.dict(os.environ, {'GMAIL_CREDENTIALS_PATH': './test.json'}):
            with patch.object(GmailMCPServer, '_find_credentials_path', return_value='./test.json'):
                server = GmailMCPServer()
                server.csv_output_dir = str(tmp_path)
                
                emails = [
                    {
                        'date': 'Mon, 20 Oct 2025 10:00:00 +0000',
                        'from': 'test@example.com',
                        'to': 'recipient@example.com',
                        'subject': 'שלום',
                        'body': 'תוכן'
                    }
                ]
                
                output_path = server.export_to_csv(emails, 'bom_test.csv')
                
                # Check for UTF-8 BOM
                with open(output_path, 'rb') as f:
                    first_bytes = f.read(3)
                    assert first_bytes == b'\xef\xbb\xbf'
    
    def test_hebrew_characters_preserved(self, tmp_path):
        """Test that Hebrew characters are preserved correctly."""
        with patch.dict(os.environ, {'GMAIL_CREDENTIALS_PATH': './test.json'}):
            with patch.object(GmailMCPServer, '_find_credentials_path', return_value='./test.json'):
                server = GmailMCPServer()
                server.csv_output_dir = str(tmp_path)
                
                hebrew_subject = "בדיקת מערכת"
                hebrew_body = "תוכן ההודעה בעברית"
                
                emails = [
                    {
                        'date': 'Mon, 20 Oct 2025 10:00:00 +0000',
                        'from': 'test@example.com',
                        'to': 'recipient@example.com',
                        'subject': hebrew_subject,
                        'body': hebrew_body
                    }
                ]
                
                output_path = server.export_to_csv(emails, 'hebrew_preserve.csv')
                
                # Read and verify
                with open(output_path, 'r', encoding='utf-8-sig') as f:
                    content = f.read()
                    assert hebrew_subject in content
                    assert hebrew_body in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

