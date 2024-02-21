# Design patterns
## _Liskov Substitution Principle_
**_It should be possible to replace an instance of a superclass with an instance of a subclass without causing breaking changes._**

The principle defines that objects of a superclass shall be replaceable with objects of its subclasses without breaking the application. That requires the objects of your subclasses to behave in the same way as the objects of your superclass.

> An overriden method of a subclass needs to accept the same input parameter vaules as the method in the superclass (same rules). The same applies to the return value of the method.

It can be implemented less restrictive validation rules but enforce stricter ones are not allowed in the subclass. The behavior of the base class must conform to the behavior of the superclass. In general, the function signature (function parameters) and return type must be unchanged in the subclass.

The main porpouse of this princple is to ensure that old codebases do not break when new code is introduced. It ensures flexible code.