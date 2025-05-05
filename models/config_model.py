from dataclasses import dataclass

@dataclass
class ConfigParameter:
    name: str
    value: str

class CppConfigGenerator:
    def generate(self, params: list, output_dir: str) -> str:
        header = """#pragma once
#include <string>
#include <unordered_map>

class BTSConfig {
public:
    std::unordered_map<std::string, std::string> params = {
"""
        for param in params:
            header += f'        {{"{param.name}", "{param.value}"}},\n'
        
        header += """    };
};
"""
        return self._save_to_file(header, "bts_config.h", output_dir)