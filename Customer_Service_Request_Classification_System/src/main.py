import os
import pandas as pd
import time
from models import customerRequests, requestClassifications
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from datetime import datetime, timedelta
from typing import Literal, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import traceback

from db_operations import (
    create_db_and_tables,
    insert_customer_requests,
    insert_request_classifications,
)

load_dotenv()

class ClassificationResult(BaseModel):
    category: Literal["technical", "billing", "sales", "feedback"]
    priority: Literal["low", "medium", "high", "urgent"]
    tags: List[str] = Field(description="Relevant tags extracted from request")
    estimated_resolution_time: int = Field(description="Estimated resolution time in hours")
    confidence: float = Field(ge=0.0, le=1.0)


model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    temperature = 0
)

agent = create_agent(
    model = model,
    tools = [],
    response_format=ClassificationResult,
    system_prompt=
    """
    You are a customer service request classification agent.

    Classify each request into exactly one category:
    - technical: technical issues, bugs, system problems
    - billing: payment issues, billing questions, account charges
    - sales: product inquiries, upgrades, new purchases
    - feedback: complaints, compliments, suggestions

    Assign priority:
    - urgent: service outages, critical failures, security issues
    - high: important business impact, billing errors, repeated problems
    - medium: standard single-user issues
    - low: general questions, minor issues, positive feedback

    Return only structured output.
    """
)

def classify_single_request(row) -> ClassificationResult:
    user_prompt = f"""
    Ticket ID: {row["ticket_id"]}
    Customer ID: {row["customer_id"]}
    Channel: {row["channel"]}
    Request Text: {row["request_text"]}
    Original Timestamp: {row["timestamp"]}
    """

    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }
    )

    return result["structured_response"]




def process_csv(csv_path: str):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        ticket_id = row["ticket_id"]
        try:
            print(f"Processing ticket: {row['ticket_id']}")

            original_timestamp = pd.to_datetime(row["timestamp"]).to_pydatetime()

            customer_request = customerRequests(
                ticket_id=row["ticket_id"],
                customer_id=row["customer_id"],
                channel=row["channel"],
                request_text=row["request_text"],
                created_at=original_timestamp,
            )

            insert_customer_requests(customer_request)

            classification_result = classify_single_request(row)
            print("AI RESULT:", classification_result)

            classification = requestClassifications(
                ticket_id=row["ticket_id"],
                category=classification_result.category,
                priority=classification_result.priority,
                tags=classification_result.tags,
                estimated_resolution_time=classification_result.estimated_resolution_time,
                confidence=classification_result.confidence,
                processed_at=datetime.now(),
            )

            print("DB CLASSIFICATION OBJECT:", classification)
            insert_request_classifications(classification)

            print(f"Completed: {row['ticket_id']}")

            time.sleep(1)


        except Exception as e:
            print(f"Error processing ticket {ticket_id}:")
            traceback.print_exc()
            continue

if __name__ == "__main__":
    create_db_and_tables()
    process_csv("data/raw/customer_requests.csv")