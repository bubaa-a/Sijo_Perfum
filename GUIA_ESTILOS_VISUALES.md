# 🎨 Guía de Estilos Visuales - Sistema de Gestión Empresarial Pro

## 📋 Tabla de Contenidos
1. [Paleta de Colores](#paleta-de-colores)
2. [Tipografía](#tipografía)
3. [Espaciado y Dimensiones](#espaciado-y-dimensiones)
4. [Componentes](#componentes)
5. [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🎨 Paleta de Colores

### Colores Primarios
Los colores primarios definen la identidad visual del sistema.

```python
PRIMARY_START = "#667eea"    # Morado claro (inicio de gradientes)
PRIMARY_END = "#764ba2"      # Morado oscuro (fin de gradientes)
PRIMARY_DARK = "#5a67d8"     # Morado oscuro (hover states)
PRIMARY_LIGHT = "#7c8cf5"    # Morado muy claro
```

**Uso:** Headers, botones principales, elementos destacados

### Colores Secundarios
```python
SECONDARY = "#4834d4"        # Azul morado
SECONDARY_DARK = "#3742fa"   # Azul morado oscuro
SECONDARY_LIGHT = "#6c5ce7"  # Azul morado claro
```

**Uso:** Encabezados de tablas, elementos de énfasis secundario

### Colores de Acción
```python
SUCCESS = "#2ed573"          # Verde (acciones exitosas)
WARNING = "#ffa502"          # Naranja (advertencias)
DANGER = "#ff3838"           # Rojo (acciones destructivas)
INFO = "#00a8ff"             # Azul cielo (información)
```

**Uso:** Botones de acción, mensajes de estado, alertas

### Colores de Estado
```python
DISPONIBLE = "#27ae60"       # Verde (productos disponibles)
STOCK_BAJO = "#f39c12"       # Naranja (stock bajo)
AGOTADO = "#e74c3c"          # Rojo (productos agotados)
ACTIVO = "#10ac84"           # Verde azulado (estado activo)
INACTIVO = "#95a5a6"         # Gris (estado inactivo)
```

**Uso:** Indicadores de estado en tablas y tarjetas

### Colores Neutros
```python
GRIS_OSCURO = "#2c3e50"      # Texto principal
GRIS_MEDIO = "#7f8c8d"       # Texto secundario
GRIS_CLARO = "#95a5a6"       # Bordes y separadores
GRIS_MUY_CLARO = "#ecf0f1"   # Fondos sutiles
```

### Fondos
```python
BG_PRIMARY = "#f0f2f5"       # Fondo principal de la aplicación
BG_SECONDARY = "#ffffff"     # Fondo de tarjetas y cards
BG_CARD = "#ffffff"          # Fondo de componentes
BG_HOVER = "#f8f9fa"         # Fondo en estado hover
```

### Bordes
```python
BORDER_LIGHT = "#e9ecef"     # Bordes sutiles
BORDER_MEDIUM = "#dee2e6"    # Bordes normales
BORDER_DARK = "#adb5bd"      # Bordes prominentes
```

---

## 📝 Tipografía

### Familia de Fuentes
```python
FAMILIA_PRINCIPAL = "Segoe UI"    # Fuente principal (Windows)
FAMILIA_ALTERNATIVA = "Arial"     # Fuente de respaldo
FAMILIA_MONOSPACE = "Consolas"    # Para datos numéricos
```

### Tamaños de Fuente
```python
XXL = 32px           # Títulos principales
XL = 24px            # Títulos de sección
LARGE = 20px         # Subtítulos grandes
GRANDE = 18px        # Títulos de tarjetas
MEDIANO_GRANDE = 16px
MEDIANO = 14px       # Texto de headers de cards
NORMAL = 12px        # Texto normal
PEQUENO = 11px       # Texto de botones
MUY_PEQUENO = 10px   # Labels de formularios
MINI = 9px           # Texto muy pequeño
```

### Pesos
```python
BOLD = "bold"         # Títulos y énfasis
NORMAL = "normal"     # Texto regular
ITALIC = "italic"     # Texto en cursiva
```

---

## 📐 Espaciado y Dimensiones

### Espaciados Estándar
```python
XXL = 40px           # Espaciado extra grande
XL = 30px            # Espaciado grande
LARGE = 25px         # Espaciado medio-grande
MEDIO = 20px         # Espaciado medio
NORMAL = 15px        # Espaciado normal
PEQUENO = 10px       # Espaciado pequeño
MUY_PEQUENO = 5px    # Espaciado muy pequeño
MINI = 3px           # Espaciado mínimo
```

### Dimensiones de Componentes

#### Alturas
```python
HEADER_HEIGHT = 100px        # Altura del header principal
FOOTER_HEIGHT = 80px         # Altura del footer
BUTTON_HEIGHT_LARGE = 45px   # Botones grandes
BUTTON_HEIGHT_NORMAL = 38px  # Botones normales
BUTTON_HEIGHT_SMALL = 32px   # Botones pequeños
ENTRY_HEIGHT = 36px          # Campos de entrada normales
ENTRY_HEIGHT_SMALL = 32px    # Campos de entrada pequeños
```

#### Anchos
```python
SIDEBAR_WIDTH = 280px
BUTTON_WIDTH_LARGE = 200px
BUTTON_WIDTH_NORMAL = 140px
BUTTON_WIDTH_SMALL = 100px
ENTRY_WIDTH_LARGE = 300px
ENTRY_WIDTH_NORMAL = 200px
ENTRY_WIDTH_SMALL = 140px
```

#### Radios de Borde
```python
RADIUS_LARGE = 15px          # Tarjetas principales
RADIUS_MEDIUM = 12px         # Cards secundarios
RADIUS_NORMAL = 10px         # Botones y modales
RADIUS_SMALL = 8px           # Campos de entrada
RADIUS_MINI = 6px            # Elementos pequeños
```

---

## 🧩 Componentes

### Botones

#### Botón Primario
```python
from config.estilos import estilo_boton_primario

btn = ctk.CTkButton(
    parent,
    text="Guardar",
    **estilo_boton_primario()
)
```

#### Botón de Acción con Color Personalizado
```python
from config.estilos import Colores, obtener_color_hover

btn = ctk.CTkButton(
    parent,
    text="🗑️ Eliminar",
    fg_color=Colores.DANGER,
    hover_color=obtener_color_hover(Colores.DANGER),
    corner_radius=Dimensiones.RADIUS_NORMAL
)
```

### Cards (Tarjetas)
```python
from config.estilos import estilo_card

card = ctk.CTkFrame(
    parent,
    **estilo_card()
)
```

### Campos de Entrada
```python
from config.estilos import estilo_entry

entry = ctk.CTkEntry(
    parent,
    **estilo_entry()
)
```

### Headers
```python
from config.estilos import estilo_header, Colores

header = ctk.CTkFrame(
    parent,
    **estilo_header()
)
```

---

## 💡 Ejemplos de Uso

### Crear una Ventana Completa
```python
from config.estilos import (Colores, Fuentes, Espaciado,
                            Dimensiones, Iconos)

class MiVentana:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.configure(bg=Colores.BG_PRIMARY)

        # Header
        header = ctk.CTkFrame(
            self.ventana,
            fg_color=(Colores.PRIMARY_START, Colores.PRIMARY_END),
            height=Dimensiones.HEADER_HEIGHT
        )
        header.pack(fill='x')

        # Título
        titulo = ctk.CTkLabel(
            header,
            text=f"{Iconos.PRODUCTOS} Mi Módulo",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.XL, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        )
        titulo.pack(padx=Espaciado.XL, pady=Espaciado.MEDIO)
```

### Crear Tarjetas de Información
```python
# Card con información
info_card = ctk.CTkFrame(
    parent,
    fg_color=Colores.BG_CARD,
    corner_radius=Dimensiones.RADIUS_MEDIUM,
    border_width=1,
    border_color=Colores.BORDER_LIGHT
)
info_card.pack(padx=Espaciado.MEDIO, pady=Espaciado.NORMAL)

# Header del card
card_header = ctk.CTkFrame(
    info_card,
    fg_color=Colores.PRIMARY_START,
    corner_radius=Dimensiones.RADIUS_NORMAL
)
card_header.pack(fill='x', padx=2, pady=2)

# Título del card
titulo_card = ctk.CTkLabel(
    card_header,
    text=f"{Iconos.INFO} Información",
    font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MEDIANO, Fuentes.BOLD),
    text_color=Colores.TEXT_WHITE
)
titulo_card.pack(pady=Espaciado.PEQUENO)
```

### Crear Formulario con Campos
```python
def crear_campo(parent, label, var):
    # Label
    lbl = ctk.CTkLabel(
        parent,
        text=label,
        font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MUY_PEQUENO, Fuentes.BOLD),
        text_color=Colores.PRIMARY_START
    )
    lbl.pack(anchor='w', pady=(Espaciado.PEQUENO, Espaciado.MINI))

    # Entry
    entry = ctk.CTkEntry(
        parent,
        textvariable=var,
        font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO),
        height=Dimensiones.ENTRY_HEIGHT,
        corner_radius=Dimensiones.RADIUS_SMALL,
        border_color=Colores.BORDER_MEDIUM,
        fg_color=Colores.BG_HOVER
    )
    entry.pack(fill='x', pady=(0, Espaciado.MUY_PEQUENO))
```

### Crear Botones de Acción
```python
def crear_botones_accion(parent):
    botones = [
        ("💾 Guardar", Colores.SUCCESS, comando_guardar),
        ("✏️ Editar", Colores.WARNING, comando_editar),
        ("🗑️ Eliminar", Colores.DANGER, comando_eliminar),
    ]

    for texto, color, comando in botones:
        btn = ctk.CTkButton(
            parent,
            text=texto,
            fg_color=color,
            hover_color=obtener_color_hover(color),
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
            height=Dimensiones.BUTTON_HEIGHT_NORMAL,
            corner_radius=Dimensiones.RADIUS_NORMAL,
            command=comando
        )
        btn.pack(fill='x', pady=Espaciado.MUY_PEQUENO)
```

---

## 🎯 Mejores Prácticas

### 1. Consistencia
- **Siempre** usa las constantes del módulo `config.estilos`
- **NO** uses valores hardcodeados de colores o tamaños
- Mantén la misma estructura en ventanas similares

### 2. Jerarquía Visual
- Usa tamaños de fuente más grandes para títulos principales
- Aplica colores primarios a elementos importantes
- Usa colores neutros para elementos secundarios

### 3. Espaciado
- Mantén espaciado consistente entre elementos similares
- Usa más espaciado alrededor de secciones importantes
- Agrupa elementos relacionados con menos espaciado

### 4. Color
- Usa colores de acción (SUCCESS, WARNING, DANGER) de forma consistente
- Los gradientes solo en headers y footers
- Fondos claros para mejor legibilidad

### 5. Accesibilidad
- Contraste adecuado entre texto y fondo
- Tamaños de fuente legibles (mínimo 10px)
- Iconos que complementen el texto, no lo reemplacen

---

## 📦 Módulos Configurados

Cada módulo del sistema tiene su propia configuración visual:

### PRODUCTOS
```python
color: '#4ecdc4' (Turquesa)
emoji: '📦'
gradiente: '#667eea' → '#764ba2'
```

### CLIENTES
```python
color: '#ff6b6b' (Rojo coral)
emoji: '👥'
gradiente: '#667eea' → '#5a67d8'
```

### VENTAS
```python
color: '#4834d4' (Morado azulado)
emoji: '💰'
gradiente: '#667eea' → '#764ba2'
```

### CUENTAS
```python
color: '#ff9ff3' (Rosa)
emoji: '💳'
gradiente: '#667eea' → '#764ba2'
```

### REPORTES
```python
color: '#feca57' (Amarillo)
emoji: '📊'
gradiente: '#667eea' → '#764ba2'
```

---

## 🔄 Actualizar una Ventana Existente

Para actualizar una ventana con los nuevos estilos:

1. **Importar el módulo de estilos**
```python
from config.estilos import (Colores, Fuentes, Espaciado,
                            Dimensiones, Iconos, obtener_color_hover,
                            estilo_entry, estilo_card, estilo_header)
```

2. **Reemplazar colores hardcodeados**
```python
# Antes
fg_color="#667eea"

# Después
fg_color=Colores.PRIMARY_START
```

3. **Usar funciones helper**
```python
# Antes
card = ctk.CTkFrame(parent, fg_color='white', corner_radius=12,
                    border_width=1, border_color='#e9ecef')

# Después
card = ctk.CTkFrame(parent, **estilo_card())
```

4. **Aplicar iconos consistentes**
```python
# Antes
text="📦 Productos"

# Después
text=f"{Iconos.PRODUCTOS} Productos"
```

---

## ✅ Checklist de Diseño

Antes de finalizar una ventana, verifica:

- [ ] Todos los colores provienen de `Colores.*`
- [ ] Todas las fuentes usan `Fuentes.*`
- [ ] Todos los espaciados usan `Espaciado.*`
- [ ] Todos los tamaños usan `Dimensiones.*`
- [ ] Los iconos usan `Iconos.*`
- [ ] Los botones tienen colores hover apropiados
- [ ] Las tarjetas usan `estilo_card()`
- [ ] Los campos de entrada usan `estilo_entry()`
- [ ] El header usa `estilo_header()`
- [ ] La ventana tiene un fondo consistente (`Colores.BG_PRIMARY`)

---

**Versión:** 1.0
**Fecha:** Octubre 2025
**Sistema:** Gestión Empresarial Pro v3.0
