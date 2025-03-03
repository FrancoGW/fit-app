# FITAPP

![FITAPP Logo](fitapp/logo.png)

## Sistema Integral de Gestión para Gimnasios

FITAPP es una aplicación moderna y completa diseñada específicamente para la administración eficiente de gimnasios, centros de fitness y estudios deportivos. Nuestra solución optimiza todos los aspectos operativos del negocio, desde la gestión de miembros hasta el seguimiento financiero.

## Características Principales

### Gestión de Miembros
- **Registro y Perfil**: Información completa de cada miembro, incluyendo datos personales, historial de pagos y asistencia.
- **Control de Acceso**: Sistema de check-in/check-out para monitorear la asistencia.
- **Seguimiento de Progreso**: Registro histórico de medidas corporales, peso y logros de fitness.

### Administración de Membresías
- **Planes Personalizables**: Creación de diferentes tipos de membresías con precios y privilegios específicos.
- **Renovaciones Automáticas**: Notificaciones de vencimiento y procesamiento de renovaciones.
- **Promociones y Descuentos**: Gestión flexible de ofertas especiales.

### Gestión Financiera
- **Control de Pagos**: Registro y seguimiento de todas las transacciones.
- **Reportes Detallados**: Análisis de ingresos, gastos y proyecciones financieras.
- **Facturación Integrada**: Generación automática de facturas y comprobantes.

### Programación de Clases
- **Calendario Dinámico**: Visualización clara de todas las clases y actividades.
- **Reservas Online**: Sistema para que los miembros puedan reservar su lugar en clases grupales.
- **Asignación de Instructores**: Administración eficiente del personal.

### Panel de Control Intuitivo
- **Vista Centralizada**: Información clave del negocio en una sola pantalla.
- **Métricas en Tiempo Real**: Estadísticas actualizadas sobre membresías, ingresos y asistencia.
- **Alertas Personalizables**: Notificaciones importantes sobre vencimientos o situaciones específicas.

## Requisitos Técnicos

- Python 3.8+
- Bases de datos SQLite (incluidas: fitapp.db, gym.db)
- Módulos y dependencias detallados en el archivo de configuración

## Instalación

1. Clone el repositorio:
```
git clone https://github.com/FrancoGW/fit-app.git
```

2. Navegue al directorio del proyecto:
```
cd fit-app
```

3. Instale las dependencias:
```
pip install -r requirements.txt
```

4. Ejecute la aplicación:
```
python main.py
```

## Estructura del Proyecto

```
FITAPP/
├── bin/                  # Archivos binarios
├── build/                # Archivos de compilación
├── config/               # Configuraciones de la aplicación
├── dist/                 # Archivos de distribución
├── include/              # Archivos de cabecera
├── lib/                  # Bibliotecas
├── models/               # Modelos de datos
├── resources/            # Recursos (imágenes, audio, etc.)
├── ui/                   # Archivos de interfaz de usuario
├── utils/                # Utilidades y herramientas
├── .gitignore            # Archivos ignorados por Git
├── asd.csv               # Datos CSV de ejemplo
├── fitapp.db             # Base de datos principal
├── gym.db                # Base de datos secundaria
├── main.py               # Punto de entrada de la aplicación
├── main.spec             # Especificaciones del programa
├── pyenv.cfg             # Configuración del entorno Python
└── README.md             # Este archivo
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, siga estos pasos:

1. Fork el repositorio
2. Cree una nueva rama (`git checkout -b feature/nueva-funcionalidad`)
3. Realice sus cambios
4. Commit sus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
5. Push a la rama (`git push origin feature/nueva-funcionalidad`)
6. Abra un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo LICENSE para más detalles.

## Contacto

Franco GW - [github.com/FrancoGW](https://github.com/FrancoGW)

Link del proyecto: [https://github.com/FrancoGW/fit-app](https://github.com/FrancoGW/fit-app)