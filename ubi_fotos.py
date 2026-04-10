# Instalar dependencias:
# pip install Pillow geopy

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
import sys
import os

def get_exif_data(image_path):
    """Extrae todos los datos EXIF de una imagen."""
    img = Image.open(image_path)
    exif_data = {}
    
    raw_exif = img._getexif()
    if not raw_exif:
        return None
    
    for tag_id, value in raw_exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_data[tag] = value
    
    return exif_data

def get_gps_info(exif_data):
    """Extrae y convierte los datos GPS del EXIF."""
    gps_info = exif_data.get("GPSInfo")
    if not gps_info:
        return None
    
    gps = {}
    for key, val in gps_info.items():
        gps[GPSTAGS.get(key, key)] = val
    
    return gps

def convert_to_degrees(value):
    """Convierte coordenadas GPS (grados, minutos, segundos) a decimal."""
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

def get_coordinates(gps_info):
    """Obtiene latitud y longitud como decimales."""
    lat = convert_to_degrees(gps_info["GPSLatitude"])
    lon = convert_to_degrees(gps_info["GPSLongitude"])
    
    if gps_info.get("GPSLatitudeRef") == "S":
        lat = -lat
    if gps_info.get("GPSLongitudeRef") == "W":
        lon = -lon
    
    return lat, lon

def get_address(lat, lon):
    """Convierte coordenadas en dirección usando Nominatim (OpenStreetMap)."""
    geolocator = Nominatim(user_agent="exif_location_finder")
    location = geolocator.reverse(f"{lat}, {lon}", language="es")
    return location.address if location else "No se encontró dirección"

def analyze_image(image_path):
    print(f"\nAnalizando: {os.path.basename(image_path)}")
    print("-" * 50)
    
    exif_data = get_exif_data(image_path)
    if not exif_data:
        print("No se encontraron metadatos EXIF.")
        return
    
    gps_info = get_gps_info(exif_data)
    if not gps_info:
        print("La imagen no tiene datos GPS en sus metadatos.")
        print("(Puede que la cámara/teléfono tenía el GPS desactivado)")
        return
    
    lat, lon = get_coordinates(gps_info)
    print(f"Latitud:  {lat:.6f}")
    print(f"Longitud: {lon:.6f}")
    
    print("Buscando dirección...")
    address = get_address(lat, lon)
    print(f"Dirección: {address}")
    
    # También muestra el link a Google Maps
    print(f"Google Maps: https://maps.google.com/?q={lat},{lon}")

# --- Uso ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Si no pasas argumento, analiza todas las imágenes en la carpeta actual
        for f in os.listdir("."):
            if f.lower().endswith((".jpg", ".jpeg", ".tiff")):
                analyze_image(f)
    else:
        analyze_image(sys.argv[1])