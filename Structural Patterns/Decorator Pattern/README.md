# Decorator Pattern

**_Decorator Pattern is a structural design pattern that allows you to attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality._**

## Description
The intent of the Decorator pattern is to add new functionality to individual objects dynamically, without affecting the behavior of other objects from the same class. This pattern uses composition instead of inheritance to extend behavior at runtime. The decorator wraps the original object and provides the same interface, allowing decorators to be stacked and combined in various ways. This promotes the Open/Closed Principle, which states that classes should be open for extension but closed for modification.

![Decorator Pattern UML](decorator_pattern.png "Decorator Pattern Diagram")

## Key Characteristics
- **Same Interface:** Decorators implement the same interface as the objects they wrap, making them interchangeable from the client's perspective.
- **Recursive Composition:** Decorators can wrap other decorators, allowing multiple layers of functionality to be added.
- **Runtime Flexibility:** Behaviors can be added or removed at runtime by adding or removing decorator wrappers.
- **Single Responsibility:** Each decorator focuses on adding one specific piece of functionality, keeping classes focused and maintainable.
- **Transparent to Clients:** Clients interact with decorated objects the same way they would with undecorated ones.

### Component
Defines the common interface for both the objects that can be decorated and the decorators themselves. This is typically an abstract class or interface that declares the operations that can be altered by decorators.

The Component interface ensures that decorators and concrete components are interchangeable, allowing clients to work with both decorated and undecorated objects uniformly.

### Concrete Component
The class that is going to be wrapped. It defines the base behavior that can be enhanced by decorators. This is the core object to which additional responsibilities can be attached.

The Concrete Component implements the Component interface and provides the default implementation of the operations. It contains the fundamental functionality that decorators will extend.

### Base Decorator
Maintains a reference to a Component object (which can be either a Concrete Component or another decorator). The Base Decorator implements the same Component interface and delegates all operations to the wrapped object.

This class serves as the foundation for all concrete decorators. It ensures that decorators conform to the Component interface while providing the wrapping mechanism. The base decorator typically forwards all requests to the wrapped component without adding behavior.

### Concrete Decorator
Extends the Base Decorator to add specific responsibilities to the component. Concrete decorators override methods of the base decorator and can execute their own behavior either before or after (or both) delegating to the wrapped object.

Each Concrete Decorator adds one specific piece of functionality. Multiple decorators can be stacked to combine behaviors, with each decorator in the chain adding its own enhancement.

## Practical Indicators
Look for these patterns in your code:

- Multiple subclasses that differ only in minor behavioral aspects
- Need to add responsibilities to individual objects, not entire classes
- Combinatorial explosion of subclasses when trying to support all feature combinations
- Requirements to add or remove responsibilities dynamically at runtime
- Need to extend functionality of classes that cannot be modified (third-party libraries, sealed classes)
- Situations where inheritance leads to rigid, hard-to-maintain class hierarchies

## Conditions to use Decorator Pattern

- Need to add responsibilities to individual objects dynamically and transparently
- Want to avoid creating a large number of subclasses to support every combination of features
- Need to extend functionality in a way that can be withdrawn or modified at runtime
- Responsibilities need to be added in various combinations to objects
- Want to follow the Open/Closed Principle by adding new functionality without modifying existing code
- Inheritance is impractical due to class explosion or when working with final/sealed classes

## Steps to implement the Decorator

1. Identify the Component interface that will be shared by both the base object and decorators
2. Create the Concrete Component class that implements the base functionality
3. Create a Base Decorator class that implements the Component interface and holds a reference to a Component object
4. Implement Concrete Decorator classes that extend the Base Decorator and add specific behavior
5. Ensure decorators delegate calls to the wrapped component and add their own behavior before or after the delegation
6. Compose decorators at runtime to achieve the desired combination of behaviors

## Best Practices

- Ensure all decorators implement the same interface as the component they decorate
- Keep decorators focused on a single responsibility (e.g., one decorator for logging, another for encryption)
- Use Dependency Injection to provide the wrapped component to decorators for better testability
- Consider the order of decorator wrapping, as it can affect the final behavior
- Avoid creating decorators that depend on specific concrete components; they should work with the Component interface
- Be mindful of the complexity introduced by deep decorator chains, which can make debugging harder
- Use meaningful names for concrete decorators that clearly indicate what functionality they add
- Consider providing factory methods or builders when decorator combinations become complex

## Summarizing

The Decorator Pattern is particularly useful when you need to add responsibilities to objects dynamically and when subclassing would result in an explosion of subclasses. It's commonly used for adding cross-cutting concerns like logging, caching, validation, or encryption to objects without modifying their core implementation.

This pattern comes with the benefit of flexibility and adherence to the Single Responsibility Principle, as each decorator handles one specific enhancement. However, it can introduce complexity through multiple small classes and deep object wrapping chains. The Decorator pattern works best when you need runtime flexibility and when the enhanced behaviors are independent and composable.
