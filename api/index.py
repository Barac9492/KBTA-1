from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/test")
async def test():
    return {"message": "Test endpoint working!", "timestamp": datetime.now().isoformat()}

@app.get("/latest")
async def latest():
    return {
        "status": "success",
        "message": "Latest briefing retrieved successfully",
        "briefing_id": "mock_briefing_001",
        "timestamp": datetime.now().isoformat(),
        "data": {
            "briefing_id": "mock_briefing_001",
            "date": datetime.now().isoformat(),
            "scraped_posts_count": 5,
            "trend_analysis": {
                "trends": [
                    {
                        "id": "trend_1",
                        "name": "Glass Skin Technique",
                        "description": "Achieving transparent, dewy skin through multi-step routines",
                        "relevance_score": 0.95
                    },
                    {
                        "id": "trend_2", 
                        "name": "Cushion Foundation Innovation",
                        "description": "New formulas with skincare benefits and longer wear",
                        "relevance_score": 0.88
                    },
                    {
                        "id": "trend_3",
                        "name": "Propolis and Honey Extracts",
                        "description": "Natural ingredients with antibacterial and moisturizing properties",
                        "relevance_score": 0.82
                    }
                ]
            },
            "synthesis_results": {
                "executive_summary": "K-beauty continues to dominate with glass skin techniques, innovative cushion foundations, and natural ingredients like propolis gaining popularity.",
                "key_insights": [
                    "Glass skin trend shows no signs of slowing down",
                    "Cushion foundations are evolving with skincare benefits",
                    "Natural ingredients like propolis are becoming mainstream"
                ],
                "actionable_recommendations": [
                    "Develop multi-step glass skin routine products",
                    "Create cushion foundations with hyaluronic acid and niacinamide",
                    "Formulate products with propolis and honey extracts"
                ],
                "market_outlook": "The K-beauty market is expected to continue growing with focus on natural ingredients and innovative formulations."
            }
        }
    } 