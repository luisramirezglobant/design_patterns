# Factory Method Pattern

**_Facade Method is a structural design pattern that provides a unified interface to a set of interfaces in a subsystem. Facade  defines a higer level interface that makes the subsystem easier to use._**

## Description
The intent of the Facade pattern is to provide a simplified interface to a complex system of classes, libraries, or frameworks. It promotes loose coupling between clients and the subsystem by abstracting away the details of subsystem components behind a single interface.
![Facade UML](Facade_pattern_UML.png "Facade Pattern Diagram")


### Facade Rules
- If you are in a particular method in a particular object you are only allowed to invoke some particular methods depending where this methods reside. 
- You are able to invoke the methods of the particular object that  you are in
Objects that has been passed as parameter their methods can be called.
- Invoke methods that you've create yourself. So all the objects (and it's) methods created inside an allowed method, can be invoked as well.
- Methods on a component of this object. All the classes instantiated within a allowed method can be invoked as well.
