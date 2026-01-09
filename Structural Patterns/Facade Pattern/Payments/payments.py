"""
Real-World Software Example: Payment Processing System with Facade Pattern

Problem: Processing payments involves coordinating multiple complex subsystems:
- Payment gateway (Stripe, PayPal, etc.)
- Database transactions
- Fraud detection service
- Email notifications
- Logging and monitoring
- Inventory management

Without a Facade, every part of your application that handles payments needs to 
know how to orchestrate all these systems correctly, leading to duplicated code,
inconsistent error handling, and maintenance nightmares.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
import uuid


# ============================================================================
# DATA MODELS
# ============================================================================

class PaymentStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"
    FRAUD_SUSPECTED = "fraud_suspected"
    FAILED = "failed"


@dataclass
class PaymentRequest:
    order_id: str
    customer_id: str
    amount: float
    currency: str
    card_token: str
    customer_email: str
    items: list


@dataclass
class PaymentResult:
    transaction_id: str
    status: PaymentStatus
    amount: float
    timestamp: datetime
    gateway_response: Optional[Dict[str, Any]] = None
    fraud_score: Optional[float] = None
    error_message: Optional[str] = None
    
    def is_successful(self) -> bool:
        return self.status == PaymentStatus.APPROVED


# ============================================================================
# SUBSYSTEM 1: Payment Gateway (e.g., Stripe API)
# ============================================================================

class PaymentGateway:
    """
    External payment processor API wrapper.
    In reality, this would be the Stripe SDK or similar.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        print(f"[Payment Gateway] Initialized with API key: {api_key[:10]}...")
    
    def charge(self, amount: float, currency: str, card_token: str, 
               metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calls the payment gateway API to process the charge.
        Returns gateway-specific response format.
        """
        print(f"[Payment Gateway] Processing charge: {amount} {currency}")
        print(f"[Payment Gateway] Card token: {card_token}")
        print(f"[Payment Gateway] Metadata: {metadata}")
        
        # Simulate API call
        transaction_id = f"txn_{uuid.uuid4().hex[:16]}"
        
        # Simulate occasional failures
        if amount > 10000:
            return {
                "success": False,
                "transaction_id": None,
                "error_code": "card_declined",
                "error_message": "Transaction amount exceeds limit"
            }
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "succeeded",
            "amount_captured": amount,
            "currency": currency
        }
    
    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Process a refund"""
        print(f"[Payment Gateway] Processing refund: {amount} for {transaction_id}")
        return {
            "success": True,
            "refund_id": f"ref_{uuid.uuid4().hex[:16]}"
        }


# ============================================================================
# SUBSYSTEM 2: Database Transaction Manager
# ============================================================================

class DatabaseTransaction:
    """
    Manages database operations within a transaction.
    Simulates SQLAlchemy or similar ORM behavior.
    """
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.in_transaction = False
        print(f"[Database] Connected to: {connection_string}")
    
    def begin(self):
        """Start a database transaction"""
        self.in_transaction = True
        print("[Database] Transaction BEGIN")
    
    def commit(self):
        """Commit the transaction"""
        if not self.in_transaction:
            raise Exception("No active transaction")
        print("[Database] Transaction COMMIT")
        self.in_transaction = False
    
    def rollback(self):
        """Rollback the transaction"""
        if not self.in_transaction:
            raise Exception("No active transaction")
        print("[Database] Transaction ROLLBACK")
        self.in_transaction = False
    
    def save_payment_record(self, payment_data: Dict[str, Any]):
        """Save payment record to database"""
        print(f"[Database] Saving payment record: {payment_data['transaction_id']}")
    
    def update_order_status(self, order_id: str, status: str):
        """Update order status"""
        print(f"[Database] Updating order {order_id} status to: {status}")
    
    def reserve_inventory(self, items: list):
        """Reserve inventory for ordered items"""
        print(f"[Database] Reserving inventory for {len(items)} items")
    
    def release_inventory(self, items: list):
        """Release inventory reservation"""
        print(f"[Database] Releasing inventory for {len(items)} items")


# ============================================================================
# SUBSYSTEM 3: Fraud Detection Service
# ============================================================================

class FraudDetectionService:
    """
    External fraud detection API (like Sift, Signifyd, etc.)
    Analyzes transactions for suspicious patterns.
    """
    
    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint
        print(f"[Fraud Detection] Connected to: {api_endpoint}")
    
    def analyze_transaction(self, payment_request: PaymentRequest) -> Dict[str, Any]:
        """
        Analyze transaction for fraud indicators.
        Returns risk score and recommendation.
        """
        print(f"[Fraud Detection] Analyzing transaction for customer: {payment_request.customer_id}")
        print(f"[Fraud Detection] Amount: {payment_request.amount} {payment_request.currency}")
        
        # Simulate fraud analysis
        risk_score = 0.15  # Low risk
        
        # High amount transactions get higher scrutiny
        if payment_request.amount > 5000:
            risk_score = 0.85
        
        return {
            "risk_score": risk_score,
            "recommendation": "approve" if risk_score < 0.5 else "review",
            "factors": ["amount_check", "velocity_check", "device_fingerprint"]
        }


# ============================================================================
# SUBSYSTEM 4: Email Notification Service
# ============================================================================

class EmailService:
    """
    Email service (like SendGrid, Amazon SES, etc.)
    Sends transactional emails to customers.
    """
    
    def __init__(self, smtp_config: Dict[str, str]):
        self.smtp_config = smtp_config
        print(f"[Email Service] Initialized with SMTP: {smtp_config['host']}")
    
    def send_payment_confirmation(self, email: str, transaction_id: str, amount: float):
        """Send payment confirmation email"""
        print(f"[Email Service] Sending confirmation to: {email}")
        print(f"[Email Service] Transaction: {transaction_id}, Amount: ${amount:.2f}")
    
    def send_payment_failure_notification(self, email: str, reason: str):
        """Send payment failure notification"""
        print(f"[Email Service] Sending failure notification to: {email}")
        print(f"[Email Service] Reason: {reason}")


# ============================================================================
# SUBSYSTEM 5: Logging and Monitoring
# ============================================================================

class LoggingService:
    """
    Centralized logging (like DataDog, Splunk, ELK stack)
    """
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        print(f"[Logging] Service initialized: {service_name}")
    
    def log_payment_attempt(self, payment_request: PaymentRequest):
        """Log payment attempt"""
        print(f"[Logging] PAYMENT_ATTEMPT - Order: {payment_request.order_id}, "
              f"Amount: {payment_request.amount}")
    
    def log_payment_success(self, transaction_id: str, amount: float):
        """Log successful payment"""
        print(f"[Logging] PAYMENT_SUCCESS - Transaction: {transaction_id}, "
              f"Amount: ${amount:.2f}")
    
    def log_payment_failure(self, order_id: str, reason: str):
        """Log payment failure"""
        print(f"[Logging] PAYMENT_FAILURE - Order: {order_id}, Reason: {reason}")
    
    def log_fraud_alert(self, customer_id: str, risk_score: float):
        """Log fraud alert"""
        print(f"[Logging] FRAUD_ALERT - Customer: {customer_id}, "
              f"Risk Score: {risk_score:.2f}")


# ============================================================================
# FACADE: Payment Processing Facade
# ============================================================================

class PaymentProcessingFacade:
    """
    Facade that coordinates all subsystems for payment processing.
    
    This is what the rest of your application should use instead of 
    directly interacting with payment gateways, databases, etc.
    """
    
    def __init__(self, 
                 gateway: PaymentGateway,
                 database: DatabaseTransaction,
                 fraud_detection: FraudDetectionService,
                 email_service: EmailService,
                 logger: LoggingService):
        self.gateway = gateway
        self.database = database
        self.fraud_detection = fraud_detection
        self.email_service = email_service
        self.logger = logger
    
    def process_payment(self, payment_request: PaymentRequest) -> PaymentResult:
        """
        High-level method that orchestrates the entire payment flow.
        
        This single method handles:
        1. Fraud detection
        2. Database transaction management
        3. Payment gateway integration
        4. Inventory management
        5. Email notifications
        6. Logging and monitoring
        7. Error handling and rollback
        """
        print("\n" + "="*70)
        print(f"💳 PROCESSING PAYMENT FOR ORDER: {payment_request.order_id}")
        print("="*70 + "\n")
        
        # Log the attempt
        self.logger.log_payment_attempt(payment_request)
        
        # Step 1: Fraud Detection (do this BEFORE charging)
        fraud_analysis = self.fraud_detection.analyze_transaction(payment_request)
        
        if fraud_analysis['recommendation'] != 'approve':
            self.logger.log_fraud_alert(
                payment_request.customer_id, 
                fraud_analysis['risk_score']
            )
            
            return PaymentResult(
                transaction_id="",
                status=PaymentStatus.FRAUD_SUSPECTED,
                amount=payment_request.amount,
                timestamp=datetime.now(),
                fraud_score=fraud_analysis['risk_score'],
                error_message="Transaction flagged for review"
            )
        
        # Step 2: Start database transaction
        self.database.begin()
        
        try:
            # Step 3: Reserve inventory
            self.database.reserve_inventory(payment_request.items)
            
            # Step 4: Process payment through gateway
            gateway_response = self.gateway.charge(
                amount=payment_request.amount,
                currency=payment_request.currency,
                card_token=payment_request.card_token,
                metadata={
                    'order_id': payment_request.order_id,
                    'customer_id': payment_request.customer_id
                }
            )
            
            if not gateway_response['success']:
                # Payment failed - rollback everything
                raise PaymentProcessingException(
                    gateway_response.get('error_message', 'Payment declined')
                )
            
            # Step 5: Save payment record
            self.database.save_payment_record({
                'transaction_id': gateway_response['transaction_id'],
                'order_id': payment_request.order_id,
                'customer_id': payment_request.customer_id,
                'amount': payment_request.amount,
                'currency': payment_request.currency,
                'status': 'completed'
            })
            
            # Step 6: Update order status
            self.database.update_order_status(payment_request.order_id, 'paid')
            
            # Step 7: Commit database transaction
            self.database.commit()
            
            # Step 8: Send confirmation email (after commit)
            self.email_service.send_payment_confirmation(
                payment_request.customer_email,
                gateway_response['transaction_id'],
                payment_request.amount
            )
            
            # Step 9: Log success
            self.logger.log_payment_success(
                gateway_response['transaction_id'],
                payment_request.amount
            )
            
            print("\n✅ PAYMENT PROCESSING COMPLETED SUCCESSFULLY\n")
            
            return PaymentResult(
                transaction_id=gateway_response['transaction_id'],
                status=PaymentStatus.APPROVED,
                amount=payment_request.amount,
                timestamp=datetime.now(),
                gateway_response=gateway_response,
                fraud_score=fraud_analysis['risk_score']
            )
            
        except Exception as e:
            # Rollback database transaction
            self.database.rollback()
            
            # Release inventory
            self.database.release_inventory(payment_request.items)
            
            # Send failure notification
            self.email_service.send_payment_failure_notification(
                payment_request.customer_email,
                str(e)
            )
            
            # Log the failure
            self.logger.log_payment_failure(payment_request.order_id, str(e))
            
            print(f"\n❌ PAYMENT PROCESSING FAILED: {str(e)}\n")
            
            return PaymentResult(
                transaction_id="",
                status=PaymentStatus.FAILED,
                amount=payment_request.amount,
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    def refund_payment(self, transaction_id: str, amount: float, 
                       order_id: str, items: list) -> bool:
        """
        High-level method for processing refunds.
        Coordinates gateway refund, database updates, and notifications.
        """
        print("\n" + "="*70)
        print(f"💸 PROCESSING REFUND FOR TRANSACTION: {transaction_id}")
        print("="*70 + "\n")
        
        self.database.begin()
        
        try:
            # Process refund through gateway
            refund_response = self.gateway.refund(transaction_id, amount)
            
            if not refund_response['success']:
                raise PaymentProcessingException("Refund failed at gateway")
            
            # Update database
            self.database.update_order_status(order_id, 'refunded')
            self.database.release_inventory(items)
            
            self.database.commit()
            
            print("\n✅ REFUND COMPLETED SUCCESSFULLY\n")
            return True
            
        except Exception as e:
            self.database.rollback()
            print(f"\n❌ REFUND FAILED: {str(e)}\n")
            return False


class PaymentProcessingException(Exception):
    """Custom exception for payment processing errors"""
    pass


# ============================================================================
# DEMONSTRATION - Comparing with and without Facade
# ============================================================================

def demonstrate_without_facade():
    """
    Shows how complex and error-prone it is to handle payments
    without a Facade - client code needs to know everything.
    """
    print("\n" + "="*70)
    print("WITHOUT FACADE - Complex, error-prone client code")
    print("="*70 + "\n")
    
    # Initialize all subsystems
    gateway = PaymentGateway("sk_test_abc123")
    database = DatabaseTransaction("postgresql://localhost/payments")
    fraud_service = FraudDetectionService("https://fraud-api.example.com")
    email = EmailService({"host": "smtp.example.com", "port": "587"})
    logger = LoggingService("payment-service")
    
    # Client code has to orchestrate everything manually
    payment_request = PaymentRequest(
        order_id="ORD-12345",
        customer_id="CUST-789",
        amount=99.99,
        currency="USD",
        card_token="tok_visa_4242",
        customer_email="customer@example.com",
        items=[{"sku": "PROD-001", "quantity": 2}]
    )
    
    print("❌ Client must manually coordinate 9+ steps:")
    print("   1. Check fraud")
    print("   2. Start database transaction")
    print("   3. Reserve inventory")
    print("   4. Call payment gateway")
    print("   5. Save payment record")
    print("   6. Update order status")
    print("   7. Commit transaction")
    print("   8. Send email")
    print("   9. Log everything")
    print("   ... and handle rollback if anything fails!")
    print("\nThis logic gets duplicated across your codebase! 🔥\n")


def demonstrate_with_facade():
    """
    Shows how simple payment processing becomes with the Facade.
    """
    print("\n" + "="*70)
    print("WITH FACADE - Simple, maintainable client code")
    print("="*70 + "\n")
    
    # Initialize subsystems (usually done in dependency injection)
    gateway = PaymentGateway("sk_test_abc123")
    database = DatabaseTransaction("postgresql://localhost/payments")
    fraud_service = FraudDetectionService("https://fraud-api.example.com")
    email = EmailService({"host": "smtp.example.com", "port": "587"})
    logger = LoggingService("payment-service")
    
    # Create the facade
    payment_processor = PaymentProcessingFacade(
        gateway, database, fraud_service, email, logger
    )
    
    # SCENARIO 1: Normal successful payment
    print("SCENARIO 1: Normal Payment")
    print("-" * 70)
    payment_request = PaymentRequest(
        order_id="ORD-12345",
        customer_id="CUST-789",
        amount=99.99,
        currency="USD",
        card_token="tok_visa_4242",
        customer_email="customer@example.com",
        items=[{"sku": "PROD-001", "quantity": 2}]
    )
    
    # Client code is now dead simple!
    result = payment_processor.process_payment(payment_request)
    
    if result.is_successful():
        print(f"✅ Payment successful! Transaction ID: {result.transaction_id}")
    else:
        print(f"❌ Payment failed: {result.error_message}")
    
    # SCENARIO 2: High-value transaction (fraud detection)
    print("\n\nSCENARIO 2: High-Value Transaction (Triggers Fraud Review)")
    print("-" * 70)
    suspicious_payment = PaymentRequest(
        order_id="ORD-67890",
        customer_id="CUST-999",
        amount=8000.00,
        currency="USD",
        card_token="tok_visa_suspicious",
        customer_email="suspicious@example.com",
        items=[{"sku": "PROD-999", "quantity": 10}]
    )
    
    result = payment_processor.process_payment(suspicious_payment)
    
    if result.status == PaymentStatus.FRAUD_SUSPECTED:
        print(f"⚠️ Transaction flagged for review. Risk score: {result.fraud_score}")
    
    # SCENARIO 3: Payment exceeds limit
    print("\n\nSCENARIO 3: Payment Exceeds Card Limit")
    print("-" * 70)
    large_payment = PaymentRequest(
        order_id="ORD-99999",
        customer_id="CUST-555",
        amount=15000.00,
        currency="USD",
        card_token="tok_visa_limit",
        customer_email="bigspender@example.com",
        items=[{"sku": "PROD-LUXURY", "quantity": 1}]
    )
    
    result = payment_processor.process_payment(large_payment)
    
    if not result.is_successful():
        print(f"❌ Payment declined: {result.error_message}")
    
    print("\n" + "="*70)
    print("KEY BENEFITS:")
    print("="*70)
    print("""
    ✅ Client code is simple - just one method call
    ✅ All complexity hidden inside the Facade
    ✅ Consistent error handling and rollback logic
    ✅ Easy to test - mock the Facade, not 5 services
    ✅ Changes to subsystems don't affect client code
    ✅ Business logic centralized in one place
    """)


if __name__ == "__main__":
    demonstrate_without_facade()
    demonstrate_with_facade()