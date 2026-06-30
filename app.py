#### Monolith version.
### To be used if performance recommendation is to use monolith instead of microservices.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional, Dict, Any
from datetime import datetime

import yaml
import logging
import re
import requests
import time

##########################################################
# Logging
##########################################################

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("Gatekeeper")


##########################################################
# FastAPI
##########################################################

app = FastAPI(
    title="Gatekeeper AI Agent",
    version="1.0",
    description="Enterprise Prompt Engineering Agent"
)


##########################################################
# Load skill.md
##########################################################

def load_skill():

    with open("skill.md", "r") as file:
        return yaml.safe_load(file)


SKILL = load_skill()


##########################################################
# MongoDB Connection
##########################################################

mongo_config = SKILL["mongodb"]

client = MongoClient(
    mongo_config["connection_string"]
)

db = client[
    mongo_config["database"]
]

logger.info("MongoDB Connected")


##########################################################
# Collections
##########################################################

fillers_col = db[
    mongo_config["collections"]["fillers"]
]

hedges_col = db[
    mongo_config["collections"]["hedges"]
]

gestures_col = db[
    mongo_config["collections"]["gestures"]
]

courtesy_col = db[
    mongo_config["collections"]["courtesy"]
]

constraints_col = db["constraints"]

explicits_col = db["explicits"]

cache_col = db["cachelist"]

llm_col = db["LowCostLLM"]


##########################################################
# Request Models
##########################################################

class PromptRequest(BaseModel):
    prompt: str


class TextRequest(BaseModel):
    text: str


class CacheRequest(BaseModel):

    request: str
    response: str
    responsetime: float
    cacheddatetime: datetime


##########################################################
# Response Models
##########################################################

class ConstraintResponse(BaseModel):

    audience: str
    length: str
    format: str
    updated_prompt: str


class ExplicitResponse(BaseModel):

    role: str
    tasks: List[str]
    tools: List[str]
    updated_prompt: str


##########################################################
# Mongo Helper Functions
##########################################################

def load_words(collection):

    """
    Returns list of words
    """

    return [
        x["value"]
        for x in collection.find()
    ]


def load_constraints():

    return list(
        constraints_col.find()
    )


def load_explicits():

    return list(
        explicits_col.find()
    )


##########################################################
# Low Cost LLM Configuration
##########################################################

def load_llm():

    config = llm_col.find_one()

    if config is None:
        raise Exception(
            "LowCostLLM configuration missing."
        )

    return config


##########################################################
# Utility
##########################################################

def normalize_spaces(text: str):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


##########################################################
# Remove Matching Words
##########################################################

def remove_phrases(
        text: str,
        phrases: List[str]
):

    """
    Removes phrases preserving case.
    """

    for phrase in sorted(
            phrases,
            key=len,
            reverse=True):

        pattern = (
            r"\b"
            + re.escape(phrase)
            + r"\b"
        )

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE
        )

    return normalize_spaces(text)


##########################################################
# Mongo Search Helpers
##########################################################

def search_constraint(text):

    """
    Returns first matching constraint.
    """

    records = load_constraints()

    text_lower = text.lower()

    for record in records:

        keyword = record["keyword"].lower()

        if keyword in text_lower:

            return record

    return None


def search_explicit(text):

    """
    Returns first matching explicit rule.
    """

    records = load_explicits()

    text_lower = text.lower()

    for record in records:

        keyword = record["keyword"].lower()

        if keyword in text_lower:

            return record

    return None


##########################################################
# Cache Search Helper
##########################################################

def search_cache(request: str):

    """
    Returns cached response if found.
    """

    cursor = cache_col.find()

    request = request.lower()

    for doc in cursor:

        if doc["request"].lower() in request:

            return doc

    return None


##########################################################
# Prompt Builders
##########################################################

def append_constraint(
        prompt,
        audience,
        length,
        format_
):

    return f"""
{prompt}

Audience:
{audience}

Expected Length:
{length}

Output Format:
{format_}
""".strip()


def append_explicit(
        prompt,
        role,
        tasks,
        tools
):

    tasks_text = "\n".join(
        f"- {x}"
        for x in tasks
    )

    tools_text = "\n".join(
        f"- {x}"
        for x in tools
    )

    return f"""
Role

{role}

Tasks

{tasks_text}

Tools

{tools_text}

Prompt

{prompt}
""".strip()


##########################################################
# Health Endpoint
##########################################################

@app.get("/")
def health():

    return {

        "status": "running",

        "service": "Gatekeeper AI Agent"

    }

##########################################################
#
# LeanContent()
#
##########################################################

def LeanContent(text: str) -> str:
    """
    Removes fillers, hedges, gestures and courtesy
    expressions from the input text.
    """

    logger.info("Executing LeanContent()")

    fillers = load_words(fillers_col)
    hedges = load_words(hedges_col)
    gestures = load_words(gestures_col)
    courtesy = load_words(courtesy_col)

    cleaned = text

    cleaned = remove_phrases(cleaned, fillers)
    cleaned = remove_phrases(cleaned, hedges)
    cleaned = remove_phrases(cleaned, gestures)
    cleaned = remove_phrases(cleaned, courtesy)

    cleaned = normalize_spaces(cleaned)

    return cleaned


##########################################################
#
# AddConstraint()
#
##########################################################

def AddConstraint(text: str) -> Dict[str, Any]:
    """
    Finds a matching constraint based on keyword.

    Mongo Collection

    constraints

    {
        keyword,
        audience,
        length,
        format
    }
    """

    logger.info("Executing AddConstraint()")

    record = search_constraint(text)

    if record is None:

        return {

            "audience": "",

            "length": "",

            "format": "",

            "updated_prompt": text

        }

    updated_prompt = append_constraint(

        prompt=text,

        audience=record["audience"],

        length=record["length"],

        format_=record["format"]

    )

    return {

        "audience": record["audience"],

        "length": record["length"],

        "format": record["format"],

        "updated_prompt": updated_prompt

    }


##########################################################
#
# AddExplicit()
#
##########################################################

def AddExplicit(text: str) -> Dict[str, Any]:
    """
    Finds explicit prompt engineering
    metadata from MongoDB.
    """

    logger.info("Executing AddExplicit()")

    record = search_explicit(text)

    if record is None:

        return {

            "role": "",

            "tasks": [],

            "tools": [],

            "updated_prompt": text

        }

    tasks = record.get("tasks", [])

    tools = record.get("tools", [])

    if isinstance(tasks, str):
        tasks = [tasks]

    if isinstance(tools, str):
        tools = [tools]

    updated_prompt = append_explicit(

        prompt=text,

        role=record["role"],

        tasks=tasks,

        tools=tools

    )

    return {

        "role": record["role"],

        "tasks": tasks,

        "tools": tools,

        "updated_prompt": updated_prompt

    }


##########################################################
#
# CheckReusability()
#
##########################################################

def CheckReusability(text: str) -> Dict[str, Any]:
    """
    Checks cachelist collection
    for reusable response.

    Returns

    {
        cached: bool,
        response: str
    }
    """

    logger.info("Executing CheckReusability()")

    cache = search_cache(text)

    if cache:

        logger.info("Cache Hit")

        return {

            "cached": True,

            "response": cache["response"],

            "request": cache["request"],

            "responsetime":
                cache.get("responsetime"),

            "cacheddatetime":
                cache.get("cacheddatetime")

        }

    logger.info("Cache Miss")

    return {

        "cached": False,

        "response": ""

    }


##########################################################
#
# UpdateCacheList()
#
##########################################################

def UpdateCacheList(
    request: str,
    response: str,
    responsetime: float,
    cacheddatetime: datetime
):
    """
    Inserts a response
    into cachelist.
    """

    logger.info("Updating cache.")

    document = {

        "request": request,

        "response": response,

        "responsetime": responsetime,

        "cacheddatetime": cacheddatetime

    }

    cache_col.insert_one(document)

    return {

        "status": "cached"

    }


##########################################################
#
# Individual API Endpoints
#
##########################################################

@app.post("/LeanContent")
def lean_content_api(request: TextRequest):

    return {

        "cleaned":

            LeanContent(request.text)

    }


@app.post(
    "/AddConstraint",
    response_model=ConstraintResponse
)
def constraint_api(request: TextRequest):

    return AddConstraint(request.text)


@app.post(
    "/AddExplicit",
    response_model=ExplicitResponse
)
def explicit_api(request: TextRequest):

    return AddExplicit(request.text)


@app.post("/CheckReusability")
def reusability_api(request: TextRequest):

    return CheckReusability(request.text)


@app.post("/UpdateCacheList")
def cache_api(request: CacheRequest):

    return UpdateCacheList(

        request.request,

        request.response,

        request.responsetime,

        request.cacheddatetime

    )


##########################################################
#
# Timing Decorator
#
##########################################################

def timed(function):

    def wrapper(*args, **kwargs):

        start = time.time()

        result = function(*args, **kwargs)

        elapsed = time.time() - start

        logger.info(
            f"{function.__name__} "
            f"completed in "
            f"{elapsed:.3f} seconds"
        )

        return result

    return wrapper


##########################################################
#
# Timed Versions
#
##########################################################

LeanContent = timed(LeanContent)

AddConstraint = timed(AddConstraint)

AddExplicit = timed(AddExplicit)

CheckReusability = timed(CheckReusability)

UpdateCacheList = timed(UpdateCacheList)

##########################################################
#
# LLM Client
#
##########################################################

def call_llm(prompt: str) -> str:
    """
    Calls low-cost LLM configured in MongoDB.
    """

    logger.info("Calling LowCostLLM")

    config = load_llm()

    provider = config.get("provider")

    model = config.get("model")

    endpoint = config.get("endpoint")

    api_key = config.get("apikey")

    payload = {

        "model": model,

        "input": prompt

    }

    headers = {

        "Content-Type": "application/json",

        "Authorization": f"Bearer {api_key}"

    }

    try:

        response = requests.post(

            endpoint,

            json=payload,

            headers=headers,

            timeout=30

        )

        response.raise_for_status()

        result = response.json()

        # generic response extraction
        return (
            result.get("output")
            or result.get("response")
            or str(result)
        )

    except Exception as e:

        logger.error(f"LLM call failed: {e}")

        raise HTTPException(
            status_code=500,
            detail="LLM call failed"
        )


##########################################################
#
# AddArchitected()
#
##########################################################

def AddArchitected(text: str) -> str:
    """
    Uses LowCostLLM to structure prompt
    into headings, lists, paragraphs.
    """

    logger.info("Executing AddArchitected()")

    system_instruction = """
Rewrite the following prompt for clarity.

Rules:
- Add headings
- Add bullet points where needed
- Add numbered lists if steps exist
- Do NOT change meaning
- Keep technical accuracy intact
"""

    final_prompt = f"""
{system_instruction}

INPUT:
{text}
""".strip()

    return call_llm(final_prompt)


##########################################################
#
# Gatekeeper Orchestrator
#
##########################################################

class GatekeeperAgent:

    """
    Orchestrates all skills:
    - Cache
    - Cleaning
    - Constraint enrichment
    - Explicit role injection
    - LLM structuring
    """

    def process(self, text: str):

        logger.info("Gatekeeper pipeline started")

        # STEP 1: Cache Check
        cache = CheckReusability(text)

        if cache["cached"]:

            logger.info("Returning cached response")

            return {

                "source": "cache",

                "response": cache["response"]

            }

        # STEP 2: Clean text
        cleaned = LeanContent(text)

        # STEP 3: Add constraints
        constraint = AddConstraint(cleaned)

        prompt = constraint["updated_prompt"]

        # STEP 4: Add explicit structure
        explicit = AddExplicit(prompt)

        prompt = explicit["updated_prompt"]

        # STEP 5: Architected LLM formatting
        structured = AddArchitected(prompt)

        final_prompt = structured

        # STEP 6: Return intermediate (LLM output)
        logger.info("Pipeline complete")

        return {

            "source": "generated",

            "response": final_prompt

        }


##########################################################
#
# Global Agent Instance
#
##########################################################

agent = GatekeeperAgent()


##########################################################
#
# Gatekeeper Main Endpoint
#
##########################################################

@app.post("/gatekeeper")
def gatekeeper_endpoint(request: PromptRequest):
    """
    Main orchestration endpoint.

    Flow:
    1. Check cache
    2. Clean content
    3. Add constraints
    4. Add explicit roles/tasks/tools
    5. Structure via LLM
    6. Return response
    """

    logger.info("Received request at /gatekeeper")

    result = agent.process(request.prompt)

    return {

        "input": request.prompt,

        "source": result["source"],

        "output": result["response"]

    }


##########################################################
#
# Debug Endpoint: Pipeline Step Preview
#
##########################################################

@app.post("/debug/pipeline")
def debug_pipeline(request: PromptRequest):

    """
    Returns intermediate transformations
    without calling LLM.
    """

    text = request.prompt

    cache = CheckReusability(text)

    cleaned = LeanContent(text)

    constraint = AddConstraint(cleaned)

    explicit = AddExplicit(constraint["updated_prompt"])

    return {

        "cache_check": cache,

        "lean_content": cleaned,

        "constraint": constraint,

        "explicit": explicit

    }


##########################################################
#
# Debug Endpoint: LLM Only
#
##########################################################

@app.post("/debug/llm")
def debug_llm(request: PromptRequest):

    """
    Sends only Architected prompt to LLM.
    """

    structured = AddArchitected(request.prompt)

    return {

        "llm_output": structured

    }


##########################################################
#
# Startup Validation Hook
#
##########################################################

@app.on_event("startup")
def startup_check():

    logger.info("Running startup validation...")

    # Validate Mongo connection
    try:

        db.list_collection_names()

        logger.info("MongoDB connection OK")

    except Exception as e:

        logger.error(f"MongoDB connection failed: {e}")

        raise e

    # Validate LLM config
    try:

        config = load_llm()

        assert "endpoint" in config

        assert "model" in config

        logger.info("LLM configuration OK")

    except Exception as e:

        logger.error(f"LLM configuration invalid: {e}")

        raise e

    logger.info("Gatekeeper startup complete")


##########################################################
#
# Root Endpoint (Enhanced)
#
##########################################################

@app.get("/")
def root():

    return {

        "service": "Gatekeeper AI Agent",

        "status": "active",

        "endpoints": {

            "gatekeeper": "/gatekeeper",

            "lean_content": "/LeanContent",

            "constraint": "/AddConstraint",

            "explicit": "/AddExplicit",

            "cache_check": "/CheckReusability",

            "cache_update": "/UpdateCacheList",

            "debug_pipeline": "/debug/pipeline",

            "debug_llm": "/debug/llm"

        }

    }


##########################################################
#
# Optional: Manual Pipeline Trigger (Dev Mode)
#
##########################################################

@app.post("/dev/run-all")
def dev_run_all(request: PromptRequest):

    """
    Runs full pipeline step-by-step
    and returns full trace.
    """

    text = request.prompt

    trace = {}

    trace["cache"] = CheckReusability(text)

    if trace["cache"]["cached"]:

        return {

            "source": "cache",

            "trace": trace,

            "output": trace["cache"]["response"]

        }

    trace["lean"] = LeanContent(text)

    trace["constraint"] = AddConstraint(trace["lean"])

    trace["explicit"] = AddExplicit(
        trace["constraint"]["updated_prompt"]
    )

    trace["architected"] = AddArchitected(
        trace["explicit"]["updated_prompt"]
    )

    return {

        "source": "generated",

        "trace": trace,

        "output": trace["architected"]

    }


##########################################################
#
# FINAL MESSAGE
#
##########################################################

logger.info("Gatekeeper API fully initialized")
