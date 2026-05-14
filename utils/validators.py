"""Input validation for Omni Executor."""
from typing import Dict, List

class InputValidator:
    """Validates user inputs."""
    
    def validate_input(self, problem: str, category: str, scale: str) -> Dict:
        """Validate required inputs."""
        errors = []
        
        if not problem or len(problem.strip()) < 10:
            errors.append("Problem description must be at least 10 characters")
        
        if not category or category.strip() == "":
            errors.append("Business category is required")
        
        if not scale or scale.strip() == "":
            errors.append("Business scale is required")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def validate_file(self, filename: str) -> Dict:
        """Validate uploaded file."""
        valid_extensions = ['.csv', '.xlsx']
        
        for ext in valid_extensions:
            if filename.lower().endswith(ext):
                return {"valid": True, "error": None}
        
        return {
            "valid": False,
            "error": f"File must be CSV or XLSX. Got: {filename}"
        }
