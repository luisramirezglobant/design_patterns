# Facade Pattern

**_Facade Method is a structural design pattern that provides a unified interface to a set of interfaces in a subsystem. Facade  defines a higer level interface that makes the subsystem easier to use._**

## Description
The intent of the Facade pattern is to provide a simplified interface to a complex system of classes, libraries, or frameworks. It promotes loose coupling between clients and the subsystem by abstracting away the details of subsystem components behind a single interface.
![Facade UML](Facade_pattern_UML.png "Facade Pattern Diagram")

## Key Characteristics
- **One-to-Many Relationship:** A Facade typically interacts with multiple subsystem class, coordinating their behavior to fulfill clients requests.
- **Simplified, Not Limited:** Even when the Facade provides a simplified way to interact with subsystems, that doesn't mean that for advanced uses the interaction with subsystem itself is restricted. Other kind of operations or complexier scenarios should be handled as well.
- **Decoupling Layer:** It creates a buffer (intermediary) between client code and subsystem implementation, making the system more maintainable and allowing subsystem internals to evolve without affecting clients. Changes in subsystems does not affect any other existant logic other than the Facade internals.

### Practical Indicators
Look for these patterns in your code:

Client code that instantiates multiple related objects together
Methods that always call the same sequence of operations across different classes
Repeated initialization or configuration logic scattered throughout the codebase
Comments explaining "how to use" multiple classes together
High coupling between application layers

### Facade Rules
- Prefer Object Composition by using Dependency Injection over Internl Instantiation.
- By the Single Responsability Principle, create each Facade per one cohesive area of functionality
- Objects that has been passed as parameter their methods can be called.
- Invoke methods that you've create yourself. So all the objects methods created inside an allowed method, can be invoked as well.
- The subsystems components should by __private__ to the Facade. This reforces that the Facade is the intended interface.
