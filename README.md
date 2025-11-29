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

Contacto / créditos
-------------------
Proyecto desarrollado como material para la asignatura de Psicología de la Memoria, Prueba de Evaluación Continua — UNED (2025/2026).