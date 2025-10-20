#!/usr/bin/env python3
"""
CSV Encoding Verification Tool
Verifies that CSV files have proper UTF-8 BOM encoding for Hebrew support.
"""

import sys
import argparse
from pathlib import Path


def check_utf8_bom(filepath: str) -> bool:
    """
    Check if file has UTF-8 BOM.
    
    Args:
        filepath: Path to CSV file
    
    Returns:
        True if UTF-8 BOM present, False otherwise
    """
    with open(filepath, 'rb') as f:
        first_bytes = f.read(3)
        return first_bytes == b'\xef\xbb\xbf'


def verify_hebrew_content(filepath: str) -> bool:
    """
    Check if Hebrew characters are readable.
    
    Args:
        filepath: Path to CSV file
    
    Returns:
        True if Hebrew content readable, False otherwise
    """
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            # Check for Hebrew Unicode range (0x0590-0x05FF)
            has_hebrew = any('\u0590' <= char <= '\u05FF' for char in content)
            return has_hebrew
    except UnicodeDecodeError:
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Verify CSV encoding for Hebrew support'
    )
    parser.add_argument(
        'filepath',
        type=str,
        help='Path to CSV file to verify'
    )
    
    args = parser.parse_args()
    
    if not Path(args.filepath).exists():
        print(f"❌ Error: File not found: {args.filepath}")
        return 1
    
    print(f"\n{'='*60}")
    print(f"CSV ENCODING VERIFICATION")
    print(f"{'='*60}")
    print(f"File: {args.filepath}\n")
    
    # Check UTF-8 BOM
    has_bom = check_utf8_bom(args.filepath)
    print(f"UTF-8 BOM: {'✅ Present' if has_bom else '❌ Missing'}")
    
    # Check Hebrew content
    has_hebrew = verify_hebrew_content(args.filepath)
    print(f"Hebrew characters: {'✅ Detected' if has_hebrew else 'ℹ️  None found'}")
    
    # Overall status
    print(f"\n{'='*60}")
    if has_bom:
        print("✅ File is properly encoded for Excel/Hebrew support")
    else:
        print("⚠️  Warning: File may not display correctly in Excel")
    print(f"{'='*60}\n")
    
    return 0 if has_bom else 1


if __name__ == '__main__':
    sys.exit(main())

