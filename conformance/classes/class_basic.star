class Greeter

    property target = "World"

    function sayHello()
        return "Hello, " + self.target + "!"
    end

end

variable g1 = Greeter()
show g1.sayHello()

variable g2 = Greeter(target = "Star")
show g2.sayHello()
