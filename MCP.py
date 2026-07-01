"""
------------------------------------------------------------
MCP (Model Context Protocol) Layer
------------------------------------------------------------

Purpose:
- Expose internal API methods as tool-callable functions
- Provide schema for external organizations
- Enable dynamic tool discovery
- Support agent + LLM tool calling
------------------------------------------------------------
"""

from typing import Dict, Any, Callable
from utils.logger import get_logger

logger = get_logger("mcp")


##########################################################
# MCP Tool Registry
##########################################################

class MCPRegistry:

    def __init__(self):

        # tool_name -> tool_definition
        self.tools: Dict[str, Dict[str, Any]] = {}

    ######################################################
    # Register Tool
    ######################################################

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable
    ):

        logger.info(f"Registering MCP tool: {name}")

        self.tools[name] = {

            "name": name,

            "description": description,

            "input_schema": input_schema,

            "handler": handler

        }

    ######################################################
    # List Tools
    ######################################################

    def list_tools(self):

        return {

            "tools": [

                {

                    "name": t["name"],

                    "description": t["description"],

                    "input_schema": t["input_schema"]

                }

                for t in self.tools.values()

            ]

        }

    ######################################################
    # Execute Tool
    ######################################################

    def execute_tool(self, name: str, payload: dict):

        if name not in self.tools:

            raise Exception(f"Tool not found: {name}")

        tool = self.tools[name]

        logger.info(f"Executing MCP tool: {name}")

        return tool["handler"](**payload)


##########################################################
# Global Registry Instance
##########################################################

mcp_registry = MCPRegistry()


##########################################################
# Tool Registration Helpers
##########################################################

def register_default_tools(api_reference: dict):
    """
    Register core Gatekeeper API methods as MCP tools.
    """

    ######################################################
    # LeanContent Tool
    ######################################################

    mcp_registry.register_tool(

        name="LeanContent",

        description="Removes fillers, hedges, gestures, and courtesy expressions",

        input_schema={

            "type": "object",

            "properties": {

                "text": {

                    "type": "string"

                }

            }

        },

        handler=api_reference["LeanContent"]

    )

    ######################################################
    # AddConstraint Tool
    ######################################################

    mcp_registry.register_tool(

        name="AddConstraint",

        description="Adds audience, format, and length constraints",

        input_schema={

            "type": "object",

            "properties": {

                "text": {"type": "string"}

            }

        },

        handler=api_reference["AddConstraint"]

    )

    ######################################################
    # AddExplicit Tool
    ######################################################

    mcp_registry.register_tool(

        name="AddExplicit",

        description="Adds role, tasks, and tools metadata",

        input_schema={

            "type": "object",

            "properties": {

                "text": {"type": "string"}

            }

        },

        handler=api_reference["AddExplicit"]

    )

    ######################################################
    # CheckReusability Tool
    ######################################################

    mcp_registry.register_tool(

        name="CheckReusability",

        description="Checks cache for reusable responses",

        input_schema={

            "type": "object",

            "properties": {

                "text": {"type": "string"}

            }

        },

        handler=api_reference["CheckReusability"]

    )

    ######################################################
    # UpdateCache Tool
    ######################################################

    mcp_registry.register_tool(

        name="UpdateCacheList",

        description="Stores request/response in cache",

        input_schema={

            "type": "object",

            "properties": {

                "request": {"type": "string"},

                "response": {"type": "string"},

                "responsetime": {"type": "number"},

                "cacheddatetime": {"type": "string"}

            }

        },

        handler=api_reference["UpdateCacheList"]

    )


##########################################################
# MCP API Helpers (FastAPI Integration)
##########################################################

def get_mcp_manifest():

    """
    Returns full MCP tool manifest
    for external organizations.
    """

    return mcp_registry.list_tools()


def call_mcp_tool(name: str, payload: dict):

    """
    Execute a registered MCP tool.
    """

    return mcp_registry.execute_tool(name, payload)
