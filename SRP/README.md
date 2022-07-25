# Design patterns
## _Single Responsability Principle_
**_Classes with only one responsability and independent of each other._**
Changing a class without affecting dependant code is the the base of this principle. Avoid update dependencies or recompile the dependent classes because the use certain responsability of an updated class.
The more responsabilities a class has, the more changes your are willing to make, also less logic and responsabilities result in code easier to explain and understand reducing the number of bugs.
A key part is avoiding oversimplify the code, is not matter to create classes with a single function and for a really speciffic porpouse. Later when you need to write code have to inject many dependencies making the code unreadable and confusing
The purposes of the single responsibility principle are to:
- Create high cohesive and robust classes, methods, and functions.
- Promote class composition
- Avoid code duplication

> Therefore, the single responsibility principle is an important rule to make your code more understandable but don’t use it as your programming bible. 
> Use common sense when developing code. There is no point in having multiple classes that just contain one function.
## Validating the principle

Adapting software to the changing requirements is often made by an the easiest and fastest approach of adding a function or a method instead of creating a new class or component. But that often results in classes with more than responsibility and makes it more and more difficult to maintain the software.
You can avoid these problems by asking a simple question before you make any changes: **What is the responsibility of your class/component/microservice?**
If your answer includes the word “and”, you’re most likely breaking the single responsibility principle. Then it’s better to take a step back and rethink your current approach. There is most likely a better way to implement it.
### Example
Let’s assume we have a class for an employee that holds methods for calculating and reporting their salary. In other words, calculating salary can be classified as reading data and further manipulating it.
While reporting salary is a data persistence operation where the data is stored in some storage medium. If we follow Martin’s single responsibility principle, these classes should be split up as the business functions are quite different.