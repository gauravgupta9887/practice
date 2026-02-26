# Base pizza class (optional for shared behaviour)
class Pizza:
    def prepare(self):
        raise NotImplementedError("This method should be overridden by \
                                  subclasses")


class CheesePizza(Pizza):
    def prepare(self):
        return "Preparing Cheese Pizza"


class PepperoniPizza(Pizza):
    def prepare(self):
        return "Preparing Pepperoni Pizza"   


class VeggiePizza(Pizza):
    def prepare(self):
        return "Preparing Veggie Pizza"


def main():
    # Manually creating pizza objects
    pizza1 = CheesePizza()
    pizza2 = PepperoniPizza()
    pizza3 = VeggiePizza()   
    print(pizza1.prepare())
    print(pizza2.prepare())
    print(pizza3.prepare())


main()
# eg to learn :- pizza shop having a chef who takes the name and give the pizza
# 1. tightly coupled :- what if I want to discontinue 1 pizza, what if I want 
# to rename?
# 2. If we add more pizzas, we will keep on adding if and else
# 3. very hard to scale


def if_else_main():
    # Manually creating pizza objects
    input = "pepperoni"

    if input == "pepperoni":
        return PepperoniPizza()
    elif input == "veggie":
        return VeggiePizza()
    elif input == "cheese":
        return CheesePizza()
    else:
        print("Not available in menu")


if_else_main()


# factory class
class PizzaFactory:
    @staticmethod
    def create_pizza(pizza_type):
        if pizza_type == "pepperoni":
            return PepperoniPizza()
        elif pizza_type == "veggie":
            return VeggiePizza()
        elif pizza_type == "cheese":
            return CheesePizza() 
        else:
            raise ValueError("Unknown pizza type: {pizza_type}")


def factory_main():
    try:
        user_input = "pepperoni"
        pizza = PizzaFactory.create_pizza(user_input)
        print(pizza.prepare())
    except ValueError as e:
        print(e)


factory_main()

# scenario
# e-commerce shop -different type of products
# different orders medicine order / lab test order / consultation order