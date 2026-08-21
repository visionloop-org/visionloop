"""
VisionLoop Legal Module
Reusable Indian LegalTech, Contract Synthesis & KYC Verification Engine
"""

from .kyc_validator import KYCValidator
from .agreement_generator import LeaseAgreementSynthesizer
from .compliance_auditor import StatutoryComplianceAuditor

__all__ = [
    "KYCValidator",
    "LeaseAgreementSynthesizer",
    "StatutoryComplianceAuditor"
]
