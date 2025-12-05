# Prueba de Evaluación Continua — Psicología de la Memoria (UNED 2025/2026)

## Descripción General

Repositorio con una **plataforma web completa** para un experimento de memoria que combina:

- **Frontend interactivo** (HTML5/CSS3/JavaScript vanilla) — Experimento autocontrolado sin dependencias externas
- **Pipeline de análisis** (Python 3.13+) — Normalización automática de datos, análisis estadístico (ANOVA 2×2 mixta) y generación de gráficos

### Objetivo Científico

Evaluar el efecto de **dos manipulaciones experimentales** en la memoria:
1. **Condición entre-sujetos**: Aprendizaje Incidental vs Intencional
2. **Condición intra-sujetos**: Nivel de Procesamiento (Superficial/Sílabas vs Profundo/Agradabilidad)

### Fases del Experimento

| Fase | Descripción | Duración |
|------|-------------|----------|
| **Consentimiento** | Información y consentimiento informado | Variable |
| **Demografía** | Edad, sexo, nivel de estudios | ~1 min |
| **Instrucciones** | Tareas específicas por condición | ~2 min |
| **Estudio** | 30 palabras con indicador de tarea (A/S) | ~2 min |
| **Atención** | Grilla de 80 letras con regla de búsqueda | 3 min |
| **Recall** | Escribir palabras recordadas | 5 min |
| **Descarga** | Exportar datos a CSV | ~30 seg |

---

## Interfaz Web

### Inicio Rápido

```bash
# Opción 1: Abrir directamente (sin servidor)
abrir https://andresamaya288.github.io/PEC_UNED/ en cualquier navegador moderno la página está publicada con Github pages

# Opción 2: Servir localmente (recomendado para pruebas)
python -m http.server 8000
# Luego acceder a http://localhost:8000
```

### Características Técnicas

- **Sin dependencias externas** — HTML5/CSS3/JavaScript puro
- **Responsive** — Optimizado para escritorio, tablet y móvil
- **Accesibilidad** — Soporte para teclado completo (Tab, Enter, Espaciadora)
- **Almacenamiento en memoria** — Datos se mantienen en sesión hasta exportación
- **Exportación automática** — CSV descargable al finalizar
- **Diseño profesional** — Inter font de Google, paleta de colores diseñada, animaciones suaves

### Estructura HTML

```
Consentimiento Resumido
  ↓
Datos Demográficos (edad, sexo, estudios)
  ↓
Instrucciones Contextualizadas (según condición)
  ↓
FASE DE ESTUDIO (30 palabras × 2 listas)
  ├─ Lista A: secuencia ASAS... (Sílabas → Agradabilidad)
  └─ Lista B: secuencia SASA... (Agradabilidad → Sílabas)
  ↓
TAREA DE Relleno (3 minutos)
  └─ Grilla 8×10 letras; buscar 'c' (a__ o __e)
  ↓
PRUEBA DE RECALL (5 minutos, auto-save)
  └─ Textarea libre con contador y temporizador
  ↓
Descarga de CSV
```

### Variables Capturadas en CSV

```
group        : Incidental | Intencional (asignado al azar)
list         : A | B (indica secuencia de tareas)
edad         : número entero
sexo         : Hombre | Mujer | No especificado
estudios     : Primaria | Secundaria | Licenciatura | Posgrado
word         : palabra presentada (30 palabras de estímulo)
cue          : S (sílaba) | A (agradabilidad)
response     : respuesta del participante en fase de estudio
recall       : palabras escritas en fase de recall (texto libre)
```

### Paleta de Colores y Tipografía

- **Font**: Inter (Google Fonts) — Sans-serif profesional
- **Primario**: `#2c3e50` — Azul oscuro corporativo
- **Acento**: `#3498db` — Azul brillante (botones, enlaces)
- **Éxito**: `#27ae60` — Verde (completado)
- **Fondo**: `#ecf0f1` — Gris claro
- **Logo**: Cuadrado responsive (aspecto 1:1) con sombra

### Privacidad y cumplimiento ético

- Consentimiento informado al inicio.
- Datos mínimos recogidos (sin nombre, email o identificadores únicos).
- Opción de retiro en cualquier momento.
- Descarga local de los datos (almacenamiento en el navegador del participante).

---

## Gestión de Datos

### Estructura de Carpetas

```
PEC_UNED/
├── index.html                              # Experimento web principal
├── README.md                               # Este archivo
├── requirements.txt                        # Dependencias Python
│
├── SCRIPTS DE ANÁLISIS
├── normalize_recalls.py                    # Normalización automática (Step 1/3)
├── analyze_recall.py                       # Análisis estadístico (Step 2/3)
├── plot_results.py                         # Generación de gráficos (Step 3/3)
├── run_analysis.py                         # Pipeline wrapper (ejecutar TODO)
│
├── DATOS ORIGINALES
├── datos/
│   ├── datos_parcipiante_N (1).csv         # CSV participante 1 (descargado desde web)
│   ├── datos_parcipiante_N (2).csv
│   ├── ...
│   └── normalized/                         # (generado automáticamente)
│       ├── datos_parcipiante_N (1).csv     # Recall normalizado
│       └── ...
│
└── RESULTADOS
    └── results/
        ├── table1.csv                      # Tabla resumen (wide format, separada por grupo)
        ├── analysis_results.txt            # Informe estadístico completo
        ├── plot_means_by_condition.png     # Gráfico 1: Medias con IC 95%
        ├── plot_interaction.png            # Gráfico 2: Interacción Grupo × Procesamiento
        ├── plot_distributions.png          # Gráfico 3: Violines por grupo
        ├── plot_boxplot.png                # Gráfico 4: Box plots
        └── plot_paired_comparison.png      # Gráfico 5: Comparación S vs A (pareado)
```

### Entrada de Datos

**Fuente**: Archivos CSV descargados desde `index.html` después de que participantes completen el experimento.

**Formato esperado**:
```csv
group,list,edad,sexo,estudios,word,cue,response,recall
Incidental,A,23,Mujer,Licenciatura,HUESO,S,HUESO,HUESO MIEL RINOCERONTE...
...
```

**Características especiales**:
- Recall puede contener typos, acentos, separadores variados → **Normalización automática**
- Fuzzy matching permite tolerar ~25% variación (ej: "frío" → "FRIO")
- Salida normalizada usa espacios como separador homogéneo

### Salida de Datos

**table1.csv** — Tabla resumen con columnas:
```
Participant, Group, List, Edad, Sexo, S_matched, S_total, A_matched, A_total, Perc_S, Perc_A
```

Ejemplo:
```csv
datos_parcipiante_N (1), Incidental, B, 22, Hombre, 2, 15, 5, 15, 13.33, 33.33
datos_parcipiante_N (4), Intencional, B, 52, Hombre, 1, 15, 9, 15, 6.67, 60.00
```

---

## Tutorial de Uso

### Escenario 1: Ejecutar el Experimento (Usuario Final)

**Tiempo**: ~15 minutos por participante

1. **Abre `index.html`** en navegador (Firefox, Chrome, Safari, Edge)
   ```
   c:\Users\USER\Documents\GitHub\PEC_UNED\index.html
   ```

2. **Lee y acepta el consentimiento**

3. **Completa el formulario demográfico**
   - Edad, sexo, nivel de estudios

4. **Sigue las instrucciones en pantalla**
   - Fase de estudio: responde A/S según la tarea indicada
   - Tarea de atención: busca todas las letras 'c' válidas (3 minutos)
   - Recall: escribe todas las palabras que recuerdes (5 minutos, temporizador activo)

5. **Descarga el CSV** al finalizar
   - Botón "Descargar Datos" en la pantalla final
   - Archivo guardado como `datos_participante_[ID].csv`

6. **Guarda el CSV en carpeta `datos/`**
   ```
   PEC_UNED/
   └── datos/
       ├── datos_parcipiante_N (1).csv
       ├── datos_parcipiante_N (2).csv
       └── ... (añadir nuevos CSV aquí)
   ```

### Escenario 2: Analizar Datos (Investigador)

**Tiempo**: ~2 minutos (automatizado)

#### Opción A: Pipeline Completo (Recomendado)

```bash
cd c:\Users\USER\Documents\GitHub\PEC_UNED

# Ejecutar todo: normalizar → analizar → graficar
python run_analysis.py
```

**Salida esperada:**
```
=================================================================
PIPELINE DE ANÁLISIS - PEC PSICOLOGÍA DE LA MEMORIA
=================================================================

[1/3] Normalizando archivos de recall...
Processing datos_parcipiante_N (1).csv → datos/normalized/...
...
[2/3] Analizando datos de recall (table1 y ANOVA)...
Total participantes procesados: 8
  Incidental: 4 participantes
  Intencional: 4 participantes
[3/3] Generando gráficos...
[OK] Todos los gráficos han sido generados exitosamente.

Archivos generados:
  - results/table1.csv
  - results/analysis_results.txt
  - results/plot_*.png (5 gráficos)
```

#### Opción B: Pasos Individuales

**Step 1: Normalizar recalls**
```bash
python normalize_recalls.py
# Salida: datos/normalized/*.csv (recall field normalizado)
```

**Step 2: Análisis estadístico**
```bash
python analyze_recall.py --datos datos/normalized
# Salida: results/table1.csv, results/analysis_results.txt
```

**Step 3: Generar gráficos**
```bash
python plot_results.py
# Salida: results/plot_*.png (5 PNG de alta calidad)
```

### Escenario 3: Verificar Resultados

```bash
# Ver tabla resumen
cat results/table1.csv

# Ver análisis completo
cat results/analysis_results.txt
```

**Salida típica:**
```
ANALYSIS SUMMARY
================
N participants: 8

Descriptive stats (means and 95% CI)
Incidental - S: mean=16.67, 95% CI=[2.97, 30.36], n=4
Incidental - A: mean=18.33, 95% CI=[-5.19, 41.86], n=4
Intencional - S: mean=48.33, 95% CI=[21.81, 74.85], n=4
Intencional - A: mean=53.33, 95% CI=[32.12, 74.55], n=4

Mixed ANOVA using pingouin (Group between, Processing within)
Source       SS    DF1  DF2    MS      F        p        np2
Group        4444  1    6      4444    28.92    0.0017   0.828
Processing   44    1    6      44      0.20     0.669    0.033
Interaction  11    1    6      11      0.05     0.830    0.008

Overall S - A: mean_diff=-33.333, p_paired=0.0002
```

---

## Metodología de Análisis

### Normalización de Recalls

**Problema**: Participantes escriben recalls con typos, acentos, separadores inconsistentes.

**Solución automática**:
```
"HUESO, MIEL rino" → ["HUESO", "MIEL", "RINOCERONTE"]
```

Pasos:
1. Tokenización por espacios/comas/pipes
2. Uppercase + eliminación de acentos
3. Fuzzy matching contra lista de 30 palabras válidas (cutoff=0.75)
4. Si hay match: usar palabra válida; si no: guardar token de todas formas
5. Salida normalizada con espacios como separador

**Ejemplo en `normalize_recalls.py`:**
```python
ALLOWED_WORDS = ["HUESO","MIEL","RINOCERONTE",...] # 30 palabras

# Para cada token en recall:
token = "rino"
matches = difflib.get_close_matches(token, ALLOWED_WORDS, cutoff=0.75)
# → ["RINOCERONTE"] (match exitoso)
```

### Análisis Estadístico

**Diseño**: 2 (Grupo: Incidental vs Intencional) × 2 (Procesamiento: S vs A)

**Método**: ANOVA 2×2 mixta
- **VI entre-sujetos**: Grupo
- **VI intra-sujetos**: Procesamiento (S vs A)
- **VD**: % de palabras recordadas

**Salida**:
- Tabla ANOVA con: SS, df, MS, F, p, η²p
- Intervalos de confianza 95% para medias
- Tests pareados (t-tests) S vs A por grupo
- Supuestos: normalidad (Shapiro-Wilk), homocedasticidad (Levene)

**Librerías Python**:
- `pingouin` — ANOVA y tests pareados
- `statsmodels` — Fallback si pingouin falla
- `pandas/numpy` — Manipulación de datos

### Visualización

Cinco gráficos generados automáticamente:

1. **Medias por condición** — Bar chart con IC 95%, separado por grupo
2. **Interacción** — Líneas (Group) × (S/A), para detectar efectos cruzados
3. **Distribuciones** — Violin plots por grupo (simetría visual)
4. **Boxplots** — Box plots con outliers, por grupo
5. **Comparación pareada** — Dispersión S vs A por participante

---

## Replicación y Extensión

### Para Replicar el Estudio

1. **Mantén invariantes**:
   - 30 palabras del estímulo (sin cambios)
   - Secuencias A/B de tareas
   - Duraciones: 3 min atención, 5 min recall

2. **Personaliza si necesitas**:
   ```javascript
   // En index.html, edita:
   const WORDS = ['HUESO', 'MIEL', ...]; // Lista de palabras
   const CUE_SEQUENCE_A = ['A','S','A',...]; // Secuencia de tareas
   const ATTENTION_DURATION = 180000; // ms (3 min)
   const RECALL_DURATION = 300000; // ms (5 min)
   const DEMOGRAPHICS_OPTIONS = {...}; // Opciones de sexo, estudios, etc.
   ```

3. **Ejecuta con participantes**:
   - Asegúrate de tener consentimiento informado
   - Respeta privacidad (anonimiza si es necesario)
   - Guarda CSVs en `datos/`

4. **Analiza automáticamente**:
   ```bash
   python run_analysis.py
   # Obtén resultados en 2 minutos
   ```

### Extensiones Posibles

#### A. Añadir más participantes
```bash
# Simplemente copiar nuevos CSV a datos/
# Ejecutar run_analysis.py nuevamente
# Resultados se regeneran automáticamente
```

#### B. Cambiar condiciones experimentales
```javascript
// index.html, línea ~50
const GROUP = Math.random() < 0.5 ? 'Incidental' : 'Intencional';

// Modificar instrucciones según GROUP
if (GROUP === 'Incidental') {
    instructionText = "Responde basándote en tu intuición...";
} else {
    instructionText = "Intenta memorizar cada palabra...";
}
```

#### C. Adicionar análisis estadístico
```python
# En analyze_recall.py, añadir:
from scipy.stats import friedmanchisquare

# Friedman test como análogo no-paramétrico
stat, pval = friedmanchisquare(data_S, data_A)
```

#### D. Personalizar gráficos
```python
# En plot_results.py:
plt.rcParams['figure.figsize'] = (12, 8)  # Tamaño
plt.rcParams['font.size'] = 14  # Font size
plt.style.use('seaborn-v0_8-darkgrid')  # Estilo
```

### Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: pandas` | Dependencias no instaladas | `pip install -r requirements.txt` |
| `CSV not found: datos/...` | CSVs no en carpeta correcta | Verificar ruta: `datos/*.csv` |
| `UnicodeDecodeError` | Encoding del archivo incorrecto | Abrir CSV en encoding UTF-8 |
| `ANOVA error: N < 3` | Muy pocos participantes | Necesitar ≥3 participantes por grupo |
| `No hay gráficos` | table1.csv tiene formato incorrecto | Revisar columnas: Perc_S, Perc_A |

---

## Referencias

- **Diseño experimental**: Craik & Lockhart (1972) — Levels of Processing
- **Análisis en Python**: pingouin documentation, statsmodels documentation
- **Psicología UNED 2025/2026**: Asignatura de Psicología de la Memoria

---

## Contacto

Proyecto desarrollado como material de evaluación continua para UNED (2025/2026).

**Estructura creada**: Diciembre 2025  
**Versión**: 1.0  
**Licencia**: Abierto para propósitos educativos

