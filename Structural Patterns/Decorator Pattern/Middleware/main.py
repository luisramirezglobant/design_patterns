"""
Production-Grade HTTP Middleware System using Decorator Pattern

This demonstrates how modern web frameworks (Express, Django, Flask) implement
middleware chains using the Decorator pattern.

Key Learning Points:
1. Why Decorator over inheritance for middleware
2. Order dependency in decorator chains
3. Request/response transformation
4. Error handling in decorator chains
5. Performance monitoring and observability
6. Real production concerns (auth, rate limiting, caching)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import time
import hashlib
import json
from collections import defaultdict


# ============================================================================
# DATA MODELS - Request/Response abstractions
# ============================================================================

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class HTTPRequest:
    """
    Represents an HTTP request.
    
    In production, this would be similar to Flask's Request or 
    Django's HttpRequest. Decorators can modify headers, body, etc.
    """
    method: HTTPMethod
    path: str
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    query_params: Dict[str, str] = field(default_factory=dict)
    
    # Context for middleware to share data
    # Similar to Flask's g object or Express's req.locals
    context: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata added by middleware
    timestamp: datetime = field(default_factory=datetime.now)
    request_id: Optional[str] = None
    
    def get_header(self, name: str, default: str = None) -> Optional[str]:
        """Case-insensitive header lookup"""
        return self.headers.get(name.lower(), default)
    
    def set_header(self, name: str, value: str):
        """Set a header (case-insensitive storage)"""
        self.headers[name.lower()] = value


@dataclass
class HTTPResponse:
    """
    Represents an HTTP response.
    
    Decorators can modify status, headers, body.
    """
    status_code: int
    body: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    
    # Performance metadata
    execution_time_ms: Optional[float] = None
    
    def set_header(self, name: str, value: str):
        """Set a response header"""
        self.headers[name.lower()] = value
    
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300
    
    def is_error(self) -> bool:
        return self.status_code >= 400


class HTTPException(Exception):
    """Base exception for HTTP errors"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


# ============================================================================
# COMPONENT INTERFACE - The base abstraction
# ============================================================================

class HTTPHandler(ABC):
    """
    COMPONENT interface in Decorator pattern.
    
    This is the common interface that both concrete handlers and 
    decorators implement. This is CRITICAL for the pattern - without
    this shared interface, decorators couldn't wrap handlers transparently.
    
    Why abstract method instead of just a function?
    - Allows state management (caching, rate limiting need state)
    - Enables polymorphism (any handler can replace any other)
    - Makes testing easier (can mock the interface)
    """
    
    @abstractmethod
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        """
        Process an HTTP request and return a response.
        
        This is the core operation that gets decorated. Every decorator
        will implement this method and delegate to the wrapped handler.
        """
        pass


# ============================================================================
# CONCRETE COMPONENT - The actual business logic
# ============================================================================

class APIHandler(HTTPHandler):
    """
    CONCRETE COMPONENT - The actual endpoint handler.
    
    This represents your business logic - the actual API endpoint that
    does the real work. In a real framework, this would be your route
    handler or view function.
    
    Notice: This knows NOTHING about authentication, caching, logging, etc.
    It's pure business logic. That's the power of Decorator - these concerns
    are added externally without polluting this code.
    """
    
    def __init__(self, endpoint_name: str):
        self.endpoint_name = endpoint_name
        # Simulate a simple in-memory data store
        self.data_store = {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
            ],
            "products": [
                {"id": 1, "name": "Laptop", "price": 999.99},
                {"id": 2, "name": "Mouse", "price": 29.99},
            ]
        }
    
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        """
        Core business logic without any middleware concerns.
        
        In production, this might query a database, call other services,
        perform calculations, etc. Notice there's no logging, no auth checks,
        no caching - decorators handle all that.
        """
        print(f"\n[APIHandler] Processing {request.method.value} {request.path}")
        
        # Route to appropriate handler based on path
        if request.path.startswith("/users"):
            return self._handle_users(request)
        elif request.path.startswith("/products"):
            return self._handle_products(request)
        else:
            return HTTPResponse(
                status_code=404,
                body=json.dumps({"error": "Endpoint not found"})
            )
    
    def _handle_users(self, request: HTTPRequest) -> HTTPResponse:
        """Handle /users endpoint"""
        if request.method == HTTPMethod.GET:
            users = self.data_store["users"]
            return HTTPResponse(
                status_code=200,
                body=json.dumps({"users": users})
            )
        elif request.method == HTTPMethod.POST:
            # Simulate creating a user
            new_user = json.loads(request.body) if request.body else {}
            new_user["id"] = len(self.data_store["users"]) + 1
            self.data_store["users"].append(new_user)
            return HTTPResponse(
                status_code=201,
                body=json.dumps({"user": new_user})
            )
        else:
            return HTTPResponse(
                status_code=405,
                body=json.dumps({"error": "Method not allowed"})
            )
    
    def _handle_products(self, request: HTTPRequest) -> HTTPResponse:
        """Handle /products endpoint"""
        if request.method == HTTPMethod.GET:
            products = self.data_store["products"]
            return HTTPResponse(
                status_code=200,
                body=json.dumps({"products": products})
            )
        else:
            return HTTPResponse(
                status_code=405,
                body=json.dumps({"error": "Method not allowed"})
            )


# ============================================================================
# BASE DECORATOR - Abstract decorator with common functionality
# ============================================================================

class MiddlewareDecorator(HTTPHandler):
    """
    BASE DECORATOR - Abstract base class for all middleware.
    
    This is a common pattern in Decorator implementations: create an abstract
    decorator that handles the delegation boilerplate, then concrete decorators
    just override the parts they care about.
    
    Key insight: This IS-A HTTPHandler (inheritance for interface conformance)
    AND HAS-A HTTPHandler (composition for delegation). This dual relationship
    is the essence of the Decorator pattern.
    """
    
    def __init__(self, handler: HTTPHandler):
        """
        Constructor receives the handler to wrap.
        
        This is the COMPOSITION part of the pattern. The decorator
        wraps another handler (which might itself be a decorator).
        """
        self._handler = handler
        self.name = self.__class__.__name__
    
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        """
        Default implementation just delegates.
        
        Concrete decorators can:
        1. Override this completely (rare)
        2. Call _before_handle() and _after_handle() (common pattern)
        3. Wrap the delegation in try/except for error handling
        """
        return self._handler.handle(request)
    
    # Template methods that concrete decorators can override
    def _before_handle(self, request: HTTPRequest):
        """Hook called before delegating to wrapped handler"""
        pass
    
    def _after_handle(self, request: HTTPRequest, response: HTTPResponse):
        """Hook called after wrapped handler returns"""
        pass


# ============================================================================
# CONCRETE DECORATORS - Each adds one specific responsibility
# ============================================================================

class LoggingMiddleware(MiddlewareDecorator):
    """
    CONCRETE DECORATOR: Request/Response logging.
    
    This is a classic middleware concern - you want to log all requests
    without modifying every endpoint handler.
    
    Notice: This decorator doesn't know or care what handler it's wrapping.
    It could be wrapping the APIHandler directly, or wrapping another
    decorator. This is transparency in action.
    """
    
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        """
        Logs request details, delegates to handler, logs response details.
        
        Pattern: Before → Delegate → After
        This is the most common decorator pattern.
        """
        # BEFORE: Log incoming request
        print(f"\n{'='*70}")
        print("[LoggingMiddleware] Incoming Request")
        print(f"  Request ID: {request.request_id}")
        print(f"  Method: {request.method.value}")
        print(f"  Path: {request.path}")
        print(f"  Headers: {request.headers}")
        print(f"  Timestamp: {request.timestamp.isoformat()}")
        
        start_time = time.time()
        
        try:
            # DELEGATE: Call the wrapped handler
            response = self._handler.handle(request)
            
            # AFTER: Log response
            elapsed_ms = (time.time() - start_time) * 1000
            print("\n[LoggingMiddleware] Response")
            print(f"  Status: {response.status_code}")
            print(f"  Execution Time: {elapsed_ms:.2f}ms")
            print(f"{'='*70}")
            
            # Enhance response with timing info
            response.execution_time_ms = elapsed_ms
            
            return response
            
        except HTTPException as e:
            # Log errors too
            elapsed_ms = (time.time() - start_time) * 1000
            print("\n[LoggingMiddleware] Error Response")
            print(f"  Status: {e.status_code}")
            print(f"  Error: {e.message}")
            print(f"  Execution Time: {elapsed_ms:.2f}ms")
            print(f"{'='*70}")
            raise


class AuthenticationMiddleware(MiddlewareDecorator):
    """
    CONCRETE DECORATOR: JWT/Token authentication.
    
    Real-world concern: Verify the request is from an authenticated user
    BEFORE allowing it to reach the business logic.
    
    This demonstrates:
    1. Short-circuiting: If auth fails, don't call wrapped handler
    2. Request modification: Add user info to request.context
    3. Error handling: Return 401 without propagating to handler
    """
    
    def __init__(self, handler: HTTPHandler, valid_tokens: set = None):
        super().__init__(handler)
        # In production, this would validate JWTs, check DB, etc.
        self.valid_tokens = valid_tokens or {"secret-token-123", "admin-token-456"}
    
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        """
        Validate authentication BEFORE delegating.
        
        Pattern: Guard clause → Delegate
        If the guard fails, we return early without calling the handler.
        """
        print("\n[AuthenticationMiddleware] Checking authentication")
        
        # Extract token from Authorization header
        auth_header = request.get_header("authorization")
        
        if not auth_header:
            print("[AuthenticationMiddleware] ❌ No Authorization header")
            return HTTPResponse(
                status_code=401,
                body=json.dumps({"error": "Authentication required"})
            )
        
        # Validate token (simplified - in production, verify JWT signature, etc.)
        token = auth_header.replace("Bearer ", "")
        
        if token not in self.valid_tokens:
            print(f"[AuthenticationMiddleware] ❌ Invalid token: {token}")
            return HTTPResponse(
                status_code=401,
                body=json.dumps({"error": "Invalid authentication token"})
            )
        
        # Authentication successful - add user info to context
        # Other middleware/handlers can access this
        user_id = "user_123" if token == "secret-token-123" else "admin_456"
        request.context["user_id"] = user_id
        request.context["is_admin"] = token.startswith("admin")
        
        print(f"[AuthenticationMiddleware] ✅ Authenticated as {user_id}")
        
        # DELEGATE: Authentication passed, continue to next handler
        return self._handler.handle(request)


class RateLimitingMiddleware(MiddlewareDecorator):
    """
    CONCRETE DECORATOR: Rate limiting to prevent abuse.
    
    Real-world concern: Limit how many requests a user can make in a time window.
    
    This demonstrates:
    1. Stateful decorator (tracks request counts)
    2. Time-based logic
    3. Early return on rate limit exceeded
    
    In production, this would use Redis for distributed rate limiting.
    """
    
    def __init__(self, handler: HTTPHandler, max_requests: int = 10, 
                 window_seconds: int = 60):
        super().__init__(handler)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        
        # In-memory tracking (production would use Redis)
        # Structure: {user_id: [(timestamp, request_count)]}
        self.request_log = defaultdict(list)
    
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        """
        Check rate limit BEFORE delegating.
        
        Pattern: Stateful guard → Delegate
        """
        # Get user identifier (from auth middleware or IP)
        user_id = request.context.get("user_id", "anonymous")
        
        print(f"\n[RateLimitingMiddleware] Checking rate limit for {user_id}")
        
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds)
        
        # Clean old entries
        self.request_log[user_id] = [
            (ts, count) for ts, count in self.request_log[user_id]
            if ts > cutoff
        ]
        
        # Count recent requests
        recent_requests = sum(count for _, count in self.request_log[user_id])
        
        if recent_requests >= self.max_requests:
            print(f"[RateLimitingMiddleware] ❌ Rate limit exceeded: "
                  f"{recent_requests}/{self.max_requests} requests")
            
            return HTTPResponse(
                status_code=429,  # Too Many Requests
                body=json.dumps({
                    "error": "Rate limit exceeded",
                    "retry_after": self.window_seconds
                })
            )
        
        # Log this request
        self.request_log[user_id].append((now, 1))
        
        print(f"[RateLimitingMiddleware] ✅ Request allowed: "
              f"{recent_requests + 1}/{self.max_requests}")
        
        # DELEGATE: Rate limit not exceeded
        return self._handler.handle(request)


class CachingMiddleware(MiddlewareDecorator):
    """
    CONCRETE DECORATOR: Response caching for GET requests.
    
    Real-world concern: Cache expensive operations to reduce load and latency.
    
    This demonstrates:
    1. Conditional behavior (only cache GET requests)
    2. Response interception and storage
    3. Cache key generation
    4. Cache invalidation
    
    In production, use Redis, Memcached, or CDN caching.
    """
    
    def __init__(self, handler: HTTPHandler, ttl_seconds: int = 300):
        super().__init__(handler)
        self.ttl_seconds = ttl_seconds
        
        # In-memory cache: {cache_key: (response, expiry_time)}
        self.cache = {}
    
    def _generate_cache_key(self, request: HTTPRequest) -> str:
        """
        Generate a unique cache key for the request.
        
        In production, include: method, path, query params, relevant headers
        """
        key_components = f"{request.method.value}:{request.path}:{request.query_params}"
        return hashlib.md5(key_components.encode()).hexdigest()
    
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        """
        Check cache → Delegate if miss → Store result
        
        Pattern: Cache lookup → Conditional delegate → Cache store
        """
        # Only cache GET requests (safe, idempotent)
        if request.method != HTTPMethod.GET:
            print("\n[CachingMiddleware] Non-GET request, bypassing cache")
            return self._handler.handle(request)
        
        cache_key = self._generate_cache_key(request)
        now = datetime.now()
        
        # Check cache
        if cache_key in self.cache:
            cached_response, expiry = self.cache[cache_key]
            
            if now < expiry:
                print(f"\n[CachingMiddleware] ✅ Cache HIT for {cache_key}")
                print(f"  Serving cached response (expires in "
                      f"{(expiry - now).seconds}s)")
                
                # Return a copy to avoid mutation
                cached_response.set_header("x-cache", "HIT")
                return cached_response
            else:
                print(f"\n[CachingMiddleware] Cache EXPIRED for {cache_key}")
                del self.cache[cache_key]
        
        print(f"\n[CachingMiddleware] ❌ Cache MISS for {cache_key}")
        
        # DELEGATE: Cache miss, fetch from handler
        response = self._handler.handle(request)
        
        # Cache successful responses
        if response.is_success():
            expiry = now + timedelta(seconds=self.ttl_seconds)
            self.cache[cache_key] = (response, expiry)
            print(f"[CachingMiddleware] Cached response (TTL: {self.ttl_seconds}s)")
            response.set_header("x-cache", "MISS")
        
        return response


class CompressionMiddleware(MiddlewareDecorator):
    """
    CONCRETE DECORATOR: GZIP compression for responses.
    
    Real-world concern: Compress response bodies to reduce bandwidth.
    
    This demonstrates:
    1. Response modification (compress body)
    2. Header manipulation (add Content-Encoding)
    3. Conditional application (only if client accepts)
    """
    
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        """
        Delegate → Compress response if applicable
        
        Pattern: Delegate → Modify response
        """
        # Check if client accepts compression
        accept_encoding = request.get_header("accept-encoding", "")
        supports_gzip = "gzip" in accept_encoding.lower()
        
        # DELEGATE: Get response first
        response = self._handler.handle(request)
        
        # Only compress if client supports it and body is substantial
        if supports_gzip and len(response.body) > 100:
            print(f"\n[CompressionMiddleware] Compressing response "
                  f"({len(response.body)} bytes)")
            
            # Simulate compression (in production, use gzip.compress())
            original_size = len(response.body)
            compressed_size = int(original_size * 0.3)  # Simulated 70% compression
            
            response.set_header("content-encoding", "gzip")
            response.set_header("x-original-size", str(original_size))
            response.set_header("x-compressed-size", str(compressed_size))
            
            print(f"[CompressionMiddleware] ✅ Compressed: {original_size} → "
                  f"{compressed_size} bytes ({100 - compressed_size/original_size*100:.1f}% reduction)")
        else:
            print("\n[CompressionMiddleware] Skipping compression "
                  "(not supported or body too small)")
        
        return response


class MetricsMiddleware(MiddlewareDecorator):
    """
    CONCRETE DECORATOR: Collect performance metrics.
    
    Real-world concern: Monitor API performance, error rates, latency.
    
    This demonstrates:
    1. Timing measurement
    2. Success/error tracking
    3. Metrics aggregation
    
    In production, send to DataDog, Prometheus, CloudWatch, etc.
    """
    
    def __init__(self, handler: HTTPHandler):
        super().__init__(handler)
        
        # In-memory metrics (production would send to monitoring system)
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_latency_ms": 0,
            "status_codes": defaultdict(int),
            "endpoint_stats": defaultdict(lambda: {"count": 0, "avg_latency_ms": 0})
        }
    
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        """
        Time execution → Delegate → Record metrics
        
        Pattern: Setup → Delegate → Measure → Record
        """
        start_time = time.time()
        
        try:
            # DELEGATE
            response = self._handler.handle(request)
            
            # Calculate metrics
            latency_ms = (time.time() - start_time) * 1000
            
            # Update metrics
            self.metrics["total_requests"] += 1
            self.metrics["total_latency_ms"] += latency_ms
            self.metrics["status_codes"][response.status_code] += 1
            
            if response.is_success():
                self.metrics["successful_requests"] += 1
            else:
                self.metrics["failed_requests"] += 1
            
            # Per-endpoint stats
            endpoint = f"{request.method.value} {request.path}"
            ep_stats = self.metrics["endpoint_stats"][endpoint]
            ep_stats["count"] += 1
            # Running average
            ep_stats["avg_latency_ms"] = (
                (ep_stats["avg_latency_ms"] * (ep_stats["count"] - 1) + latency_ms) 
                / ep_stats["count"]
            )
            
            print("\n[MetricsMiddleware] Recorded metrics:")
            print(f"  Latency: {latency_ms:.2f}ms")
            print(f"  Status: {response.status_code}")
            print(f"  Success Rate: "
                  f"{self.metrics['successful_requests']}/{self.metrics['total_requests']}")
            
            return response
            
        except HTTPException as e:
            latency_ms = (time.time() - start_time) * 1000
            self.metrics["total_requests"] += 1
            self.metrics["failed_requests"] += 1
            self.metrics["status_codes"][e.status_code] += 1
            self.metrics["total_latency_ms"] += latency_ms
            raise
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Return metrics summary (for monitoring dashboard)"""
        total = self.metrics["total_requests"]
        if total == 0:
            return {}
        
        return {
            "total_requests": total,
            "success_rate": f"{self.metrics['successful_requests']/total*100:.1f}%",
            "avg_latency_ms": f"{self.metrics['total_latency_ms']/total:.2f}",
            "status_codes": dict(self.metrics["status_codes"]),
            "endpoint_stats": dict(self.metrics["endpoint_stats"])
        }


class CORSMiddleware(MiddlewareDecorator):
    """
    CONCRETE DECORATOR: CORS (Cross-Origin Resource Sharing) headers.
    
    Real-world concern: Enable cross-origin requests from browsers.
    
    This demonstrates:
    1. Adding headers to responses
    2. Handling preflight OPTIONS requests
    """
    
    def __init__(self, handler: HTTPHandler, allowed_origins: list = None):
        super().__init__(handler)
        self.allowed_origins = allowed_origins or ["*"]
    
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        """
        Handle OPTIONS preflight → Delegate → Add CORS headers
        
        Pattern: Special case handling → Delegate → Modify response
        """
        # Handle preflight OPTIONS request
        if request.method == HTTPMethod.GET and request.path == "OPTIONS":
            print("\n[CORSMiddleware] Handling preflight OPTIONS request")
            response = HTTPResponse(status_code=204)  # No Content
        else:
            # DELEGATE for normal requests
            response = self._handler.handle(request)
        
        # Add CORS headers to all responses
        origin = request.get_header("origin", "*")
        
        if origin in self.allowed_origins or "*" in self.allowed_origins:
            response.set_header("access-control-allow-origin", origin)
            response.set_header("access-control-allow-methods", "GET, POST, PUT, DELETE")
            response.set_header("access-control-allow-headers", "Content-Type, Authorization")
            response.set_header("access-control-max-age", "3600")
            
            print(f"\n[CORSMiddleware] Added CORS headers for origin: {origin}")
        
        return response


# ============================================================================
# DEMONSTRATION - Show the power and flexibility of Decorator
# ============================================================================

def demonstrate_decorator_pattern():
    """
    Comprehensive demonstration of HTTP middleware using Decorator pattern.
    """
    
    print("\n" + "="*70)
    print("HTTP MIDDLEWARE SYSTEM - DECORATOR PATTERN DEMONSTRATION")
    print("="*70)
    
    # Create the base handler (core business logic)
    api_handler = APIHandler("UserAPI")
    
    print("\n" + "="*70)
    print("SCENARIO 1: Undecorated Handler (No Middleware)")
    print("="*70)
    print("Just the core business logic, no cross-cutting concerns")
    
    request1 = HTTPRequest(
        method=HTTPMethod.GET,
        path="/users",
        headers={"accept-encoding": "gzip"}
    )
    response1 = api_handler.handle(request1)
    print(f"\nResult: {response1.status_code} - {response1.body[:100]}")
    
    print("\n" + "="*70)
    print("SCENARIO 2: Single Decorator (Just Logging)")
    print("="*70)
    print("Adding logging middleware to track requests")
    
    # Wrap with logging
    logged_handler = LoggingMiddleware(api_handler)
    
    request2 = HTTPRequest(
        method=HTTPMethod.GET,
        path="/products",
        headers={"accept-encoding": "gzip"},
        request_id="req-001"
    )
    # Printed response by the loggingMiddleware
    logged_handler.handle(request2)
    
    print("\n" + "="*70)
    print("SCENARIO 3: Stacked Decorators (Full Middleware Chain)")
    print("="*70)
    print("Building a production-ready middleware stack")
    print("Order matters! Let's see why...")
    
    # Build the middleware chain - ORDER IS CRITICAL
    # Client Request Flow: 
    #   → Metrics (outermost, times everything)
    #   → Logging (logs the request)
    #   → CORS (adds CORS headers)
    #   → Authentication (checks auth)
    #   → Rate Limiting (prevents abuse)
    #   → Caching (returns cached if available)
    #   → Compression (compresses response)
    #   → API Handler (core business logic)
    
    full_handler = MetricsMiddleware(
        LoggingMiddleware(
            CORSMiddleware(
                AuthenticationMiddleware(
                    RateLimitingMiddleware(
                        CachingMiddleware(
                            CompressionMiddleware(
                                api_handler
                            ),
                            ttl_seconds=60
                        ),
                        max_requests=5,
                        window_seconds=60
                    ),
                    valid_tokens={"secret-token-123", "admin-token-456"}
                ),
                allowed_origins=["https://example.com", "*"]
            )
        )
    )
    
    # TEST 1: Successful authenticated request
    print("\n" + "-"*70)
    print("TEST 1: Authenticated GET request (should succeed and cache)")
    print("-"*70)
    
    request3 = HTTPRequest(
        method=HTTPMethod.GET,
        path="/users",
        headers={
            "authorization": "Bearer secret-token-123",
            "accept-encoding": "gzip",
            "origin": "https://example.com"
        },
        request_id="req-002"
    )
    response3 = full_handler.handle(request3)
    print(f"\n✅ Final Response: {response3.status_code}")
    print(f"   Headers: {response3.headers}")
    
    # TEST 2: Same request (should hit cache)
    print("\n" + "-"*70)
    print("TEST 2: Same request again (should return from cache)")
    print("-"*70)
    
    request4 = HTTPRequest(
        method=HTTPMethod.GET,
        path="/users",
        headers={
            "authorization": "Bearer secret-token-123",
            "accept-encoding": "gzip",
            "origin": "https://example.com"
        },
        request_id="req-003"
    )
    response4 = full_handler.handle(request4)
    print(f"\n✅ Cache Status: {response4.headers.get('x-cache', 'UNKNOWN')}")
    
    # TEST 3: Unauthenticated request (should fail at auth middleware)
    print("\n" + "-"*70)
    print("TEST 3: Unauthenticated request (should fail)")
    print("-"*70)
    
    request5 = HTTPRequest(
        method=HTTPMethod.GET,
        path="/users",
        headers={"accept-encoding": "gzip"},
        request_id="req-004"
    )
    response5 = full_handler.handle(request5)
    print(f"\n❌ Response: {response5.status_code} - {response5.body}")
    
    # TEST 4: Rate limiting (make multiple requests)
    print("\n" + "-"*70)
    print("TEST 4: Rate limiting (make 6 requests, limit is 5)")
    print("-"*70)
    
    for i in range(6):
        request_rl = HTTPRequest(
            method=HTTPMethod.GET,
            path="/products",
            headers={
                "authorization": "Bearer secret-token-123",
                "accept-encoding": "gzip"
            },
            request_id=f"req-rl-{i+1}"
        )
        response_rl = full_handler.handle(request_rl)
        
        if response_rl.status_code == 429:
            print(f"\n⚠️  Request {i+1}: RATE LIMITED (429)")
            break
        else:
            print(f"\n✅ Request {i+1}: Success ({response_rl.status_code})")
    
    # Show metrics
    print("\n" + "="*70)
    print("METRICS SUMMARY")
    print("="*70)
    
    metrics_summary = full_handler.get_metrics_summary()
    print(json.dumps(metrics_summary, indent=2))
    
    print("\n" + "="*70)
    print("KEY INSIGHTS DEMONSTRATED")
    print("="*70)
    print("""
    1. SINGLE RESPONSIBILITY
       - Each decorator has ONE job (auth, caching, logging, etc.)
       - Easy to test, maintain, and reason about
    
    2. ORDER MATTERS
       - Metrics wraps everything (measures total time)
       - Auth before rate limiting (auth is cheaper)
       - Caching before compression (cache compressed responses)
       - This order minimizes resource usage
    
    3. TRANSPARENCY
       - API handler knows nothing about middleware
       - Can add/remove middleware without changing handler
       - Same HTTPHandler interface throughout
    
    4. COMPOSITION OVER INHERITANCE
       - Could have 2^7 = 128 combinations with inheritance
       - With decorators: 7 classes, infinite combinations
    
    5. RUNTIME FLEXIBILITY
       - Can build different middleware stacks per endpoint
       - Can add/remove middleware dynamically
       - Each request can have custom middleware
    
    6. SHORT-CIRCUITING
       - Auth middleware can reject without calling handler
       - Cache can return without calling handler
       - Rate limiter can block without calling handler
       - This is efficient and clean
    
    7. CROSS-CUTTING CONCERNS
       - Logging, metrics, auth are separate from business logic
       - Business logic stays clean and focused
       - Middleware is reusable across all endpoints
    """)
    
    print("\n" + "="*70)
    print("WHY DECORATOR OVER OTHER PATTERNS?")
    print("="*70)
    print("""
    NOT STRATEGY:
    - Strategy swaps ONE algorithm (sort algorithm, pricing strategy)
    - Decorator STACKS multiple behaviors (logging + auth + caching)
    - Can't get the same effect with strategy
    
    NOT CHAIN OF RESPONSIBILITY:
    - Chain stops when one handler processes request
    - Decorator calls ALL decorators in sequence
    - Every decorator executes (unless short-circuit)
    
    NOT PROXY:
    - Proxy controls ACCESS (lazy loading, protection)
    - Decorator adds BEHAVIOR (logging, caching, compression)
    - Proxy is about when/if to delegate, decorator is about what to add
    
    DECORATOR IS UNIQUE:
    - Transparent wrapping (same interface)
    - Stackable behaviors
    - Order-dependent execution
    - Each layer adds value
    - Perfect for middleware pattern
    """)
    
    print("\n" + "="*70)
    print("PRODUCTION CONSIDERATIONS")
    print("="*70)
    print("""
    1. ERROR HANDLING
       - Each decorator should handle its own errors gracefully
       - Decide: propagate or return error response?
       - Example: Auth returns 401, doesn't propagate exception
    
    2. PERFORMANCE
       - Deep decorator chains have overhead (small but measurable)
       - Each decorator adds function call + logic
       - Profile and optimize hot paths
       - Consider: Do you need ALL decorators ALL the time?
    
    3. DEBUGGING
       - Stack traces can be deep with many decorators
       - Add request IDs for tracing through the chain
       - Good logging in each decorator helps
    
    4. CONFIGURATION
       - Use builder/factory pattern for common configurations
       - Don't make developers manually stack 10 decorators
       - Example: `create_authenticated_cached_handler()`
    
    5. TESTING
       - Test decorators independently with mock handlers
       - Test handler without decorators (pure business logic)
       - Test full stack for integration
       - Easy to mock any layer
    
    6. FRAMEWORKS
       - Express.js uses this exact pattern: app.use(middleware)
       - Django: MIDDLEWARE setting in settings.py
       - Flask: @app.before_request, @app.after_request
       - FastAPI: dependencies and middleware
       - Spring: @Around aspect (AOP, similar concept)
    """)


if __name__ == "__main__":
    demonstrate_decorator_pattern()