# Ejemplo: Evaluación Rigurosa de Plan de Implementación

## Contexto
El usuario ha propuesto usar SQLite para almacenar temporalmente los eventos web antes de pasarlos a BigQuery, argumentando que será "rápido y barato" para el MVP.

## Entrada
"Quiero implementar SQLite en Streamlit como capa intermedia temporal para los eventos de clics antes del batch de la noche hacia nuestro DWH. Es más fácil que montar Kafka por ahora."

## Salida Esperada

**Veredicto**: Incierto / Potencialmente Engañoso

**Fallas clave en el pensamiento**:
1. **Asunción de concurrencia**: Asumes que SQLite manejará bien escrituras concurrentes desde múltiples sesiones de Streamlit, lo cual suele resultar en bloqueos de base de datos.
2. **Ciclo de vida de Streamlit**: Olvidas que Streamlit re-ejecuta el script de arriba a abajo.

**Contra-argumento más fuerte**:
La naturaleza sin estado y multi-hilo de Streamlit hace que SQLite sea una de las peores opciones para registrar eventos de alta frecuencia. Los bloqueos de escritura degradarán la experiencia de usuario inmediatamente ni bien dos personas cliquen a la vez. 

**Evidencia que resolvería la duda**:
Pruebas de carga donde simules 10 usuarios haciendo clic simultáneamente guardando en la misma DB SQLite desde Streamlit sin errores de concurrencia.
