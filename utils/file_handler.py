"""File handling for CSV and Excel uploads."""
import pandas as pd
from typing import Tuple, List, Optional
import io

class FileHandler:
    """Handles file uploads and processing."""
    
    def load_and_validate(self, uploaded_file) -> Tuple[Optional[pd.DataFrame], List[str]]:
        """Load and validate uploaded file."""
        issues = []
        
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                return None, ["Invalid file type"]
            
            # Check for issues
            if df.shape[0] == 0:
                issues.append("File is empty")
            
            if df.shape[1] == 0:
                issues.append("File has no columns")
            
            # Check missing data
            missing_pct = df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100
            if missing_pct > 50:
                issues.append(f"High missing data: {missing_pct:.1f}%")
            
            return df, issues
        
        except Exception as e:
            return None, [f"Error reading file: {str(e)}"]
