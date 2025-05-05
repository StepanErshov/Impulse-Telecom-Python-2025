import os
from generators.json_generator import JSONGenerator
from generators.xml_generator import XMLGenerator
from validator.validator import DataValidator
from parsers.xml_parser import XMLParser
from parsers.json_parser import JSONParser
from generators.yang_generator import YANGGenerator
from generators.proto_generator import ProtoGenerator
from validator.validator import validate_uml_model

def ensure_out_dir():
    if not os.path.exists("out"):
        os.makedirs("out")

def ParsAndGen():
    with open("input/impulse_test_input.xml") as f:
        xml_data = f.read()
    
    with open("input/config.json") as f:
        json_data = f.read()

    uml_model = XMLParser.parse(xml_data)
    config_params = JSONParser.parse(json_data)

    if not validate_uml_model(uml_model):
        print("Invalid UML model!")
        return

    os.makedirs("out", exist_ok=True)
    
    generators = [
        YANGGenerator(),
        ProtoGenerator()
    ]

    for generator in generators:
        try:
            output_path = generator.generate(uml_model, "out")
            print(f"Generated: {output_path}")
        except Exception as e:
            print(f"Generation failed: {str(e)}")


def main():
    ParsAndGen()
    ensure_out_dir()
    #change to file path
    sample_data = {
        "config": {"version": "1.0", "author": "user"},
        "devices": ["antenna", "radio_module"]
    }
    
    if not DataValidator.validate(sample_data):
        print("Error validation data!")
        return

    generators = [JSONGenerator(), XMLGenerator()]
    for gen in generators:
        gen.generate(sample_data, "out")

if __name__ == "__main__":
    main()