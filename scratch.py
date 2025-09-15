import xml.etree.ElementTree as ET

def alto_to_text(xml_path: str) -> str:
    """
    Convert an ALTO XML OCR file into plain text with newlines preserved.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Namespace handling
    ns = {"alto": "http://schema.ccs-gmbh.com/ALTO"}

    all_lines = []
    for textblock in root.findall(".//alto:TextBlock", ns):
        block_lines = []
        for textline in textblock.findall("alto:TextLine", ns):
            words = [string.attrib.get("CONTENT", "") for string in textline.findall("alto:String", ns)]
            if words:
                block_lines.append(" ".join(words))
        if block_lines:
            all_lines.append("\n".join(block_lines))

    return "\n\n".join(all_lines)


# Example usage
xml_file = "0188.xml"  # your downloaded file
plain_text = alto_to_text(xml_file)

# Save to TXT
with open("0188.txt", "w", encoding="utf-8") as f:
    f.write(plain_text)


print("Preview of extracted text:")
print(plain_text)




'''
import requests

def download_xml(url: str, save_path: str) -> None:
    """
    Download an XML file (METS or ALTO) from Chronicling America
    and save it locally.
    """
    response = requests.get(url)
    response.raise_for_status()  # raises an error if download fails
    
    with open(save_path, "wb") as f:
        f.write(response.content)
    
    print(f"Saved XML to {save_path}")


# Example usage
xml_url = "https://tile.loc.gov/storage-services/service/ndnp/uuml/batch_uuml_four_ver01/data/sn85058130/00100478225/1903091801/0188.xml"
save_as = "0188.xml"

download_xml(xml_url, save_as)
'''


'''import requests
import xml.etree.ElementTree as ET

def extract_alto_from_mets(mets_url: str) -> str:
    """Fetch METS, follow link to ALTO OCR file, return plain text OCR."""
    # Step 1: Fetch METS
    mets_response = requests.get(mets_url)
    mets_response.raise_for_status()
    mets_root = ET.fromstring(mets_response.content)

    # Namespaces
    ns = {
        "mets": "http://www.loc.gov/METS/",
        "xlink": "http://www.w3.org/1999/xlink"
    }

    # Step 2: Try multiple possible fileGrp USE values
    alto_url = None
    for use_value in ["ocr", "alto", "ALTO", "ocr/alto"]:
        for flocat in mets_root.findall(f".//mets:fileGrp[@USE='{use_value}']//mets:FLocat", ns):
            alto_url = flocat.attrib.get(f"{{{ns['xlink']}}}href")
            if alto_url:
                break
        if alto_url:
            break

    if not alto_url:
        raise ValueError("No ALTO OCR file reference found in METS.")

    # Step 3: Fetch ALTO file
    alto_response = requests.get(alto_url)
    alto_response.raise_for_status()
    alto_root = ET.fromstring(alto_response.content)

    # Step 4: Extract text with line breaks
    all_lines = []
    for textblock in alto_root.findall(".//TextBlock"):
        block_lines = []
        for textline in textblock.findall("TextLine"):
            words = [string.attrib.get("CONTENT", "") for string in textline.findall("String")]
            if words:
                block_lines.append(" ".join(words))
        if block_lines:
            all_lines.append("\n".join(block_lines))

    return "\n\n".join(all_lines)


# Example usage
mets_url = "https://tile.loc.gov/storage-services/service/ndnp/uuml/batch_uuml_four_ver01/data/sn85058130/00100478225/1903091801/0188.xml"
text = extract_alto_from_mets(mets_url)
print(text[:500])
'''