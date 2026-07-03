# Abstracción de Estrategias (estrategias.md)

Este archivo contiene explicaciones simplificadas de conceptos complejos del proyecto,
utilizando la Técnica Feynman para asegurar el entendimiento y el aprendizaje mutuo.

---

## 🧠 Ejemplo: Framework de Agentes (Rama exp1)

### 1. Explicación Simple (Feynman)
Imagina que estás construyendo una casa. En lugar de tener un solo maestro de obra sabelotodo que intenta hacerlo todo (y a veces se equivoca o se confunde), decides contratar a especialistas: un electricista, un plomero y un pintor. 

Cada uno de ellos tiene su propio manual de instrucciones específico (los "agentes especializados"). Pero para que no se peleen entre sí ni pongan tuberías donde van cables, creamos un plano general de la casa (la "arquitectura") y un manual de convivencia básico (las "rules" de comportamiento).

La carpeta `.agent/perfil/` es como tu libreta de notas personal. Le dice a los especialistas: "Oigan, sé de electricidad, pero de plomería explíquenme las cosas paso a paso o con manzanas". Así ellos ajustan sus explicaciones para que tú siempre tengas el control y puedas verificar su trabajo sin volverte un experto plomero.

### 2. Vacíos de Comprensión Identificados
- [ ] ¿Cómo aseguramos que el LLM lea `perfil.md` al inicio de cada turno de forma automática?
- [ ] ¿Cómo estructuraremos el Feynman de la base de datos vectorial cuando la configuremos?

### 3. Analogía del Mundo Real
- *El linter / compiler*: Un corrector ortográfico estricto que no te deja publicar un libro si tiene un solo error de tipografía.
