#!/usr/bin/env python3
"""
Daily K-beauty trend briefing runner with CLI support
"""

import asyncio
import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('briefing.log')
        ]
    )

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run K-beauty daily trend briefing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_daily_briefing.py                    # Run normal briefing
  python run_daily_briefing.py --dry-run         # Test without saving outputs
  python run_daily_briefing.py --verbose         # Detailed logging
  python run_daily_briefing.py --dry-run --verbose  # Debug mode
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run in dry-run mode (no outputs saved)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force run even if already completed today'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['markdown', 'json', 'notion', 'all'],
        default='all',
        help='Output format to generate (default: all)'
    )
    
    return parser.parse_args()

async def run_briefing(args):
    """Run the daily briefing with CLI arguments."""
    # Import here to avoid dependency issues with help command
    try:
        from core.pipeline import DailyBriefingPipeline
        from core.config import config
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False
    
    logger = logging.getLogger(__name__)
    
    print("🎀 K-Beauty Daily Trend Briefing")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Dry run: {'Yes' if args.dry_run else 'No'}")
    print(f"📤 Output format: {args.output_format}")
    print(f"⚡ Force run: {'Yes' if args.force else 'No'}")
    print()
    
    try:
        # Initialize pipeline
        pipeline = DailyBriefingPipeline()
        
        # Check if already run today (unless forced)
        if not args.force and not args.dry_run:
            latest_briefing = pipeline.get_latest_briefing()
            if latest_briefing:
                latest_date = datetime.fromisoformat(latest_briefing.get('date', '')).date()
                if latest_date == datetime.now().date():
                    logger.info("Briefing already completed today. Use --force to run again.")
                    print("✅ Briefing already completed today")
                    return True
        
        # Configure output based on CLI args
        if args.output_format != 'all':
            if args.output_format == 'markdown':
                config.output.notion_enabled = False
                config.output.json_enabled = False
            elif args.output_format == 'json':
                config.output.notion_enabled = False
                config.output.markdown_enabled = False
            elif args.output_format == 'notion':
                config.output.markdown_enabled = False
                config.output.json_enabled = False
        
        # Run the briefing
        logger.info("Starting daily briefing pipeline...")
        briefing = await pipeline.run_daily_briefing()
        
        if briefing:
            # Log success
            logger.info("Daily briefing completed successfully")
            print("\n✅ Daily briefing completed successfully!")
            print(f"📊 Briefing ID: {briefing.briefing_id}")
            print(f"📈 Trends identified: {len(briefing.trend_analysis.trends)}")
            print(f"🎯 Priority trends: {len(briefing.synthesis_results.priority_trends)}")
            print(f"💡 Market opportunities: {len(briefing.synthesis_results.market_opportunities)}")
            print(f"⚠️ Risk factors: {len(briefing.synthesis_results.risk_factors)}")
            print(f"📝 Posts analyzed: {briefing.scraped_posts_count}")
            
            # Show top priority trends
            if briefing.synthesis_results.priority_trends:
                print("\n🏆 Top Priority Trends:")
                for trend in briefing.synthesis_results.priority_trends[:3]:
                    print(f"  #{trend.rank} {trend.trend_name} ({trend.business_impact.value} impact)")
            
            # Show output files (if not dry run)
            if not args.dry_run:
                output_files = pipeline.output_pipeline.get_output_files(briefing)
                if output_files:
                    print("\n📁 Output files created:")
                    for file in output_files:
                        print(f"  • {file}")
            
            print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Log to file for monitoring
            with open('briefing_success.log', 'a') as f:
                f.write(f"{datetime.now().isoformat()} - SUCCESS - {briefing.briefing_id}\n")
            
            return True
            
        else:
            # Log failure
            logger.error("Daily briefing failed")
            print("\n❌ Daily briefing failed!")
            status = pipeline.get_status()
            if status.error_message:
                print(f"Error: {status.error_message}")
            
            # Log to file for monitoring
            with open('briefing_error.log', 'a') as f:
                f.write(f"{datetime.now().isoformat()} - FAILED - {status.error_message}\n")
            
            return False
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n💥 Unexpected error: {e}")
        
        # Log to file for monitoring
        with open('briefing_error.log', 'a') as f:
            f.write(f"{datetime.now().isoformat()} - ERROR - {str(e)}\n")
        
        return False

def main():
    """Main function with CLI support."""
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Run the briefing
    success = asyncio.run(run_briefing(args))
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 