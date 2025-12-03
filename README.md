# Análisis de Inclusión Digital - Valle del Cauca & Jamundí

## 📊 Descripción del Proyecto

Proyecto de análisis integral de inclusión digital enfocado en Valle del Cauca y específicamente en el municipio de Jamundí, Colombia. El objetivo principal es analizar patrones de conectividad a internet, brechas de infraestructura y equidad digital a través de diferentes estratos socioeconómicos utilizando datasets gubernamentales oficiales.

Este proyecto genera insights accionables para stakeholders incluyendo funcionarios gubernamentales, empresas de telecomunicaciones e investigadores mediante un dashboard interactivo en PowerBI que visualiza cobertura de conectividad, métricas de calidad, competencia de mercado e impacto educativo.

## 🎯 Objetivos

- Analizar la evolución de la conectividad a internet en Jamundí desde 2017 hasta 2021
- Identificar brechas de acceso digital entre diferentes estratos socioeconómicos
- Evaluar la calidad de los servicios de internet (velocidad de descarga/subida)
- Medir la concentración del mercado de telecomunicaciones
- Correlacionar conectividad con indicadores educativos
- Mapear zonas WiFi públicas y su distribución geográfica
- Calcular índices de equidad digital (Gini, brecha de conectividad)

## 📁 Estructura del Proyecto

```
.
├── README.md                           # Este archivo
├── preparación datos/
│   ├── procesamiento_datos.py              # Script de preparación y limpieza de datos
│   └── datos/                              # Directorio de datos (generados automáticamente)
│       ├── conectividad_pais_raw.csv      # Datos crudos de conectividad (API)
│       ├── conectividad_pais.csv          # Datos limpios de conectividad
│       ├── Zonas_WiFi_en_el_Departamento_del_Valle_del_Cauca.csv
│       ├── MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR_BÁSICA_Y_MEDIA_POR_MUNICIPIO.csv
│       ├── censo_social_2018_jamundi.csv
│       └── censo_proyecciones_jamundi_2020-2035.csv
└── KPIsConectividadJamundi.pbix         # Dashboard PowerBI
```

## 🗃️ Fuentes de Datos

### Datos de Conectividad
- **Fuente**: [Datos Abiertos Colombia](https://www.datos.gov.co)
- **API**: Accesos a Internet Fijo por Municipio
- **Período**: 2017-2021 (trimestral)
- **Variables**: proveedor, tecnología, velocidad_bajada, velocidad_subida, no_de_accesos, segmento (estrato)

### Zonas WiFi Públicas
- **Fuente**: [Datos Abiertos Colombia](https://www.datos.gov.co)
- **Contenido**: Ubicación de zonas WiFi públicas en Valle del Cauca
- **Variables**: coordenadas geográficas, ubicación, dirección

### Estadísticas Educativas
- **Fuente**: [Ministerio de Educación Nacional (MEN) a través de Datos Abiertos Colombia](https://www.datos.gov.co)
- **Contenido**: Estadísticas de educación preescolar, básica y media
- **Variables**: cobertura neta/bruta, deserción, aprobación, sedes conectadas a internet

### Censo y Proyecciones Poblacionales
- **Fuente**: [DANE - Censo Nacional 2018](https://www.dane.gov.co)
- **Contenido**: 
  - Censo social 2018 (características demográficas y limitaciones físicas)
  - Proyecciones poblacionales 2020-2035 post-COVID-19

## 🛠️ Stack Tecnológico

### Preparación de Datos
- **Python 3.x**
  - `pandas`: Manipulación y análisis de datos
  - `numpy`: Operaciones numéricas
  - `requests`: Descarga de datos desde APIs
  - `openpyxl`: Lectura de archivos Excel
  - `python-dotenv`: Gestión de variables de entorno

### Visualización
- **Microsoft PowerBI Desktop**: Dashboard interactivo con múltiples vistas analíticas

### Datos Geográficos
- Códigos DIVIPOLA para geografía administrativa colombiana
- Integración con mapas de TomTom y Microsoft

## 📦 Instalación y Configuración

### Prerrequisitos
```bash
Python 3.8+
PowerBI Desktop
```

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd analisis-inclusion-digital-jamundi
```

### 2. Instalar Dependencias
```bash
pip install pandas numpy requests openpyxl python-dotenv
```

### 3. Configurar Variables de Entorno
Crear un archivo `.env` en la carpeta 'preparación datos' del proyecto a partir del archivos `.env.example`: 
```
APP_TOKEN=tu_token_de_datos_gov_co
SECRET_TOKEN=tu_token_secreto_de_datos_gov_co
```

Para obtener un token de API:
1. Visita https://www.datos.gov.co
2. Regístrate o inicia sesión
3. Solicita un token de API en tu perfil

### 4. Ejecutar el Script de Preparación de Datos
```bash
python procesamiento_datos.py
```

Este script:
- ✅ Descarga datos de conectividad desde la API de datos.gov.co
- ✅ Limpia y normaliza datos (convierte XDSL de Kbps a Mbps)
- ✅ Detecta y reemplaza outliers usando método IQR
- ✅ Descarga automáticamente archivos del DANE si no existen localmente
- ✅ Filtra datos específicos para Jamundí
- ✅ Genera archivos CSV procesados en el directorio `datos/`

### 5. Abrir el Dashboard
```bash
# Abrir con PowerBI Desktop
dashboard_conectividad.pbix
```

## 📊 Estructura del Dashboard

### Página 1: Panorama General de Accesos
- **Total de Accesos**: Métrica principal de penetración de internet
- **Penetración por cada 100 habitantes**: Indicador de cobertura poblacional
- **Conectividad Escolar**: Porcentaje de sedes educativas con internet
- **Serie temporal**: Evolución de accesos por trimestre y segmento (estratos 1-6)
- **Distribución por segmento**: Pie chart de accesos en último trimestre

### Página 2: Calidad del Servicio
- **Velocidad de Descarga/Subida Promedio**: Tendencias por estrato y tecnología
- **Categorías de Velocidad**: 
  - Básico (<25 Mbps)
  - Banda Ancha (25-99 Mbps)
  - Alta Velocidad (100-999 Mbps)
- **Índice de Simetría**: Relación entre velocidad de subida y bajada
- **Porcentaje de Fibra**: Adopción de tecnología FTTH

### Página 3: Competencia de Mercado
- **HHI (Herfindahl-Hirschman Index)**: Concentración del mercado
  - HHI > 2500: Alta concentración
  - 1500 < HHI < 2500: Concentración moderada
  - HHI < 1500: Mercado competitivo
- **Distribución por Proveedor**: Top proveedores y su participación de mercado
- **Tecnologías Desplegadas**: Cable, FTTH, HFC, XDSL, Satelital, etc.

### Página 4: Equidad Digital
- **Coeficiente de Gini**: Medida de desigualdad en acceso (0 = perfecta igualdad, 1 = desigualdad total)
- **Brecha de Conectividad**: Diferencia entre estratos altos y bajos
- **Brecha de Velocidad**: Gap de calidad del servicio entre estratos
- **Mapa de Zonas WiFi**: Distribución geográfica de acceso público
- **Acceso por Categoría de Ingresos**: Comparación entre estratos socioeconómicos

## 🔑 KPIs Principales

### 1. Cobertura de Acceso
- Total de Accesos
- Penetración por cada 100 habitantes
- Tasa de crecimiento trimestral/anual
- Cobertura por estrato socioeconómico

### 2. Calidad de Desempeño
- Velocidad promedio de descarga/subida
- Índice de simetría (relación subida/bajada)
- Distribución por categorías de velocidad
- Latencia y estabilidad (cuando disponible)

### 3. Infraestructura Tecnológica
- Porcentaje de accesos por tecnología (FTTH, HFC, XDSL, etc.)
- Tasa de adopción de fibra óptica
- Cobertura de tecnologías de nueva generación

### 4. Competencia de Mercado
- HHI (Herfindahl-Hirschman Index)
- Participación de mercado por proveedor
- Número de proveedores activos
- Oportunidades de adopción FTTH en áreas desatendidas

### 5. Métricas de Equidad
- Coeficiente de Gini
- Brecha de conectividad (diferencia max-min entre estratos)
- Brecha de velocidad

## 🔧 Procesamiento de Datos

### Limpieza y Normalización

El script `procesamiento_datos.py` implementa las siguientes operaciones:

#### 1. Normalización de Unidades
```python
# XDSL se registra en Kbps, otras tecnologías en Mbps
# Conversión de XDSL: Kbps → Mbps (dividir por 1000)
```

#### 2. Detección de Outliers (Método IQR)
- Cálculo por grupos: tecnología × segmento
- Límites: Q1 - 1.5×IQR y Q3 + 1.5×IQR
- Reemplazo: outliers → mediana del grupo

**Ventajas del método IQR sobre Z-score**:
- Más robusto ante distribuciones asimétricas
- No asume normalidad de datos
- Mejor manejo de valores extremos en datos de conectividad

#### 3. Manejo de Datos Faltantes
- Remoción de filas/columnas completamente vacías
- Filtrado específico por municipio (Jamundí)
- Validación de consistencia de códigos DIVIPOLA

#### 4. Descarga Automática
```python
# Descarga inteligente: solo si el archivo no existe
download_file(url, destination)
# Evita re-descargas innecesarias de archivos grandes del DANE
```

## 📈 Casos de Uso

### Para Funcionarios Gubernamentales
- Identificar áreas prioritarias para inversión en infraestructura digital
- Evaluar el impacto de políticas de conectividad
- Medir brechas de equidad digital para programas sociales
- Monitorear cumplimiento de metas de conectividad escolar

### Para Empresas de Telecomunicaciones
- Análisis de oportunidades de mercado en áreas desatendidas
- Benchmarking de calidad de servicio vs. competencia
- Identificación de segmentos con demanda insatisfecha
- Planificación estratégica de despliegue de FTTH

### Para Instituciones Educativas
- Correlación entre conectividad y deserción escolar
- Priorización de sedes para programas de conectividad
- Evaluación del impacto de internet en indicadores educativos

### Para Investigadores
- Análisis longitudinal de inclusión digital (2017-2021)
- Estudios de equidad digital y estratificación socioeconómica
- Evaluación de competencia en mercados de telecomunicaciones
- Proyecciones de necesidades futuras basadas en tendencias

## 🚀 Próximos Pasos

### Corto Plazo
- [ ] Actualizar con datos de 2022-2024 (cuando estén disponibles)
- [ ] Incorporar datos de uso de datos móviles
- [ ] Añadir métricas de asequibilidad (precio/Mbps)
- [ ] Implementar alertas automáticas para cambios significativos

### Mediano Plazo
- [ ] Expandir análisis a todos los municipios de Valle del Cauca
- [ ] Desarrollar modelo predictivo de adopción de internet
- [ ] Crear comparativas departamentales
- [ ] Implementar dashboard web interactivo (Plotly Dash / Streamlit)

### Largo Plazo
- [ ] Integración con datos de uso real de internet (si disponibles)
- [ ] Análisis de correlación con indicadores socioeconómicos adicionales
- [ ] Sistema de recomendación de políticas públicas basado en ML
- [ ] API pública para acceso programático a KPIs

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Notas Importantes

### Calidad de Datos
- **Inconsistencias de unidades**: XDSL históricamente registrado en Kbps requiere normalización
- **Outliers**: Datos históricos contienen valores imposibles que indican errores de entrada
- **Valores faltantes**: Datos de educación pueden tener campos vacíos en ciertos años

### Consideraciones Metodológicas
- El número de accesos se usa como proxy de hogares para cálculos ponderados
- Las proyecciones poblacionales fueron actualizadas post-COVID-19 por el DANE
- HHI se calcula solo sobre proveedores activos en el último trimestre

### Limitaciones
- Datos agregados por trimestre (no hay granularidad mensual)
- No incluye datos de internet móvil (solo conexiones fijas)
- Estratos 5 y 6 tienen menor representación en la muestra

## 📄 Licencia

Este proyecto utiliza datos públicos del gobierno colombiano. El código y análisis son de uso libre para fines educativos y de investigación.

## 📧 Contacto

Para preguntas, sugerencias o colaboraciones:
- Proyecto: Análisis de Inclusión Digital - Valle del Cauca & Jamundí
- Fuentes de datos: [datos.gov.co](https://www.datos.gov.co), [DANE](https://www.dane.gov.co), [MEN](https://www.mineducacion.gov.co)