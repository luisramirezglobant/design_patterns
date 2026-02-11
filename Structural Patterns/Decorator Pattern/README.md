# Decorator Pattern

**_Decorator Pattern is a structural design pattern that attaches additional responsibilities to objects dynamically, providing a flexible alternative to extending class functionality. This is done at runtime without modifying the original class._**

## Description
The intent of the Decorator pattern is to allow behavior to be added to individual objects dynamically, without affecting the behavior of other objects from the same class. It is used to extend or modify the behavior of objects at runtime by wrapping them in decorator objects. This pattern promotes the Open/Closed Principle, which states that classes should be open for extension but closed for modification.

![Decorator Pattern UML](decorator_pattern.png "Decorator Pattern Diagram")

## Key Characteristics
- **Composition over Inheritance:** Uses object composition to add functionality instead of creating subclasses, avoiding class explosion.
- **Runtime Flexibility:** Decorators can be added or removed at runtime, providing dynamic behavior modification.
- **Transparent Wrapping:** Decorators implement the same interface as the component they wrap, making them interchangeable.
- **Stackable Behavior:** Multiple decorators can be stacked to combine different behaviors, creating flexible combinations.
- **Single Responsibility:** Each decorator adds one specific behavior, following the Single Responsibility Principle.

### Component (Interface)
Common interface for both the wrappers (decorators) and the wrapped object (concrete component). This interface defines the base operations that can be enhanced by decorators. The intended functionality defined here is supposed to be extended or modified by the decorators without changing the original implementation.

In code, this is typically an abstract class or interface that declares the operations that both the Concrete Component and all Decorators must implement.

### Concrete Component
The class that is going to be wrapped. It defines the base behavior which can be altered or extended by the decorators. This is the core object that provides the fundamental functionality, and decorators add additional features on top of it.

The Concrete Component implements the Component interface and represents the object to which additional responsibilities can be attached dynamically.

### Base Decorator
References a wrapped object (component object) and maintains a reference to it. Defines an interface that can contain both concrete components and other decorators. The base decorator implements the Component interface and delegates all operations to the wrapped object.

This class serves as the foundation for all concrete decorators, providing the basic structure for wrapping components and forwarding requests. It can optionally add behavior before or after forwarding the request to the wrapped object.

### Concrete Decorator
Defines the extra behavior that can be added to components dynamically. Concrete decorators override methods of the base decorator and execute their behavior either before or after calling the parent method (which forwards to the wrapped component).

Each concrete decorator adds a specific responsibility or feature. Multiple decorators can be stacked together, with each decorator wrapping the previous one, creating a chain of enhanced functionality.

## Practical Indicators
Look for these patterns in your code:

- Need to add features to objects dynamically without creating numerous subclasses
- Want to add responsibilities to objects at runtime that weren't anticipated at design time
- Need to combine multiple features in different ways without class explosion
- Want to add cross-cutting concerns (logging, validation, caching) to objects
- Require the ability to add or remove features from objects dynamically
- Need to extend functionality without modifying existing code (Open/Closed Principle)

## Conditions to use Decorator Pattern

- Need to add responsibilities to objects dynamically and transparently
- Want to extend functionality without creating subclasses for every possible combination
- Require the ability to add or remove features at runtime
- Need to combine multiple behaviors in flexible ways
- Want to add cross-cutting concerns without modifying core classes
- Need to follow the Open/Closed Principle by extending behavior without modification

## Steps to implement the Decorator

1. Define the Component interface that declares the operations that can be decorated
2. Create the Concrete Component class that implements the Component interface with base functionality
3. Create the Base Decorator class that implements the Component interface and maintains a reference to a Component
4. Create Concrete Decorator classes that extend the Base Decorator and add specific behaviors
5. Compose decorators by wrapping components with decorators, and stack multiple decorators as needed

## Best Practices

- Ensure decorators implement the same interface as the component they wrap for transparency
- Keep each decorator focused on a single responsibility (one decorator, one feature)
- Use composition to combine decorators rather than creating decorators that do multiple things
- Be mindful of the order of decorators when stacking them, as order can affect behavior
- Consider the performance overhead of multiple decorator layers
- Use Dependency Injection to provide components to decorators for better testability
- Document the intended use and stacking order of decorators when order matters

## Summarizing

The Decorator Pattern is particularly useful when you need to add functionality to objects dynamically without modifying their structure. It's commonly used for adding features like logging, caching, validation, encryption, or formatting to objects at runtime. The pattern allows you to combine behaviors flexibly by stacking decorators, avoiding the need to create a subclass for every possible combination of features.

This pattern provides great flexibility and follows the Open/Closed Principle, but comes with the cost of increased complexity due to multiple small classes and the need to understand decorator composition. The pattern is especially powerful when you need to add features that can be combined in various ways, making it ideal for scenarios where inheritance would lead to an explosion of subclasses.
