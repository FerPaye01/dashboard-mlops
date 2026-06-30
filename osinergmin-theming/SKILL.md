---
name: osinergmin-theming
description: Applies Osinergmin branding (colors and logo) to Chainlit applications. Use this skill when a user wants to customize their chatbot with the official visual identity of Osinergmin (Peru).
---

# Osinergmin Theming Skill (Manual 2024)

Este Skill proporciona las directrices y recursos para adaptar interfaces (Streamlit y Chainlit) bajo la identidad visual oficial de **Osinergmin** (Perú), basada en su **Manual de Identidad Visual - 2024**.

## 🎨 Especificaciones de la Identidad Visual

### 1. Paleta de Colores Oficiales


*   **Azul Osinergmin (Color Principal):** `HEX #0039AA` (RGB: `0, 57, 170` | CMYK: `98, 79, 0, 0`). Transmite seriedad, seguridad y confianza.
*   **Amarillo Osinergmin (Color Principal):** `HEX #FBE122` (RGB: `251, 225, 34` | CMYK: `4, 10, 88, 0`). Transmite cercanía, energía y accesibilidad.
*   **Colores Complementarios:**
    *   Celeste Secundario: `HEX #03A9F4` (RGB: `3, 169, 244`)
    *   Verde Osinergmin: `HEX #35CC29` (RGB: `53, 204, 41`)
    *   Naranja: `HEX #F6A229` (RGB: `246, 162, 41`)
    *   Celeste Claro (Sky Blue): `HEX #D2F7FC` (RGB: `210, 247, 252`)
    *   Gris Claro: `HEX #F2F2F2` (RGB: `242, 242, 242`)
    *   Mostaza: `HEX #BFAB49` (RGB: `191, 171, 73`)

*   **Proporción de Uso Recomendada:** 65% colores principales (Azul y Amarillo) y 35% colores complementarios.

### 2. Tipografía Institucional

La tipografía oficial para medios digitales es **Poppins** (Sans-Serif), seleccionada por su alta legibilidad, modernidad y neutralidad.
*   **Títulos:** Poppins Extrabold / Bold.
*   **Subtítulos:** Poppins Semibold / Medium.
*   **Cuerpo:** Poppins Regular.

### 3. Logotipo e Isotipo (Turbina de Pelton)

El isotipo es un símbolo circular que representa una **Turbina de Pelton** con 4 aspas orientadas en sentido horario hacia la derecha (símbolo de avance y modernidad).
*   **Versión sobre Fondo Oscuro / Azul:** El isotipo y la palabra "Osinergmin" se presentan en blanco (`#FFFFFF`), y el tagline va en una caja amarilla (`#FBE122`) con texto en azul/negro.
*   **Tagline Oficial:** `"TRABAJANDO POR UNA ENERGÍA Y MINERÍA SEGURAS Y SOSTENIBLES"` en letras mayúsculas.

---

## 🛠️ Directrices de Implementación para Streamlit

Para aplicar el Manual de Identidad de Osinergmin en Streamlit, configure:

1.  **Fichero `.streamlit/config.toml`:**
    ```toml
    [theme]
    primaryColor = "#0039AA"
    backgroundColor = "#0B0F19"
    secondaryBackgroundColor = "#0F172A"
    textColor = "#F8FAFC"
    font = "sans serif"
    ```
2.  **Inyección CSS Corporativa (Poppins & Proporciones):**
    *   Importar la fuente `Poppins` desde Google Fonts.
    *   Establecer `Poppins` como font-family global.
    *   Aplicar `#0039AA` en bordes y selectores.
    *   Usar `#FBE122` para destacar elementos clave.
    *   Badges de estado alineados: Verde (`#35CC29`) para estado correcto y Naranja (`#F6A229`) para advertencias.

## 📁 Archivos Relacionados
*   **Manual de Identidad:** `Manual de Identidad Visual de Osinergmin.pdf`
*   **Logotipo:** `indicaciones-logo-principal.png`
