variable x = "outer"

if true
    variable x = "inner"
    show x
end

show x
