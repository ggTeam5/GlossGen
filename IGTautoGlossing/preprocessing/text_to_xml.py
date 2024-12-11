import xml.etree.ElementTree as ET
from xml.dom import minidom

def parse_txt_to_dict(txt_file):
    """
    Parse the txt file and extract information into a dictionary format.
    This function is designed to work with a variety of language formats.
    """
    data = []
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_igt = None
    for line in lines:
        # Skip empty lines or irrelevant lines
        if not line.strip(): #enter if string is empty
            continue
        
        # Process line by line to identify tags
        line = line.strip()
        
        if line.startswith("doc_id"):
            # Start of a new IGT block
            if current_igt:
                data.append(current_igt)
            current_igt = {
                'id': line.split()[1],
                'lines': [],
                'language': None,  # Default to None, can be set from metadata later
                'language_code': None  # Language code can be extracted from metadata
            }
        
        elif line.startswith("line"):
            line_parts = line.split("tag=")
            if len(line_parts) > 1:
                tag = line_parts[1].split()[0]
                content = line.split(":")[-1].strip()
                current_igt['lines'].append({
                    'tag': tag,
                    'content': content
                })

        elif line.startswith("language:"):
            # Extract language information from metadata lines
            current_igt['language'] = line.split(":")[-1].strip()

    if current_igt:
        data.append(current_igt)
    
    return data

def create_xml_from_dict(data):
    """
    Convert parsed dictionary data into XML structure, flexible for multiple languages.
    """
    root = ET.Element("xigt-corpus", xmlns_dc="http://purl.org/dc/elements/1.1/",
                      xmlns_olac="http://www.language-archives.org/OLAC/1.1/",
                      xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance")

    for entry in data:
        igt = ET.SubElement(root, "igt", id=entry['id'], doc_id=entry['id'])
        metadata = ET.SubElement(igt, "metadata")
        meta = ET.SubElement(metadata, "meta", id="meta1")
        
        # Language metadata
        dc_subject = ET.SubElement(meta, "dc:subject", olac_code="aae", xsi_type="olac:language")
        dc_subject.text = entry['language'] if entry['language'] else "Unknown Language"
        
        dc_language = ET.SubElement(meta, "dc:language", olac_code="en", xsi_type="olac:language")
        dc_language.text = "English"  # Default to English for the translation
        
        # Add lines under different tiers
        tier_r = ET.SubElement(igt, "tier", id="r", type="odin", state="raw")
        for line in entry['lines']:
            item = ET.SubElement(tier_r, "item", id=f"r{entry['lines'].index(line)+1}", line=str(entry['lines'].index(line)+1), tag=line['tag'])
            item.text = line['content']

        tier_c = ET.SubElement(igt, "tier", id="c", type="odin", alignment="r", state="cleaned")
        for line in entry['lines']:
            item = ET.SubElement(tier_c, "item", id=f"c{entry['lines'].index(line)+1}", alignment=f"r{entry['lines'].index(line)+1}", line=str(entry['lines'].index(line)+1), tag=line['tag'])
            item.text = line['content']

        tier_n = ET.SubElement(igt, "tier", id="n", type="odin", alignment="c", state="normalized")
        for line in entry['lines']:
            item = ET.SubElement(tier_n, "item", id=f"n{entry['lines'].index(line)+1}", alignment=f"c{entry['lines'].index(line)+1}", line=str(entry['lines'].index(line)+1), tag=line['tag'])
            item.text = line['content']

    # Convert the tree to a string and use minidom to prettify
    xml_str = ET.tostring(root, encoding='utf-8', method='xml')
    parsed_xml = minidom.parseString(xml_str)
    return parsed_xml.toprettyxml(indent="  ")  # Pretty format the XML with indentation

def save_xml_to_file(xml_data, output_file):
    """
    Save the generated XML data to a file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_data)

def main():
    # Input and Output file paths
    input_txt = 'aae.txt'  # You can replace this with any input text file
    output_xml = 'aae.xml'  # You can specify a different output file name if needed

    # Parse the txt file and convert to dict
    data = parse_txt_to_dict(input_txt)

    # Create XML from the dictionary data
    xml_data = create_xml_from_dict(data)

    # Save the generated XML data to the output file
    save_xml_to_file(xml_data, output_xml)

    print(f"XML file has been successfully created: {output_xml}")

if __name__ == "__main__":
    main()
