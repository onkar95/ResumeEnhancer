# import os

# os.environ["LANGSMITH_TRACING"] = "true"
# os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
# os.environ["LANGSMITH_API_KEY"] = "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"
# os.environ["LANGSMITH_PROJECT"] = "Resume-enhancer"

# from langsmith import traceable

# @traceable
# def hello():
#     return "hello"

# print(hello())

import json
from langsmith import Client
from dotenv import load_dotenv

load_dotenv()

client = Client()

# Replace with your actual top-level trace ID from LangSmith
# TRACE_ID = "019f4fdb-22da-7c80-8fd7-f3c8dba24490"
# TRACE_ID = "019f50de-c7fd-7f33-bfee-fc5fe8ff4534"
# TRACE_ID = "019f50e4-dce7-74a3-ae25-209914f66d7a"
# TRACE_ID = "019f515f-c636-7e60-8ff8-f0ac63d2ee17"
# TRACE_ID = "019f5178-6073-70e1-8351-8ff031584bba"
TRACE_ID = "019f5b92-cae1-7a53-9781-7b1c4e0add53"


# 1. Fetch all runs belonging to this specific trace
all_runs = list(client.list_runs(trace_id=TRACE_ID))

# 2. Process and extract inputs/outputs for every single nested node
trace_data = []
for run in all_runs:
    trace_data.append({
        "node_name": run.name,
        "run_type": run.run_type,       # e.g., 'chain', 'llm', 'tool'
        "run_id": str(run.id),
        "parent_run_id": str(run.parent_run_id) if run.parent_run_id else None,
        "inputs": run.inputs,
        "outputs": run.outputs,
        "latency_ms": (run.end_time - run.start_time).total_seconds() * 1000 if run.end_time else None
    })

# 3. Save the complete data locally as a JSON file
with open("uploads/complete_trace_6.json", "w") as f:
    json.dump(trace_data, f, indent=2)

print(
    f"Successfully copied {len(trace_data)} runs from the trace into complete_trace.json!")
