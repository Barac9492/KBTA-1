#!/usr/bin/env python3
"""
Test script to demonstrate dry-run functionality
"""

import subprocess
import sys

def test_dry_run():
    """Test the dry-run functionality."""
    print("🧪 Testing K-Beauty Briefing Dry Run")
    print("=" * 50)
    
    try:
        # Test dry-run command
        result = subprocess.run([
            sys.executable, "run_daily_briefing.py", 
            "--dry-run", "--verbose"
        ], capture_output=True, text=True)
        
        print("Command executed successfully!")
        print(f"Exit code: {result.returncode}")
        print("\n📋 Output:")
        print(result.stdout)
        
        if result.stderr:
            print("\n⚠️ Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

if __name__ == "__main__":
    success = test_dry_run()
    sys.exit(0 if success else 1) 