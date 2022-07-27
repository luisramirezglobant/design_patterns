# Design patterns
## _Open-Closed Principle_
**_Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification._**
Write code to be able to add new functionality without changing the existing base code. This is done in order to prevent
sitautions in which a change to one class also requires you to adapt all de depending classes.
> After you've written and tested certain class, you should not modify It. Instead you should extend It.

To achieve this we are going to use interfaces instead of superclasses (classes with inheritance). The main benefit is an additional level of abstraction which enables loose coupling. Every interface are independant of each other and don't need to share any code, if you consider it beneficial that two implementations of an interface share some code, you can either use inheritance or composition.

As a tool in python to fulfill this principle we have [abstract classes](https://breakdance.github.io/breakdance/) which are classes that cannot be instantiated, but we can create classes that inherit from them.