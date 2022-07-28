# Design patterns
## _Interface Segregation Principle_
**_High level modules should not depend on low level modules_**

> High-level modules, which provide complex logic, should be easily reusable and unaffected by changes in low-level modules, which provide utility features.

Based on this idea, Robert C. Martin’s definition of the Dependency Inversion Principle consists of two parts:

1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
2. Abstractions should not depend on details. Details should depend on abstractions.

The dependency inversion principle aims to reduce the coupling between classes by creating an abstraction layer between them.