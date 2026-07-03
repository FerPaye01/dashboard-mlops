---
trigger: always_on
---

# 📱 Principios de Responsive

Reglas para diseño responsive mobile-first.

---

## Enfoque Mobile-First

- Estilos base para **375px** (móvil pequeño)
- Media queries **ascendentes** (`min-width`)
- Nunca usar `max-width` para breakpoints

```css
/* Base: móvil */
.elemento { padding: 8px; }

/* Tablet+ */
@media (min-width: 768px) {
  .elemento { padding: 16px; }
}

/* Desktop+ */
@media (min-width: 1024px) {
  .elemento { padding: 24px; }
}
```

---

## Breakpoints Oficiales

| Nombre | Ancho | Dispositivo |
|--------|-------|-------------|
| base | < 375px | Móvil pequeño |
| sm | 375px+ | Móvil |
| md | 768px+ | Tablet |
| lg | 1024px+ | Desktop |
| xl | 1920px+ | Desktop grande |

---

## Doble Interfaz

El proyecto tiene **dos experiencias** distintas:

| Interfaz | Breakpoint | Características |
|----------|------------|-----------------|
| Móvil | < 768px | Touch-first, vertical, gestos |
| Desktop | 768px+ | Mouse-first, horizontal, hover |

### Reglas de Doble Interfaz
- Componentes pueden tener **lógica diferente** por interfaz, no solo estilos
- Usar clases utilitarias: `.mobile-only`, `.desktop-only`
- Considerar interacciones distintas (swipe vs click)

---

## Variables CSS

Usar variables de `src/styles/variables.css`:

```css
:root {
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
}
```

---

## Checklist de Componente Responsive

- [ ] Funciona en 375px sin scroll horizontal
- [ ] Textos legibles sin zoom
- [ ] Botones mínimo 44x44px para touch
- [ ] Probado en 768px y 1024px
