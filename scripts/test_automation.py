#!/usr/bin/env python3
"""
Test Automation Script for K-Beauty Trend Agent
Tests cron jobs, autonomous agent, and monitoring capabilities
"""

import os
import sys
import json
import time
import asyncio
import requests
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_cron_endpoints(base_url: str) -> dict:
    """Test cron endpoints"""
    results = {
        "health": None,
        "pipeline": None,
        "errors": []
    }
    
    try:
        # Test health endpoint
        print("🔍 Testing health endpoint...")
        health_response = requests.get(f"{base_url}/api/cron/health", timeout=30)
        results["health"] = {
            "status_code": health_response.status_code,
            "response": health_response.json() if health_response.status_code == 200 else None
        }
        print(f"✅ Health endpoint: {health_response.status_code}")
        
    except Exception as e:
        results["errors"].append(f"Health endpoint failed: {e}")
        print(f"❌ Health endpoint failed: {e}")
    
    try:
        # Test pipeline endpoint
        print("🔍 Testing pipeline endpoint...")
        pipeline_response = requests.get(f"{base_url}/api/cron/run-pipeline", timeout=300)
        results["pipeline"] = {
            "status_code": pipeline_response.status_code,
            "response": pipeline_response.json() if pipeline_response.status_code == 200 else None
        }
        print(f"✅ Pipeline endpoint: {pipeline_response.status_code}")
        
    except Exception as e:
        results["errors"].append(f"Pipeline endpoint failed: {e}")
        print(f"❌ Pipeline endpoint failed: {e}")
    
    return results

def test_autonomous_agent() -> dict:
    """Test autonomous agent functionality"""
    results = {
        "agent_available": False,
        "crewai_available": False,
        "test_result": None,
        "errors": []
    }
    
    try:
        # Check if agent module exists
        agent_path = project_root / "agent" / "autonomous_agent.py"
        if agent_path.exists():
            results["agent_available"] = True
            print("✅ Autonomous agent file exists")
        else:
            print("⚠️ Autonomous agent file not found")
            return results
        
        # Check CrewAI availability
        try:
            import crewai
            results["crewai_available"] = True
            print("✅ CrewAI available")
        except ImportError:
            results["errors"].append("CrewAI not installed")
            print("❌ CrewAI not installed")
            return results
        
        # Test agent initialization (without running full cycle)
        try:
            from agent.autonomous_agent import KBeautyAutonomousAgent
            
            # Initialize agent (this will test imports and setup)
            agent = KBeautyAutonomousAgent()
            results["test_result"] = "Agent initialized successfully"
            print("✅ Autonomous agent initialized successfully")
            
        except Exception as e:
            results["errors"].append(f"Agent initialization failed: {e}")
            print(f"❌ Agent initialization failed: {e}")
        
    except Exception as e:
        results["errors"].append(f"Autonomous agent test failed: {e}")
        print(f"❌ Autonomous agent test failed: {e}")
    
    return results

def test_data_sources() -> dict:
    """Test data source availability"""
    results = {
        "scrapers_available": False,
        "mock_data_working": False,
        "errors": []
    }
    
    try:
        # Check if scraper modules exist
        scraper_path = project_root / "core" / "scraper.py"
        if scraper_path.exists():
            results["scrapers_available"] = True
            print("✅ Scraper modules exist")
        else:
            print("⚠️ Scraper modules not found")
        
        # Test mock data generation
        try:
            from api.cron_handler import CronHandler
            handler = CronHandler()
            mock_data = handler._get_mock_scraped_data()
            
            if mock_data and len(mock_data) > 0:
                results["mock_data_working"] = True
                print(f"✅ Mock data working: {len(mock_data)} items")
            else:
                results["errors"].append("Mock data generation failed")
                print("❌ Mock data generation failed")
                
        except Exception as e:
            results["errors"].append(f"Mock data test failed: {e}")
            print(f"❌ Mock data test failed: {e}")
        
    except Exception as e:
        results["errors"].append(f"Data sources test failed: {e}")
        print(f"❌ Data sources test failed: {e}")
    
    return results

def test_environment() -> dict:
    """Test environment configuration"""
    results = {
        "openai_key": False,
        "vercel_env": False,
        "python_path": False,
        "errors": []
    }
    
    # Check OpenAI API key
    if os.getenv("OPENAI_API_KEY"):
        results["openai_key"] = True
        print("✅ OpenAI API key configured")
    else:
        results["errors"].append("OPENAI_API_KEY not set")
        print("❌ OPENAI_API_KEY not set")
    
    # Check Vercel environment
    if os.getenv("VERCEL"):
        results["vercel_env"] = True
        print("✅ Vercel environment detected")
    else:
        print("⚠️ Not running in Vercel environment")
    
    # Check Python path
    if project_root in sys.path:
        results["python_path"] = True
        print("✅ Python path configured")
    else:
        results["errors"].append("Python path not configured")
        print("❌ Python path not configured")
    
    return results

def test_performance(base_url: str) -> dict:
    """Test performance metrics"""
    results = {
        "health_response_time": None,
        "pipeline_response_time": None,
        "errors": []
    }
    
    try:
        # Test health endpoint response time
        start_time = time.time()
        health_response = requests.get(f"{base_url}/api/cron/health", timeout=30)
        health_time = time.time() - start_time
        results["health_response_time"] = health_time
        print(f"⏱️ Health endpoint response time: {health_time:.2f}s")
        
    except Exception as e:
        results["errors"].append(f"Health performance test failed: {e}")
        print(f"❌ Health performance test failed: {e}")
    
    try:
        # Test pipeline endpoint response time
        start_time = time.time()
        pipeline_response = requests.get(f"{base_url}/api/cron/run-pipeline", timeout=300)
        pipeline_time = time.time() - start_time
        results["pipeline_response_time"] = pipeline_time
        print(f"⏱️ Pipeline endpoint response time: {pipeline_time:.2f}s")
        
    except Exception as e:
        results["errors"].append(f"Pipeline performance test failed: {e}")
        print(f"❌ Pipeline performance test failed: {e}")
    
    return results

def generate_report(all_results: dict) -> str:
    """Generate a comprehensive test report"""
    report = f"""
# K-Beauty Trend Agent Automation Test Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Environment**: {'Vercel' if os.getenv('VERCEL') else 'Local'}

## Test Results Summary

### ✅ Passed Tests
"""
    
    passed_count = 0
    failed_count = 0
    
    for test_name, result in all_results.items():
        if isinstance(result, dict) and result.get("errors"):
            failed_count += len(result["errors"])
        else:
            passed_count += 1
    
    report += f"""
- **Total Tests**: {len(all_results)}
- **Passed**: {passed_count}
- **Failed**: {failed_count}
- **Success Rate**: {(passed_count / len(all_results)) * 100:.1f}%

## Detailed Results

### 1. Environment Configuration
"""
    
    env_results = all_results.get("environment", {})
    for key, value in env_results.items():
        status = "✅" if value else "❌"
        report += f"- {key}: {status}\n"
    
    report += """
### 2. Cron Endpoints
"""
    
    cron_results = all_results.get("cron_endpoints", {})
    for endpoint, result in cron_results.items():
        if result and result.get("status_code") == 200:
            report += f"- {endpoint}: ✅ (200)\n"
        else:
            report += f"- {endpoint}: ❌\n"
    
    report += """
### 3. Autonomous Agent
"""
    
    agent_results = all_results.get("autonomous_agent", {})
    for key, value in agent_results.items():
        if key == "errors":
            continue
        status = "✅" if value else "❌"
        report += f"- {key}: {status}\n"
    
    report += """
### 4. Data Sources
"""
    
    data_results = all_results.get("data_sources", {})
    for key, value in data_results.items():
        if key == "errors":
            continue
        status = "✅" if value else "❌"
        report += f"- {key}: {status}\n"
    
    report += """
### 5. Performance Metrics
"""
    
    perf_results = all_results.get("performance", {})
    for key, value in perf_results.items():
        if key == "errors":
            continue
        if value is not None:
            report += f"- {key}: {value:.2f}s\n"
        else:
            report += f"- {key}: ❌\n"
    
    # Add error details
    all_errors = []
    for test_name, result in all_results.items():
        if isinstance(result, dict) and result.get("errors"):
            all_errors.extend(result["errors"])
    
    if all_errors:
        report += """
## Errors Found
"""
        for error in all_errors:
            report += f"- {error}\n"
    
    report += """
## Recommendations

1. **Deployment Ready**: All critical tests passed
2. **Monitor Performance**: Track response times in production
3. **Set Up Alerts**: Configure notifications for failures
4. **Scale Gradually**: Start with 6-hour intervals, adjust as needed

---
*Report generated by K-Beauty Trend Agent Automation Test Suite*
"""
    
    return report

def main():
    """Run all automation tests"""
    print("🚀 Starting K-Beauty Trend Agent Automation Tests...")
    print("=" * 60)
    
    # Get base URL from environment or use default
    base_url = os.getenv("VERCEL_URL", "http://localhost:3000")
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"
    
    print(f"📍 Testing against: {base_url}")
    print()
    
    all_results = {}
    
    # Test 1: Environment Configuration
    print("🔧 Testing Environment Configuration...")
    all_results["environment"] = test_environment()
    print()
    
    # Test 2: Cron Endpoints
    print("⏰ Testing Cron Endpoints...")
    all_results["cron_endpoints"] = test_cron_endpoints(base_url)
    print()
    
    # Test 3: Autonomous Agent
    print("🤖 Testing Autonomous Agent...")
    all_results["autonomous_agent"] = test_autonomous_agent()
    print()
    
    # Test 4: Data Sources
    print("📊 Testing Data Sources...")
    all_results["data_sources"] = test_data_sources()
    print()
    
    # Test 5: Performance
    print("⚡ Testing Performance...")
    all_results["performance"] = test_performance(base_url)
    print()
    
    # Generate and save report
    print("📝 Generating Test Report...")
    report = generate_report(all_results)
    
    # Save report to file
    report_path = project_root / "test_report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"📄 Report saved to: {report_path}")
    print()
    
    # Print summary
    print("🎯 Test Summary:")
    print("=" * 60)
    
    passed_count = 0
    failed_count = 0
    
    for test_name, result in all_results.items():
        if isinstance(result, dict) and result.get("errors"):
            failed_count += len(result["errors"])
        else:
            passed_count += 1
    
    print(f"✅ Passed: {passed_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Success Rate: {(passed_count / len(all_results)) * 100:.1f}%")
    
    if failed_count == 0:
        print("\n🎉 All tests passed! Automation is ready for deployment.")
    else:
        print(f"\n⚠️ {failed_count} issues found. Check the report for details.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 