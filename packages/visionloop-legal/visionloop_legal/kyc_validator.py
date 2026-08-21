import re
from typing import Tuple

INDIAN_STATE_CODES = {
    "01": "Jammu & Kashmir", "02": "Himachal Pradesh", "03": "Punjab", "04": "Chandigarh",
    "06": "Haryana", "07": "Delhi", "08": "Rajasthan", "09": "Uttar Pradesh",
    "19": "West Bengal", "27": "Maharashtra", "29": "Karnataka", "33": "Tamil Nadu", "36": "Telangana"
}

PAN_ENTITY_TYPES = {
    'C': 'Company', 'P': 'Individual / Proprietor', 'H': 'HUF', 'F': 'Partnership / LLP',
    'A': 'Association of Persons', 'T': 'Trust', 'G': 'Government Agency'
}

class KYCValidator:
    """Validates Indian identity documents and tax numbers (PAN, GSTIN, Aadhaar hash)."""
    
    @staticmethod
    def validate_pan(pan: str) -> Tuple[bool, str]:
        """
        Validates 10-character alphanumeric PAN format: [A-Z]{5}[0-9]{4}[A-Z]
        Returns: (is_valid: bool, entity_type: str)
        """
        pan_clean = pan.strip().upper()
        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", pan_clean):
            return False, "Invalid PAN structure"
            
        entity_code = pan_clean[3]
        entity_type = PAN_ENTITY_TYPES.get(entity_code, "Unknown Entity")
        return True, entity_type

    @staticmethod
    def validate_gstin(gstin: str) -> Tuple[bool, str]:
        """
        Validates 15-character GSTIN format: 2-digit state code + 10-digit PAN + 1 entity digit + 'Z' + 1 checksum char.
        Returns: (is_valid: bool, state_name: str)
        """
        gstin_clean = gstin.strip().upper()
        pattern = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
        if not re.match(pattern, gstin_clean):
            return False, "Invalid GSTIN format"
            
        state_code = gstin_clean[:2]
        state_name = INDIAN_STATE_CODES.get(state_code, f"State Code {state_code}")
        return True, state_name
