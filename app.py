import streamlit as st
import zipfile
import os
import shutil
from lxml import etree
from shapely.geometry import Point, Polygon

# --- KONFIGURASI NAMESPACE KML ---
NS = {'k': 'http://www.opengis.net/kml/2.2'}

# --- TEMPLATE XML (STYLE & SCHEMA - WAJIB ADA AGAR POPUP BENAR) ---
XML_STYLES = """
<root>
    <Schema name="HOME" id="S_HOME_SSSSSSSSSSSSSSSSSSSSSSSSSSSS">
        <SimpleField type="string" name="HOMEPASS_ID"><displayName><b>HOMEPASS_ID</b></displayName></SimpleField>
        <SimpleField type="string" name="CLUSTER_NAME"><displayName><b>CLUSTER_NAME</b></displayName></SimpleField>
        <SimpleField type="string" name="PREFIX_ADDRESS"><displayName><b>PREFIX_ADDRESS</b></displayName></SimpleField>
        <SimpleField type="string" name="STREET_NAME"><displayName><b>STREET_NAME</b></displayName></SimpleField>
        <SimpleField type="string" name="HOUSE_NUMBER"><displayName><b>HOUSE_NUMBER</b></displayName></SimpleField>
        <SimpleField type="string" name="BLOCK"><displayName><b>BLOCK</b></displayName></SimpleField>
        <SimpleField type="string" name="FLOOR"><displayName><b>FLOOR</b></displayName></SimpleField>
        <SimpleField type="string" name="RT"><displayName><b>RT</b></displayName></SimpleField>
        <SimpleField type="string" name="RW"><displayName><b>RW</b></displayName></SimpleField>
        <SimpleField type="string" name="DISTRICT"><displayName><b>DISTRICT</b></displayName></SimpleField>
        <SimpleField type="string" name="SUB_DISTRICT"><displayName><b>SUB_DISTRICT</b></displayName></SimpleField>
        <SimpleField type="string" name="FDT_CODE"><displayName><b>FDT_CODE</b></displayName></SimpleField>
        <SimpleField type="string" name="FAT_CODE"><displayName><b>FAT_CODE</b></displayName></SimpleField>
        <SimpleField type="string" name="BUILDING_LATITUDE"><displayName><b>BUILDING_LATITUDE</b></displayName></SimpleField>
        <SimpleField type="string" name="BUILDING_LONGITUDE"><displayName><b>BUILDING_LONGITUDE</b></displayName></SimpleField>
        <SimpleField type="string" name="Category_BizPass"><displayName><b>Category BizPass</b></displayName></SimpleField>
        <SimpleField type="string" name="POST_CODE"><displayName><b>POST CODE</b></displayName></SimpleField>
        <SimpleField type="string" name="ADDRESS_POLE___FAT"><displayName><b>ADDRESS POLE / FAT</b></displayName></SimpleField>
        <SimpleField type="string" name="OV_UG"><displayName><b>OV_UG</b></displayName></SimpleField>
        <SimpleField type="string" name="HOUSE_COMMENT_"><displayName><b>HOUSE_COMMENT_</b></displayName></SimpleField>
        <SimpleField type="string" name="BUILDING_NAME"><displayName><b>BUILDING_NAME</b></displayName></SimpleField>
        <SimpleField type="string" name="TOWER"><displayName><b>TOWER</b></displayName></SimpleField>
        <SimpleField type="string" name="APTN"><displayName><b>APTN</b></displayName></SimpleField>
        <SimpleField type="string" name="FIBER_NODE__HFC_"><displayName><b>FIBER_NODE__HFC_</b></displayName></SimpleField>
        <SimpleField type="string" name="ADDRESS_POLE___FAT_2"><displayName><b>ADDRESS POLE / FAT</b></displayName></SimpleField>
        <SimpleField type="string" name="ID_Area"><displayName><b>ID_Area</b></displayName></SimpleField>
        <SimpleField type="string" name="Clamp_Hook_ID"><displayName><b>Clamp_Hook_ID</b></displayName></SimpleField>
        <SimpleField type="string" name="DEPLOYMENT_TYPE"><displayName><b>DEPLOYMENT_TYPE</b></displayName></SimpleField>
        <SimpleField type="string" name="NEED_SURVEY"><displayName><b>NEED_SURVEY</b></displayName></SimpleField>
    </Schema>
    <StyleMap id="SM_HOME">
        <Pair><key>normal</key><styleUrl>#SN_HOME</styleUrl></Pair>
        <Pair><key>highlight</key><styleUrl>#SH_HOME</styleUrl></Pair>
    </StyleMap>
    <Style id="SH_HOME">
        <IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href></Icon></IconStyle>
        <BalloonStyle><text><![CDATA[<table border="0"><tr><td><b>HOMEPASS_ID</b></td><td>$[HOME/HOMEPASS_ID]</td></tr><tr><td><b>CLUSTER_NAME</b></td><td>$[HOME/CLUSTER_NAME]</td></tr><tr><td><b>PREFIX_ADDRESS</b></td><td>$[HOME/PREFIX_ADDRESS]</td></tr><tr><td><b>STREET_NAME</b></td><td>$[HOME/STREET_NAME]</td></tr><tr><td><b>HOUSE_NUMBER</b></td><td>$[HOME/HOUSE_NUMBER]</td></tr><tr><td><b>BLOCK</b></td><td>$[HOME/BLOCK]</td></tr><tr><td><b>FLOOR</b></td><td>$[HOME/FLOOR]</td></tr><tr><td><b>RT</b></td><td>$[HOME/RT]</td></tr><tr><td><b>RW</b></td><td>$[HOME/RW]</td></tr><tr><td><b>DISTRICT</b></td><td>$[HOME/DISTRICT]</td></tr><tr><td><b>SUB_DISTRICT</b></td><td>$[HOME/SUB_DISTRICT]</td></tr><tr><td><b>FDT_CODE</b></td><td>$[HOME/FDT_CODE]</td></tr><tr><td><b>FAT_CODE</b></td><td>$[HOME/FAT_CODE]</td></tr><tr><td><b>BUILDING_LATITUDE</b></td><td>$[HOME/BUILDING_LATITUDE]</td></tr><tr><td><b>BUILDING_LONGITUDE</b></td><td>$[HOME/BUILDING_LONGITUDE]</td></tr><tr><td><b>Category BizPass</b></td><td>$[HOME/Category_BizPass]</td></tr><tr><td><b>POST CODE</b></td><td>$[HOME/POST_CODE]</td></tr><tr><td><b>ADDRESS POLE / FAT</b></td><td>$[HOME/ADDRESS_POLE___FAT]</td></tr><tr><td><b>OV_UG</b></td><td>$[HOME/OV_UG]</td></tr><tr><td><b>HOUSE_COMMENT_</b></td><td>$[HOME/HOUSE_COMMENT_]</td></tr><tr><td><b>BUILDING_NAME</b></td><td>$[HOME/BUILDING_NAME]</td></tr><tr><td><b>TOWER</b></td><td>$[HOME/TOWER]</td></tr><tr><td><b>APTN</b></td><td>$[HOME/APTN]</td></tr><tr><td><b>FIBER_NODE__HFC_</b></td><td>$[HOME/FIBER_NODE__HFC_]</td></tr><tr><td><b>ADDRESS POLE / FAT</b></td><td>$[HOME/ADDRESS_POLE___FAT_2]</td></tr><tr><td><b>ID_Area</b></td><td>$[HOME/ID_Area]</td></tr><tr><td><b>Clamp_Hook_ID</b></td><td>$[HOME/Clamp_Hook_ID]</td></tr><tr><td><b>DEPLOYMENT_TYPE</b></td><td>$[HOME/DEPLOYMENT_TYPE]</td></tr><tr><td><b>NEED_SURVEY</b></td><td>$[HOME/NEED_SURVEY]</td></tr></table>]]></text></BalloonStyle>
    </Style>
    <Style id="SN_HOME">
        <IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle>
        <BalloonStyle><text><![CDATA[<table border="0"><tr><td><b>HOMEPASS_ID</b></td><td>$[HOME/HOMEPASS_ID]</td></tr><tr><td><b>CLUSTER_NAME</b></td><td>$[HOME/CLUSTER_NAME]</td></tr><tr><td><b>PREFIX_ADDRESS</b></td><td>$[HOME/PREFIX_ADDRESS]</td></tr><tr><td><b>STREET_NAME</b></td><td>$[HOME/STREET_NAME]</td></tr><tr><td><b>HOUSE_NUMBER</b></td><td>$[HOME/HOUSE_NUMBER]</td></tr><tr><td><b>BLOCK</b></td><td>$[HOME/BLOCK]</td></tr><tr><td><b>FLOOR</b></td><td>$[HOME/FLOOR]</td></tr><tr><td><b>RT</b></td><td>$[HOME/RT]</td></tr><tr><td><b>RW</b></td><td>$[HOME/RW]</td></tr><tr><td><b>DISTRICT</b></td><td>$[HOME/DISTRICT]</td></tr><tr><td><b>SUB_DISTRICT</b></td><td>$[HOME/SUB_DISTRICT]</td></tr><tr><td><b>FDT_CODE</b></td><td>$[HOME/FDT_CODE]</td></tr><tr><td><b>FAT_CODE</b></td><td>$[HOME/FAT_CODE]</td></tr><tr><td><b>BUILDING_LATITUDE</b></td><td>$[HOME/BUILDING_LATITUDE]</td></tr><tr><td><b>BUILDING_LONGITUDE</b></td><td>$[HOME/BUILDING_LONGITUDE]</td></tr><tr><td><b>Category BizPass</b></td><td>$[HOME/Category_BizPass]</td></tr><tr><td><b>POST CODE</b></td><td>$[HOME/POST_CODE]</td></tr><tr><td><b>ADDRESS POLE / FAT</b></td><td>$[HOME/ADDRESS_POLE___FAT]</td></tr><tr><td><b>OV_UG</b></td><td>$[HOME/OV_UG]</td></tr><tr><td><b>HOUSE_COMMENT_</b></td><td>$[HOME/HOUSE_COMMENT_]</td></tr><tr><td><b>BUILDING_NAME</b></td><td>$[HOME/BUILDING_NAME]</td></tr><tr><td><b>TOWER</b></td><td>$[HOME/TOWER]</td></tr><tr><td><b>APTN</b></td><td>$[HOME/APTN]</td></tr><tr><td><b>FIBER_NODE__HFC_</b></td><td>$[HOME/FIBER_NODE__HFC_]</td></tr><tr><td><b>ADDRESS POLE / FAT</b></td><td>$[HOME/ADDRESS_POLE___FAT_2]</td></tr><tr><td><b>ID_Area</b></td><td>$[HOME/ID_Area]</td></tr><tr><td><b>Clamp_Hook_ID</b></td><td>$[HOME/Clamp_Hook_ID]</td></tr><tr><td><b>DEPLOYMENT_TYPE</b></td><td>$[HOME/DEPLOYMENT_TYPE]</td></tr><tr><td><b>NEED_SURVEY</b></td><td>$[HOME/NEED_SURVEY]</td></tr></table>]]></text></BalloonStyle>
    </Style>
</root>
"""

# --- HELPER FUNCTIONS ---

def get_coordinates(placemark):
    """Mengekstrak koordinat (lon, lat) dari Placemark"""
    try:
        coords_str = placemark.find(".//k:coordinates", namespaces=NS).text.strip()
        parts = coords_str.split(',')
        return float(parts[0]), float(parts[1])
    except:
        return None

def create_extended_data(data_dict, schema_url="#S_HOME_SSSSSSSSSSSSSSSSSSSSSSSSSSSS"):
    """Membuat elemen ExtendedData KML"""
    ed = etree.Element("ExtendedData")
    sd = etree.SubElement(ed, "SchemaData", schemaUrl=schema_url)
    
    for key, value in data_dict.items():
        data_elem = etree.SubElement(sd, "SimpleData", name=key)
        data_elem.text = str(value)
    
    return ed

def find_folder(root, folder_names):
    """Mencari folder berdasarkan hirarki nama"""
    current = root
    for name in folder_names:
        found = False
        for folder in current.findall(".//k:Folder", namespaces=NS):
            fname = folder.find("k:name", namespaces=NS)
            if fname is not None and fname.text.strip() == name:
                current = folder
                found = True
                break
        if not found:
            return None
    return current

def parse_boundary_fat(boundary_folder):
    """Mengubah Boundary FAT KML menjadi Objek Shapely Polygon"""
    boundaries = []
    if boundary_folder is None:
        return boundaries
    
    for placemark in boundary_folder.findall(".//k:Placemark", namespaces=NS):
        name_tag = placemark.find("k:name", namespaces=NS)
        name = name_tag.text.strip() if name_tag is not None else "UNKNOWN"
        
        # Cari coordinates di dalam Polygon/LinearRing
        coords_str = placemark.find(".//k:coordinates", namespaces=NS)
        
        if coords_str is not None:
            raw_coords = coords_str.text.strip().split()
            points = []
            for c in raw_coords:
                parts = c.split(',')
                # Ambil Lon, Lat saja (abaikan altitude)
                points.append((float(parts[0]), float(parts[1])))
            
            if len(points) >= 3:
                poly = Polygon(points)
                # Simpan polygon dan centroid untuk titik tarik kabel
                boundaries.append({
                    "name": name,
                    "poly": poly,
                    "centroid": (poly.centroid.x, poly.centroid.y) 
                })
    return boundaries

# --- MAIN PROCESS ---

def process_kmz_large(input_file_path, form_data):
    """Memproses file KMZ besar dengan membaca langsung dari disk"""
    
    # 1. Buka KMZ
    try:
        kmz = zipfile.ZipFile(input_file_path, 'r')
    except zipfile.BadZipFile:
        return None, "File rusak atau bukan format ZIP/KMZ yang valid."

    kml_filename = [f for f in kmz.namelist() if f.endswith('.kml')]
    if not kml_filename:
        return None, "Tidak ditemukan file .kml di dalam arsip."
    
    # Baca content KML ke memori (tetap butuh RAM untuk XML tree)
    kml_content = kmz.read(kml_filename[0])
    
    # 2. Parse XML
    parser = etree.XMLParser(strip_cdata=False)
    root = etree.fromstring(kml_content, parser)
    doc = root.find(".//k:Document", namespaces=NS)
    
    if doc is None:
        return None, "Struktur KML tidak valid (Document tag hilang)."

    # 3. Inject Styles (Penting agar tabel popup muncul)
    # Cek apakah style sudah ada agar tidak duplikat
    if doc.find(".//k:StyleMap[@id='SM_HOME']", namespaces=NS) is None:
        style_root = etree.fromstring(XML_STYLES)
        for child in style_root:
            doc.insert(0, child)

    # 4. Cari Folder Penting
    dist_folder = find_folder(doc, ["DISTRIBUSI"])
    if dist_folder is None:
        return None, "Folder 'DISTRIBUSI' tidak ditemukan!"

    # --- LOGIC FOLDER BARU (HP > HOME / HOME BIZ) ---
    hp_folder = find_folder(dist_folder, ["HP"])
    
    homes_residence = []
    homes_biz = []
    
    if hp_folder is not None:
        # Coba cari HOME dan HOME BIZ didalam HP
        f_home = find_folder(hp_folder, ["HOME"])
        if f_home is not None:
            homes_residence = f_home.findall(".//k:Placemark", namespaces=NS)
            
        f_biz = find_folder(hp_folder, ["HOME BIZ"])
        if f_biz is not None:
            homes_biz = f_biz.findall(".//k:Placemark", namespaces=NS)
    else:
        # Fallback: Cari langsung di DISTRIBUSI jika folder HP tidak ada
        f_home = find_folder(dist_folder, ["HOME"])
        if f_home is not None:
            homes_residence = f_home.findall(".//k:Placemark", namespaces=NS)
        
        f_biz = find_folder(dist_folder, ["HOME BIZ"])
        if f_biz is not None:
            homes_biz = f_biz.findall(".//k:Placemark", namespaces=NS)

    # Folder Boundary
    boundary_folder = find_folder(dist_folder, ["BOUNDARY FAT"])
    boundaries = parse_boundary_fat(boundary_folder)

    # Buat Folder Output untuk Kabel Drop
    drop_folder = etree.Element("Folder")
    name_elem = etree.SubElement(drop_folder, "name")
    name_elem.text = "GENERATED DROP CABLES"
    dist_folder.append(drop_folder)

    # 5. Gabungkan List untuk Loop dan Beri Label Tipe
    all_homes = []
    for h in homes_residence:
        all_homes.append((h, "RESIDENCE"))
    for h in homes_biz:
        all_homes.append((h, "BUSINESS"))
    
    processed_count = 0
    drops_count = 0

    # 6. PROCESSING LOOP
    for placemark, home_type in all_homes:
        coords = get_coordinates(placemark)
        if not coords:
            continue
            
        point = Point(coords[0], coords[1])
        home_name = placemark.find("k:name", namespaces=NS).text or "No Name"
        
        # --- LOGIC UTAMA: Point in Polygon (Cari FAT) ---
        found_fat = "-"
        fat_coord = None
        
        # Cek satu per satu boundary
        for boundary in boundaries:
            if boundary['poly'].contains(point):
                found_fat = boundary['name']
                fat_coord = boundary['centroid']
                break
        
        # --- GENERATE DROP CABLE (Garis Lurus) ---
        if fat_coord:
            drops_count += 1
            # Buat Placemark Garis
            line_placemark = etree.SubElement(drop_folder, "Placemark")
            ln_name = etree.SubElement(line_placemark, "name")
            ln_name.text = f"{found_fat} to {home_name}"
            
            style = etree.SubElement(line_placemark, "Style")
            lstyle = etree.SubElement(style, "LineStyle")
            color = etree.SubElement(lstyle, "color")
            color.text = "ffff00ff" # Warna Magenta (AABBGGRR)
            width = etree.SubElement(lstyle, "width")
            width.text = "2"
            
            ln_geom = etree.SubElement(line_placemark, "LineString")
            tess = etree.SubElement(ln_geom, "tessellate")
            tess.text = "1"
            ln_coords = etree.SubElement(ln_geom, "coordinates")
            # Format KML: lon,lat,alt lon,lat,alt
            ln_coords.text = f"{fat_coord[0]},{fat_coord[1]},0 {coords[0]},{coords[1]},0"

        # --- BERSIHKAN DATA LAMA & INJECT DATA BARU ---
        # Hapus tag lama agar bersih
        for tag in ["description", "ExtendedData", "Style", "styleUrl"]:
            old = placemark.find(f"k:{tag}", namespaces=NS)
            if old is not None:
                placemark.remove(old)
        
        # Set Style Baru ke Template
        style_url = etree.SubElement(placemark, "styleUrl")
        style_url.text = "#SM_HOME"
        
        # Siapkan Data Popup
        data_map = {
            "HOMEPASS_ID": "-",
            "CLUSTER_NAME": form_data['cluster'],
            "PREFIX_ADDRESS": "JL.", 
            "STREET_NAME": "-",
            "HOUSE_NUMBER": home_name,
            "BLOCK": "-", "FLOOR": "-", "RT": "-", "RW": "-",
            "DISTRICT": form_data['district'],
            "SUB_DISTRICT": form_data['subdistrict'],
            "FDT_CODE": "-", 
            "FAT_CODE": found_fat, # HASIL POINT IN POLYGON
            "BUILDING_LATITUDE": f"{coords[1]:.6f}",
            "BUILDING_LONGITUDE": f"{coords[0]:.6f}",
            "Category_BizPass": home_type, # HASIL DETEKSI FOLDER
            "POST_CODE": form_data['postcode'],
            "ADDRESS_POLE___FAT": "-",
            "OV_UG": form_data['ov_ug'],
            "HOUSE_COMMENT_": form_data['comment'],
            "BUILDING_NAME": "-", "TOWER": "-", "APTN": "-", 
            "FIBER_NODE__HFC_": "-", "ADDRESS_POLE___FAT_2": "-", 
            "ID_Area": form_data['id_area'],
            "Clamp_Hook_ID": "-", 
            "DEPLOYMENT_TYPE": form_data['deployment'],
            "NEED_SURVEY": form_data['survey']
        }
        
        # Inject ExtendedData
        ed = create_extended_data(data_map)
        placemark.append(ed)
        processed_count += 1

    # 7. Packaging KMZ Baru (Simpan ke Disk)
    output_kmz_path = "processed_output.kmz"
    # Kompresi level 5 agar seimbang antara speed dan size
    with zipfile.ZipFile(output_kmz_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=5) as zf:
        zf.writestr('doc.kml', etree.tostring(root, pretty_print=True))
    
    return output_kmz_path, f"Selesai! {processed_count} titik diproses, {drops_count} kabel drop dibuat."

# --- UI STREAMLIT ---

st.set_page_config(page_title="ABD Maker Pro", layout="wide")

st.title("📡 ABD Maker Pro (Large File Support)")
st.markdown("""
**Automated Boundary Detection & Metadata Injector** Features: Auto Category (Home/Biz), Boundary FAT Detection, Auto Drop Cable.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("1. Upload Data")
    st.info("Support file > 2GB (Pastikan config.toml sudah diatur).")
    uploaded_file = st.file_uploader("Upload File KMZ", type="kmz")
    
    st.header("2. Parameter Desain")
    with st.form("design_params"):
        cluster = st.text_input("Cluster Name", "CLUSTER_DEMO")
        district = st.text_input("District", "KECAMATAN")
        subdistrict = st.text_input("Sub District", "KELURAHAN")
        id_area = st.text_input("ID Area", "12MDN...")
        postcode = st.text_input("Post Code", "12345")
        ov_ug = st.selectbox("OV/UG", ["O", "U"], index=0)
        deployment = st.text_input("Deployment Type", "G_BROWNFIELD")
        survey = st.text_input("Need Survey", "NO")
        comment = st.text_input("House Comment", "NEED SURVEY")
        
        submitted = st.form_submit_button("🚀 Mulai Proses")

with col2:
    st.header("3. Hasil Proses")
    
    if uploaded_file and submitted:
        form_data = {
            "cluster": cluster, "district": district, "subdistrict": subdistrict,
            "id_area": id_area, "postcode": postcode, "ov_ug": ov_ug,
            "deployment": deployment, "survey": survey, "comment": comment
        }
        
        # TRIK HEMAT MEMORI:
        # Simpan file yang diupload ke disk sementara, jangan simpan di RAM
        temp_filename = "temp_input.kmz"
        
        try:
            with open(temp_filename, "wb") as f:
                # Menulis chunk demi chunk agar RAM aman
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("Sedang membedah KMZ, mencari Boundary FAT, dan menarik kabel..."):
                # Panggil fungsi processing dengan PATH file
                output_path, msg = process_kmz_large(temp_filename, form_data)
                
                if output_path:
                    st.success(msg)
                    
                    # Baca hasil olahan untuk tombol download
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Hasil (KMZ)",
                            data=f,
                            file_name=f"PROCESSED_{uploaded_file.name}",
                            mime="application/vnd.google-earth.kmz"
                        )
                    
                    # Bersihkan file output
                    if os.path.exists(output_path):
                        os.remove(output_path)
                else:
                    st.error(msg)
                    
        except Exception as e:
            st.error(f"Terjadi Kesalahan: {str(e)}")
            st.exception(e) # Tampilkan detail error untuk debugging
            
        finally:
            # Selalu bersihkan file input sementara
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    elif not uploaded_file:
        st.info("Silakan upload file KMZ terlebih dahulu di panel sebelah kiri.")