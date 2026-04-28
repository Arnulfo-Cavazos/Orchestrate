from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Union
from datetime import datetime, timedelta
import pandas as pd
import os
from pydantic import BaseModel, field_validator

app = FastAPI(
    title="SAP Copilot API",
    description="API para consultar datos de SAP (materiales, inventario, órdenes de producción)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

class Material(BaseModel):
    material_id: str
    material_name: str
    material_type: str
    unit_of_measure: str
    standard_price: float
    material_group: str

class InventoryItem(BaseModel):
    material_id: str
    material_name: str
    warehouse: str
    storage_location: str
    quantity: int
    reserved_quantity: int
    available_quantity: int
    last_updated: str

    # ✅ FIX: convierte warehouse y storage_location a string aunque vengan como int del CSV
    @field_validator('warehouse', 'storage_location', mode='before')
    @classmethod
    def coerce_to_str(cls, v):
        return str(v)

class ProductionOrder(BaseModel):
    order_id: str
    material_id: str
    material_name: str
    order_quantity: int
    produced_quantity: int
    status: str
    start_date: str
    due_date: str
    warehouse: str
    priority: str
    completion_percentage: float

    @field_validator('warehouse', mode='before')
    @classmethod
    def coerce_warehouse_to_str(cls, v):
        return str(v)

class CoverageAnalysis(BaseModel):
    material_id: str
    material_name: str
    current_stock: int
    reserved_quantity: int
    available_quantity: int
    total_demand_30_days: float
    coverage_days: float
    status: str
    recommendation: str

def load_materials():
    df = pd.read_csv(os.path.join(DATA_DIR, "materials.csv"))
    return df

def load_inventory():
    df = pd.read_csv(os.path.join(DATA_DIR, "inventory.csv"))
    return df

def load_production_orders():
    df = pd.read_csv(os.path.join(DATA_DIR, "production_orders.csv"))
    return df

def load_demand_forecast():
    df = pd.read_csv(os.path.join(DATA_DIR, "demand_forecast.csv"))
    return df

@app.get("/")
def read_root():
    return {
        "message": "SAP Copilot API - Bienvenido",
        "version": "1.0.0",
        "endpoints": {
            "materials": "/api/materials",
            "inventory": "/api/inventory/stock",
            "production_orders": "/api/production/orders",
            "coverage": "/api/inventory/coverage"
        }
    }

@app.get("/api/materials", response_model=List[Material])
def get_materials(
    material_id: Optional[str] = Query(None, description="ID del material"),
    material_name: Optional[str] = Query(None, description="Nombre del material")
):
    df = load_materials()
    if material_id:
        df = df[df['material_id'] == material_id]
    if material_name:
        df = df[df['material_name'].str.contains(material_name, case=False, na=False)]
    if df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron materiales")
    return df.to_dict('records')

@app.get("/api/inventory/stock", response_model=List[InventoryItem])
def get_inventory_stock(
    material_id: Optional[str] = Query(None, description="ID del material"),
    warehouse: Optional[str] = Query(None, description="Código del almacén"),
    min_quantity: Optional[int] = Query(None, description="Cantidad mínima disponible")
):
    inventory_df = load_inventory()
    materials_df = load_materials()
    df = inventory_df.merge(materials_df[['material_id', 'material_name']], on='material_id', how='left')
    if material_id:
        df = df[df['material_id'] == material_id]
    if warehouse:
        df = df[df['warehouse'].astype(str) == warehouse]  # ✅ comparar como string
    if min_quantity is not None:
        df = df[df['available_quantity'] >= min_quantity]
    if df.empty:
        raise HTTPException(status_code=404, detail="No se encontró inventario")
    return df.to_dict('records')

@app.get("/api/production/orders", response_model=List[ProductionOrder])
def get_production_orders(
    status: Optional[str] = Query(None, description="Estado de la orden"),
    warehouse: Optional[str] = Query(None, description="Almacén"),
    due_within_days: Optional[int] = Query(None, description="Vence en X días"),
    priority: Optional[str] = Query(None, description="Prioridad")
):
    orders_df = load_production_orders()
    materials_df = load_materials()
    df = orders_df.merge(materials_df[['material_id', 'material_name']], on='material_id', how='left')
    if status:
        df = df[df['status'] == status]
    if warehouse:
        df = df[df['warehouse'].astype(str) == warehouse]  # ✅ comparar como string
    if priority:
        df = df[df['priority'] == priority]
    if due_within_days is not None:
        today = datetime.now().date()
        target_date = today + timedelta(days=due_within_days)
        df['due_date_parsed'] = pd.to_datetime(df['due_date']).dt.date
        df = df[df['due_date_parsed'] <= target_date]
        df = df.drop('due_date_parsed', axis=1)
    df['completion_percentage'] = (df['produced_quantity'] / df['order_quantity'] * 100).round(2)
    if df.empty:
        raise HTTPException(status_code=404, detail="No se encontraron órdenes")
    return df.to_dict('records')

@app.get("/api/inventory/coverage", response_model=List[CoverageAnalysis])
def get_inventory_coverage(
    material_id: Optional[str] = Query(None, description="ID del material"),
    warehouse: Optional[str] = Query(None, description="Almacén"),
    days: int = Query(30, description="Días de cobertura a analizar")
):
    inventory_df = load_inventory()
    materials_df = load_materials()
    forecast_df = load_demand_forecast()
    today = datetime.now().date()
    end_date = today + timedelta(days=days)
    forecast_df['forecast_date'] = pd.to_datetime(forecast_df['forecast_date']).dt.date
    forecast_filtered = forecast_df[
        (forecast_df['forecast_date'] >= today) &
        (forecast_df['forecast_date'] <= end_date)
    ]
    demand_summary = forecast_filtered.groupby(['material_id', 'warehouse'])['forecasted_demand'].sum().reset_index()
    demand_summary.columns = ['material_id', 'warehouse', 'total_demand']
    df = inventory_df.merge(materials_df[['material_id', 'material_name']], on='material_id', how='left')
    df = df.merge(demand_summary, on=['material_id', 'warehouse'], how='left')
    df['total_demand'] = df['total_demand'].fillna(0)
    if material_id:
        df = df[df['material_id'] == material_id]
    if warehouse:
        df = df[df['warehouse'].astype(str) == warehouse]  # ✅ comparar como string
    df['coverage_days'] = df.apply(
        lambda row: (row['available_quantity'] / (row['total_demand'] / days)) if row['total_demand'] > 0 else 999,
        axis=1
    )
    df['coverage_days'] = df['coverage_days'].round(1)

    def get_status(coverage):
        if coverage >= 30:
            return "OPTIMO"
        elif coverage >= 15:
            return "ACEPTABLE"
        elif coverage >= 7:
            return "BAJO"
        else:
            return "CRITICO"

    def get_recommendation(row):
        if row['coverage_days'] < 7:
            return f"URGENTE: Ordenar {int(row['total_demand'] * 2)} unidades"
        elif row['coverage_days'] < 15:
            return f"Considerar ordenar {int(row['total_demand'])} unidades"
        elif row['coverage_days'] < 30:
            return "Monitorear consumo"
        else:
            return "Stock suficiente"

    df['status'] = df['coverage_days'].apply(get_status)
    df['recommendation'] = df.apply(get_recommendation, axis=1)
    result = df[[
        'material_id', 'material_name', 'quantity', 'reserved_quantity',
        'available_quantity', 'total_demand', 'coverage_days', 'status', 'recommendation'
    ]].rename(columns={
        'quantity': 'current_stock',
        'total_demand': 'total_demand_30_days'
    })
    if result.empty:
        raise HTTPException(status_code=404, detail="No se encontró análisis de cobertura")
    return result.to_dict('records')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)