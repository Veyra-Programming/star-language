function makeAdder(x)
    function add(y)
        return x + y
    end
    return add
end

variable add5 = makeAdder(5)
show add5(10)
show add5(20)
