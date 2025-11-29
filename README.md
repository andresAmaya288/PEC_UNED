Prueba de Evaluación Continua Psicología UNED 2025/2026 — UNED

Cambios recientes (mejoras):

- Al hacer clic en una letra durante la "Tarea de atención (distractor)", ahora se alterna la selección (click sobre una letra marcada la desmarca).
- La secuencia de letras del ejercicio de atención se genera con más variedad (bloques aleatorios) para evitar repetir exactamente el mismo segmento.
- Mejoras de compatibilidad con dispositivos móviles: meta viewport, objetivos táctiles más grandes, soporte pointer events y teclado (Enter/Espacio) + mejor visualización del temporizador.

Prueba rápida:

1. Abre `index.html` en tu navegador (es un archivo estático — no requiere servidor).
2. Completa la parte de estudio y al llegar a la "Tarea de atención (distractor)" prueba clicar/tocar en distintas letras. Pulsa otra vez sobre una letra marcada para desmarcarla.
3. Prueba en el modo desarrollo de tu navegador (Device Toolbar) para comprobar comportamiento táctil y tamaños en pantalla pequeña.

Si quieres otra estrategia para generar la lista (p. ej. longitudes diferentes o patrones compatibles con tu experimento), dime cuál prefieres y lo ajusto.

Cambios adicionales hechos ahora:

- Las listas A y B ya no se calculan por las 15 primeras y 15 últimas. La lista A sigue la secuencia solicitada de cues (30 posiciones):
	A S A S S A S A S S A A S S A S A S A S A S A A S A S A A S
	La lista B usa la secuencia invertida (A ↔ S) como pediste.
- La Tarea de atención ahora genera una secuencia larga pero se muestra en una caja compacta y desplazable para mantener la coherencia visual con el resto del experimento.

- El formulario demográfico ahora ofrece opciones de sexo fijas: `Hombre`, `Mujer` y `No especificado`.
- La fase de memoria tiene un límite de tiempo de **5 minutos**; si se agota el tiempo, la respuesta se guarda automáticamente y se ofrece la descarga de los resultados.

Si quieres ajustar la secuencia (por ejemplo invertirla parcialmente, o especificar un patrón diferente) o controlar la longitud exacta del texto de relleno, dime el patrón/longitud y lo adapto.

Mejoras de diseño aplicadas:

- Interfaz más profesional, responsive y centrada — nuevo contenedor (`.app`) con card, paleta de colores y una tipografía legible (Inter).
- Barra de progreso visible durante la fase de estudio para seguir el avance (indicador numérico y barra visual).
- Controles y botones con mejor contraste y estados, áreas táctiles más grandes para dispositivos móviles.
- Mejora de la zona de la Tarea de atención (espaciado, límites de altura y scroll para mantener visible el header, focus visible, texto de ayuda y temporizador más visible).

Nota sobre cegamiento:

- La interfaz ahora muestra solamente 'I' o 'N' en la barra superior para el grupo (I = Intencional, N = No-intencional / Incidental). Esto es sólo un cambio de presentación; internamente los datos siguen registrando la condición completa para análisis.

Para revisar los cambios abre `index.html` y prueba el flujo completo en escritorio y en el modo móvil del inspector del navegador.

Textos actualizados:

- La pantalla de instrucciones y la propia hoja de la Tarea de atención muestran ahora el texto de instrucciones ampliado (explicando el objetivo: marcar las 'c' precedidas de 'a' o seguidas de 'e' y el límite de 3 minutos).
- La prueba de memoria (recall) ahora contiene el texto de instrucciones ampliado y un temporizador visible de 5 minutos; si se agota, la respuesta se guarda automáticamente.
