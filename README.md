# 📊 Sistema de Consulta - Simulacro Saber 11°

## 🎯 Descripción

Sistema completo de consulta de resultados del simulacro Saber 11° para la **Concentración Educativa del Sur de Montelíbano**, con **172 reportes individuales** generados automáticamente.

---

## 📁 Contenido del Paquete

```
simulacro_completo/
├── index_simulacro.html          → Página principal de búsqueda
├── indice_estudiantes.json       → Base de datos de estudiantes (172)
├── grupos_rendimiento.html       → Listado completo por grupos
└── reportes_simulacro/           → 172 reportes individuales en HTML
    ├── 1a2b3c4d5e6f.html
    ├── 2b3c4d5e6f7g.html
    └── ... (172 archivos)
```

**Total:** 175 archivos (3 principales + 172 reportes)

---

## 🎓 Información del Simulacro

### **Áreas Evaluadas** (105 preguntas total):
1. **Matemáticas** - 20 preguntas (0-100 puntos)
2. **Lectura Crítica** - 20 preguntas (0-100 puntos)
3. **Inglés** - 25 preguntas (0-100 puntos)
4. **Ciencias Naturales** - 20 preguntas (0-100 puntos)
5. **Ciencias Sociales** - 20 preguntas (0-100 puntos)

**Puntaje Total:** 0-500 puntos (suma de las 5 áreas)

### **Estadísticas Generales:**
- Total de estudiantes: **172**
- Promedio general: **141.22 / 500**
- Puntaje más alto: **193 puntos**
- Puntaje más bajo: **91 puntos**

### **Promedios por Área:**
- Matemáticas: **23.23 / 100**
- Lectura Crítica: **28.17 / 100**
- Inglés: **29.67 / 100**
- Ciencias Naturales: **33.02 / 100** (mejor área)
- Ciencias Sociales: **27.12 / 100**

---

## 👥 Grupos de Rendimiento

Los 172 estudiantes están divididos en **6 grupos** según su desempeño:

| Grupo | Emoji | Estudiantes | Promedio | Descripción |
|-------|-------|-------------|----------|-------------|
| Grupo 1 | 🦅 | 29 | 173.41 | Rendimiento superior |
| Grupo 2 | 🦁 | 29 | 154.66 | Rendimiento alto |
| Grupo 3 | 🐺 | 29 | 145.38 | Rendimiento medio-alto |
| Grupo 4 | 🐯 | 29 | 135.69 | Rendimiento medio |
| Grupo 5 | 🐻 | 28 | 125.96 | Rendimiento básico |
| Grupo 6 | 🐼 | 28 | 110.61 | Requiere refuerzo |

---

## 🚀 Cómo Usar

### **Opción 1: Uso Local Inmediato (1 minuto)**

1. Descomprime el archivo `Simulacro_Saber11_Completo.zip`
2. Abre la carpeta `simulacro_completo`
3. Haz doble clic en `index_simulacro.html`
4. Busca por nombre o apellido
5. ¡Listo! El reporte se abrirá automáticamente

**Prueba con nombres como:** KEINER, NICOLAS, VALENTINA, SAMUEL

---

### **Opción 2: Publicar en Internet (5 minutos)**

#### **A. Netlify (MÁS FÁCIL)**

1. Ve a [netlify.com](https://netlify.com)
2. Regístrate gratis
3. Arrastra toda la carpeta `simulacro_completo`
4. Espera 30 segundos
5. Obtendrás un link como: `https://simulacro-montelibano.netlify.app`

#### **B. GitHub Pages**

1. Crea repositorio en [github.com](https://github.com)
2. Sube todos los archivos
3. Activa GitHub Pages
4. Tu sitio estará en: `https://tu-usuario.github.io/simulacro`

---

## 📊 Características de los Reportes Individuales

Cada reporte incluye:

### **📈 Visualizaciones:**
- **Gráfico Radar:** Muestra el rendimiento en las 5 áreas
- **Gráfico de Barras:** Compara el puntaje del estudiante vs. promedio del grupo

### **📋 Información Detallada:**
- Nombre del estudiante
- Puntaje total (0-500)
- Posición entre 172 estudiantes
- Grupo de rendimiento (1-6 con emoji)
- Puntaje por cada área
- Número de respuestas correctas por área
- Barra de progreso visual por área

### **💬 Comentarios Personalizados:**
Cada área tiene un comentario único según el rendimiento:
- **Excelente** (70-100): Felicitaciones y motivación
- **Bueno** (50-69): Reconocimiento y sugerencias
- **Regular** (30-49): Orientación para mejorar
- **Bajo** (0-29): Recomendaciones de refuerzo urgente

### **✅ Comparación:**
- Compara cada puntaje con el promedio del grupo
- Indica si está por encima o por debajo (+/- puntos)

---

## 🗂️ Listado de Grupos (grupos_rendimiento.html)

### **Incluye:**
- Vista general con estadísticas
- 6 secciones (una por grupo)
- Tabla con todos los estudiantes de cada grupo
- Posición, nombre y puntaje total
- Código de colores por nivel de desempeño
- Promedio de cada grupo

### **Ideal para:**
- Reuniones de directivos
- Planificación de estrategias de refuerzo
- Identificación de estudiantes que requieren apoyo
- Reconocimiento de estudiantes destacados

---

## 🔍 Sistema de Búsqueda

### **Búsqueda Inteligente:**
- Por **nombre** (ej: KEINER, VALENTINA)
- Por **apellido** (ej: ACOSTA, AGAMEZ)
- Búsqueda parcial (ej: "VAL" encuentra VALENTINA)
- No distingue mayúsculas/minúsculas

### **Resultados:**
- Si hay 1 coincidencia → Abre el reporte directamente
- Si hay múltiples → Muestra lista para seleccionar
- Si no hay → Mensaje de error con sugerencias

---

## 📱 Compartir con Estudiantes

### **Mensaje Sugerido (WhatsApp/Email):**

```
📊 RESULTADOS SIMULACRO SABER 11°

Estimados estudiantes y padres:

Ya pueden consultar los resultados individuales del simulacro en:
🔗 [TU-LINK-AQUI]

CÓMO CONSULTAR:
1. Ingresa a la página
2. Escribe tu nombre o apellido
3. Haz clic en "Buscar Mi Reporte"
4. Revisa tu reporte completo

El reporte incluye:
✅ Tu puntaje en cada área
✅ Tu posición entre 172 estudiantes
✅ Comparación con promedios
✅ Comentarios personalizados
✅ Grupo de rendimiento

Úsalo para identificar tus fortalezas y áreas de mejora.

Att: Concentración Educativa del Sur de Montelíbano
```

---

## 🎨 Características Técnicas

### **Reportes:**
- ✅ HTML responsivo (móvil, tablet, PC)
- ✅ Gráficos interactivos (Chart.js)
- ✅ Código único por estudiante
- ✅ Imprimible (botón integrado)
- ✅ Sin necesidad de internet después de cargar

### **Búsqueda:**
- ✅ JSON liviano (37KB)
- ✅ Búsqueda instantánea
- ✅ Interfaz intuitiva
- ✅ Animaciones suaves

### **Seguridad:**
- ⚠️ Sin autenticación (acceso público)
- ℹ️ Códigos únicos (difíciles de adivinar)
- ℹ️ Datos estáticos (no se pueden modificar)

---

## 📈 Análisis de Resultados

### **Áreas Críticas (Requieren Refuerzo):**
1. **Matemáticas** (23.23) - Nivel más bajo
2. **Ciencias Sociales** (27.12)
3. **Lectura Crítica** (28.17)

### **Áreas Fortaleza:**
1. **Ciencias Naturales** (33.02) - Mejor desempeño
2. **Inglés** (29.67)

### **Recomendaciones Generales:**
- Implementar talleres de matemáticas urgentes
- Reforzar comprensión de lectura en todas las áreas
- Programas diferenciados según grupo de rendimiento
- Atención especial a Grupo 6 (28 estudiantes)

---

## 🛠️ Personalización

### **Cambiar Colores:**
En cualquier HTML, busca:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```
Reemplaza con los colores institucionales.

### **Agregar Logo:**
En el `<div class="logo">` puedes cambiar el emoji 📊 por:
```html
<img src="logo.png" style="width: 100%; height: 100%; border-radius: 50%;">
```

---

## 📞 Créditos y Soporte

**Diseñado por:** Froylan Jiménez

### **Incluye:**
- ✅ 172 reportes individuales personalizados
- ✅ Sistema de búsqueda web
- ✅ Listado por grupos de rendimiento
- ✅ Comentarios adaptativos por área
- ✅ Gráficos interactivos
- ✅ Diseño profesional y responsive

---

## 📊 Estructura de Archivos

### **Archivos Principales:**
- `index_simulacro.html` (14KB) - Página de búsqueda
- `indice_estudiantes.json` (37KB) - Base de datos
- `grupos_rendimiento.html` (55KB) - Listado de grupos

### **Reportes:**
- 172 archivos HTML
- ~15KB cada uno
- Código único por estudiante
- Incluyen gráficos Chart.js (desde CDN)

### **Peso Total:**
- Comprimido: **580 KB**
- Descomprimido: ~3 MB

---

## ✨ Ventajas del Sistema

✅ **Sin servidor complejo** - Solo archivos HTML
✅ **Hosting gratis** - Netlify, GitHub Pages
✅ **Sin base de datos** - Todo en JSON
✅ **Búsqueda rápida** - Instantánea
✅ **Reportes únicos** - Personalizados por estudiante
✅ **Responsive** - Funciona en cualquier dispositivo
✅ **Imprimible** - PDF desde navegador
✅ **Profesional** - Diseño moderno y limpio

---

## 🎯 Próximos Pasos

1. ✅ **Probar localmente** (ya puedes)
2. ⏭️ **Publicar en Netlify** (5 minutos)
3. ⏭️ **Compartir link con estudiantes**
4. ⏭️ **Analizar resultados por grupos**
5. ⏭️ **Implementar planes de mejora**
6. ⏭️ **Realizar seguimiento**

---

## 📋 Checklist para Publicación

- [ ] Descomprimir archivos
- [ ] Probar búsqueda localmente
- [ ] Verificar que abran los reportes
- [ ] Subir a Netlify/GitHub Pages
- [ ] Probar en línea
- [ ] Crear mensaje para estudiantes
- [ ] Compartir link
- [ ] Monitorear accesos

---

**🎉 ¡Todo listo para usar!**

El sistema está **100% funcional** y preparado para compartir con tus estudiantes. Solo necesitas publicarlo y compartir el link.

---

**Versión:** 1.0  
**Fecha:** Febrero 2026  
**Estudiantes:** 172  
**Reportes Generados:** 172  
**Estado:** ✅ LISTO PARA PUBLICAR

---

# 🆕 Simulacro Final — Julio 2026 (sim5)

**Este es el simulacro más reciente y el primero calculado con las respuestas reales
de los estudiantes** (los anteriores se estimaban a partir del simulacro externo).

## Archivos

| Archivo | Qué es |
|---|---|
| `index_sim5.html` | **Buscador de estudiantes** — punto de entrada |
| `analisis_sim5.html` | Consolidado general + acceso a los 5 análisis por área |
| `analisis_sim5_lectura_critica.html` | Análisis de Lectura Crítica |
| `analisis_sim5_matematicas.html` | Análisis de Matemáticas |
| `analisis_sim5_sociales.html` | Análisis de Sociales y Ciudadanas |
| `analisis_sim5_ciencias_naturales.html` | Análisis de Ciencias Naturales |
| `analisis_sim5_ingles.html` | Análisis de Inglés |
| `reportes_sim5/` | **148 informes individuales** (uno por estudiante) |
| `indice_sim5.json` | Índice: nombre, curso, global, puesto |
| `indice_areas_sim5.json` | Puntajes por área de cada estudiante |
| `datos_sim5/` | CSV originales de Sesión 1 y Sesión 2 |
| `generar_sim5.py` | Generador reproducible (semilla fija) |

Cada análisis por área trae: promedio, mediana, máximo, mínimo y desviación;
**los 15 mejores puntajes**, **los 15 más bajos**, promedio por curso,
distribución por rangos y la tabla completa de los 148 estudiantes.

## Estructura de la prueba

**Sesión 1 — 106 preguntas** (la #10 fue anulada, quedan 105 efectivas)

| Área | Preguntas | Total |
|---|---|---|
| Matemáticas | 1 – 22 | 22 (21 efectivas) |
| Lectura Crítica | 23 – 58 | 36 |
| Sociales y Ciudadanas | 59 – 80 | 22 |
| Ciencias Naturales | 81 – 106 | 26 |

**Sesión 2 — 115 preguntas**

| Área | Preguntas | Total |
|---|---|---|
| Sociales y Ciudadanas | 1 – 22 | 22 |
| Matemáticas | 23 – 44 | 22 |
| Ciencias Naturales | 45 – 70 | 26 |
| Inglés | 71 – 115 | 45 |

**Consolidado:** Ciencias Naturales 52 · Inglés 45 · Sociales 44 · Matemáticas 43 · Lectura Crítica 36 → **220 preguntas efectivas**

## Cálculo de puntajes

```
Puntaje de área (0–100) = round(aciertos / preguntas del área × 100)
Global ICFES   (0–500)  = round( (3 × (LC + Mat + Soc + CN) + Ing) / 13 × 5 )
```

Niveles de desempeño global: **Alto** ≥ 326 · **Medio** 220–325 · **Básico** < 220.

## Resultados generales

- Estudiantes: **148** (6 cursos: 11-1 a 11-6)
- Promedio global: **242.7 / 500** — máximo **385** · mínimo **144**
- Con opciones en la Universidad de Córdoba (global ≥ 246.75): **64**

Promedios por área (0–100):

| Área | Promedio |
|---|---|
| Lectura Crítica | **57.3** |
| Ciencias Sociales - C. Ciudadanas | **49.6** |
| Matemáticas | **47.4** |
| Inglés | **43.3** |
| Ciencias Naturales | **41.7** |

## ⚠️ Nota metodológica: 15 estudiantes con Sesión 1 estimada

El export de la Sesión 1 llegó **incompleto**: faltan 15 estudiantes del bloque
alfabético *Fuentes Méndez … Hernández Peñates* que sí presentaron la Sesión 2.

Para no dejarlos sin informe, sus puntajes de Sesión 1 —incluida **toda** Lectura
Crítica— se estimaron por **regresión lineal** a partir de su desempeño real en la
Sesión 2, calibrada con los 133 estudiantes que sí tienen ambas sesiones, y se
redondearon a un número entero de aciertos alcanzable.

Estos estudiantes aparecen marcados **(S1 est.)** en las tablas de análisis y con un
**aviso rojo visible** en su informe individual. Si aparece el CSV completo de la
Sesión 1, basta reemplazar `datos_sim5/sesion1.csv` y volver a ejecutar
`python3 generar_sim5.py` para regenerar todo con datos reales.

## Regenerar

```bash
python3 generar_sim5.py
```

Reproducible: semilla fija, mismos resultados en cada corrida.
No modifica los simulacros anteriores (externo, sim2, sim3, sim4).
