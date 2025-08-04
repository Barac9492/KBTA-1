#!/usr/bin/env python3
"""
Generate Sample Archive Data
Creates sample briefings to populate the archive for demonstration
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

def generate_sample_briefings():
    """Generate sample briefings for archive demonstration"""
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Sample briefings for the last 7 days
    sample_briefings = [
        {
            "briefing_id": "briefing_20250801",
            "date": "2025-08-01T05:00:00",
            "scraped_posts_count": 12,
            "trend_analysis": {
                "trends": [
                    {
                        "id": "trend_1",
                        "name": "PDRN Salmon Sperm",
                        "description": "Polydeoxyribonucleotide from salmon sperm for skin regeneration",
                        "relevance_score": 0.95,
                        "growth_rate": 0.25,
                        "time_to_market": "short_term"
                    },
                    {
                        "id": "trend_2",
                        "name": "Micro-Needle Serums",
                        "description": "Advanced delivery systems for better ingredient penetration",
                        "relevance_score": 0.88,
                        "growth_rate": 0.18,
                        "time_to_market": "medium_term"
                    }
                ]
            },
            "synthesis_results": {
                "executive_summary": "K-beauty continues to innovate with PDRN and micro-needling technologies.",
                "key_insights": [
                    "PDRN salmon sperm is the hottest trend with 25% growth",
                    "Micro-needling serums are gaining mainstream adoption"
                ],
                "actionable_recommendations": [
                    "Develop PDRN-based products for anti-aging market",
                    "Create micro-needling serums for better ingredient delivery"
                ],
                "market_outlook": "The K-beauty market is expected to continue growing with focus on innovative ingredients."
            }
        },
        {
            "briefing_id": "briefing_20250730",
            "date": "2025-07-30T05:00:00",
            "scraped_posts_count": 8,
            "trend_analysis": {
                "trends": [
                    {
                        "id": "trend_1",
                        "name": "Korean Haircare",
                        "description": "K-beauty expanding to haircare with innovative formulations",
                        "relevance_score": 0.82,
                        "growth_rate": 0.30,
                        "time_to_market": "medium_term"
                    },
                    {
                        "id": "trend_2",
                        "name": "Glass Skin Routine",
                        "description": "Multi-step routines for transparent, dewy skin",
                        "relevance_score": 0.78,
                        "growth_rate": 0.15,
                        "time_to_market": "short_term"
                    }
                ]
            },
            "synthesis_results": {
                "executive_summary": "Korean haircare emerges as the next big category while glass skin remains popular.",
                "key_insights": [
                    "Korean haircare is the next big category to watch",
                    "Glass skin routines continue to dominate social media"
                ],
                "actionable_recommendations": [
                    "Expand into Korean haircare formulations",
                    "Develop multi-step glass skin routine products"
                ],
                "market_outlook": "Haircare represents the next frontier for K-beauty expansion."
            }
        },
        {
            "briefing_id": "briefing_20250728",
            "date": "2025-07-28T05:00:00",
            "scraped_posts_count": 15,
            "trend_analysis": {
                "trends": [
                    {
                        "id": "trend_1",
                        "name": "Propolis and Honey Extracts",
                        "description": "Natural ingredients with antibacterial and moisturizing properties",
                        "relevance_score": 0.85,
                        "growth_rate": 0.22,
                        "time_to_market": "short_term"
                    },
                    {
                        "id": "trend_2",
                        "name": "Cushion Foundation Innovation",
                        "description": "New formulas with skincare benefits and longer wear",
                        "relevance_score": 0.79,
                        "growth_rate": 0.12,
                        "time_to_market": "medium_term"
                    }
                ]
            },
            "synthesis_results": {
                "executive_summary": "Natural ingredients like propolis are becoming mainstream while cushion foundations evolve.",
                "key_insights": [
                    "Natural ingredients like propolis are becoming mainstream",
                    "Cushion foundations are evolving with skincare benefits"
                ],
                "actionable_recommendations": [
                    "Formulate products with propolis and honey extracts",
                    "Create cushion foundations with hyaluronic acid and niacinamide"
                ],
                "market_outlook": "Clean beauty and natural ingredients continue to drive innovation."
            }
        }
    ]
    
    # Save each briefing
    for briefing in sample_briefings:
        # Save as JSON
        json_file = output_dir / f"{briefing['briefing_id']}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(briefing, f, indent=2, ensure_ascii=False)
        
        # Save as Markdown
        markdown_file = output_dir / f"{briefing['briefing_id']}.md"
        markdown_content = f"""# K-Beauty Trend Briefing

**Date**: {briefing['date']}
**Briefing ID**: {briefing['briefing_id']}

## Executive Summary
{briefing['synthesis_results']['executive_summary']}

## Key Insights
{chr(10).join([f"- {insight}" for insight in briefing['synthesis_results']['key_insights']])}

## Actionable Recommendations
{chr(10).join([f"- {rec}" for rec in briefing['synthesis_results']['actionable_recommendations']])}

## Market Outlook
{briefing['synthesis_results']['market_outlook']}

---
*Generated automatically by K-Beauty Trend Agent*
"""
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Generated: {briefing['briefing_id']}")
    
    print(f"\n✅ Generated {len(sample_briefings)} sample briefings in {output_dir}/")
    print("📁 Archive page will now show these briefings when you visit:")
    print("   https://kbeauty-trend-agent-kftpav0f3-ethancho12-gmailcoms-projects.vercel.app/archive")

if __name__ == "__main__":
    generate_sample_briefings() 