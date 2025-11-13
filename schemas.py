"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, Dict

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Industrial products for Oil & Gas
    Collection name: "product"
    """
    name: str = Field(..., description="Product name")
    category: str = Field(..., description="Category, e.g., Cryogenic Valves, Pumps, Drilling Sensors")
    short_description: Optional[str] = Field(None, description="Short marketing description")
    specs: Optional[Dict[str, str]] = Field(default=None, description="Key specifications as key-value pairs")
    image_url: Optional[HttpUrl] = Field(default=None, description="Product image URL")
    datasheet_url: Optional[HttpUrl] = Field(default=None, description="Link to product datasheet PDF")
    brand: Optional[str] = Field(default=None, description="OEM brand or manufacturer")
    model: Optional[str] = Field(default=None, description="Model number")
    in_stock: bool = Field(True, description="Stock availability")

class Inquiry(BaseModel):
    """
    RFQ/Contact inquiries from website
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Full name of requester")
    company: str = Field(..., description="Company name")
    email: EmailStr = Field(..., description="Work email")
    phone: Optional[str] = Field(None, description="Phone number")
    message: str = Field(..., description="Request details or message")
    product_id: Optional[str] = Field(None, description="Related product id (if any)")
