from typing import Dict, List
from models.uml_model import UMLClass, Aggregation


class ModelValidator:
    """Class for validating UML model structure and consistency."""

    @staticmethod
    def validate_uml_model(uml_model: Dict) -> bool:
        """Validate UML model structure and content.

        Args:
            uml_model: Dictionary containing UML model data

        Returns:
            bool: True if model is valid, False otherwise
        """
        if not ModelValidator._validate_structure(uml_model):
            return False

        classes = uml_model["classes"]
        aggregations = uml_model["aggregations"]

        checks = [
            ModelValidator._validate_root_class(classes),
            ModelValidator._validate_unique_class_names(classes),
            ModelValidator._validate_class_attributes(classes),
            ModelValidator._validate_aggregations(aggregations, classes)
        ]

        return all(checks)

    @staticmethod
    def _validate_structure(model: Dict) -> bool:
        """Validate basic model structure."""
        required_keys = {"classes", "aggregations"}
        return all(key in model for key in required_keys)

    @staticmethod
    def _validate_root_class(classes: List[UMLClass]) -> bool:
        """Validate root class existence and uniqueness."""
        root_classes = [cls for cls in classes if cls.is_root]
        return len(root_classes) == 1

    @staticmethod
    def _validate_unique_class_names(classes: List[UMLClass]) -> bool:
        """Validate class name uniqueness."""
        names = [cls.name for cls in classes]
        return len(names) == len(set(names))

    @staticmethod
    def _validate_class_attributes(classes: List[UMLClass]) -> bool:
        """Validate class attributes."""
        valid_types = {"uint32", "string", "boolean", "int", "float", "double"}
        for cls in classes:
            attr_names = [attr["name"] for attr in cls.attributes]
            if len(attr_names) != len(set(attr_names)):
                return False
            for attr in cls.attributes:
                if attr["type"].lower() not in valid_types:
                    return False
        return True

    @staticmethod
    def _validate_aggregations(aggregations: List[Aggregation],
                             classes: List[UMLClass]) -> bool:
        """Validate aggregation relationships."""
        class_names = {cls.name for cls in classes}
        for agg in aggregations:
            if (agg.source not in class_names or 
                agg.target not in class_names or
                not ModelValidator._validate_multiplicity(agg.source_multiplicity) or
                not ModelValidator._validate_multiplicity(agg.target_multiplicity)):
                return False
        return True

    @staticmethod
    def _validate_multiplicity(multiplicity: str) -> bool:
        """Validate multiplicity format."""
        if multiplicity == "*":
            return True
        if ".." in multiplicity:
            parts = multiplicity.split("..")
            if len(parts) != 2:
                return False
            try:
                lower = int(parts[0]) if parts[0] else 0
                upper = int(parts[1]) if parts[1] else float('inf')
                return lower <= upper
            except ValueError:
                return False
        try:
            int(multiplicity)
            return True
        except ValueError:
            return False
    




class DataValidator:
    @staticmethod
    def validate(data: dict) -> bool:
        required_fields = ["config", "devices"]
        return all(field in data for field in required_fields)