from xml.etree import ElementTree as ET
from .base_generator import BaseGenerator

class XMLGenerator(BaseGenerator):
    def generate(self, data: dict, output_dir: str) -> str:
        def dict_to_xml(tag: str, d: dict) -> ET.Element:
            elem = ET.Element(tag)
            for key, val in d.items():
                if isinstance(val, dict):
                    elem.append(dict_to_xml(key, val))
                elif isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            elem.append(dict_to_xml(key, item))
                        else:
                            child = ET.Element(key)
                            child.text = str(item)
                            elem.append(child)
                else:
                    child = ET.Element(key)
                    child.text = str(val)
                    elem.append(child)
            return elem

        root = dict_to_xml("Configuration", data)
        xml_content = ET.tostring(root, encoding='unicode', method='xml')
        pretty_xml = self._prettify_xml(xml_content)
        
        filename = f"config_{self.timestamp}.xml"
        return self._save_to_file(pretty_xml, filename, output_dir)

    def _prettify_xml(self, xml_str: str) -> str:
        from xml.dom import minidom
        parsed = minidom.parseString(xml_str)
        return parsed.toprettyxml(indent="  ")