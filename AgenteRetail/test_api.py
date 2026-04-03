"""
Script de prueba para verificar que la API funciona correctamente
Ejecutar: python test_api.py
"""

import requests
import json

# Cambiar esta URL cuando despliegues en Render
BASE_URL = "http://localhost:8000"

def test_health():
    """Prueba el endpoint de health check"""
    print("\n🔍 Probando Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200

def test_buscar_zapatos():
    """Prueba el endpoint de búsqueda"""
    print("\n🔍 Probando Búsqueda de Zapatos...")
    
    # Prueba 1: Buscar Nike
    print("\n--- Búsqueda: Nike ---")
    response = requests.post(f"{BASE_URL}/buscar_zapatos?marca=Nike&limite=3")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total resultados: {data['total_resultados']}")
    print(f"Mensaje: {data['mensaje']}")
    if data['zapatos']:
        print(f"Primer resultado: {data['zapatos'][0]['marca']} {data['zapatos'][0]['modelo']}")
    
    # Prueba 2: Buscar por tipo y precio
    print("\n--- Búsqueda: Running con precio máximo $2000 ---")
    response = requests.post(f"{BASE_URL}/buscar_zapatos?tipo=Running&precio_max=2000")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total resultados: {data['total_resultados']}")
    print(f"Mensaje: {data['mensaje']}")
    
    # Prueba 3: Buscar por talla
    print("\n--- Búsqueda: Talla 25 ---")
    response = requests.post(f"{BASE_URL}/buscar_zapatos?talla=25&limite=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total resultados: {data['total_resultados']}")
    
    return response.status_code == 200

def test_recomendar_zapatos():
    """Prueba el endpoint de recomendaciones"""
    print("\n🔍 Probando Recomendaciones de Zapatos...")
    
    # Prueba 1: Recomendaciones para correr
    print("\n--- Recomendación: Para correr ---")
    response = requests.post(f"{BASE_URL}/recomendar_zapatos?uso=correr&limite=3")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total recomendaciones: {data['total']}")
    print(f"Razón: {data['razon']}")
    if data['recomendaciones']:
        print(f"Primera recomendación: {data['recomendaciones'][0]['marca']} {data['recomendaciones'][0]['modelo']}")
    
    # Prueba 2: Recomendaciones casuales con presupuesto
    print("\n--- Recomendación: Casual con presupuesto $2000 ---")
    response = requests.post(f"{BASE_URL}/recomendar_zapatos?uso=casual&presupuesto=2000&limite=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total recomendaciones: {data['total']}")
    print(f"Razón: {data['razon']}")
    
    # Prueba 3: Recomendaciones para trabajo
    print("\n--- Recomendación: Para trabajo ---")
    response = requests.post(f"{BASE_URL}/recomendar_zapatos?uso=trabajo&genero=Unisex")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total recomendaciones: {data['total']}")
    
    return response.status_code == 200

def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("🧪 PRUEBAS DE LA API - GRUPO NASAN")
    print("=" * 60)
    
    try:
        # Verificar que el servidor está corriendo
        print(f"\n📡 Conectando a: {BASE_URL}")
        response = requests.get(BASE_URL)
        print("✅ Servidor está corriendo")
        
        # Ejecutar pruebas
        results = []
        results.append(("Health Check", test_health()))
        results.append(("Búsqueda de Zapatos", test_buscar_zapatos()))
        results.append(("Recomendaciones", test_recomendar_zapatos()))
        
        # Resumen
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE PRUEBAS")
        print("=" * 60)
        for name, passed in results:
            status = "✅ PASÓ" if passed else "❌ FALLÓ"
            print(f"{name}: {status}")
        
        all_passed = all(result[1] for result in results)
        if all_passed:
            print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
            print("✅ La API está lista para desplegarse en Render")
        else:
            print("\n⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: No se pudo conectar a {BASE_URL}")
        print("Asegúrate de que el servidor está corriendo:")
        print("  python main.py")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()

# Made with Bob
