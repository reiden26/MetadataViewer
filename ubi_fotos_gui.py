# Interfaz gráfica moderna y minimalista para visualizar metadatos EXIF
# pip install Pillow geopy

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ExifTags
from geopy.geocoders import Nominatim
import webbrowser
import os
import threading
import hashlib

class ModernMetadataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Metadata")
        self.root.geometry("1100x750")
        self.root.minsize(950, 650)
        self.root.configure(bg="#f5f5f7")

        # Variables
        self.current_image_path = None
        self.coords = None
        self.current_photo = None

        # Colores modernos
        self.colors = {
            'bg': "#f5f5f7",
            'card': "#ffffff",
            'primary': "#007aff",
            'text': "#1c1c1e",
            'text_secondary': "#8e8e93",
            'border': "#e5e5ea",
            'success': "#34c759",
            'warning': "#ff9500"
        }

        self._configure_styles()
        self._build_ui()

    def _configure_styles(self):
        """Configura estilos modernos para ttk."""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Frame estilo tarjeta
        self.style.configure(
            "Card.TFrame",
            background=self.colors['card']
        )

        # Labels
        self.style.configure(
            "Title.TLabel",
            font=("Inter", 24, "bold"),
            foreground=self.colors['text'],
            background=self.colors['bg']
        )

        self.style.configure(
            "Subtitle.TLabel",
            font=("Inter", 12),
            foreground=self.colors['text_secondary'],
            background=self.colors['bg']
        )

        self.style.configure(
            "CardTitle.TLabel",
            font=("Inter", 14, "bold"),
            foreground=self.colors['text'],
            background=self.colors['card']
        )

        self.style.configure(
            "Label.TLabel",
            font=("Inter", 10),
            foreground=self.colors['text_secondary'],
            background=self.colors['card']
        )

        self.style.configure(
            "Value.TLabel",
            font=("Inter", 11),
            foreground=self.colors['text'],
            background=self.colors['card']
        )

        # Botón primario
        self.style.configure(
            "Primary.TButton",
            font=("Inter", 11, "bold"),
            foreground="white",
            background=self.colors['primary'],
            padding=(20, 12)
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", "#0051d5"), ("disabled", "#c7c7cc")]
        )

        # Botón secundario
        self.style.configure(
            "Secondary.TButton",
            font=("Inter", 11),
            foreground=self.colors['primary'],
            background=self.colors['card'],
            padding=(15, 10)
        )

    def _build_ui(self):
        """Construye la interfaz moderna."""
        # Frame principal con padding
        self.main_container = tk.Frame(self.root, bg=self.colors['bg'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)

        # Header
        self._create_header()

        # Área de contenido (inicialmente vacía)
        self.content_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # Estado inicial - mensaje de bienvenida
        self._show_welcome_state()

    def _create_header(self):
        """Crea el header con título y botón de selección."""
        header = tk.Frame(self.main_container, bg=self.colors['bg'])
        header.pack(fill=tk.X)

        # Título y subtítulo (izquierda)
        title_frame = tk.Frame(header, bg=self.colors['bg'])
        title_frame.pack(side=tk.LEFT)

        title = tk.Label(
            title_frame,
            text="Metadata",
            font=("Inter", 32, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title.pack(anchor=tk.W)

        subtitle = tk.Label(
            title_frame,
            text="Visualiza metadatos EXIF y ubicación de tus fotografías",
            font=("Inter", 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        subtitle.pack(anchor=tk.W, pady=(5, 0))

        # Botón de selección (derecha) con borde redondeado usando Canvas
        btn_frame = tk.Frame(header, bg=self.colors['bg'])
        btn_frame.pack(side=tk.RIGHT)

        # Crear botón redondeado con Canvas
        self._create_rounded_button(btn_frame, "+  Seleccionar imagen", self._select_image)

    def _create_rounded_button(self, parent, text, command):
        """Crea un botón con bordes redondeados usando Canvas."""
        # Dimensiones
        width = 180
        height = 44
        radius = 22  # Radio para bordes redondeados

        # Canvas para dibujar el botón
        canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg=self.colors['bg'],
            highlightthickness=0,
            bd=0,
            cursor="hand2"
        )
        canvas.pack()

        # Función para dibujar rectángulo redondeado
        def draw_rounded_rect(x, y, w, h, r, color):
            """Dibuja un rectángulo con esquinas redondeadas."""
            points = [
                x+r, y,           # Top edge start
                x+w-r, y,         # Top edge end
                x+w, y,           # Top right corner start
                x+w, y+r,         # Top right corner end
                x+w, y+h-r,       # Right edge
                x+w, y+h,         # Bottom right corner
                x+w-r, y+h,       # Bottom edge end
                x+r, y+h,         # Bottom edge start
                x, y+h,           # Bottom left corner
                x, y+h-r,         # Left edge
                x, y+r,           # Top left corner
                x, y              # Close
            ]
            return canvas.create_polygon(
                points,
                fill=color,
                outline=color,
                smooth=True
            )

        # Dibujar el botón (fondo)
        btn_bg = draw_rounded_rect(0, 0, width, height, radius, self.colors['primary'])

        # Añadir texto
        text_id = canvas.create_text(
            width/2, height/2,
            text=text,
            font=("Inter", 12, "bold"),
            fill="white",
            anchor="center"
        )

        # Efectos hover y click
        def on_enter(e):
            canvas.itemconfig(btn_bg, fill="#0051d5", outline="#0051d5")

        def on_leave(e):
            canvas.itemconfig(btn_bg, fill=self.colors['primary'], outline=self.colors['primary'])

        def on_click(e):
            canvas.itemconfig(btn_bg, fill="#004494", outline="#004494")
            command()

        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)

    def _show_welcome_state(self):
        """Muestra el estado inicial sin imagen seleccionada."""
        self.welcome_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.welcome_frame.pack(expand=True)

        # Icono grande (emoji)
        icon = tk.Label(
            self.welcome_frame,
            text="🖼️",
            font=("Segoe UI", 72),
            bg=self.colors['bg']
        )
        icon.pack()

        text = tk.Label(
            self.welcome_frame,
            text="Selecciona una imagen para comenzar",
            font=("Inter", 14),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        text.pack(pady=(20, 0))

        hint = tk.Label(
            self.welcome_frame,
            text="Soporta JPG, PNG, TIFF y otros formatos",
            font=("Inter", 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        hint.pack(pady=(10, 0))

    def _select_image(self):
        """Abre diálogo para seleccionar imagen."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.tiff *.tif"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("Todos los archivos", "*.*")
            ]
        )

        if file_path:
            self.current_image_path = file_path
            self._process_image(file_path)

    def _process_image(self, image_path):
        """Procesa la imagen en un hilo separado."""
        # Ocultar estado de bienvenida
        if hasattr(self, 'welcome_frame'):
            self.welcome_frame.pack_forget()

        # Mostrar spinner
        self._show_loading_state()

        # Ejecutar en hilo separado
        thread = threading.Thread(target=self._extract_metadata, args=(image_path,))
        thread.daemon = True
        thread.start()

    def _show_loading_state(self):
        """Muestra el estado de carga."""
        # Limpiar content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        loading_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        loading_frame.pack(expand=True)

        # Spinner animado (usando un canvas)
        self.spinner_canvas = tk.Canvas(
            loading_frame,
            width=60,
            height=60,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        self.spinner_canvas.pack()

        self.spinner_angle = 0
        self._animate_spinner()

        text = tk.Label(
            loading_frame,
            text="Analizando imagen...",
            font=("Inter", 13),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        text.pack(pady=(20, 0))

    def _animate_spinner(self):
        """Anima el spinner."""
        if not hasattr(self, 'spinner_canvas') or not self.spinner_canvas.winfo_exists():
            return

        self.spinner_canvas.delete("all")

        # Dibujar círculos animados
        import math
        cx, cy = 30, 30
        radius = 20

        for i in range(8):
            angle = (self.spinner_angle + i * 45) * math.pi / 180
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)

            # Opacidad decreciente
            alpha = 1.0 - (i * 0.12)
            size = 4 + (1 - alpha) * 2

            color = f"#{int(0 * alpha + 245 * (1-alpha)):02x}{int(122 * alpha + 245 * (1-alpha)):02x}{int(255 * alpha + 247 * (1-alpha)):02x}"
            self.spinner_canvas.create_oval(
                x-size, y-size, x+size, y+size,
                fill=self.colors['primary'] if i == 0 else "#d1d1d6",
                outline=""
            )

        self.spinner_angle += 30
        self.root.after(50, self._animate_spinner)

    def _extract_metadata(self, image_path):
        """Extrae metadatos de la imagen."""
        try:
            img = Image.open(image_path)

            # Guardar referencia
            self.current_image = img.copy()

            # Extraer datos con Pillow
            exif_data = self._get_exif_data(image_path)
            basic_info = self._get_basic_info(image_path, img)

            # Intentar con biblioteca 'exif' si está disponible (más potente)
            exif_alt_data = self._get_exif_with_exif_library(image_path)
            if exif_alt_data:
                print(f"DEBUG - Datos EXIF alternativos encontrados")
                # Fusionar datos
                if exif_data:
                    exif_data.update(exif_alt_data)
                else:
                    exif_data = exif_alt_data

            # Debug: imprimir keys de EXIF
            if exif_data:
                print(f"DEBUG - Tags EXIF encontrados: {list(exif_data.keys())}")
                if 'GPSInfo' in exif_data:
                    print(f"DEBUG - GPSInfo raw: {exif_data['GPSInfo']}")

            # Procesar GPS si existe
            self.coords = None
            address = None
            gps_error = None
            has_empty_gps = False

            if exif_data:
                gps_info_raw = exif_data.get('GPSInfo')

                # Verificar si GPSInfo existe pero está vacío
                if gps_info_raw is not None:
                    if isinstance(gps_info_raw, dict) and len(gps_info_raw) == 0:
                        has_empty_gps = True
                        print("DEBUG - GPSInfo existe pero está VACÍO")
                    else:
                        gps_info = self._get_gps_info(exif_data)
                        if gps_info and len(gps_info) > 0:
                            print(f"DEBUG - GPSInfo procesado: {gps_info}")
                            try:
                                lat, lon = self._get_coordinates(gps_info)
                                self.coords = (lat, lon)
                                print(f"DEBUG - Coordenadas: {lat}, {lon}")
                                address = self._get_address(lat, lon)
                            except Exception as gps_e:
                                gps_error = str(gps_e)
                                print(f"DEBUG - Error procesando GPS: {gps_error}")
                        else:
                            has_empty_gps = True

                # Intentar extraer GPS de la biblioteca 'exif' (nombres diferentes)
                if not self.coords and 'gps_latitude' in exif_data and 'gps_longitude' in exif_data:
                    print("DEBUG - Intentando extraer GPS de biblioteca exif")
                    try:
                        lat = self._convert_dms_tuple(exif_data['gps_latitude'])
                        lon = self._convert_dms_tuple(exif_data['gps_longitude'])

                        # Aplicar referencias
                        lat_ref = exif_data.get('gps_latitude_ref', 'N')
                        lon_ref = exif_data.get('gps_longitude_ref', 'E')

                        if lat_ref == 'S':
                            lat = -lat
                        if lon_ref == 'W':
                            lon = -lon

                        self.coords = (lat, lon)
                        print(f"DEBUG - Coordenadas extraídas de exif lib: {lat}, {lon}")
                        address = self._get_address(lat, lon)
                    except Exception as e:
                        print(f"DEBUG - Error con exif lib GPS: {e}")

            # Actualizar UI
            self.root.after(0, self._show_results, img, basic_info, exif_data, address, gps_error, has_empty_gps)

        except Exception as e:
            self.root.after(0, self._show_error, str(e))

    def _show_results(self, img, basic_info, exif_data, address, gps_error=None, has_empty_gps=False):
        """Muestra los resultados en la interfaz moderna."""
        # Detener spinner
        if hasattr(self, 'spinner_canvas'):
            del self.spinner_canvas

        # Limpiar frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Frame de dos columnas
        results_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Columna izquierda - Imagen
        left_col = tk.Frame(results_frame, bg=self.colors['bg'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        self._create_image_card(left_col, img)

        # Columna derecha - Metadatos
        right_col = tk.Frame(results_frame, bg=self.colors['bg'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))

        self._create_metadata_cards(right_col, basic_info, exif_data, address, gps_error, has_empty_gps)

    def _create_image_card(self, parent, img):
        """Crea la tarjeta de la imagen con sombra."""
        # Frame contenedor para sombra
        shadow_frame = tk.Frame(
            parent,
            bg="#d1d1d6"
        )
        shadow_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 2), pady=(0, 2))

        card = tk.Frame(
            shadow_frame,
            bg=self.colors['card'],
            highlightbackground=self.colors['border'],
            highlightthickness=0,
            bd=0
        )
        card.pack(fill=tk.BOTH, expand=True, padx=(0, 2), pady=(0, 2))

        # Título de la tarjeta
        title = tk.Label(
            card,
            text="Vista previa",
            font=("Inter", 13, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        title.pack(anchor=tk.W, padx=20, pady=(20, 15))

        # Canvas para la imagen
        canvas_frame = tk.Frame(card, bg=self.colors['card'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.image_canvas = tk.Canvas(
            canvas_frame,
            bg="#f2f2f7",
            highlightthickness=0
        )
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

        # Mostrar imagen centrada y ajustada
        self._display_image(img)

        # Bind resize
        self.image_canvas.bind("<Configure>", lambda e: self._display_image(self.current_image))

    def _display_image(self, img):
        """Muestra la imagen ajustada al canvas."""
        if img is None:
            return

        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()

        if canvas_width < 10 or canvas_height < 10:
            canvas_width, canvas_height = 400, 400

        # Calcular escala manteniendo proporción
        img_ratio = img.width / img.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)

        # Redimensionar
        resized = img.resize((new_width, new_height), Image.LANCZOS)
        self.current_photo = ImageTk.PhotoImage(resized)

        # Limpiar y mostrar
        self.image_canvas.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.image_canvas.create_image(x, y, anchor=tk.NW, image=self.current_photo)

    def _create_metadata_cards(self, parent, basic_info, exif_data, address, gps_error=None, has_empty_gps=False):
        """Crea las tarjetas de metadatos."""
        # Configurar estilo del scrollbar para que sea moderno y minimalista
        self.style.configure(
            "Custom.Vertical.TScrollbar",
            background=self.colors['bg'],
            troughcolor=self.colors['bg'],
            borderwidth=0,
            relief=tk.FLAT,
            width=8
        )
        self.style.map(
            "Custom.Vertical.TScrollbar",
            background=[
                ("active", "#c7c7cc"),
                ("pressed", "#8e8e93"),
                ("!active", "#e5e5ea")
            ]
        )

        # Scrollable frame
        canvas = tk.Canvas(parent, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview, style="Custom.Vertical.TScrollbar")

        self.metadata_container = tk.Frame(canvas, bg=self.colors['bg'])
        self.metadata_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.metadata_container, anchor=tk.NW, width=450)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tarjeta 1: Información del archivo
        self._create_info_card(
            "Información del archivo",
            [
                ("Nombre", basic_info.get('file_name', 'N/A')),
                ("Tamaño", self._format_file_size(basic_info.get('file_size', 0))),
                ("Formato", basic_info.get('format', 'N/A')),
                ("Dimensiones", basic_info.get('image_size', 'N/A')),
                ("Megapíxeles", f"{basic_info.get('megapixels', 'N/A')} MP"),
            ]
        )

        # Tarjeta 2: EXIF (si existe)
        if exif_data:
            exif_items = []

            if 'DateTimeOriginal' in exif_data:
                exif_items.append(("Fecha de captura", str(exif_data['DateTimeOriginal'])))
            if 'Make' in exif_data:
                exif_items.append(("Marca", str(exif_data['Make'])))
            if 'Model' in exif_data:
                exif_items.append(("Modelo", str(exif_data['Model'])))
            if 'LensModel' in exif_data:
                exif_items.append(("Lente", str(exif_data['LensModel'])))
            if 'ExposureTime' in exif_data:
                exif_items.append(("Exposición", str(exif_data['ExposureTime'])))
            if 'FNumber' in exif_data:
                exif_items.append(("Apertura", f"f/{exif_data['FNumber']}"))
            if 'ISOSpeedRatings' in exif_data:
                exif_items.append(("ISO", str(exif_data['ISOSpeedRatings'])))
            if 'FocalLength' in exif_data:
                exif_items.append(("Distancia focal", f"{exif_data['FocalLength']}mm"))

            if exif_items:
                self._create_info_card("Datos de la cámara", exif_items)

        # Tarjeta 3: Ubicación (si existe)
        if self.coords:
            lat, lon = self.coords
            location_items = [
                ("Latitud", f"{lat:.6f}"),
                ("Longitud", f"{lon:.6f}"),
            ]
            if address:
                location_items.append(("Dirección", address))

            self._create_location_card(location_items)
        elif has_empty_gps:
            # GPS existe pero está vacío
            self._create_simple_card(
                "Ubicación",
                "GPS estaba activado pero no se capturaron coordenadas.\n\nEsto ocurre cuando:\n• No había señal de satélites al tomar la foto\n• El GPS aún no había fijado la posición\n• La configuración de la cámara no guarda GPS\n\nPara futuras fotos:\n1. Asegúrate de que el GPS del celular esté activo\n2. Espera unos segundos tras abrir la cámara\n3. Verifica que la app de cámara tenga permiso de ubicación",
                icon="📡"
            )
        elif gps_error:
            # Error al procesar GPS
            self._create_simple_card(
                "Ubicación",
                f"Datos GPS encontrados pero error al procesar:\n{gps_error}\n\nEsto puede deberse a un formato de coordenadas no estándar.",
                icon="⚠️"
            )
        else:
            # Mensaje de no ubicación
            self._create_simple_card(
                "Ubicación",
                "Esta imagen no contiene datos GPS.\n\n¿El GPS estaba activado al tomar la foto?",
                icon="📍"
            )

    def _create_info_card(self, title, items):
        """Crea una tarjeta de información con sombra y bordes suaves."""
        # Frame contenedor para sombra
        shadow_frame = tk.Frame(
            self.metadata_container,
            bg="#d1d1d6"  # Color de sombra suave
        )
        shadow_frame.pack(fill=tk.X, pady=(0, 18), padx=(2, 4))

        # Tarjeta principal (encima de la sombra, ligeramente desplazada)
        card = tk.Frame(
            shadow_frame,
            bg=self.colors['card'],
            highlightbackground=self.colors['border'],
            highlightthickness=0,
            bd=0
        )
        card.pack(fill=tk.BOTH, expand=True, padx=(0, 2), pady=(0, 2))

        # Título
        title_lbl = tk.Label(
            card,
            text=title,
            font=("Inter", 13, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        title_lbl.pack(anchor=tk.W, padx=20, pady=(20, 15))

        # Items
        for label, value in items:
            row = tk.Frame(card, bg=self.colors['card'])
            row.pack(fill=tk.X, padx=20, pady=5)

            lbl = tk.Label(
                row,
                text=label,
                font=("Inter", 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['card'],
                width=15,
                anchor=tk.W
            )
            lbl.pack(side=tk.LEFT)

            val = tk.Label(
                row,
                text=str(value),
                font=("Inter", 11),
                fg=self.colors['text'],
                bg=self.colors['card'],
                wraplength=280,
                justify=tk.LEFT
            )
            val.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        # Padding bottom
        tk.Frame(card, height=10, bg=self.colors['card']).pack()

    def _create_location_card(self, items):
        """Crea la tarjeta de ubicación con sombra y botón de maps."""
        # Frame contenedor para sombra
        shadow_frame = tk.Frame(
            self.metadata_container,
            bg="#d1d1d6"
        )
        shadow_frame.pack(fill=tk.X, pady=(0, 18), padx=(2, 4))

        card = tk.Frame(
            shadow_frame,
            bg=self.colors['card'],
            highlightbackground=self.colors['border'],
            highlightthickness=0,
            bd=0
        )
        card.pack(fill=tk.BOTH, expand=True, padx=(0, 2), pady=(0, 2))

        # Header con icono
        header = tk.Frame(card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        icon = tk.Label(
            header,
            text="🌍",
            font=("Segoe UI", 20),
            bg=self.colors['card']
        )
        icon.pack(side=tk.LEFT)

        title_lbl = tk.Label(
            header,
            text="Ubicación detectada",
            font=("Inter", 13, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        title_lbl.pack(side=tk.LEFT, padx=(10, 0))

        # Items
        for label, value in items:
            row = tk.Frame(card, bg=self.colors['card'])
            row.pack(fill=tk.X, padx=20, pady=5)

            lbl = tk.Label(
                row,
                text=label,
                font=("Inter", 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['card'],
                width=12,
                anchor=tk.W
            )
            lbl.pack(side=tk.LEFT)

            val = tk.Label(
                row,
                text=str(value),
                font=("Inter", 11),
                fg=self.colors['text'],
                bg=self.colors['card'],
                wraplength=290,
                justify=tk.LEFT
            )
            val.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        # Botón de Google Maps
        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(15, 20))

        maps_btn = tk.Button(
            btn_frame,
            text="Abrir en Google Maps →",
            font=("Inter", 10, "bold"),
            bg=self.colors['success'],
            fg="white",
            activebackground="#248a3d",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self._open_maps
        )
        maps_btn.pack(anchor=tk.W)

    def _create_simple_card(self, title, message, icon="ℹ️"):
        """Crea una tarjeta simple con mensaje y sombra."""
        # Frame contenedor para sombra
        shadow_frame = tk.Frame(
            self.metadata_container,
            bg="#d1d1d6"
        )
        shadow_frame.pack(fill=tk.X, pady=(0, 18), padx=(2, 4))

        card = tk.Frame(
            shadow_frame,
            bg=self.colors['card'],
            highlightbackground=self.colors['border'],
            highlightthickness=0,
            bd=0
        )
        card.pack(fill=tk.BOTH, expand=True, padx=(0, 2), pady=(0, 2))

        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(padx=20, pady=20)

        icon_lbl = tk.Label(
            content,
            text=icon,
            font=("Segoe UI", 32),
            bg=self.colors['card']
        )
        icon_lbl.pack()

        title_lbl = tk.Label(
            content,
            text=title,
            font=("Inter", 13, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        title_lbl.pack(pady=(10, 5))

        msg_lbl = tk.Label(
            content,
            text=message,
            font=("Inter", 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['card'],
            wraplength=300,
            justify=tk.CENTER
        )
        msg_lbl.pack()

    def _show_error(self, error_msg):
        """Muestra error en la interfaz."""
        if hasattr(self, 'spinner_canvas'):
            del self.spinner_canvas

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        error_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        error_frame.pack(expand=True)

        icon = tk.Label(
            error_frame,
            text="⚠️",
            font=("Segoe UI", 48),
            bg=self.colors['bg']
        )
        icon.pack()

        title = tk.Label(
            error_frame,
            text="Error al procesar",
            font=("Inter", 16, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title.pack(pady=(20, 10))

        msg = tk.Label(
            error_frame,
            text=error_msg,
            font=("Inter", 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg'],
            wraplength=400
        )
        msg.pack()

    # Métodos auxiliares
    def _get_exif_data(self, image_path):
        """Extrae datos EXIF de forma robusta."""
        img = Image.open(image_path)
        exif_data = {}

        # Método 1: _getexif() (tradicional)
        raw_exif = img._getexif()
        if raw_exif:
            for tag_id, value in raw_exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                exif_data[tag] = value

        # Método 2: getexif() (nuevo en Pillow)
        if not exif_data:
            try:
                exif = img.getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag = ExifTags.TAGS.get(tag_id, tag_id)
                        exif_data[tag] = value
            except:
                pass

        # Método 3: Extraer GPS directamente si existe el tag
        try:
            if hasattr(img, 'info') and 'exif' in img.info:
                exif_dict = {}
                if raw_exif:
                    for tag_id, value in raw_exif.items():
                        tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                        exif_dict[tag_name] = value

                # Verificar si hay datos GPS crudos
                if 'GPSInfo' in exif_dict:
                    gps_data = exif_dict['GPSInfo']
                    if gps_data and len(gps_data) > 0:
                        print(f"DEBUG - GPSInfo encontrado con datos: {gps_data}")
        except Exception as e:
            print(f"DEBUG - Error extrayendo EXIF alternativo: {e}")

        return exif_data if exif_data else None

    def _get_gps_info(self, exif_data):
        """Extrae información GPS de los datos EXIF de forma robusta."""
        gps_info = exif_data.get("GPSInfo")
        if not gps_info:
            return None

        # Si está vacío, retornar None
        if isinstance(gps_info, dict) and len(gps_info) == 0:
            print("DEBUG - GPSInfo es un diccionario vacío")
            return None

        gps = {}
        # Si gps_info es un dict, procesarlo normalmente
        if isinstance(gps_info, dict):
            for key, val in gps_info.items():
                tag_name = ExifTags.GPSTAGS.get(key, key)
                gps[tag_name] = val
        elif isinstance(gps_info, (tuple, list)):
            # Algunos formatos devuelven tuplas
            print(f"DEBUG - GPSInfo es tupla/lista: {gps_info}")
            # Intentar mapear por posición
            gps_tags = ['GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude',
                       'GPSAltitudeRef', 'GPSAltitude']
            for i, val in enumerate(gps_info):
                if i < len(gps_tags):
                    gps[gps_tags[i]] = val
        else:
            # Si no es dict, intentar usar directamente
            gps = gps_info

        print(f"DEBUG - GPS tags encontrados: {list(gps.keys()) if isinstance(gps, dict) else 'No es dict'}")
        return gps

    def _convert_dms_tuple(self, dms_tuple):
        """Convierte tupla DMS de la biblioteca exif a decimal."""
        if not dms_tuple or len(dms_tuple) < 3:
            raise ValueError("Formato DMS inválido")

        # Cada elemento es una tupla (numerador, denominador)
        def to_float(v):
            if isinstance(v, (tuple, list)) and len(v) == 2:
                return float(v[0]) / float(v[1]) if v[1] != 0 else float(v[0])
            return float(v)

        d = to_float(dms_tuple[0])
        m = to_float(dms_tuple[1])
        s = to_float(dms_tuple[2])

        return d + (m / 60.0) + (s / 3600.0)

    def _convert_to_degrees(self, value):
        """Convierte coordenadas GPS a decimal, manejando varios formatos."""
        try:
            # Manejar si value es una tupla/lista de 3 elementos
            if isinstance(value, (tuple, list)) and len(value) >= 3:
                return self._convert_dms_tuple(value)
            else:
                # Si es un solo valor, convertir directamente
                return float(value)
        except Exception as e:
            raise ValueError(f"Error convirtiendo coordenada {value}: {e}")

    def _get_coordinates(self, gps_info):
        """Obtiene latitud y longitud decimales del GPSInfo."""
        print(f"DEBUG - Procesando GPSInfo: {gps_info}")

        # Verificar que tenemos las claves necesarias
        lat_key = "GPSLatitude" if "GPSLatitude" in gps_info else 2  # 2 es el ID de GPSLatitude
        lon_key = "GPSLongitude" if "GPSLongitude" in gps_info else 4  # 4 es el ID de GPSLongitude
        lat_ref_key = "GPSLatitudeRef" if "GPSLatitudeRef" in gps_info else 1
        lon_ref_key = "GPSLongitudeRef" if "GPSLongitudeRef" in gps_info else 3

        gps_lat = gps_info.get(lat_key)
        gps_lon = gps_info.get(lon_key)

        if gps_lat is None or gps_lon is None:
            raise ValueError(f"No se encontraron coordenadas. Claves disponibles: {list(gps_info.keys())}")

        print(f"DEBUG - GPSLatitude raw: {gps_lat} (tipo: {type(gps_lat)})")
        print(f"DEBUG - GPSLongitude raw: {gps_lon} (tipo: {type(gps_lon)})")

        lat = self._convert_to_degrees(gps_lat)
        lon = self._convert_to_degrees(gps_lon)

        # Aplicar referencia (N/S, E/W)
        lat_ref = gps_info.get(lat_ref_key, 'N')
        lon_ref = gps_info.get(lon_ref_key, 'E')

        print(f"DEBUG - GPSLatitudeRef: {lat_ref}, GPSLongitudeRef: {lon_ref}")

        if lat_ref == "S" or lat_ref == b'S':
            lat = -lat
        if lon_ref == "W" or lon_ref == b'W':
            lon = -lon

        return lat, lon

    def _get_exif_with_exif_library(self, image_path):
        """Intenta extraer EXIF usando la biblioteca 'exif' (más moderna)."""
        try:
            from exif import Image as ExifImage
            with open(image_path, 'rb') as f:
                img_exif = ExifImage(f)
                if img_exif.has_exif:
                    data = {}
                    # Intentar extraer atributos comunes de EXIF
                    exif_attrs = [
                        'make', 'model', 'datetime', 'datetime_original',
                        'gps_latitude', 'gps_latitude_ref', 'gps_longitude',
                        'gps_longitude_ref', 'gps_altitude', 'lens_model',
                        'focal_length', 'f_number', 'exposure_time', 'iso'
                    ]
                    for attr in exif_attrs:
                        try:
                            val = getattr(img_exif, attr, None)
                            if val is not None:
                                data[attr] = val
                        except:
                            pass
                    print(f"DEBUG - Datos extraídos con biblioteca exif: {list(data.keys())}")
                    return data if data else None
        except ImportError:
            print("DEBUG - Biblioteca 'exif' no instalada (pip install exif)")
        except Exception as e:
            print(f"DEBUG - Error con biblioteca exif: {e}")
        return None

    def _get_basic_info(self, image_path, img):
        info = {}
        file_stats = os.stat(image_path)
        info['file_name'] = os.path.basename(image_path)
        info['file_size'] = file_stats.st_size
        info['file_path'] = image_path

        with open(image_path, 'rb') as f:
            md5_hash = hashlib.md5(f.read()).hexdigest()
            info['checksum'] = md5_hash

        info['format'] = img.format
        info['mode'] = img.mode
        info['width'] = img.width
        info['height'] = img.height
        info['image_size'] = f"{img.width}x{img.height}"
        info['megapixels'] = round((img.width * img.height) / 1000000, 1)

        if img.format == 'JPEG':
            info['file_type_extension'] = 'jpg'
            info['mime_type'] = 'image/jpeg'
        elif img.format == 'PNG':
            info['file_type_extension'] = 'png'
            info['mime_type'] = 'image/png'

        return info

    def _format_file_size(self, size_bytes):
        for unit in ['B', 'kB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def _get_address(self, lat, lon):
        try:
            geolocator = Nominatim(user_agent="exif_location_finder_gui")
            location = geolocator.reverse(f"{lat}, {lon}", language="es")
            return location.address if location else None
        except Exception:
            return None

    def _open_maps(self):
        if self.coords:
            lat, lon = self.coords
            url = f"https://maps.google.com/?q={lat},{lon}"
            webbrowser.open(url)


def main():
    root = tk.Tk()
    app = ModernMetadataApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
