using JuMP
using Ipopt


m = Model(Ipopt.Optimizer)

@variable(m, x1 >= 0)
@variable(m, x2 >= 0)

@objective(m, Max, 3x1 + 5x2)

# specify the constraints
@constraint(m, x1 <= 4)
@NLconstraint(m, 9x1^2 + 5x2^2 <= 216)

print(m)

optimize!(m)

status = termination_status(m)

println("Solution status: ", status)

println("Objective value: ", objective_value(m))

println("Values: ", value(x1))

println("Values: ", value(x2))
