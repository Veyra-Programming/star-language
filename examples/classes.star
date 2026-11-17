# Object-Oriented Programming in Star 0.2

class BankAccount

    property owner
    property balance = 0.0

    function deposit(amount)
        self.balance = self.balance + amount
        show "Deposited " + amount + ". New balance: " + self.balance
    end

    function withdraw(amount)
        if amount > self.balance
            show "Insufficient funds for " + self.owner
            return false
        end
        self.balance = self.balance - amount
        show "Withdrew " + amount + ". Remaining balance: " + self.balance
        return true
    end

    function getSummary()
        return "Account [" + self.owner + "]: $" + self.balance
    end

end

# Instantiation using named properties
variable account = BankAccount(
    owner = "Alex Star",
    balance = 100.0
)

show account.getSummary()
account.deposit(50.0)
account.withdraw(30.0)
account.withdraw(200.0)
show account.getSummary()
