#!/usr/bin/env python3
"""
Direct Gmail Email Fetcher
Standalone script for testing Gmail API integration without MCP server.
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from gmail_mcp_server import GmailMCPServer


def main():
    """Main entry point for direct email fetching."""
    parser = argparse.ArgumentParser(
        description='Fetch emails from Gmail and export to CSV'
    )
    parser.add_argument(
        '--label',
        type=str,
        help='Gmail label to filter by'
    )
    parser.add_argument(
        '--start-date',
        type=str,
        help='Start date in YYYY-MM-DD format'
    )
    parser.add_argument(
        '--end-date',
        type=str,
        help='End date in YYYY-MM-DD format'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output CSV filename'
    )
    parser.add_argument(
        '--max-results',
        type=int,
        default=100,
        help='Maximum number of emails to retrieve (default: 100)'
    )
    
    args = parser.parse_args()
    
    # Initialize server
    server = GmailMCPServer()
    
    # Execute search and export
    result = server.search_and_export(
        label=args.label,
        start_date=args.start_date,
        end_date=args.end_date,
        output_filename=args.output,
        max_results=args.max_results
    )
    
    # Print results
    print("\n" + "="*60)
    print("EMAIL EXTRACTION RESULTS")
    print("="*60)
    print(f"Status: {'SUCCESS' if result['success'] else 'FAILED'}")
    print(f"Emails found: {result['count']}")
    print(f"Message: {result['message']}")
    if result['output_file']:
        print(f"Output file: {result['output_file']}")
    print("="*60 + "\n")
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())

