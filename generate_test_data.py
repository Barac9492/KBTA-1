#!/usr/bin/env python3
"""
Generate test data for the K-Beauty Trend Agent
This script creates realistic briefing data for testing the frontend.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def generate_test_briefing():
    """Generate a realistic test briefing."""
    
    briefing = {
        "briefing_id": f"test_briefing_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "date": datetime.now().isoformat(),
        "scraped_posts_count": 15,
        "trend_analysis": {
            "trends": [
                {
                    "id": "trend_001",
                    "name": "Glass Skin 2.0",
                    "description": "Advanced glass skin techniques using multi-step routines with fermented ingredients and ceramides",
                    "relevance_score": 0.95,
                    "category": "SKIN_CARE",
                    "business_impact": "HIGH",
                    "time_to_market": "short_term",
                    "keywords": ["glass skin", "fermented ingredients", "ceramides", "multi-step"],
                    "sources": ["naver_blog", "instagram"]
                },
                {
                    "id": "trend_002",
                    "name": "Cushion Foundation Innovation",
                    "description": "New generation cushion foundations with skincare benefits, SPF protection, and 24-hour wear",
                    "relevance_score": 0.88,
                    "category": "MAKEUP",
                    "business_impact": "HIGH",
                    "time_to_market": "medium_term",
                    "keywords": ["cushion foundation", "skincare benefits", "SPF", "long wear"],
                    "sources": ["youtube", "naver_blog"]
                },
                {
                    "id": "trend_003",
                    "name": "Propolis and Honey Extracts",
                    "description": "Natural antibacterial and moisturizing ingredients gaining popularity in K-beauty formulations",
                    "relevance_score": 0.82,
                    "category": "INGREDIENTS",
                    "business_impact": "MEDIUM",
                    "time_to_market": "immediate",
                    "keywords": ["propolis", "honey", "natural", "antibacterial"],
                    "sources": ["instagram", "naver_blog"]
                },
                {
                    "id": "trend_004",
                    "name": "Retinol Alternatives",
                    "description": "Gentle alternatives to retinol using bakuchiol and other plant-based ingredients",
                    "relevance_score": 0.78,
                    "category": "SKIN_CARE",
                    "business_impact": "MEDIUM",
                    "time_to_market": "short_term",
                    "keywords": ["bakuchiol", "retinol alternative", "gentle", "plant-based"],
                    "sources": ["youtube", "instagram"]
                },
                {
                    "id": "trend_005",
                    "name": "Sustainable Packaging",
                    "description": "Eco-friendly packaging solutions and refillable containers becoming standard in K-beauty",
                    "relevance_score": 0.75,
                    "category": "PACKAGING",
                    "business_impact": "LOW",
                    "time_to_market": "long_term",
                    "keywords": ["sustainable", "eco-friendly", "refillable", "packaging"],
                    "sources": ["naver_blog", "instagram"]
                }
            ]
        },
        "synthesis_results": {
            "executive_summary": "K-beauty continues to evolve with a focus on advanced glass skin techniques, innovative cushion foundations, and natural ingredients. The market is shifting towards gentle, effective formulations with sustainable packaging becoming increasingly important.",
            "key_insights": [
                "Glass skin techniques are becoming more sophisticated with fermented ingredients and ceramides",
                "Cushion foundations are evolving to include skincare benefits and longer wear times",
                "Natural ingredients like propolis and honey are gaining mainstream acceptance",
                "Gentle alternatives to retinol are in high demand",
                "Sustainable packaging is becoming a key differentiator"
            ],
            "actionable_recommendations": [
                "Develop multi-step glass skin routines with fermented ingredients and ceramides",
                "Create cushion foundations with hyaluronic acid, niacinamide, and SPF protection",
                "Formulate products with propolis and honey extracts for antibacterial benefits",
                "Research and develop bakuchiol-based alternatives to retinol",
                "Invest in sustainable packaging solutions and refillable containers"
            ],
            "market_outlook": "The K-beauty market is expected to continue growing at 8-10% annually, with focus on natural ingredients, innovative formulations, and sustainable practices. Brands that can combine efficacy with gentleness and environmental responsibility will have a competitive advantage."
        }
    }
    
    return briefing

def save_test_data():
    """Save test data to the output directory."""
    
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate test briefing
    briefing = generate_test_briefing()
    
    # Save as JSON
    json_file = output_dir / f"{briefing['briefing_id']}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(briefing, f, indent=2, ensure_ascii=False)
    
    # Save as markdown
    markdown_file = output_dir / f"{briefing['briefing_id']}.md"
    markdown_content = generate_markdown(briefing)
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ Test data generated:")
    print(f"   JSON: {json_file}")
    print(f"   Markdown: {markdown_file}")
    print(f"   Briefing ID: {briefing['briefing_id']}")

def generate_markdown(briefing):
    """Generate markdown content from briefing data."""
    
    md = f"""# K-Beauty Daily Trend Briefing

**Date:** {briefing['date']}  
**Briefing ID:** {briefing['briefing_id']}  
**Sources Analyzed:** {briefing['scraped_posts_count']}

## Executive Summary

{briefing['synthesis_results']['executive_summary']}

## Key Insights

"""
    
    for insight in briefing['synthesis_results']['key_insights']:
        md += f"- {insight}\n"
    
    md += "\n## Trend Analysis\n\n"
    
    for trend in briefing['trend_analysis']['trends']:
        md += f"### {trend['name']}\n\n"
        md += f"**Relevance Score:** {trend['relevance_score']:.2f}\n\n"
        md += f"{trend['description']}\n\n"
        md += f"**Business Impact:** {trend['business_impact']}\n"
        md += f"**Time to Market:** {trend['time_to_market'].replace('_', ' ').title()}\n\n"
        
        if trend.get('keywords'):
            md += f"**Keywords:** {', '.join(trend['keywords'])}\n\n"
    
    md += "## Actionable Recommendations\n\n"
    
    for rec in briefing['synthesis_results']['actionable_recommendations']:
        md += f"- {rec}\n"
    
    md += f"\n## Market Outlook\n\n{briefing['synthesis_results']['market_outlook']}\n"
    
    return md

if __name__ == "__main__":
    save_test_data() 