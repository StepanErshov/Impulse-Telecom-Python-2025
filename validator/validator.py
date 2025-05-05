class DataValidator:
    @staticmethod
    def validate(data: dict) -> bool:
        required_fields = ["config", "devices"]
        return all(field in data for field in required_fields)
    

from typing import Dict, List
from models.uml_model import UMLClass, Aggregation

def validate_uml_model(uml_model: Dict) -> bool:
    """Проверяет корректность UML-модели перед генерацией"""
    if not _validate_structure(uml_model):
        return False
    
    classes = uml_model["classes"]
    aggregations = uml_model["aggregations"]
    
    if not _validate_root_class(classes):
        return False
    
    if not _validate_unique_class_names(classes):
        return False
    
    if not _validate_class_attributes(classes):
        return False

    if not _validate_aggregations(aggregations, classes):
        return False
    
    return True

def _validate_structure(model: Dict) -> bool:
    """Проверяет базовую структуру модели"""
    required_keys = {"classes", "aggregations"}
    return all(key in model for key in required_keys)

def _validate_root_class(classes: List[UMLClass]) -> bool:
    """Проверяет наличие ровно одного корневого класса"""
    root_classes = [cls for cls in classes if cls.is_root]
    
    if len(root_classes) == 0:
        print("Ошибка: В модели отсутствует корневой класс (isRoot=true)")
        return False
    
    if len(root_classes) > 1:
        print("Ошибка: В модели больше одного корневого класса")
        return False
    
    return True

def _validate_unique_class_names(classes: List[UMLClass]) -> bool:
    """Проверяет уникальность имен классов"""
    names = [cls.name for cls in classes]
    
    if len(names) != len(set(names)):
        duplicates = {name for name in names if names.count(name) > 1}
        print(f"Ошибка: Найдены дубликаты классов: {', '.join(duplicates)}")
        return False
    
    return True

def _validate_class_attributes(classes: List[UMLClass]) -> bool:
    """Проверяет атрибуты всех классов"""
    valid_types = {"uint32", "string", "boolean", "int", "float", "double"}
    
    for cls in classes:
        attr_names = [attr["name"] for attr in cls.attributes]
        if len(attr_names) != len(set(attr_names)):
            duplicates = {n for n in attr_names if attr_names.count(n) > 1}
            print(f"Ошибка: В классе '{cls.name}' дубликаты атрибутов: {', '.join(duplicates)}")
            return False
        
        for attr in cls.attributes:
            if attr["type"].lower() not in valid_types:
                print(f"Ошибка: В классе '{cls.name}' недопустимый тип атрибута '{attr['name']}': {attr['type']}")
                return False
    
    return True

def _validate_aggregations(aggregations: List[Aggregation], classes: List[UMLClass]) -> bool:
    """Проверяет корректность отношений агрегации"""
    class_names = {cls.name for cls in classes}
    
    for agg in aggregations:
        if agg.source not in class_names:
            print(f"Ошибка: Агрегация ссылается на несуществующий класс '{agg.source}'")
            return False
            
        if agg.target not in class_names:
            print(f"Ошибка: Агрегация ссылается на несуществующий класс '{agg.target}'")
            return False

        if not _validate_multiplicity(agg.source_multiplicity):
            print(f"Ошибка: Некорректный формат sourceMultiplicity '{agg.source_multiplicity}' в агрегации {agg.source}->{agg.target}")
            return False
            
        if not _validate_multiplicity(agg.target_multiplicity):
            print(f"Ошибка: Некорректный формат targetMultiplicity '{agg.target_multiplicity}' в агрегации {agg.source}->{agg.target}")
            return False
    
    return True

def _validate_multiplicity(multiplicity: str) -> bool:
    """Проверяет корректность формата multiplicity"""
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