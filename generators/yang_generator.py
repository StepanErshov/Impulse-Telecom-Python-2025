from generators.base_generator import BaseGenerator

class YANGGenerator(BaseGenerator):
    def generate(self, uml_model: dict, output_dir: str) -> str:
        yang_content = f"""module bts-config {{
    namespace "urn:bts:config";
    prefix btscfg;
    revision 2024-05-11 {{
        description "Generated from UML model";
    }}
"""

        for cls in uml_model["classes"]:
            yang_content += f"""
    container {cls.name.lower()} {{
        description "{cls.documentation}";
"""
            for attr in cls.attributes:
                yang_type = self._map_type(attr["type"])
                yang_content += f"""
        leaf {attr["name"]} {{
            type {yang_type};
            description "Auto-generated attribute";
        }}
"""
            yang_content += "    }\n"
        
        yang_content += "}"
        return self._save_to_file(yang_content, "bts-config.yang", output_dir)

    def _map_type(self, uml_type: str) -> str:
        type_mapping = {
            "uint32": "uint32",
            "string": "string",
            "boolean": "boolean"
        }
        return type_mapping.get(uml_type, "string")