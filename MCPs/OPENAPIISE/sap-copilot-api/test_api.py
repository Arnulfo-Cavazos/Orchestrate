"""
Script de prueba simple para verificar que la API funciona correctamente
"""
import sys
import os

# Agregar el directorio app al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from main import app, load_materials, load_inventory, load_production_orders, load_demand_forecast
    print("✓ Importación exitosa de módulos")
    
    # Probar carga de datos
    print("\n--- Probando carga de datos CSV ---")
    
    materials = load_materials()
    print(f"✓ Materiales cargados: {len(materials)} registros")
    
    inventory = load_inventory()
    print(f"✓ Inventario cargado: {len(inventory)} registros")
    
    orders = load_production_orders()
    print(f"✓ Órdenes de producción cargadas: {len(orders)} registros")
    
    forecast = load_demand_forecast()
    print(f"✓ Pronóstico de demanda cargado: {len(forecast)} registros")
    
    print("\n--- Verificando estructura de la API ---")
    print(f"✓ Título de la API: {app.title}")
    print(f"✓ Versión: {app.version}")
    print(f"✓ Rutas disponibles: {len(app.routes)}")
    
    print("\n✅ Todas las pruebas básicas pasaron exitosamente!")
    print("\nPara iniciar el servidor, ejecuta:")
    print("  python app/main.py")
    print("  o")
    print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
except Exception as e:
    print(f"\n❌ Error durante las pruebas: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Made with Bob
