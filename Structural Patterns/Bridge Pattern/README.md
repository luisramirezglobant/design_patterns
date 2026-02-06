# Bridge Pattern

**_Decouple an abstraction from its implementation, prioritizing that both of them can be changed independently._**

## Description
The bridge pattern, also known as the bridge design pattern, is a structural design pattern. Structural design patterns deal with how classes and objects can be put together to form larger structures. The main goal of the bridge pattern is to separate abstraction and implementation so that they can be developed and modified independently of each other.
![Bridge Pattern UML Diagram](bridge_pattern_uml.png)

### Abstraction
Abstraction (also called interface) is a high-level control layer for some entity. This is the element or interface with which the **client interacts**.

This work delegation is made by maintaining a reference to an object of type **Implementation** (or implementor).

In code, this is reflected in an abstract class (ABC for example in Python) that will have a constructor to the **Implementation** class.

### Implementation or Implementors
Also called the ==Bridge==. Declares the interface that is common to all concrete implementations. So the abstraction can only communicate with an implementation object through methods defined here.

The methods declared here typically are only primitive operations, while the abstraction defines higher-level operations on those primitives.

_Abstractions use the implementation's methods to perform their operations._

### Refined Abstraction
They are classes that inherit from the **Abstraction** class. They extend the interface defined by the abstraction (may add more methods to those declared in the abstraction).
They perform complex operations by using the primitives in the implementation.

### Concrete Implementation
Contains the specifics on how the different implementations are going to behave. So it implements the methods according to its own scenario for that specific object.

## Summarizing
This pattern applies whenever you have cases with multiple variations of a single component. Like a remote control that needs to work with different devices. So instead of creating a subclass for each variant, we can separate the common functionality from the **platform-specific code**.
This comes at the cost of increased complexity, since we are handling multiple implementations. Changes have to be performed on multiple sides.