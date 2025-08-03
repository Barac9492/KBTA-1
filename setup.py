#!/usr/bin/env python3
"""
K-Beauty Trend Agent Setup Script
Helps users set up the project with all necessary dependencies and configuration.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    """Print setup banner."""
    print("=" * 60)
    print("🎀 K-Beauty Trend Agent Setup")
    print("=" * 60)
    print("Setting up your intelligent K-beauty trend analysis system...")
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    return True

def setup_playwright():
    """Install Playwright browsers."""
    print("🌐 Setting up Playwright browsers...")
    
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], 
                      check=True, capture_output=True)
        print("✅ Playwright browsers installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Playwright browsers: {e}")
        print("Please run: playwright install chromium")
        return False
    return True

def create_env_file():
    """Create .env file from template."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    try:
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created from template")
        print("⚠️  Please update .env with your API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    directories = ["data", "logs", "cache"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")

def check_configuration():
    """Check if configuration is complete."""
    print("🔧 Checking configuration...")
    
    # Check if .env exists
    if not Path(".env").exists():
        print("❌ .env file not found")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check required environment variables
    required_vars = ["OPENAI_API_KEY"]
    optional_vars = ["NOTION_TOKEN", "NOTION_DATABASE_ID"]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"⚠️  Missing optional environment variables: {', '.join(missing_optional)}")
        print("   Notion integration will be disabled")
    
    print("✅ Configuration check completed")
    return True

def test_installation():
    """Test the installation."""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import openai
        import playwright
        import fastapi
        import notion_client
        print("✅ All required packages imported successfully")
        
        # Test scraper
        print("🔍 Testing scraper...")
        from scripts.scrape_naver_blog import KBeautyScraper
        scraper = KBeautyScraper()
        print("✅ Scraper initialized successfully")
        
        # Test agent runner
        print("🤖 Testing agent runner...")
        from scripts.run_agents import TrendAgentRunner
        runner = TrendAgentRunner()
        print("✅ Agent runner initialized successfully")
        
        # Test API
        print("🌐 Testing API...")
        from api.app import app
        print("✅ API initialized successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update your .env file with API keys:")
    print("   - OPENAI_API_KEY: Get from https://platform.openai.com")
    print("   - NOTION_TOKEN: Get from https://www.notion.so/my-integrations")
    print("   - NOTION_DATABASE_ID: Your Notion database ID")
    print("\n2. Run the scraper:")
    print("   python scripts/scrape_naver_blog.py")
    print("\n3. Run the agents:")
    print("   python scripts/run_agents.py")
    print("\n4. Start the API server:")
    print("   uvicorn api.app:app --reload")
    print("\n5. Push to Notion (optional):")
    print("   python scripts/push_to_notion.py")
    print("\n6. Access the dashboard:")
    print("   Open frontend/dashboard.jsx in your React app")
    print("\nFor more information, see README.md")
    print("=" * 60)

def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Setup Playwright
    if not setup_playwright():
        return
    
    # Create directories
    create_directories()
    
    # Create .env file
    if not create_env_file():
        return
    
    # Check configuration
    if not check_configuration():
        print("\n⚠️  Please update your .env file and run setup again")
        return
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed")
        return
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 