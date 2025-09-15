import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from PyPDF2 import PdfReader

def get_gps_info(exif_data):
    if 'GPSInfo' not in exif_data:
        return None

    gps_info = {}
    for key, val in exif_data['GPSInfo'].items():
        tag_name = GPSTAGS.get(key, key)
        gps_info[tag_name] = val
    
    return gps_info

def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    decimal_val = degrees + minutes + seconds
    if ref in ['S', 'W']:
        decimal_val = -decimal_val
    return decimal_val

def analyze_image_metadata(file_path):
    try:
        image = Image.open(file_path)
        exif_data_raw = image._getexif()

        if not exif_data_raw:
            return "No EXIF metadata found in this image."

        output_lines = [f"✅ Found EXIF Metadata for: {file_path}\n"]
        exif_data_decoded = {}

        for tag_id, value in exif_data_raw.items():
            tag_name = TAGS.get(tag_id, tag_id)
            exif_data_decoded[tag_name] = value
        
        for tag, value in exif_data_decoded.items():
            if tag != 'GPSInfo':
                output_lines.append(f"{str(tag):25}: {str(value)}")

        gps_info = get_gps_info(exif_data_decoded)
        if gps_info:
            output_lines.append("\n--- GPS Information ---")
            lat_dms = gps_info.get('GPSLatitude')
            lon_dms = gps_info.get('GPSLongitude')
            lat_ref = gps_info.get('GPSLatitudeRef')
            lon_ref = gps_info.get('GPSLongitudeRef')

            if lat_dms and lon_dms and lat_ref and lon_ref:
                lat_decimal = get_decimal_from_dms(lat_dms, lat_ref)
                lon_decimal = get_decimal_from_dms(lon_dms, lon_ref)
                output_lines.append(f"{'Latitude':25}: {lat_decimal}")
                output_lines.append(f"{'Longitude':25}: {lon_decimal}")
                output_lines.append(f"{'Google Maps Link':25}: https://www.google.com/maps?q={lat_decimal},{lon_decimal}")
        
        return "\n".join(output_lines)

    except Exception as e:
        return f"❌ Could not read image file: {e}"

def analyze_pdf_metadata(file_path):
    """Analyzes and returns the metadata of a PDF file."""
    try:
        with open(file_path, 'rb') as f:
            pdf = PdfReader(f)
            metadata = pdf.metadata
            
            if not metadata:
                return "No metadata found in this PDF."
            
            output_lines = [f"✅ Found Metadata for: {file_path}\n"]
            for key, value in metadata.items():
                clean_key = key.lstrip('/')
                output_lines.append(f"{str(clean_key):25}: {str(value)}")
            
            return "\n".join(output_lines)
            
    except Exception as e:
        return f"❌ Could not read PDF file: {e}"

def export_to_file(data, original_file_path):
    base_name = os.path.basename(original_file_path)
    output_filename = f"{base_name}_metadata.txt"
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(data)
    print(f"\n✅ Metadata successfully exported to '{output_filename}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python advanced_analyzer.py <file_path> [--export]")
        sys.exit(1)

    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ Error: The file '{file_path}' was not found.")
        sys.exit(1)

    file_extension = os.path.splitext(file_path)[1].lower()
    metadata_result = ""

    if file_extension in ['.jpg', '.jpeg', '.tiff', '.png']:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            print("PyPDF2 is not installed. Please run 'pip install PyPDF2' to analyze PDF files.")
            sys.exit(1)
            
        metadata_result = analyze_image_metadata(file_path)
    elif file_extension == '.pdf':
        metadata_result = analyze_pdf_metadata(file_path)
    else:
        print(f"Unsupported file type: {file_extension}. This script supports images and PDFs.")
        sys.exit(1)
        
    print(metadata_result)

    if '--export' in sys.argv:
        export_to_file(metadata_result, file_path)
