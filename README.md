# Base Station Configuration Generator

A project for automatic generation of base station configuration artifacts from UML models and JSON parameters.


## Project structure
```
Impulse Telecom Python 2025/
│
├── generators/ # Artifact Generators
│ ├── base_generator.py # Base class generator
│ ├── json_generator.py # Generator JSON
│ ├── proto_generator.py # Generator Protocol Buffers
│ ├── xml_generator.py # Generator XML
│ └── yang_generator.py # Generator YANG-models
│
├── input/ # Input files
│ ├── config.json # Configuration example
│ ├── impulse_test_input.xml # Test UML-model
│ └── patched_config.json # Modified configuration
│
├── models/ # Data Models
│ ├── config_model.py # Configuration Parameter Model
│ └── uml_model.py # Model UML-classes
│
├── out/ # Generated files
│ ├── bts-config.yang # Example YANG-model
│ ├── config_*.json/xml # Genereted config
│ └── meta.json # Metadata generate
│
├── parsers/ # Parsers input data
│ ├── json_parser.py # Parser JSON
│ └── xml_parser.py # Parser XML
│
└── validator/ # Validators
└── validator.py # Validator UML-model
```

## Requirements

- Python 3.11
- Only Python standard libraries

## Installation

1. Clone repository:
   ```bash
   git clone <repo-url>
   cd Impulse_Telecom_Python_2025

2. Make sure you are using Python 3.11:
```bash
python --version
```
## Usage

1. Place the input files in the input/ folder:
   - impulse_test_input.xml - UML model of base station
   - config.json - configuration parameters

2. Start generation:
```bash
python main.py
```
3. The results will be saved in the out/ folder:
   - Configuration files (JSON/XML)
   - YANG models
   - Proto-files
   - Generation metadata

## Implementation Features
### ✅ Supported Generation Formats:
   - YANG-Models for NETCONF
   - Protocol Buffers for gRPC
   - JSON/XML configuration
   - C++ headers files
### ✅ Validation Checks:
   - UML Model Correctness
   - Attribute Type Check
   - Validation of Relationships between Classes
   - Name Uniqueness Check
### ✅ Architectural Solutions:
   - Object-Oriented Approach
   - "Strategy" Pattern for Generators
   - Separation into Modules (Parsers/Generators/Validators)
   - Automatic Output Directory Creation
   
