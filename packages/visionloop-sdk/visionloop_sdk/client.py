from typing import Optional

# Import sub-modules
from visionloop_finance import (
    IndianTaxEngine, 
    SinkingFundCalculator, 
    MSMEInterestCalculator, 
    UPIGenerator, 
    StandaloneZohoBooksClient
)
from visionloop_telematics import (
    BatterySLAEngine, 
    GeofenceEngine, 
    MaintenanceScheduler, 
    ImmobilizerSafetyProtocol, 
    StreamParser
)
from visionloop_legal import (
    KYCValidator, 
    LeaseAgreementSynthesizer, 
    StatutoryComplianceAuditor
)
from visionloop_comms import (
    CollectionReminderEngine, 
    WhatsAppDispatcher
)

class FinanceNamespace:
    tax = IndianTaxEngine
    sinking_fund = SinkingFundCalculator
    msme = MSMEInterestCalculator
    upi = UPIGenerator
    zoho = StandaloneZohoBooksClient

class TelematicsNamespace:
    battery = BatterySLAEngine
    geofence = GeofenceEngine
    maintenance = MaintenanceScheduler
    immobilizer = ImmobilizerSafetyProtocol
    parser = StreamParser

class LegalNamespace:
    kyc = KYCValidator
    agreements = LeaseAgreementSynthesizer
    compliance = StatutoryComplianceAuditor

class CommsNamespace:
    reminders = CollectionReminderEngine
    whatsapp = WhatsAppDispatcher

class VisionLoopSDK:
    """
    VisionLoop Master SDK
    Unified gateway accessing Finance, Telematics, Legal, and Communications automation engines.
    """
    def __init__(self, whatsapp_phone_id: str = "", whatsapp_token: str = ""):
        self.finance = FinanceNamespace()
        self.telematics = TelematicsNamespace()
        self.legal = LegalNamespace()
        self.comms = CommsNamespace()
        self.whatsapp = WhatsAppDispatcher(whatsapp_phone_id, whatsapp_token)
