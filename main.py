import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Product, Inquiry

app = FastAPI(title="OGX Industrial Supply API", description="B2B Oil & Gas industrial equipment supplier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "OGX Industrial Supply Backend is running"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response


# -------------------- Products Endpoints --------------------
@app.post("/api/products", response_model=dict)
def create_product(product: Product):
    try:
        new_id = create_document("product", product)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products", response_model=List[dict])
def list_products(category: Optional[str] = None, limit: int = 24):
    try:
        filter_q = {"category": category} if category else {}
        docs = get_documents("product", filter_q, limit)
        # Convert ObjectId to str
        for d in docs:
            d["id"] = str(d.get("_id"))
            d.pop("_id", None)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/products/seed", response_model=dict)
def seed_products():
    """Seed database with sample Oil & Gas products if empty or missing."""
    try:
        samples: List[Product] = [
            Product(
                name="Cryogenic Solenoid Valve",
                category="Cryogenic Valves",
                short_description="Stainless steel cryogenic solenoid valve for LNG service",
                specs={"size": "1/2\"", "rating": "Class 600", "temp": "-196°C"},
                image_url=None,
                datasheet_url="https://example.com/datasheets/cryogenic-solenoid.pdf",
                brand="CryoFlow",
                model="CSV-600",
                in_stock=True,
            ),
            Product(
                name="API Process Pump",
                category="Process Pumps",
                short_description="Horizontal end-suction process pump per API 610",
                specs={"capacity": "120 m3/h", "head": "80 m", "material": "A216 WCB"},
                image_url=None,
                datasheet_url="https://example.com/datasheets/api610-pump.pdf",
                brand="ProPump",
                model="PP-610",
                in_stock=True,
            ),
            Product(
                name="Mud Logging Sensor",
                category="Drilling Sensors",
                short_description="Real-time drilling mud density & flow sensor",
                specs={"range": "0-3 SG", "protocol": "Modbus RTU"},
                image_url=None,
                datasheet_url="https://example.com/datasheets/mud-sensor.pdf",
                brand="DrillSense",
                model="MS-300",
                in_stock=False,
            ),
            Product(
                name="Cryogenic Globe Valve",
                category="Cryogenic Valves",
                short_description="Extended bonnet globe valve for LNG cold service",
                specs={"size": "2\"", "rating": "Class 300", "material": "CF8M"},
                image_url=None,
                datasheet_url="https://example.com/datasheets/cryogenic-globe.pdf",
                brand="ArcticValve",
                model="CGV-300",
                in_stock=True,
            ),
            Product(
                name="Multistage Boiler Feed Pump",
                category="Process Pumps",
                short_description="High-pressure boiler feed pump for utilities",
                specs={"stages": "6", "pressure": "35 bar"},
                image_url=None,
                datasheet_url="https://example.com/datasheets/boiler-feed.pdf",
                brand="ThermoFlow",
                model="BFP-6S",
                in_stock=True,
            ),
            Product(
                name="Downhole Pressure Sensor",
                category="Drilling Sensors",
                short_description="High-temp downhole pressure sensor for MWD",
                specs={"pressure": "20k psi", "temp": "175°C"},
                image_url=None,
                datasheet_url="https://example.com/datasheets/downhole-pressure.pdf",
                brand="GeoProbe",
                model="DPS-20K",
                in_stock=False,
            ),
        ]

        inserted = 0
        for p in samples:
            # check duplicate by name+model
            exists = get_documents("product", {"name": p.name, "model": p.model}, limit=1)
            if not exists:
                create_document("product", p)
                inserted += 1

        return {"status": "ok", "inserted": inserted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------- Inquiries (RFQ) Endpoints --------------------
@app.post("/api/inquiries", response_model=dict)
def create_inquiry(inquiry: Inquiry):
    try:
        new_id = create_document("inquiry", inquiry)
        return {"id": new_id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
