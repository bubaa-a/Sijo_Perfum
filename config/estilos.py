"""
Configuración de estilos visuales unificados para todo el sistema
Paleta de colores, tipografía y constantes de diseño
"""

# ============================================
# PALETA DE COLORES PRINCIPAL
# ============================================

class Colores:
    """Paleta de colores unificada del sistema"""

    # Colores primarios (gradientes)
    PRIMARY_START = "#667eea"
    PRIMARY_END = "#764ba2"
    PRIMARY_DARK = "#5a67d8"
    PRIMARY_LIGHT = "#7c8cf5"

    # Colores secundarios
    SECONDARY = "#4834d4"
    SECONDARY_DARK = "#3742fa"
    SECONDARY_LIGHT = "#6c5ce7"

    # Colores de acción
    SUCCESS = "#2ed573"
    SUCCESS_HOVER = "#26b85f"
    WARNING = "#ffa502"
    WARNING_HOVER = "#ff9000"
    DANGER = "#ff3838"
    DANGER_HOVER = "#e62020"
    INFO = "#00a8ff"
    INFO_HOVER = "#0088cc"

    # Colores de estado
    DISPONIBLE = "#27ae60"
    STOCK_BAJO = "#f39c12"
    AGOTADO = "#e74c3c"
    ACTIVO = "#10ac84"
    INACTIVO = "#95a5a6"

    # Colores neutros
    GRIS_OSCURO = "#2c3e50"
    GRIS_MEDIO = "#7f8c8d"
    GRIS_CLARO = "#95a5a6"
    GRIS_MUY_CLARO = "#ecf0f1"

    # Fondos
    BG_PRIMARY = "#f0f2f5"
    BG_SECONDARY = "#ffffff"
    BG_CARD = "#ffffff"
    BG_HOVER = "#f8f9fa"

    # Bordes
    BORDER_LIGHT = "#e9ecef"
    BORDER_MEDIUM = "#dee2e6"
    BORDER_DARK = "#adb5bd"

    # Texto
    TEXT_PRIMARY = "#2c3e50"
    TEXT_SECONDARY = "#7f8c8d"
    TEXT_WHITE = "#ffffff"
    TEXT_MUTED = "#6c757d"

    # Backgrounds de alertas
    ALERT_SUCCESS_BG = "#d1ecf1"
    ALERT_SUCCESS_TEXT = "#0c5460"
    ALERT_WARNING_BG = "#fff3cd"
    ALERT_WARNING_TEXT = "#856404"
    ALERT_DANGER_BG = "#f8d7da"
    ALERT_DANGER_TEXT = "#721c24"
    ALERT_INFO_BG = "#d1f2eb"
    ALERT_INFO_TEXT = "#0c5460"


# ============================================
# TIPOGRAFÍA
# ============================================

class Fuentes:
    """Configuración de fuentes del sistema"""

    FAMILIA_PRINCIPAL = "Segoe UI"
    FAMILIA_ALTERNATIVA = "Arial"
    FAMILIA_MONOSPACE = "Consolas"

    # Tamaños
    XXL = 32
    XL = 24
    LARGE = 20
    GRANDE = 18
    MEDIANO_GRANDE = 16
    MEDIANO = 14
    NORMAL = 12
    PEQUENO = 11
    MUY_PEQUENO = 10
    MINI = 9

    # Pesos
    BOLD = "bold"
    NORMAL_WEIGHT = "normal"
    ITALIC = "italic"


# ============================================
# ESPACIADOS Y DIMENSIONES
# ============================================

class Espaciado:
    """Espaciados estándar del sistema"""

    # Padding
    XXL = 40
    XL = 30
    LARGE = 25
    MEDIO = 20
    NORMAL = 15
    PEQUENO = 10
    MUY_PEQUENO = 5
    MINI = 3

    # Margins
    MARGIN_XXL = 40
    MARGIN_XL = 30
    MARGIN_LARGE = 25
    MARGIN_MEDIO = 20
    MARGIN_NORMAL = 15
    MARGIN_PEQUENO = 10
    MARGIN_MUY_PEQUENO = 5


class Dimensiones:
    """Dimensiones estándar de componentes"""

    # Alturas
    HEADER_HEIGHT = 100
    FOOTER_HEIGHT = 80
    BUTTON_HEIGHT_LARGE = 45
    BUTTON_HEIGHT_NORMAL = 38
    BUTTON_HEIGHT_SMALL = 32
    ENTRY_HEIGHT = 36
    ENTRY_HEIGHT_SMALL = 32

    # Anchos
    SIDEBAR_WIDTH = 280
    BUTTON_WIDTH_LARGE = 200
    BUTTON_WIDTH_NORMAL = 140
    BUTTON_WIDTH_SMALL = 100
    ENTRY_WIDTH_LARGE = 300
    ENTRY_WIDTH_NORMAL = 200
    ENTRY_WIDTH_SMALL = 140

    # Radios de borde
    RADIUS_LARGE = 15
    RADIUS_MEDIUM = 12
    RADIUS_NORMAL = 10
    RADIUS_SMALL = 8
    RADIUS_MINI = 6


# ============================================
# CONFIGURACIÓN DE MÓDULOS
# ============================================

class ModuloConfig:
    """Configuración visual por módulo"""

    PRODUCTOS = {
        'color': '#4ecdc4',
        'hover': '#45b7b8',
        'emoji': '📦',
        'nombre': 'PRODUCTOS',
        'descripcion': 'Gestión de Inventario',
        'gradiente_start': '#667eea',
        'gradiente_end': '#764ba2'
    }

    CLIENTES = {
        'color': '#ff6b6b',
        'hover': '#ee5a52',
        'emoji': '👥',
        'nombre': 'CLIENTES',
        'descripcion': 'Base de Datos CRM',
        'gradiente_start': '#667eea',
        'gradiente_end': '#5a67d8'
    }

    VENTAS = {
        'color': '#4834d4',
        'hover': '#3742fa',
        'emoji': '💰',
        'nombre': 'VENTAS',
        'descripcion': 'Punto de Venta',
        'gradiente_start': '#667eea',
        'gradiente_end': '#764ba2'
    }

    CUENTAS = {
        'color': '#ff9ff3',
        'hover': '#f368e0',
        'emoji': '💳',
        'nombre': 'CUENTAS',
        'descripcion': 'Cuentas Corrientes',
        'gradiente_start': '#667eea',
        'gradiente_end': '#764ba2'
    }

    REPORTES = {
        'color': '#feca57',
        'hover': '#ff9f43',
        'emoji': '📊',
        'nombre': 'REPORTES',
        'descripcion': 'Analytics & BI',
        'gradiente_start': '#667eea',
        'gradiente_end': '#764ba2'
    }


# ============================================
# EFECTOS Y ANIMACIONES
# ============================================

class Efectos:
    """Configuración de efectos visuales"""

    # Sombras (se pueden simular con bordes en tkinter)
    SHADOW_LIGHT = 1
    SHADOW_MEDIUM = 2
    SHADOW_HEAVY = 3

    # Opacidades (valores de 0 a 1)
    OPACITY_FULL = 1.0
    OPACITY_HIGH = 0.9
    OPACITY_MEDIUM = 0.7
    OPACITY_LOW = 0.5
    OPACITY_VERY_LOW = 0.3

    # Tiempos de transición (ms)
    TRANSITION_FAST = 150
    TRANSITION_NORMAL = 300
    TRANSITION_SLOW = 500


# ============================================
# HELPERS DE ESTILO
# ============================================

def obtener_color_hover(color_base):
    """Retorna el color hover para un color base"""
    mapa_colores = {
        Colores.SUCCESS: Colores.SUCCESS_HOVER,
        Colores.WARNING: Colores.WARNING_HOVER,
        Colores.DANGER: Colores.DANGER_HOVER,
        Colores.INFO: Colores.INFO_HOVER,
        "#00a8ff": "#0088cc",
        "#ffa502": "#e69500",
        "#ff3838": "#e62020",
        "#747d8c": "#5f6770",
        "#2ed573": "#26b85f",
        "#10ac84": "#0e9670",
        "#9b59b6": "#8e44ad",
        "#f39c12": "#e67e22"
    }
    return mapa_colores.get(color_base, color_base)


def crear_gradiente_tuple(start, end):
    """Retorna una tupla de gradiente para CustomTkinter"""
    return (start, end)


def estilo_boton_primario():
    """Retorna configuración de estilo para botón primario"""
    return {
        'fg_color': Colores.PRIMARY_START,
        'hover_color': Colores.PRIMARY_DARK,
        'font': (Fuentes.FAMILIA_PRINCIPAL, Fuentes.NORMAL, Fuentes.BOLD),
        'corner_radius': Dimensiones.RADIUS_NORMAL,
        'height': Dimensiones.BUTTON_HEIGHT_NORMAL,
        'border_width': 0
    }


def estilo_boton_secundario():
    """Retorna configuración de estilo para botón secundario"""
    return {
        'fg_color': Colores.GRIS_CLARO,
        'hover_color': Colores.GRIS_MEDIO,
        'font': (Fuentes.FAMILIA_PRINCIPAL, Fuentes.NORMAL, Fuentes.BOLD),
        'corner_radius': Dimensiones.RADIUS_NORMAL,
        'height': Dimensiones.BUTTON_HEIGHT_NORMAL,
        'border_width': 0
    }


def estilo_entry():
    """Retorna configuración de estilo para campos de entrada"""
    return {
        'font': (Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO),
        'corner_radius': Dimensiones.RADIUS_SMALL,
        'border_width': 1,
        'border_color': Colores.BORDER_MEDIUM,
        'fg_color': Colores.BG_HOVER,
        'text_color': Colores.TEXT_PRIMARY,
        'height': Dimensiones.ENTRY_HEIGHT
    }


def estilo_card():
    """Retorna configuración de estilo para tarjetas"""
    return {
        'fg_color': Colores.BG_CARD,
        'corner_radius': Dimensiones.RADIUS_MEDIUM,
        'border_width': 1,
        'border_color': Colores.BORDER_LIGHT
    }


def estilo_header():
    """Retorna configuración de estilo para headers"""
    return {
        'fg_color': crear_gradiente_tuple(Colores.PRIMARY_START, Colores.PRIMARY_END),
        'height': Dimensiones.HEADER_HEIGHT,
        'corner_radius': 0
    }


# ============================================
# ICONOS Y EMOJIS
# ============================================

class Iconos:
    """Iconos y emojis utilizados en el sistema"""

    # Acciones
    GUARDAR = "💾"
    EDITAR = "✏️"
    ELIMINAR = "🗑️"
    BUSCAR = "🔍"
    ACTUALIZAR = "🔄"
    EXPORTAR = "📤"
    IMPRIMIR = "🖨️"
    CERRAR = "✖"
    CONFIGURACION = "⚙️"
    AYUDA = "💡"

    # Módulos
    PRODUCTOS = "📦"
    CLIENTES = "👥"
    VENTAS = "💰"
    CUENTAS = "💳"
    REPORTES = "📊"
    DASHBOARD = "🏠"

    # Estados
    EXITO = "✅"
    ADVERTENCIA = "⚠️"
    ERROR = "❌"
    INFO = "ℹ️"
    ACTIVO = "🚀"

    # Otros
    FECHA = "📅"
    HORA = "🕐"
    TELEFONO = "📱"
    EMAIL = "📧"
    UBICACION = "📍"
    DINERO = "💵"
    STOCK = "📊"
    EMPRESA = "🏢"
    GRAFICO = "📈"
    DOCUMENTO = "📄"
    LIMPIAR = "🧹"
    ETIQUETA = "🏷️"
