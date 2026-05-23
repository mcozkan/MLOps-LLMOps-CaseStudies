from fastapi import APIRouter, Depends, status
import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Iterator, Tuple

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model
from models import ProductReview, RawProductReview, ProductReviewRate
from database import get_db, create_db_and_tables
from sqlmodel import Session
import os

load_dotenv()

create_db_and_tables()


router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("review_analysis")

SYSTEM_PROMPT = (
    "You analyze product reviews and return structured data.\n"
    "Sentiment values:\n"
    "  - 'positive': clearly favorable overall.\n"
    "  - 'negative': clearly unfavorable overall.\n"
    "  - 'neutral': purely factual / indifferent / no clear evaluation.\n"
    "  - 'mixed': contains both clearly positive and clearly negative points.\n"
    "Always include an honest 'confidence' (0-1). Lower it for short, "
    "ambiguous, sarcastic, or off-topic reviews. Detect 'language' as a "
    "two-letter ISO 639-1 code (e.g. 'en', 'tr', 'de')."
)

REQUIRED_FIELDS = ("user", "product", "review")

def build_agent():
    model = init_chat_model(
        "gemini-2.5-flash-lite",
        # Kwargs passed to the model:
        temperature=0.1,
        timeout=30,
        max_tokens=500,
        model_provider="google_genai",
        )

    return create_agent(
        model=model,
        tools=[],
        response_format=ToolStrategy(schema=ProductReview),
        system_prompt=SYSTEM_PROMPT,
    )

def analyze_one(agent, review_text: str) -> ProductReview:
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"Analyze this review: '{review_text}'",
        }]
    })
    response = result.get("structured_response")
    if response is None:
        raise RuntimeError("agent returned no structured_response")
    return response


agent = build_agent()

@router.post("/llm/chat", response_model=ProductReviewRate, status_code=status.HTTP_201_CREATED)
async def make_chat(request: RawProductReview, session: Session = Depends(get_db)):
    try:
        analysis = analyze_one(agent, request.review)
    except Exception as e:
        log.error(e)


    product_review = ProductReviewRate(
                user_info = request.user,
                review = request.review,
                product = request.product,
                rate = analysis.rating,
                confidence = analysis.confidence,
                sentiment = analysis.sentiment,
                language = analysis.language,
                key_points = json.dumps(analysis.key_points))
                
                
   

    with session:
        session.add(product_review)
        session.commit()
        session.refresh(product_review)

    return  product_review