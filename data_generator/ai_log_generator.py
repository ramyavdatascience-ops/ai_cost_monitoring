import json
import random
import uuid
import time
from datetime import datetime
import boto3

# Create Kinesis client
kinesis_client = boto3.client("kinesis", region_name="us-east-1")

STREAM_NAME = "ai-cost-monitoring-stream"

models = ["gpt-4", "gpt-4o", "claude-3", "gemini-pro"]
users = ["team_analytics", "team_marketing", "team_product", "team_support"]

def generate_log():
    tokens_input = random.randint(100, 2000)
    tokens_output = random.randint(50, 1000)

    cost = round((tokens_input + tokens_output) * 0.00002, 5)

    log = {
        "request_id": str(uuid.uuid4()),
        "user_team": random.choice(users),
        "model": random.choice(models),
        "tokens_input": tokens_input,
        "tokens_output": tokens_output,
        "cost_usd": cost,
        "timestamp": datetime.utcnow().isoformat()
    }

    return log


while True:
    log = generate_log()

    # send data to Kinesis
    response = kinesis_client.put_record(
    StreamName=STREAM_NAME,
    Data=json.dumps(log),
    PartitionKey=log["request_id"]
)

    print("Response:", response)

    time.sleep(1)