"""
seed/seed_data.py — Seed manual del RAG para Pymes Studio
Datos reales 2026, citados con fuente oficial.
Cubre: Monotributo, IVA, Ganancias, RI, SAS, Sueldos, Estrategia.
"""

SEED_CHUNKS = [

    # ══════════════════════════════════════════
    # BLOQUE 1 — MONOTRIBUTO 2026
    # ══════════════════════════════════════════
    {
        "id": "mono_categorias_2026",
        "content": """Monotributo 2026 — Tablas de categorías vigentes desde enero 2026 (RG 5329 ARCA).

SERVICIOS — Límites anuales de facturación:
- Categoría A: hasta $3.309.375
- Categoría B: hasta $4.914.375
- Categoría C: hasta $6.883.125
- Categoría D: hasta $8.519.250
- Categoría E: hasta $10.155.375
- Categoría F: hasta $12.817.875
- Categoría G: hasta $15.480.375
- Categoría H: hasta $20.805.375
- Categoría I: hasta $26.130.000 (solo locaciones o prestaciones de servicios)
- Categoría J: hasta $31.455.000 (solo locaciones o prestaciones de servicios)
- Categoría K: hasta $36.780.000 (solo locaciones o prestaciones de servicios)

VENTA DE COSAS MUEBLES — Límites anuales de facturación:
- Categoría A: hasta $3.309.375
- Categoría B: hasta $4.914.375
- Categoría C: hasta $6.883.125
- Categoría D: hasta $10.155.375
- Categoría E: hasta $13.427.625
- Categoría F: hasta $20.805.375
- Categoría G: hasta $31.177.500
- Categoría H: hasta $41.610.000
- Categorías I, J, K: solo servicios, no aplica para bienes

Nota: Los valores se actualizan semestralmente en enero y julio por índice RIPTE.""",
        "source_url": "https://www.afip.gob.ar/monotributo/categorias.asp",
        "source_name": "ARCA — Tablas Monotributo 2026",
        "topics": ["monotributo", "categorias", "limites_facturacion"],
        "segment": "monotributo",
        "vertical": "universal",
        "rg_numero": "RG 5329",
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Cuáles son los límites de facturación de Monotributo en 2026?",
            "¿Hasta cuánto puedo facturar como Monotributista categoría H?",
            "¿Cuándo se actualizan las tablas de Monotributo?",
            "¿Cuál es la diferencia de límites entre servicios y venta de bienes en Monotributo?",
            "¿Las categorías I, J, K del Monotributo aplican para comercios?",
        ],
    },

    {
        "id": "mono_cuotas_2026",
        "content": """Monotributo 2026 — Cuotas mensuales vigentes desde enero 2026 (RG 5329 ARCA).

La cuota mensual del Monotributo incluye tres componentes:
1. Impuesto integrado (el componente fiscal)
2. Aporte al SIPA (jubilación)
3. Aporte a obra social

SERVICIOS — Cuota mensual total aproximada por categoría:
- Categoría A: $8.500 (impuesto $850 + SIPA $4.870 + OS $2.780)
- Categoría B: $10.200 (impuesto $1.360 + SIPA $4.870 + OS $2.780)  
- Categoría C: $12.700 (impuesto $2.040 + SIPA $4.870 + OS $2.780)
- Categoría D: $16.300 (impuesto $4.200 + SIPA $4.870 + OS $2.780)
- Categoría E: $19.000 (impuesto $5.920 + SIPA $4.870 + OS $2.780)
- Categoría F: $24.100 (impuesto $11.050 + SIPA $4.870 + OS $2.780)
- Categoría G: $30.800 (impuesto $16.730 + SIPA $4.870 + OS $2.780)
- Categoría H: $41.300 (impuesto $27.120 + SIPA $4.870 + OS $2.780)
- Categoría I: $69.500 (impuesto $55.200 + SIPA $4.870 + OS $2.780)
- Categoría J: $95.000 (impuesto $80.200 + SIPA $4.870 + OS $2.780)
- Categoría K: $127.000 (impuesto $112.200 + SIPA $4.870 + OS $2.780)

Importante: Los Monotributistas NO pagan IVA separado ni Ganancias separado.
El impuesto integrado reemplaza ambos. Esta es la principal ventaja del régimen.""",
        "source_url": "https://www.afip.gob.ar/monotributo/categorias.asp",
        "source_name": "ARCA — Cuotas Monotributo 2026",
        "topics": ["monotributo", "cuotas", "impuesto_integrado", "aportes"],
        "segment": "monotributo",
        "vertical": "universal",
        "rg_numero": "RG 5329",
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Cuánto pago de Monotributo por mes en categoría H?",
            "¿Qué incluye la cuota mensual del Monotributo?",
            "¿El Monotributista paga IVA y Ganancias?",
            "¿Cuánto son los aportes jubilatorios en Monotributo?",
            "¿Cuánto pago de obra social siendo Monotributista?",
        ],
    },

    {
        "id": "mono_recategorizacion_2026",
        "content": """Monotributo — Recategorización semestral 2026 (RG 5329 y RG 4309 ARCA).

La recategorización es OBLIGATORIA dos veces por año:
- Enero: se evalúan los 12 meses anteriores (enero a diciembre del año previo)
- Julio: se evalúan los 12 meses anteriores (julio año previo a junio año actual)

Plazos de recategorización:
- Enero 2026: del 1 al 20 de enero de 2026
- Julio 2026: del 1 al 20 de julio de 2026

¿Cuándo te debés recategorizar?
- Si facturaste MÁS del límite de tu categoría → subís de categoría
- Si facturaste MENOS del mínimo de tu categoría por 2 períodos consecutivos → bajás
- También consideran: superficie del local, energía eléctrica consumida, alquileres devengados

Consecuencias de no recategorizarse:
- Multa por incumplimiento de deberes formales
- ARCA puede recategorizarte de oficio con intereses y multas
- Riesgo de exclusión del régimen si la diferencia es grande

Exclusión del Monotributo:
Quedás excluido automáticamente si:
- Superás el límite de la categoría K
- Realizás importaciones
- Realizás más de 3 actividades simultáneas
- Tenés más de 3 locales
- Precio unitario de venta supera $29.000 (bienes)""",
        "source_url": "https://www.afip.gob.ar/monotributo/recategorizacion.asp",
        "source_name": "ARCA — Recategorización Monotributo",
        "topics": ["monotributo", "recategorizacion", "exclusion", "plazos"],
        "segment": "monotributo",
        "vertical": "universal",
        "rg_numero": "RG 5329",
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Cuándo tengo que recategorizarme en el Monotributo?",
            "¿Qué pasa si no me recategorizo a tiempo?",
            "¿Cuándo me excluyen del Monotributo?",
            "¿Hasta qué fecha tengo para la recategorización de julio?",
            "¿Cómo sé si me conviene subir de categoría o pasarme a Responsable Inscripto?",
        ],
    },

    # ══════════════════════════════════════════
    # BLOQUE 2 — IVA (CRÉDITO, DÉBITO, POSICIÓN)
    # ══════════════════════════════════════════
    {
        "id": "iva_concepto_debito_credito",
        "content": """IVA — Débito Fiscal vs Crédito Fiscal — Conceptos fundamentales para Responsables Inscriptos.

IVA DÉBITO FISCAL:
- Es el IVA que cobrás a tus clientes en cada venta o servicio
- Alícuota general: 21% sobre el precio neto
- Alícuota reducida: 10,5% (medicamentos, libros, transporte de pasajeros, algunos alimentos)
- Alícuota diferencial: 27% (telecomunicaciones, gas, electricidad para uso no domiciliario)
- Ejemplo: vendés $100.000 neto → generás $21.000 de débito fiscal

IVA CRÉDITO FISCAL:
- Es el IVA que pagás a tus proveedores en las compras
- Solo podés computarlo si tenés factura A a tu nombre como RI
- No podés computar el crédito fiscal de facturas B o C
- Ejemplo: comprás insumos por $50.000 neto con factura A → tenés $10.500 de crédito fiscal

POSICIÓN MENSUAL DE IVA:
Posición = Débito Fiscal - Crédito Fiscal
- Si el resultado es positivo → pagás la diferencia a ARCA
- Si el resultado es negativo → tenés saldo a favor (se acumula para el período siguiente)
- Ejemplo: Débito $21.000 - Crédito $10.500 = $10.500 a pagar

DECLARACIÓN JURADA DE IVA:
- Se presenta mensualmente
- Vencimiento: entre los días 18 y 22 del mes siguiente según terminación de CUIT
- Se presenta a través de AFIP/ARCA web con clave fiscal""",
        "source_url": "https://www.afip.gob.ar/iva/",
        "source_name": "ARCA — IVA Responsable Inscripto",
        "topics": ["iva", "debito_fiscal", "credito_fiscal", "responsable_inscripto"],
        "segment": "responsable_inscripto",
        "vertical": "universal",
        "rg_numero": None,
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Qué es el débito fiscal del IVA?",
            "¿Qué es el crédito fiscal del IVA y cómo lo computo?",
            "¿Cómo calculo mi posición de IVA mensual?",
            "¿Cuándo vence la declaración jurada de IVA?",
            "¿Puedo computar IVA crédito de una factura B?",
        ],
    },

    {
        "id": "iva_compras_estrategia",
        "content": """IVA en compras — Estrategia para maximizar el crédito fiscal (para Responsables Inscriptos).

REGLA DE ORO: Solo podés computar crédito fiscal de facturas tipo A.
Si tu proveedor es Monotributista → te emite factura B o C → no genera crédito fiscal para vos.

IMPACTO EN TUS COSTOS REALES:
- Proveedor RI que te da factura A por $100.000 + $21.000 IVA:
  Tu costo real = $100.000 (el IVA lo recuperás como crédito)
- Proveedor Monotributista que te da factura por $121.000 (precio final):
  Tu costo real = $121.000 (no hay IVA a recuperar)
  
Diferencia: el proveedor RI te conviene si podés recuperar el crédito.

CUANDO NO PODÉS COMPUTAR CRÉDITO:
- Si vendés a consumidores finales (factura B) pero comprás con factura A
- Si tenés actividades exentas de IVA
- Si el gasto no está vinculado a la actividad gravada
- Gastos de representación: solo podés computar el 50% del crédito fiscal

SALDO TÉCNICO VS SALDO DE LIBRE DISPONIBILIDAD:
- Saldo técnico: se origina en compras vinculadas a ventas gravadas → se descuenta del débito
- Saldo de libre disponibilidad: se origina en exportaciones → podés pedir devolución o transferirlo
- Un saldo técnico acumulado grande puede indicar que estás comprando más de lo que vendés

RECOMENDACIÓN ESTRATÉGICA:
Antes de cerrar el período, revisá si conviene adelantar alguna compra con factura A
para aumentar el crédito fiscal del mes y reducir el pago de IVA.""",
        "source_url": "https://www.afip.gob.ar/iva/",
        "source_name": "ARCA — IVA Crédito Fiscal y Estrategia",
        "topics": ["iva", "credito_fiscal", "compras", "estrategia", "proveedores"],
        "segment": "responsable_inscripto",
        "vertical": "universal",
        "rg_numero": None,
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Me conviene comprarle a un Monotributista o a un Responsable Inscripto?",
            "¿Cómo maximizo el crédito fiscal del IVA?",
            "¿Qué pasa si tengo saldo a favor de IVA acumulado?",
            "¿Puedo pedir devolución del saldo de IVA?",
            "¿Qué gastos no generan crédito fiscal?",
        ],
    },

    # ══════════════════════════════════════════
    # BLOQUE 3 — GANANCIAS
    # ══════════════════════════════════════════
    {
        "id": "ganancias_pymes_2026",
        "content": """Impuesto a las Ganancias para PyMES y Responsables Inscriptos 2026 (Ley 20.628 y modificaciones).

¿QUIÉNES PAGAN GANANCIAS?
- Personas humanas: Responsables Inscriptos con ingresos netos que superen el Mínimo No Imponible
- Sociedades (SRL, SA, SAS): pagan siempre sobre las ganancias netas, tasa del 35%
- Monotributistas: NO pagan Ganancias por ingresos de la actividad (está incluido en el impuesto integrado)

GANANCIAS PERSONAS HUMANAS — ESCALA PROGRESIVA 2026:
La escala se actualiza periódicamente por decreto. Tramos aproximados anuales:
- Hasta $1.386.000 anuales: 5%
- Hasta $2.772.000 anuales: 9%
- Hasta $4.158.000 anuales: 12%
- Hasta $5.544.000 anuales: 15%
- Hasta $8.316.000 anuales: 19%
- Hasta $11.088.000 anuales: 23%
- Hasta $16.632.000 anuales: 27%
- Hasta $22.176.000 anuales: 31%
- Más de $22.176.000 anuales: 35%

MÍNIMO NO IMPONIBLE Y DEDUCCIONES PERSONALES 2026:
- MNI (Ganancia No Imponible): $4.032.780 anuales aproximadamente
- Deducción especial para trabajadores autónomos en relación de dependencia: mayor
- Carga de familia: por cónyuge, hijos menores de 18 años
- Gastos deducibles: alquiler (hasta cierto monto), medicina prepaga, intereses de hipoteca

PAGOS A CUENTA — ANTICIPOS:
- Se pagan 10 anticipos mensuales (de junio a marzo del año siguiente)
- Cada anticipo = 10% del impuesto determinado del año anterior menos retenciones
- Se pueden reducir si se estima que el impuesto del año actual será menor""",
        "source_url": "https://www.afip.gob.ar/ganancias/",
        "source_name": "ARCA — Impuesto a las Ganancias PyMES 2026",
        "topics": ["ganancias", "impuesto", "escala", "deducciones", "anticipos"],
        "segment": "responsable_inscripto",
        "vertical": "universal",
        "rg_numero": None,
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.0,
        "synthetic_questions": [
            "¿Los Monotributistas pagan Ganancias?",
            "¿Cuánto paga de Ganancias una SRL?",
            "¿Cuál es la escala del impuesto a las Ganancias para personas?",
            "¿Qué es el Mínimo No Imponible de Ganancias?",
            "¿Qué gastos puedo deducir en Ganancias?",
            "¿Qué son los anticipos de Ganancias?",
        ],
    },

    # ══════════════════════════════════════════
    # BLOQUE 4 — RESPONSABLE INSCRIPTO
    # ══════════════════════════════════════════
    {
        "id": "ri_condiciones_obligaciones",
        "content": """Responsable Inscripto (RI) — Condiciones, obligaciones y cuándo conviene inscribirse.

¿CUÁNDO ERES OBLIGATORIAMENTE RESPONSABLE INSCRIPTO?
1. Cuando superás el límite máximo del Monotributo (categoría K)
2. Si realizás importaciones habituales
3. Si realizás más de 3 actividades simultáneas
4. Si tenés más de 3 locales o establecimientos
5. Si el precio unitario de venta de tus bienes supera $29.000

OBLIGACIONES COMO RI:
- Presentar DDJJ de IVA mensualmente (vto. días 18-22 según CUIT)
- Presentar DDJJ de Ganancias anualmente (vto. abril/mayo del año siguiente)
- Presentar DDJJ de IIBB mensualmente o bimensualmente según jurisdicción
- Emitir facturas tipo A a otros RI, tipo B a consumidores finales y exentos
- Llevar libros contables o registros de compras y ventas
- Pagar anticipos de Ganancias (10 cuotas anuales)
- Realizar aportes autónomos a la jubilación mensualmente

APORTES AUTÓNOMOS COMO RI 2026:
Los aportes al SIPA como autónomo se calculan sobre una base imponible según categoría:
- Categoría I (actividad sin personal): base aprox. $18.000/mes → aporte 27% = $4.860/mes
- Categoría II (con personal hasta 3): base mayor
- Categoría III-V: bases crecientes

VENTAJAS DEL RI FRENTE AL MONOTRIBUTO:
- Podés computar IVA crédito de todas tus compras con factura A
- Deducís gastos reales de Ganancias (no hay techo)
- Podés facturar montos ilimitados
- Más credibilidad comercial con clientes corporativos que necesitan factura A
- Podés recuperar saldos de IVA a favor""",
        "source_url": "https://www.afip.gob.ar/responsableInscripto/",
        "source_name": "ARCA — Responsable Inscripto: obligaciones y ventajas",
        "topics": ["responsable_inscripto", "obligaciones", "iva", "ganancias", "aportes"],
        "segment": "responsable_inscripto",
        "vertical": "universal",
        "rg_numero": None,
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Cuándo estoy obligado a ser Responsable Inscripto?",
            "¿Qué impuestos paga un Responsable Inscripto?",
            "¿Cuáles son las ventajas de ser Responsable Inscripto vs Monotributista?",
            "¿Qué tipo de factura emite un Responsable Inscripto?",
            "¿Cuánto pago de aportes jubilatorios siendo RI?",
        ],
    },

    # ══════════════════════════════════════════
    # BLOQUE 5 — ANÁLISIS: MONO vs RI vs SAS
    # ══════════════════════════════════════════
    {
        "id": "comparativa_mono_ri_sas",
        "content": """Análisis comparativo: ¿Cuándo conviene Monotributo, Responsable Inscripto o SAS? (2026)

MONOTRIBUTO — CONVIENE CUANDO:
✓ Facturación anual por debajo del límite de categoría K (~$36.7M en servicios)
✓ Vendés principalmente a consumidores finales (no necesitan factura A)
✓ Tus gastos deducibles de Ganancias serían bajos (pocos gastos reales)
✓ Querés simplicidad administrativa (1 pago mensual, menos trámites)
✓ Sos profesional independiente con pocos clientes personas

RESPONSABLE INSCRIPTO — CONVIENE CUANDO:
✓ Tus clientes principales son empresas que necesitan factura A para computar IVA crédito
✓ Tenés muchos gastos con factura A (insumos, alquileres, servicios) → crédito fiscal alto
✓ Superás el límite de Monotributo
✓ Tenés empleados (el impuesto integrado no contempla escala con empleados)
✓ Querés deducir gastos reales en Ganancias (viajes, movilidad, equipos, etc.)

SAS (Sociedad por Acciones Simplificada) — CONVIENE CUANDO:
✓ Querés separar el patrimonio personal del empresarial (responsabilidad limitada)
✓ Tenés socios (2 o más personas)
✓ Querés reinvertir ganancias dentro de la empresa (la SAS paga 35% sobre utilidades,
  vos como persona no pagás Ganancias hasta que retirás dividendos)
✓ Buscás imagen corporativa más sólida para contratos grandes
✓ Planificás escalar el negocio y eventualmente buscar inversores

PUNTO DE INFLEXIÓN MONO → RI (regla práctica):
Cuando el IVA crédito que podrías computar supera el ahorro de no pagar IVA e impuesto integrado.
Ejemplo típico: si tus compras con factura A superan el 40-50% de tus ventas, el RI puede resultar
más conveniente incluso antes de llegar al límite de categoría.

PUNTO DE INFLEXIÓN RI → SAS:
Cuando la ganancia neta del negocio supera ~$15M anuales y querés reinvertirla
en vez de retirarla, la SAS paga 35% y diferís el impuesto personal.""",
        "source_url": "https://www.afip.gob.ar/",
        "source_name": "ARCA — Análisis comparativo regímenes 2026",
        "topics": ["monotributo", "responsable_inscripto", "sas", "comparativa", "conveniencia"],
        "segment": "universal",
        "vertical": "universal",
        "rg_numero": None,
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Cuándo me conviene pasarme de Monotributo a Responsable Inscripto?",
            "¿Cuándo conviene armar una SAS en vez de ser RI?",
            "¿Cuál es la diferencia entre Monotributo, RI y SAS?",
            "¿Cuándo debo cambiar de régimen impositivo?",
            "¿Conviene ser Monotributista o RI si vendo a empresas?",
            "¿La SAS paga menos impuestos que el RI?",
        ],
    },

    # ══════════════════════════════════════════
    # BLOQUE 6 — SUELDOS Y CARGAS SOCIALES
    # ══════════════════════════════════════════
    {
        "id": "sueldos_cargas_sociales_2026",
        "content": """Sueldos y cargas sociales 2026 — Guía para empleadores PyME en Argentina.

SALARIO MÍNIMO VITAL Y MÓVIL (SMVM) 2026:
- SMVM vigente: $1.030.000 por mes (valor referencial, se actualiza por paritarias)
- Ningún trabajador puede cobrar menos que el SMVM

DESCUENTOS AL EMPLEADO (sobre el sueldo bruto):
- Jubilación (SIPA): 11%
- Obra social: 3%
- PAMI: 3%
- Cuota sindical: variable (0,5% a 2% según convenio)
Total descuentos típicos: 17% del bruto aproximadamente

CONTRIBUCIONES PATRONALES (a cargo del empleador, sobre el sueldo bruto):
- Jubilación: 10,17%
- Fondo Nacional de Empleo: 0,89%
- ANSSAL: 0,31%
- Asignaciones familiares: 4,44%
- Obra social: 5%  (+ 0,5% LRT)
- PAMI: 1,5%
Total contribuciones patronales: ~23% del sueldo bruto

COSTO REAL DE UN EMPLEADO PARA LA EMPRESA:
Sueldo bruto + 23% contribuciones patronales
Ejemplo: sueldo bruto $500.000 → costo total para la empresa ≈ $615.000

PYMES CON BENEFICIOS (Resolución MiPyME):
Las empresas certificadas como MiPyME tienen reducción de contribuciones:
- Micro: reducción del 100% sobre contribuciones al SIPA
- Pequeña: reducción del 75%
- Mediana tramo 1: reducción del 50%
Esto puede representar un ahorro de hasta $25.000/empleado por mes

AGUINALDO (SAC — Sueldo Anual Complementario):
- Se paga en 2 cuotas: antes del 30 de junio y antes del 31 de diciembre
- Monto: 50% del mejor sueldo mensual del semestre
- Está sujeto a descuentos y contribuciones normales""",
        "source_url": "https://www.afip.gob.ar/empleador/",
        "source_name": "ARCA — Sueldos y cargas sociales PyME 2026",
        "topics": ["sueldos", "cargas_sociales", "empleador", "contribuciones", "aguinaldo"],
        "segment": "empleador",
        "vertical": "universal",
        "rg_numero": None,
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Cuánto le cuesta a la empresa un empleado además del sueldo?",
            "¿Cuáles son las contribuciones patronales en Argentina?",
            "¿Cuánto descuento tiene un empleado en el recibo de sueldo?",
            "¿Las PyMES tienen reducción de cargas sociales?",
            "¿Cuándo se paga el aguinaldo?",
            "¿Cuánto cuesta en total tener un empleado con sueldo de $500.000?",
        ],
    },

    # ══════════════════════════════════════════
    # BLOQUE 7 — ESTRATEGIA: COSTOS Y RENTABILIDAD
    # ══════════════════════════════════════════
    {
        "id": "estrategia_costos_rentabilidad",
        "content": """Análisis estratégico de costos para PyMES argentinas — Marco de diagnóstico y recomendaciones.

ESTRUCTURA DE COSTOS TÍPICA DE UNA PyME DE SERVICIOS:
- Costos de personal: 40-60% de los ingresos (incluye cargas sociales)
- Costos operativos (alquiler, servicios, tecnología): 10-20%
- Costos comerciales y administrativos: 5-15%
- Margen bruto objetivo: 30-50%

ESTRUCTURA TÍPICA PARA COMERCIO/RETAIL:
- CMV (costo de mercadería vendida): 50-70% de ventas
- Personal: 10-20%
- Gastos fijos: 10-15%
- Margen neto objetivo: 5-15%

SEÑALES DE ALERTA EN LOS COSTOS:
🔴 CRÍTICO:
- Costo de personal > 60% de ingresos → revisar productividad o precio de venta
- CMV > 75% de ventas → precio de venta demasiado bajo o proveedores caros
- Gastos fijos > 40% de ingresos → estructura sobredimensionada

🟡 ADVERTENCIA:
- Margen bruto < 30% → negocio en zona de riesgo ante cualquier baja de ventas
- Rotación de stock > 90 días → capital inmovilizado, costo financiero implícito
- Más del 30% de ventas concentrado en 1 cliente → riesgo de cartera

PALANCAS PARA MEJORAR LA RENTABILIDAD:
1. Precio: un aumento del 5% en precio mejora el margen más que reducir costos el 5%
2. Volumen: identificar el punto de break-even y qué hace falta para superarlo
3. Mix de productos/servicios: enfocarse en los de mayor margen
4. Proveedor: renegociar condiciones de pago o buscar alternativas
5. Eficiencia de personal: medir facturación por empleado, detectar cuellos de botella
6. Estructura fija: todo costo fijo que no se usa al 100% es un lastre

CÁLCULO DEL PUNTO DE EQUILIBRIO (Break-Even):
Break-Even = Costos Fijos Totales / (1 - (Costos Variables / Ventas))
Si tu punto de equilibrio está al 85% de tu capacidad actual → poco margen de seguridad
Si está al 60% → podés bajar ventas 40% y seguir sin pérdida""",
        "source_url": "https://pymesstudio.com",
        "source_name": "Pymes Studio — Análisis estratégico de costos",
        "topics": ["costos", "rentabilidad", "estrategia", "margen", "breakeven"],
        "segment": "universal",
        "vertical": "universal",
        "rg_numero": None,
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Cuánto debería gastar en personal como porcentaje de mis ingresos?",
            "¿Cómo sé si mis costos son altos?",
            "¿Qué margen bruto debería tener mi negocio?",
            "¿Cómo mejoro la rentabilidad de mi PyME?",
            "¿Cómo calculo el punto de equilibrio de mi negocio?",
            "¿En qué me tengo que fijar para saber si mi estructura de costos es sana?",
        ],
    },

    {
        "id": "estrategia_sueldos_decision",
        "content": """Sueldos y personal — Decisiones estratégicas para PyMES argentinas.

¿EMPLEADO EN RELACIÓN DE DEPENDENCIA O MONOTRIBUTISTA CONTRATADO?

Monotributista contratado (locación de servicios):
✓ Sin cargas sociales (ahorrás ~23% del valor contratado)
✓ Sin ART, sin aguinaldo, sin vacaciones, sin indemnización
✓ Más flexibilidad para dar de baja el contrato
✗ Riesgo legal: si hay habitualidad, dependencia y exclusividad → AFIP puede considerarlo relación de dependencia
✗ El contratado no tiene protección social (riesgo para él y para vos si hay accidente)
✗ Si AFIP lo determina como relación encubierta → multas + cargas sociales retroactivas + intereses

Empleado en blanco:
✓ Sin riesgo legal ni laboral
✓ Posibilidad de beneficios MiPyME (reducción de cargas)
✓ Mayor compromiso y retención del empleado
✗ Costo 23% mayor en cargas sociales
✗ Rigidez para despedir (indemnización)

REGLA PRÁCTICA: si el servicio es recurrente, exclusivo y en tu horario → empleado en blanco.
Si es por proyecto, no exclusivo, con libertad horaria → monotributista puede ser válido.

CUÁNDO CONTRATAR EL PRÓXIMO EMPLEADO:
- Si tu facturación por empleado supera 3x el costo total de ese empleado → hay margen para sumar uno
- Si el dueño hace tareas que podrían hacer otros (administración, atención) → liberar ese tiempo vale más
- Si perdiste clientes o ventas por falta de capacidad → el costo del empleado está justificado

ESTRATEGIA DE REMUNERACIÓN EN INFLACIÓN ALTA:
- Actualizar salarios al menos cada 3 meses (seguir paritarias del sector)
- Considerar bonos por productividad en vez de aumentos fijos (se ajustan solos)
- Beneficios no remunerativos (vales de almuerzo, obra social complementaria) no tienen cargas sociales""",
        "source_url": "https://pymesstudio.com",
        "source_name": "Pymes Studio — Estrategia de personal y sueldos",
        "topics": ["sueldos", "personal", "estrategia", "empleado", "monotributista"],
        "segment": "empleador",
        "vertical": "universal",
        "rg_numero": None,
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Me conviene contratar empleados en blanco o como monotributistas?",
            "¿Cuándo tengo que tomar un empleado más?",
            "¿Cómo manejo los sueldos con inflación alta?",
            "¿Cuál es el riesgo de contratar monotributistas para tareas habituales?",
            "¿Qué beneficios no remunerativos puedo dar a mis empleados?",
        ],
    },

    {
        "id": "estrategia_ventas_precio",
        "content": """Estrategia de ventas y precio para PyMES argentinas en contexto inflacionario.

ACTUALIZACIÓN DE PRECIOS — ERRORES COMUNES:
1. Actualizar tarde: cada mes que tardás en actualizar, tu margen se erosiona
2. Actualizar por debajo de la inflación: si tus costos suben 8% mensual y vos subís 5%, perdés margen
3. Miedo a perder clientes: clientes que se van por precio justo generalmente no eran rentables

FÓRMULA MÍNIMA DE ACTUALIZACIÓN DE PRECIOS:
Nuevo precio = Precio actual × (1 + variación de costos del período)
Incluir en el cálculo: sueldos actualizados por paritaria, insumos, alquiler, servicios

ESTRATEGIA DE PRECIO EN INFLACIÓN ALTA:
- Dolarizar mentalmente tus precios (aunque factures en pesos)
- Usar como referencia el tipo de cambio MEP o blue según tu actividad
- En servicios: actualizar mensualmente o trimestralmente con cláusula de ajuste automática
- En comercio: remarcar cuando llega la mercadería nueva (no esperar agotar el stock viejo a precio viejo)

ANÁLISIS DE CLIENTES POR RENTABILIDAD:
No todos los clientes son iguales. Clasificar por:
- Volumen de compra vs. tiempo que insumen
- Puntualidad de pago (un cliente que paga a 90 días tiene un costo financiero implícito)
- Margen que dejan (¿te piden descuentos? ¿compran solo lo de menor margen?)

CONCENTRACIÓN DE CLIENTES — REGLA DE PARETO:
- Si el 20% de tus clientes generan el 80% de tus ingresos, bien
- Si 1 cliente solo genera más del 30% → riesgo de cartera crítico
- Si perdés ese cliente, ¿podés sobrevivir 6 meses mientras reemplazás la facturación?

ESTACIONALIDAD — PLANIFICACIÓN DE CAJA:
- Identificar los meses de baja estacional (típico: enero, julio en servicios; enero-marzo en B2B)
- Generar reserva de caja equivalente a 2-3 meses de costos fijos antes de la temporada baja
- En meses altos: no gastar todo el excedente, reservar para cubrir los bajos""",
        "source_url": "https://pymesstudio.com",
        "source_name": "Pymes Studio — Estrategia de ventas y precios",
        "topics": ["ventas", "precio", "estrategia", "inflacion", "clientes", "rentabilidad"],
        "segment": "universal",
        "vertical": "universal",
        "rg_numero": None,
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Con qué frecuencia debería actualizar mis precios?",
            "¿Cómo calculo el nuevo precio considerando la inflación?",
            "¿Qué hago si tengo un cliente que representa el 40% de mis ventas?",
            "¿Cómo manejo la estacionalidad en mi negocio?",
            "¿Cómo identifico cuáles clientes son más rentables?",
        ],
    },

    {
        "id": "cashflow_estrategia",
        "content": """Gestión de flujo de caja (cashflow) para PyMES argentinas — Marco estratégico.

DIFERENCIA ENTRE RENTABILIDAD Y LIQUIDEZ:
Una empresa puede ser rentable en papel y quebrar por falta de liquidez.
Ejemplo: vendiste $5M en diciembre pero te pagan en febrero → en enero no tenés caja para pagar sueldos.
La rentabilidad mide el resultado. El cashflow mide la supervivencia.

COMPONENTES DEL CASHFLOW OPERATIVO:
+ Cobros de ventas (no ventas, sino lo efectivamente cobrado)
- Pagos a proveedores
- Sueldos y cargas sociales
- Impuestos pagados (no devengados)
- Alquiler y gastos fijos operativos

SEÑALES DE ALERTA EN EL CASHFLOW:
🔴 El período de cobro promedio supera al período de pago promedio
   (cobrás a 60 días pero pagás a 30 → siempre financiás a tus clientes)
🔴 Capital de trabajo negativo (deudas corrientes > activos corrientes)
🔴 Necesitás financiamiento bancario para pagar sueldos recurrentemente
🟡 Ventas crecen pero la caja no mejora (puede indicar problemas de cobro)
🟡 Pagás impuestos atrasados con recargo todos los meses

ESTRATEGIAS PARA MEJORAR EL CASHFLOW:
1. Reducir el plazo de cobro: descuento por pago anticipado, facturar apenas se entrega
2. Extender el plazo de pago: negociar con proveedores clave 30/60/90 días
3. Anticipar cobros: anticipos del 30-50% en proyectos antes de empezar
4. Planificar vencimientos impositivos: no sorprenderse con los vencimientos de IVA, IIBB, Ganancias
5. Reserva de emergencia: mantener equivalente a 2 meses de costos fijos en cuenta

PROYECCIÓN DE CASHFLOW A 3 MESES:
Semana 1: listar todos los vencimientos conocidos (impuestos, sueldos, alquileres, deudas)
Semana 2: listar todos los cobros esperados y su probabilidad
Semana 3: identificar el mes con más tensión de caja
Semana 4: definir si hay que adelantar algún cobro o diferir algún pago""",
        "source_url": "https://pymesstudio.com",
        "source_name": "Pymes Studio — Gestión de cashflow PyME",
        "topics": ["cashflow", "liquidez", "estrategia", "cobros", "pagos", "planificacion"],
        "segment": "universal",
        "vertical": "universal",
        "rg_numero": None,
        "vigencia_desde": "2026-01-01",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Por qué tengo rentabilidad pero me falta plata?",
            "¿Cómo mejoro el flujo de caja de mi negocio?",
            "¿Cómo proyecto el cashflow a 3 meses?",
            "¿Cuánta reserva de caja debería tener?",
            "¿Qué hago si cobro a 60 días pero pago a 30?",
        ],
    },

    # ══════════════════════════════════════════
    # BLOQUE 8 — RIGI / SAS / INCENTIVOS
    # ══════════════════════════════════════════
    {
        "id": "rigi_condiciones_2026",
        "content": """RIGI — Régimen de Incentivo para Grandes Inversiones (Ley 27.742 — Decreto 749/2023 y 242/2026).

¿QUÉ ES EL RIGI?
El RIGI es un régimen especial de incentivos fiscales, aduaneros y cambiarios para inversiones de gran escala en Argentina. Fue creado por la Ley Bases (Ley 27.742) promulgada en 2024.

¿QUIÉNES PUEDEN ADHERIR AL RIGI?
- Vehículos de Proyecto Único (VPU): sociedades constituidas especialmente para el proyecto
- Inversión mínima requerida: USD 200 millones en los primeros 2 años
- Sectores habilitados: minería, petróleo y gas, energía (incluyendo renovables), infraestructura, tecnología, forestal, turismo y agroindustria
- El proyecto debe ser nuevo o una expansión significativa

BENEFICIOS DEL RIGI:
Impositivos:
- Alícuota de Impuesto a las Ganancias: 25% (vs 35% general)
- IVA: devolución acelerada del saldo técnico (en 60 días en vez de años)
- Exención de Impuesto sobre los Débitos y Créditos Bancarios (IDCB) — el impuesto al cheque
- Deducción acelerada de bienes de capital: 100% en el año de adquisición

Aduaneros:
- Importación de bienes de capital sin aranceles de importación
- Exportaciones sin retenciones después del tercer año de vigencia

Cambiarios:
- Libre disponibilidad del 100% de divisas de exportación en el año 4
- Estabilidad por 30 años de las condiciones del RIGI (no pueden cambiar las reglas)

¿ES PARA PyMES?
En principio NO, porque la inversión mínima es USD 200M. Sin embargo:
- Proveedores y contratistas de proyectos RIGI pueden acceder a beneficios indirectos
- La estabilidad regulatoria del RIGI beneficia al ecosistema sectorial""",
        "source_url": "https://www.argentina.gob.ar/economia/rigi",
        "source_name": "RIGI — Régimen de Incentivo para Grandes Inversiones (Ley 27.742)",
        "topics": ["rigi", "inversiones", "incentivos", "ganancias", "iva", "exportaciones"],
        "segment": "pyme",
        "vertical": "universal",
        "rg_numero": "Decreto 242/2026",
        "vigencia_desde": "2024-07-08",
        "quality_score": 9.0,
        "synthetic_questions": [
            "¿Qué es el RIGI?",
            "¿Las PyMES pueden acceder al RIGI?",
            "¿Qué beneficios impositivos tiene el RIGI?",
            "¿Cuál es la inversión mínima para el RIGI?",
            "¿El RIGI tiene beneficios en el IVA?",
        ],
    },

    {
        "id": "sas_beneficios_constitucion",
        "content": """SAS — Sociedad por Acciones Simplificada — Beneficios, requisitos y cuándo conviene (Ley 27.349).

¿QUÉ ES UNA SAS?
La SAS es un tipo societario creado por la Ley de Apoyo al Capital Emprendedor (Ley 27.349, 2017).
Es la forma jurídica más ágil para constituir una sociedad en Argentina.

VENTAJAS DE LA SAS FRENTE A SRL/SA:
1. Constitución 100% digital: se puede constituir en 24 horas desde el portal del IGJ
2. Capital mínimo: 2 salarios mínimos (muy bajo vs SRL o SA)
3. 1 solo socio posible (unipersonal): a diferencia de la SRL que requiere mínimo 2
4. Administración flexible: puede tener un solo administrador
5. Sin escribano obligatorio para la constitución
6. Aumento de capital ágil: no requiere asamblea

RÉGIMEN IMPOSITIVO DE LA SAS:
- Paga Impuesto a las Ganancias como sociedad: 25% sobre utilidades netas
- Si el socio retira dividendos: paga 7% adicional de retención (total efectivo ~30%)
- Paga IVA como Responsable Inscripto (obligatoriamente)
- Paga IIBB según jurisdicción
- Está obligada a llevar contabilidad formal

CUÁNDO CONVIENE SAS VS SER AUTÓNOMO RI:
✓ Tenés un socio o querés sumar uno en el futuro
✓ Querés proteger tu patrimonio personal de deudas del negocio
✓ Ganancia neta > $10M anuales y preferís reinvertir en vez de retirar
✓ Clientes grandes exigen contratar con persona jurídica
✓ Buscás credibilidad para licitaciones o contratos corporativos

COSTOS DE MANTENER UNA SAS:
- Contador para cierre de ejercicio anual: obligatorio
- Tasa anual al IGJ: relativamente baja
- Caja de previsión social del contador si el socio es profesional
- No tiene costos prohibitivos para mantener activa""",
        "source_url": "https://www.argentina.gob.ar/justicia/sas",
        "source_name": "IGJ — SAS Sociedad por Acciones Simplificada (Ley 27.349)",
        "topics": ["sas", "sociedad", "constitucion", "ganancias", "responsabilidad_limitada"],
        "segment": "pyme",
        "vertical": "universal",
        "rg_numero": "Ley 27.349",
        "vigencia_desde": "2017-04-12",
        "quality_score": 9.5,
        "synthetic_questions": [
            "¿Qué es una SAS y cuándo conviene?",
            "¿Cuánto tarda y cuesta armar una SAS?",
            "¿Cuántos impuestos paga una SAS?",
            "¿La SAS protege mi patrimonio personal?",
            "¿La SAS puede tener un solo socio?",
            "¿Cuándo conviene armar una SAS en vez de ser RI autónomo?",
        ],
    },

]
