# uv run fastmcp dev inspector mcp_server.py
import os
import requests
from fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("Django-API-Reader")

# Configuration for your Django Backend
DJANGO_API_URL = os.getenv("DJANGO_API_URL", "http://127.0.0.1:8000/api")

def get_headers():
    return {
        "Content-Type": "application/json"
    }

# --- MCP RESOURCES (Read-only data endpoints) ---

@mcp.resource("django://menu-items/list")
def list_menu_items() -> str:
    """Fetches a full list of menu items from the Django REST API."""
    try:
        response = requests.get(f"{DJANGO_API_URL}/menu-items/", headers=get_headers())
        response.raise_for_status()
        return response.text # Returns raw JSON string to the AI
    except requests.RequestException as e:
        return f"Error connecting to Django backend: {str(e)}"

# --- MCP TOOLS (Parametrized read or action endpoints) ---

@mcp.tool()
def get_menu_item_details(menu_item_id: int) -> dict:
    """
    Retrieves detailed information about a specific menu item by ID from the Django backend.
    """
    try:
        response = requests.get(f"{DJANGO_API_URL}/menu-items/{menu_item_id}/", headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch menu item {menu_item_id}: {str(e)}"}

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8585)