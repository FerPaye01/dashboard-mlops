---
trigger: always_on
---

# 📜 Instrucciones de Comportamiento

Patrones de trabajo y convenciones del proyecto.

---

## Naming Conventions
- Todos los nombres de **variables, funciones, clases, archivos y directorios** deben estar en **ESPAÑOL**.
- El texto visible para el usuario final (UI) también en **ESPAÑOL**.

### Variables y Funciones — `snake_Mayus`
- Variables: `snake_Mayus` → `datos_Usuario`, `lista_Tarjetas`
- Funciones: `snake_Mayus` → `obtener_Tarjeta()`, `guardar_Datos()`
- Clases: `Pascal_Mayus` → `Gestor_Tarjetas`, `Servicio_Usuario`
- Constantes: `SCREAMING_SNAKE_CASE` → `MAX_REINTENTOS`, `URL_API`

### Archivos y Directorios
- Directorios: `kebab-case` o minúsculas → `components/`, `pages/`, `utils/`, `styles/`
- Componentes: `snake_case` con extensión → `lista_tarjetas.js`
- Estilos: `snake_case` con extensión → `lista_tarjetas.css`
- Utilidades: `snake_case` con extensión → `logger.js`

### Comentarios
- En **español** (para legibilidad del equipo)
- Breves y directos
- Un comentario por función explicando el propósito

---

## Logging Obligatorio

Toda función importante debe registrar su inicio, fin y estados internos relevantes. El sistema de logging se define por capa tecnológica — **no depende de ningún archivo externo**, debe recrearse si no existe.

### 🟡 Capa JavaScript / TypeScript (Angular, Node)

Implementar una función `log` local o en `utils/logger.js` con esta convención:

| Nivel | Cuándo usarlo | Ejemplo |
|-------|---------------|---------|
| `LOG_DEBUG` | Detalles técnicos internos | `log('DEBUG', 'valor_X', x)` |
| `LOG_INFO` | Información general del flujo | `log('INFO', 'proceso iniciado')` |
| `LOG_WARN` | Situación inesperada no crítica | `log('WARN', 'dato faltante')` |
| `LOG_ERROR` | Error crítico con contexto | `log('ERROR', 'fallo al guardar', error)` |

```javascript
// Función de log autocontenida — recrear si no existe
function log(nivel, mensaje, datos = null) {
  const entrada = `[${nivel}] ${mensaje}`
  datos ? console.log(entrada, datos) : console.log(entrada)
}
```

### 🐍 Capa Python (FastAPI, scripts)

Usar el módulo estándar `logging` de Python con esta convención:

| Nivel | Cuándo usarlo | Ejemplo |
|-------|---------------|---------|
| `LOG_DEBUG` | Detalles técnicos | `logger.debug('valor: %s', x)` |
| `LOG_INFO` | Flujo general | `logger.info('proceso iniciado')` |
| `LOG_WARN` | Situación inesperada | `logger.warning('dato faltante')` |
| `LOG_ERROR` | Error crítico | `logger.error('fallo: %s', e)` |

```python
# Configuración mínima autocontenida — recrear si no existe
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
```

---

## Sin Tests Formales

- ❌ No crear archivos de test
- ✅ Validar funcionalidad directamente en desarrollo
- ✅ Usar logs para debugging
- ✅ Probar manualmente en navegador

---

## Entorno Virtual Python (venv)

Buena práctica obligatoria para cualquier trabajo con Python:

- ❌ **Prohibido instalar dependencias Python de forma global**
- ✅ **Siempre activar el `venv` del proyecto** antes de instalar, ejecutar o levantar servicios
- Si no existe: `python -m venv venv`
- Para activar: `source venv/bin/activate` (Linux/Mac)
- Toda dependencia nueva debe quedar en `requirements.txt`

---


## Consentimiento de Creación de Archivos

- ❌ **Prohibido crear archivos nuevos de forma autónoma**
- ✅ Se requiere **aprobación o instrucción explícita** del usuario antes de inicializar cualquier archivo físico nuevo
- La confirmación debe ser al menos una oración directa en el chat (no basta con un "sí" implícito en el contexto)
- Aplica a: código fuente, configuración, assets, scripts y documentación

---

## Estructura de Código
### Funciones — JavaScript
```javascript
// Obtiene tarjeta por id
function obtener_Tarjeta(id_Tarjeta) {
  log('INFO', 'obtener_Tarjeta iniciada', id_Tarjeta)

  // Búsqueda directa sin abstracciones
  const tarjeta = lista_Tarjetas.find(t => t.id === id_Tarjeta)

  log('DEBUG', 'resultado', tarjeta)
  return tarjeta
}
```

### Funciones — Python
```python
# Obtiene documento por id
def obtener_Documento(id_Documento: str) -> dict:
    logger.info('obtener_Documento iniciada: %s', id_Documento)

    # Búsqueda directa
    resultado = coleccion.get(id_Documento)

    logger.debug('resultado: %s', resultado)
    return resultado
```
