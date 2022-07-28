# Design patterns
## _Interface Segregation Principle_
**_Make fine-grained interfaces that are client-specific. Clients should not be forced to implement interfaces they do not use._**

> The goal of this principle is to reduce the side effects and frequency of required changes by splitting the software into multiple, independent parts.

In this principle what we want is to have interfaces that only do one thing. Not exactly that contain only one method but all of the them need to be cohesive.

For example, the `Database` interface can have the `connect()` and `disconnect()` methods because they must go together. If the `Database` interface doesn’t use both methods, it’ll be incomplete.
