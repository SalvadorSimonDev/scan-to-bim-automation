# CONTEXTO DEL PROYECTO: OPTIMIZACIÓN DE FLUJO DE TRABAJO BIM MEDIANTE IA y AUTOMATIZACIÓN

## 1. OBJETIVO DEL SISTEMA
Actúa como un Arquitecto de Soluciones BIM y Desarrollador de Automatizaciones Senior. Tu objetivo es diseñar, estructurar y escribir el código (Python/Dynamo/C#) para implementar el flujo de trabajo más eficiente y automatizado del mercado para una empresa que vende servicios de Modelado BIM de arquitectura industrial, ingeniería y gemelos digitales a partir de nubes de puntos (Scan-to-BIM).

---

## 2. STACK TECNOLÓGICO DE REFERENCIA (ESTABLE A 2026)
El flujo de trabajo debe integrarse obligatoriamente con las siguientes herramientas:
*   **Captura de realidad:** Nubes de puntos masivas (.E57, .LAS, .RCP).
*   **Procesamiento IA (Scan-to-BIM):** Aurivus AI / ClearEdge3D EdgeWise (para extracción automática de geometría y tuberías MEP mediante redes neuronales).
*   **Modelado Central:** Autodesk Revit (Entorno paramétrico).
*   **Automatización Interna:** Python (pyRevit), Dynamo (Revit API) y C# (Revit SDK).
*   **Gestión y Control de Calidad IA:** CheckToBuild / Verity (para control de desviaciones Scan-vs-BIM).
*   **Estándar de Interoperabilidad:** OpenBIM (IFC 4.3 / IFC 5.0).

---

## 3. ARQUITECTURA DEL FLUJO DE TRABAJO ÓPTIMO (END-TO-END)

El flujo se divide en 4 fases críticas. Necesito que automatices los puentes de datos entre ellas:

### FASE 1: Ingesta de Datos y Segmentación IA (Nube de Puntos)
*   **Proceso:** El escaneo láser industrial se sube a la plataforma de IA (Aurivus/EdgeWise).
*   **Acción de la IA:** Clasificación automática de capas (Muros, Suelos, Vigas de acero, Tuberías MEP, Conductos HVAC).
*   **Salida:** Archivo geométrico pre-clasificado o familias nativas preliminares.

### FASE 2: Importación y Enlazado Automatizado en Revit
*   *Aquí requerimos automatización de código.*
*   **Requerimiento:** Crear un script que automatice la inserción de la nube de puntos orientada correctamente según las coordenadas compartidas del proyecto y cargue el modelo preliminar generado por la IA de reconstrucción.

### FASE 3: Auditoría de Datos, Parámetros y Control de Calidad (QC)
*   *Fase crítica de automatización.* El modelo industrial requiere una carga masiva de datos (parámetros de tuberías, materiales, sistemas, códigos Omniclass/Uniclass).
*   **Requerimiento:** Scripts para auditar de forma automática que no existan elementos duplicados y que todos los elementos extraídos por la IA tengan los parámetros requeridos por el cliente antes de la entrega.

### FASE 4: Control de Desviaciones (Scan-vs-BIM) y Entrega
*   **Proceso:** Herramientas de IA comparan el modelo BIM finalizado con la nube de puntos original para certificar la precisión milimétrica del modelo vendido.

---

## 4. INSTRUCCIONES PARA LA GENERACIÓN DE CÓDIGO Y SOLUCIONES

A partir de este momento, cuando te solicite una tarea, debes aplicar las siguientes reglas de desarrollo:

1.  **Código Limpio y Documentado:** Todo script en Python (para pyRevit o Dynamo) debe incluir manejo de excepciones (`try/except`), transacciones de la API de Revit cerradas correctamente (`TransactionManager`) y comentarios claros.
2.  **Enfoque Industrial:** Ten en cuenta que los modelos industriales manejan miles de tuberías y conexiones estructurales. El código debe ser óptimo en rendimiento para no congelar Revit.
3.  **Independencia de Interfaz:** Prioriza soluciones que utilicen la API de Revit mediante Python para que se ejecuten en segundo plano sin requerir clics del usuario.

---

## 5. PRIMER REQUERIMIENTO DE DESARROLLO

Para iniciar con el pie derecho y demostrar el valor al equipo, genera el siguiente script automatizado:

**Tarea:** Escribe un script en **Python para pyRevit (Revit API)** que recorra todas las tuberías (`Pipe`) y conductos (`Duct`) que fueron importados desde la herramienta de IA (Aurivus/EdgeWise). El script debe:
1.  Detectar automáticamente su diámetro/tamaño y su longitud.
2.  Escribir de forma masiva en un Parámetro de Proyecto Compartido llamado `"Estado_Revision_IA"` el valor `"Pendiente de Validar Humana"` si el elemento no está conectado en ambos extremos, o `"Validado Automático"` si la topología de la red de tuberías es correcta y continua.

Muestra el código estructurado y listo para producción.