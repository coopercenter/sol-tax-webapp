def land_value(total_acerage, inside_acerage, outside_acerage, baseline_value, inside_fence_value, outside_fence_value, fmv_increase, yrs_between, starting_year):
    baseline=[]
    inside = []
    outside = []
    difference = []

    offset = starting_year - 2020
    for i in range(0, offset):
        baseline.append(0)
        inside.append(0)
        outside.append(0)


    for i in range(0, 2050-starting_year):
        if( i % 5 == 0):
            baseline.append(int(baseline_value * total_acerage * ((1.012)**(i+1))))
        else:
            baseline.append(baseline[i + offset-1])
        if( i % 6 == 0):
            inside.append(int(inside_fence_value * inside_acerage * ((1.012)**(i+1))))
            outside.append(int(outside_fence_value * outside_acerage * ((1.012)**(i+1))))
        else:
            inside.append(inside[i + offset-1])
            outside.append(outside[i + offset-1])
    
    for i in range(len(baseline)):
        difference.append(inside[i] + outside[i] - baseline[i])
    return difference, baseline


total_acerage = 2354
inside_acerage = 910
outside_acerage = total_acerage - inside_acerage
baseline_value = 1277.16
inside_fence_value = 10000
outside_fence_value = 1277
fmv_increase = 1.2
yrs_between = 5

print(land_value(total_acerage, inside_acerage, outside_acerage, baseline_value, inside_fence_value, outside_fence_value, fmv_increase, yrs_between, 2023)[1])
print(len(list([.9, .9, .9, .9, .8973, .8729, .85, .82, .79, .76, .73, .69, .66, .62, .58, .53, .49, .44, .38, .33, .27, .21, .14, .10, .10, .10, .10, .10, .10, .10, .10])))
