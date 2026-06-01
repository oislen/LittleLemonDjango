# uv run fastmcp dev inspector mcp_server.py
import os
import requests
from typing import Optional, Dict, Any
from fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("Django-API-Reader")

# Configuration for your Django Backend
# Note: In docker-compose, change this default to "http://web:8000/api" if your django service is named "web"
DJANGO_API_URL = os.getenv("DJANGO_API_URL", "http://127.0.0.1:8000/api")

def get_headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json"
    }

# =====================================================================
# --- MCP RESOURCES (Read-only data endpoints for bulk loading) -------
# =====================================================================

#@mcp.resource("django://categories/list")
#def list_categories() -> str:
#    """Fetches a full list of food categories from the Django REST API."""
#    try:
#        response = requests.get(f"{DJANGO_API_URL}/categories/", headers=get_headers())
#        response.raise_for_status()
#        return response.text
#    except requests.RequestException as e:
#        return f"Error connecting to Django backend categories endpoint: {str(e)}"

@mcp.resource("django://menu-items/list")
def list_menu_items() -> str:
    """Fetches a full list of menu items from the Django REST API."""
    try:
        response = requests.get(f"{DJANGO_API_URL}/menu-items/", headers=get_headers())
        response.raise_for_status()
        return response.text 
    except requests.RequestException as e:
        return f"Error connecting to Django backend menu items endpoint: {str(e)}"

#@mcp.resource("django://bookings/list")
#def list_bookings() -> str:
#    """Fetches a list of all table/restaurant bookings from the Django REST API."""
#    try:
#        response = requests.get(f"{DJANGO_API_URL}/bookings/", headers=get_headers())
#        response.raise_for_status()
#        return response.text
#    except requests.RequestException as e:
#        return f"Error connecting to Django backend bookings endpoint: {str(e)}"

#@mcp.resource("django://orders/list")
#def list_orders() -> str:
#    """Fetches a list of all customer orders from the Django REST API."""
#    try:
#        response = requests.get(f"{DJANGO_API_URL}/orders/", headers=get_headers())
#        response.raise_for_status()
#        return response.text
#    except requests.RequestException as e:
#        return f"Error connecting to Django backend orders endpoint: {str(e)}"

#@mcp.resource("django://users/list")
#def list_users() -> str:
#    """Fetches a system user list from the Django REST API."""
#    try:
#        response = requests.get(f"{DJANGO_API_URL}/users/", headers=get_headers())
#        response.raise_for_status()
#        return response.text
#    except requests.RequestException as e:
#        return f"Error connecting to Django backend users endpoint: {str(e)}"


# =====================================================================
# --- MCP TOOLS (Parameterized read or mutation action endpoints) -----
# =====================================================================

# --- CATEGORY TOOLS ---
#@mcp.tool()
#def get_category_details(category_id: int) -> Dict[str, Any]:
#    """Retrieves specific details about a food category by ID."""
#    try:
#        response = requests.get(f"{DJANGO_API_URL}/categories/{category_id}/", headers=get_headers())
#        response.raise_for_status()
#        return response.json()
#    except requests.RequestException as e:
#        return {"error": f"Failed to fetch category {category_id}: {str(e)}"}

#@mcp.tool()
#def create_category(name: str, slug: str) -> Dict[str, Any]:
#    """Creates a new food category in the system."""
#    try:
#        payload = {"name": name, "slug": slug}
#        response = requests.post(f"{DJANGO_API_URL}/categories/", json=payload, headers=get_headers())
#        response.raise_for_status()
#        return response.json()
#    except requests.RequestException as e:
#        return {"error": f"Failed to create category: {str(e)}"}


# --- MENU ITEM TOOLS ---
@mcp.tool()
def get_menu_item_details(menu_item_id: int) -> Dict[str, Any]:
    """Retrieves detailed information about a specific menu item by ID from the Django backend."""
    try:
        response = requests.get(f"{DJANGO_API_URL}/menu-items/{menu_item_id}/", headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch menu item {menu_item_id}: {str(e)}"}

#@mcp.tool()
#def create_menu_item(title: str, price: float, category_id: int, featured: bool = False) -> Dict[str, Any]:
#    """Creates a new menu item in the database system."""
#    try:
#        payload = {"title": title, "price": price, "category": category_id, "featured": featured}
#        response = requests.post(f"{DJANGO_API_URL}/menu-items/", json=payload, headers=get_headers())
#        response.raise_for_status()
#        return response.json()
#    except requests.RequestException as e:
#        return {"error": f"Failed to create menu item: {str(e)}"}


# --- BOOKING TOOLS ---
#@mcp.tool()
#def create_booking(first_name: str, reservation_date: str, reservation_slot: int) -> Dict[str, Any]:
#    """
#    Creates a restaurant table booking. 
#    reservation_date should follow the format 'YYYY-MM-DD'.
#    """
#    try:
#        payload = {
#            "first_name": first_name, 
#            "reservation_date": reservation_date, 
#            "reservation_slot": reservation_slot
#        }
#        response = requests.post(f"{DJANGO_API_URL}/bookings/", json=payload, headers=get_headers())
#        response.raise_for_status()
#        return response.json()
#    except requests.RequestException as e:
#        return {"error": f"Failed to establish booking: {str(e)}"}

#@mcp.tool()
#def get_booking_details(booking_id: int) -> Dict[str, Any]:
#    """Retrieves complete details of an individual reservation booking by ID."""
#    try:
#        response = requests.get(f"{DJANGO_API_URL}/bookings/{booking_id}/", headers=get_headers())
#        response.raise_for_status()
#        return response.json()
#    except requests.RequestException as e:
#        return {"error": f"Failed to fetch booking {booking_id}: {str(e)}"}

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8585)