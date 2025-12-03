Prueba de Evaluación Continua Psicología UNED — PEC Psicología de la Memoria 2025/2026

Descripción
-----------
Este repositorio contiene una implementación web simple (archivo estático `index.html`) utilizada para una práctica / experimento de evaluación continua en Psicología (UNED). El experimento incluye tres fases principales:

- Fase de estudio: presentación secuencial de palabras con una letra indicadora (A/S) y registro de las respuestas.
- Tarea de atención (distractor): una hoja de letras donde los participantes deben marcar las letras 'c' que cumplan la regla (precedidas por 'a' o seguidas por 'e').
- Prueba de memoria (recall): campo de texto para que el participante escriba todas las palabras que recuerde.

Finalidad
---------
El código sirve como base para un experimento corto de laboratorio/online. Está diseñado para ser claro, accesible y fácil de modificar para diferentes condiciones experimentales (listas A/B, duración, instrucciones, etc.).

Privacidad y ética
------------------
La versión incluida guarda datos mínimos (edad, sexo, estudios, respuestas en la fase de estudio y las entradas de recuerdo). Diseña y usa este experimento respetando las normas éticas de investigación de tu institución: informa a los participantes, obtén consentimiento y maneja los datos de forma segura y anónima.

Uso local (rápido)
------------------
1. Abre `index.html` en un navegador moderno (no necesita servidor). 
2. Sigue las instrucciones en pantalla y completa el experimento.
3. Al finalizar se genera un CSV con los datos descargable desde la interfaz.

Notas técnicas
--------------
- La interfaz está optimizada para escritorio y móviles (responsive). 
- `data` se mantiene en memoria y se exporta a CSV al terminar la prueba.
- Para cambiar patrones, duraciones o comportamiento (p. ej. validación automática o registro de la tarea de atención), edita `index.html` directamente.

Análisis Estadístico de Resultados
-----------------------------------

### Requisitos

Python 3.8+ con dependencias:
```
pip install pandas numpy scipy statsmodels pingouin
```

### Ejecución Rápida

1. Descarga los CSV de cada participante desde `index.html` → carpeta `datos/`
2. Ejecuta:
   ```bash
   python analyze_recall.py
   ```
3. Revisa resultados en `results/`:
   - `table1.csv` — Tabla resumen de porcentajes
   - `analysis_results.txt` — Análisis ANOVA 2×2 e intervalos de confianza

### Descripción del Análisis

El script `analyze_recall.py`:

- **Calcula porcentajes (%)** de palabras recordadas correctamente por participante y tipo de procesamiento (S: sílabas; A: agradabilidad).
- **Genera Tabla 1** (wide format) con medias por grupo y condición.
- **Realiza ANOVA 2×2 mixta** (Grupo × Procesamiento):
  - VI1 (entre-sujetos): Grupo (Incidental vs Intencional)
  - VI2 (intra-sujetos): Nivel de Procesamiento (S vs A)
  - Reporta efectos principales, interacción, y tamaños del efecto (η²p)
- **Calcula intervalos de confianza (95%)** para medias y diferencias pareadas.
- **Realiza comparaciones pareadas (t-tests)** para S vs A general y por grupo.

### Ejemplo de Salida

**Estadísticos Descriptivos:**
```
Incidental - S: mean=26.67, 95% CI=[-6.46, 59.79], n=3
Incidental - A: mean=8.89, 95% CI=[-0.67, 18.45], n=3
Intencional - S: mean=51.11, 95% CI=[12.87, 89.36], n=3
Intencional - A: mean=48.89, 95% CI=[1.08, 96.70], n=3
```

**ANOVA 2×2:**
```
Source       SS    DF1  DF2    MS       F        p        np2
Group        3114  1    4      3114.8   8.95     0.040    0.691
Processing   300   1    4      300      5.79     0.074    0.591
Interaction  181   1    4      181.5    3.50     0.135    0.467
```

**Paired Comparisons (S − A):**
```
Overall S - A: mean_diff=-32.222, 95% CI=[-47.814, -16.630], p_paired=0.0032
Intencional S - A: mean_diff=-44.444, 95% CI=[-69.742, -19.147], p_paired=0.0171, n=3
```

### Interpretación

- **Efecto Grupo (p = 0.040):** Significativo. Grupo intencional recuerda más.
- **Efecto Procesamiento (p = 0.074):** Marginal/no significativo globalmente.
- **Interacción (p = 0.135):** No significativa.
- **Pareado (p = 0.003):** Significativo. Se recuerdan más palabras en A que en S.

### Estructura de Carpetas

```
PEC_UNED/
├── index.html                           # Experimento web
├── analyze_recall.py                    # Script de análisis ← EJECUTAR
├── README.md                            # Este archivo
├── datos/
│   ├── datos_parcipiante_N (1).csv
│   ├── datos_parcipiante_N (2).csv
│   └── ...
└── results/
    ├── table1.csv                       # Tabla resumen
    └── analysis_results.txt             # Informe completo
```

### Troubleshooting

**Error: "ModuleNotFoundError"**
```bash
pip install --upgrade pandas numpy scipy statsmodels pingouin
```

**Archivos CSV no encontrados**
Asegúrate de que los CSV están en `datos/` con estructura: `group,list,edad,sexo,estudios,word,cue,response,recall`

Contacto / créditos
-------------------
Proyecto desarrollado como material para la asignatura de Psicología de la Memoria, Prueba de Evaluación Continua — UNED (2025/2026).