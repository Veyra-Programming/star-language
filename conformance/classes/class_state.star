class Counter

    property count = 0

    function increment()
        self.count = self.count + 1
    end

    function getCount()
        return self.count
    end

end

variable c = Counter()
c.increment()
c.increment()
c.increment()
show c.getCount()
