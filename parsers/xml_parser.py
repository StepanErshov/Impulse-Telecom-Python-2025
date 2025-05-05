import xml.etree.ElementTree as ET
from models.uml_model import UMLClass, Aggregation

class XMLParser:
    @staticmethod
    def parse(xml_content: str) -> dict:
        root = ET.fromstring(xml_content)
        model = {
            "classes": [],
            "aggregations": []
        }
        
        for elem in root:
            if elem.tag == "Class":
                cls = UMLClass(
                    name=elem.attrib["name"],
                    is_root=elem.attrib.get("isRoot", "false") == "true",
                    documentation=elem.attrib.get("documentation", ""),
                    attributes=[]
                )
                
                for attr in elem.findall("Attribute"):
                    cls.attributes.append({
                        "name": attr.attrib["name"],
                        "type": attr.attrib["type"]
                    })
                
                model["classes"].append(cls)
            
            elif elem.tag == "Aggregation":
                model["aggregations"].append(Aggregation(
                    source=elem.attrib["source"],
                    target=elem.attrib["target"],
                    source_multiplicity=elem.attrib["sourceMultiplicity"],
                    target_multiplicity=elem.attrib["targetMultiplicity"]
                ))
        
        return model