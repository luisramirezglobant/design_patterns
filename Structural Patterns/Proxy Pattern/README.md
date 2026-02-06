# Proxy Pattern

**_Proxy Pattern is a structural design pattern that provides a placeholder or surrogate for another object to control access to it. A proxy acts as an intermediary between the client and the real object, allowing you to add additional functionality or control without changing the real object's code._**

## Description
The intent of the Proxy pattern is to provide a surrogate or placeholder for another object to control access to it. This pattern is useful when you need to add functionality such as lazy initialization, access control, logging, or caching without modifying the original object. The proxy maintains a reference to the real object and forwards requests to it, but can also perform additional operations before or after forwarding.

![Proxy Pattern UML](proxy_pattern_uml.png "Proxy Pattern Diagram")

## Key Characteristics
- **Same Interface:** The Proxy implements the same interface as the real object, making it interchangeable from the client's perspective.
- **Controlled Access:** The Proxy controls access to the real object, allowing you to add functionality like lazy loading, access control, or caching.
- **Transparent Operation:** Clients interact with the Proxy as if it were the real object, without knowing about the proxy's existence.
- **Delegation:** The Proxy forwards requests to the real object when appropriate, but can also handle requests independently.

### Subject (Interface)
Defines the common interface for both the **Real Subject** and the **Proxy**. This ensures that the Proxy can be used anywhere the Real Subject is expected. The client code works with this interface, making it unaware of whether it's dealing with a proxy or the real object.

In code, this is typically an abstract class or interface that declares the operations that both the Proxy and Real Subject must implement.

### Real Subject
The actual object that performs the real work. This is the object that the Proxy represents and controls access to. The Real Subject contains the core business logic and is what the client ultimately needs to interact with.

The Real Subject is typically expensive to create, requires access control, or needs additional functionality like logging or caching.

### Proxy
Maintains a reference to the Real Subject and implements the same interface. The Proxy controls access to the Real Subject and can perform additional operations such as:

- **Lazy Initialization:** Creating the Real Subject only when it's actually needed
- **Access Control:** Checking permissions before allowing access to the Real Subject
- **Caching:** Storing results to avoid repeated expensive operations
- **Logging:** Recording access or operations for monitoring purposes
- **Remote Access:** Handling network communication for remote objects

The Proxy forwards requests to the Real Subject when appropriate, but can also handle requests independently without involving the Real Subject.

## Types of Proxies

### Virtual Proxy
Creates expensive objects on demand. Useful for lazy loading scenarios where creating the object is costly (e.g., loading large images, database connections, or complex computations).

### Protection Proxy
Controls access to the Real Subject based on permissions or security rules. Acts as a gatekeeper that validates access rights before allowing operations.

### Remote Proxy
Represents an object that exists in a different address space (e.g., on a remote server). Handles the communication details and makes remote objects appear as if they were local.

### Smart Reference
Adds additional functionality when accessing the Real Subject, such as reference counting, locking, or logging access patterns.

## Practical Indicators
Look for these patterns in your code:

- Need to control access to an object without changing its interface
- Expensive object creation that should be deferred until needed
- Access control or security checks required before object access
- Need to add cross-cutting concerns like logging, caching, or monitoring
- Remote object access that needs to appear local
- Objects that require lazy initialization or resource management

## Conditions to use Proxy Pattern

- Need to control access to an object without modifying its code
- Want to add functionality like lazy loading, caching, or access control
- Require a placeholder for an expensive-to-create object
- Need to add cross-cutting concerns (logging, monitoring) transparently
- Want to provide a local representation of a remote object

## Steps to implement the Proxy

1. Identify the interface that both the Real Subject and Proxy will implement
2. Create the Real Subject class that implements the interface
3. Create the Proxy class that also implements the interface and maintains a reference to the Real Subject
4. Implement the control logic in the Proxy (lazy loading, access control, caching, etc.)
5. Forward requests from the Proxy to the Real Subject when appropriate

## Best Practices

- Ensure the Proxy implements the same interface as the Real Subject to maintain substitutability
- Use lazy initialization only when the object creation is truly expensive
- Keep the Proxy focused on a single responsibility (e.g., caching OR access control, not both)
- Consider using the Proxy pattern when you need to add functionality without modifying existing code (Open/Closed Principle)
- Be mindful of the performance overhead introduced by the Proxy layer
- Use Dependency Injection to provide the Real Subject to the Proxy for better testability

## Summarizing

The Proxy Pattern is particularly useful when you need to add a layer of indirection between clients and objects. It's commonly used for lazy loading of expensive resources, implementing access control, adding caching mechanisms, or providing remote access to objects. The pattern allows you to enhance functionality without modifying the original object, following the Open/Closed Principle.

This pattern comes with the benefit of separation of concerns, but adds complexity by introducing an additional layer. The Proxy must maintain consistency with the Real Subject's interface and behavior to ensure transparency to clients.
