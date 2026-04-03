# 🤖 Ejemplos de Uso con watsonx Orchestrate

## Cómo el Agente Usa las Tools

Una vez importadas las tools en watsonx Orchestrate, el agente puede responder automáticamente a consultas de clientes sobre zapatos.

## 📝 Ejemplos de Conversaciones

### Ejemplo 1: Búsqueda Específica

**Cliente**: "Busco tenis Nike para correr"

**Agente** (internamente usa `buscar_zapatos`):
```
Parámetros: marca=Nike, tipo=Running
```

**Respuesta del Agente**:
```
Encontré 3 opciones de tenis Nike para correr:

1. Nike Revolution 6 - $1,599
   - Color: Negro
   - Tallas: 22-30
   - Stock: 55 unidades
   - Descripción: Tenis para correr económicos y cómodos

2. Nike Pegasus 39 - $2,999
   - Color: Azul
   - Tallas: 23-30
   - Stock: 33 unidades
   - Descripción: Tenis versátiles para correr con amortiguación React

3. Nike Air Max 270 - $2,499
   - Color: Negro
   - Tallas: 22-30
   - Stock: 45 unidades
   - Descripción: Zapatillas deportivas con tecnología Air Max

¿Te gustaría más información sobre alguno de estos modelos?
```

---

### Ejemplo 2: Búsqueda con Presupuesto

**Cliente**: "Necesito zapatos casuales blancos de menos de $2000"

**Agente** (usa `buscar_zapatos`):
```
Parámetros: tipo=Casual, color=Blanco, precio_max=2000
```

**Respuesta del Agente**:
```
Perfecto, encontré 4 opciones de zapatos casuales blancos dentro de tu presupuesto:

1. Reebok Classic Leather - $1,699
   - Tallas: 23-30
   - Stock: 41 unidades
   - Tenis clásicos de piel para estilo casual

2. Converse Chuck Taylor All Star - $1,299
   - Tallas: 20-30
   - Stock: 67 unidades
   - Zapatillas icónicas de lona para todos los días

3. Fila Disruptor II - $1,799
   - Tallas: 22-28
   - Stock: 42 unidades
   - Zapatillas chunky con estilo retro de los 90s

4. Nike Court Vision Low - $1,799
   - Tallas: 22-30
   - Stock: 49 unidades
   - Zapatillas inspiradas en el básquetbol clásico

Todos están disponibles y dentro de tu presupuesto de $2,000.
```

---

### Ejemplo 3: Recomendaciones

**Cliente**: "¿Qué zapatos me recomiendas para ir al trabajo?"

**Agente** (usa `recomendar_zapatos`):
```
Parámetros: uso=trabajo, limite=5
```

**Respuesta del Agente**:
```
Para ir al trabajo, te recomiendo estos zapatos cómodos y elegantes:

1. Skechers Go Walk 6 - $1,899
   - Color: Gris
   - Zapatillas ultra cómodas para caminar
   - Perfectas para estar de pie todo el día

2. Adidas Stan Smith - $2,099
   - Color: Verde
   - Tenis minimalistas con diseño elegante
   - Versátiles para ambiente casual de oficina

3. Converse Chuck Taylor All Star - $1,299
   - Color: Negro
   - Clásicas y profesionales
   - Cómodas para todo el día

4. Reebok Classic Leather - $1,699
   - Color: Blanco
   - Estilo limpio y profesional
   - Muy cómodas

5. New Balance 574 Core - $2,199
   - Color: Gris
   - Diseño discreto y cómodo
   - Ideales para largas jornadas

Estas opciones combinan comodidad y estilo profesional. ¿Te interesa alguna en particular?
```

---

### Ejemplo 4: Búsqueda por Talla

**Cliente**: "Tengo talla 26, ¿qué opciones hay?"

**Agente** (usa `buscar_zapatos`):
```
Parámetros: talla=26, limite=10
```

**Respuesta del Agente**:
```
¡Excelente! Tenemos 28 modelos disponibles en talla 26. Aquí están los más populares:

1. Nike Air Max 270 - $2,499 (Deportivo, Negro)
2. Adidas Ultraboost 22 - $3,299 (Running, Blanco)
3. Puma Suede Classic - $1,899 (Casual, Azul)
4. Converse Chuck Taylor - $1,299 (Casual, Negro)
5. Vans Old Skool - $1,499 (Skate, Negro)

¿Buscas algún tipo específico? Puedo filtrar por deporte, casual, running, etc.
```

---

### Ejemplo 5: Recomendación con Presupuesto

**Cliente**: "Quiero empezar a correr, tengo $2500 de presupuesto"

**Agente** (usa `recomendar_zapatos`):
```
Parámetros: uso=correr, presupuesto=2500
```

**Respuesta del Agente**:
```
¡Genial que quieras empezar a correr! Aquí están mis mejores recomendaciones dentro de tu presupuesto:

1. Nike Revolution 6 - $1,599 ⭐ MEJOR PRECIO
   - Económicos pero de calidad
   - Perfectos para principiantes
   - Stock: 55 unidades

2. Under Armour Charged Assert 9 - $1,999
   - Amortiguación Charged
   - Muy cómodos
   - Stock: 31 unidades

3. Adidas Ultraboost 22 - $2,299 (Ligeramente sobre presupuesto)
   - Tecnología Boost premium
   - Retorno de energía
   - Stock: 32 unidades

Para empezar, te recomiendo especialmente el Nike Revolution 6. Es económico, cómodo y perfecto para principiantes. ¿Te gustaría saber más sobre alguno?
```

---

### Ejemplo 6: Consulta Compleja

**Cliente**: "Necesito zapatos Adidas o Nike, casuales o deportivos, que no pasen de $2500"

**Agente** (usa `buscar_zapatos` dos veces o con lógica):
```
Primera búsqueda: marca=Nike, precio_max=2500
Segunda búsqueda: marca=Adidas, precio_max=2500
```

**Respuesta del Agente**:
```
Encontré 8 opciones que cumplen tus criterios:

NIKE:
1. Air Max 270 - $2,499 (Deportivo, Negro)
2. Revolution 6 - $1,599 (Running, Negro)
3. Court Vision Low - $1,799 (Casual, Blanco)

ADIDAS:
1. Ultraboost 22 - $2,299 (Running, Blanco)
2. Stan Smith - $2,099 (Casual, Verde)
3. Superstar - $2,299 (Casual, Blanco)
4. NMD R1 - $2,299 (Casual, Negro)
5. ZX 2K Boost - $2,499 (Casual, Gris)

Todas están dentro de tu presupuesto de $2,500. ¿Prefieres algo más deportivo o casual?
```

---

## 🎯 Casos de Uso del Agente

### 1. Búsqueda Directa (`buscar_zapatos`)
El agente usa este endpoint cuando el cliente:
- Menciona una marca específica
- Busca un tipo concreto (running, casual, etc.)
- Especifica color, talla o precio
- Quiere ver opciones específicas

### 2. Recomendaciones (`recomendar_zapatos`)
El agente usa este endpoint cuando el cliente:
- Pregunta "¿qué me recomiendas?"
- Menciona una actividad (correr, caminar, trabajo)
- No sabe qué buscar
- Pide sugerencias

### 3. Combinación de Ambos
El agente puede usar ambos endpoints en una conversación:
1. Primero recomienda con `recomendar_zapatos`
2. Luego refina con `buscar_zapatos` según feedback

---

## 💡 Tips para el Agente

### Información que Siempre Debe Incluir:
- ✅ Marca y modelo
- ✅ Precio
- ✅ Rango de tallas disponibles
- ✅ Stock disponible
- ✅ Descripción breve

### Información Adicional Útil:
- 🎨 Color
- 👥 Género (Hombre/Mujer/Unisex)
- 🏃 Tipo de uso
- 💰 Comparación de precios

### Preguntas de Seguimiento Sugeridas:
- "¿Te gustaría ver más opciones?"
- "¿Prefieres otro color?"
- "¿Necesitas una talla específica?"
- "¿Tienes un presupuesto en mente?"
- "¿Para qué actividad los necesitas?"

---

## 🔄 Flujo de Conversación Típico

```
Cliente: "Hola, busco zapatos"
  ↓
Agente: "¡Hola! ¿Qué tipo de zapatos buscas? ¿Para correr, casual, trabajo?"
  ↓
Cliente: "Para correr"
  ↓
Agente: [usa recomendar_zapatos con uso=correr]
  ↓
Agente: "Te recomiendo estos 5 modelos para correr..."
  ↓
Cliente: "¿Tienes algo más barato?"
  ↓
Agente: [usa recomendar_zapatos con uso=correr, presupuesto=2000]
  ↓
Agente: "Claro, aquí opciones más económicas..."
  ↓
Cliente: "Me gusta el Nike Revolution 6"
  ↓
Agente: "Excelente elección! Está disponible en talla 22-30, precio $1,599..."
```

---

## 📊 Métricas de Éxito

El agente debe poder:
- ✅ Responder en menos de 3 segundos
- ✅ Encontrar productos relevantes en el 95% de casos
- ✅ Proporcionar al menos 3 opciones cuando hay stock
- ✅ Manejar consultas ambiguas pidiendo clarificación
- ✅ Combinar múltiples criterios de búsqueda

---

**Nota**: Estos son ejemplos. El agente de watsonx Orchestrate generará respuestas naturales basadas en los datos de la API.