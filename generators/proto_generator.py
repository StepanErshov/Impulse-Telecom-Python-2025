from generators.base_generator import BaseGenerator
from typing import Dict, List

class ProtoGenerator(BaseGenerator):
    def generate(self, uml_model: Dict, output_dir: str) -> str:
        """Генерирует .proto файл из UML-модели"""
        proto_content = self._generate_proto_header()
        
        for cls in uml_model["classes"]:
            proto_content += self._generate_class_message(cls)
        
        proto_content += self._generate_aggregation_relations(uml_model["aggregations"])
        
        return self._save_to_file(proto_content, "bts_config.proto", output_dir)

    def _generate_proto_header(self) -> str:
        return """syntax = "proto3";

package bts.config;
option go_package = "github.com/bts/config";

import "google/protobuf/empty.proto";

// Автоматически сгенерировано из UML-модели
// Версия: 1.0

"""

    def _generate_class_message(self, cls: Dict) -> str:
        message = f"message {cls['name']} {{\n"
        
        for i, attr in enumerate(cls["attributes"], start=1):
            proto_type = self._map_type(attr["type"])
            message += f"    {proto_type} {attr['name']} = {i};"
            
            if cls.get("documentation"):
                message += f" // {cls['documentation']}"
            message += "\n"
        
        message += "}\n\n"
        return message

    def _generate_aggregation_relations(self, aggregations: List[Dict]) -> str:
        relations = "// Определения отношений между классами\n"
        
        for agg in aggregations:
            relations += f"""
message {agg['source']}To{agg['target']}Relation {{
    string source_id = 1;  // ID {agg['source']}
    string target_id = 2;  // ID {agg['target']}
    string relation_type = 3;  // Всегда "aggregation"
    string source_multiplicity = 4;  // {agg['source_multiplicity']}
    string target_multiplicity = 5;  // {agg['target_multiplicity']}
}}

"""
        return relations

    def _map_type(self, uml_type: str) -> str:
        """Конвертирует UML-типы в Proto-типы"""
        type_mapping = {
            "uint32": "uint32",
            "string": "string",
            "boolean": "bool",
            "int": "int32",
            "float": "float",
            "double": "double"
        }
        return type_mapping.get(uml_type.lower(), "string")