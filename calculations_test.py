# def getSimulationValues(simulation):
#     years = int(simulation.initial_year)
#     assessed_20 = int(simulation.initial_investment)
#     rs_rate = int(simulation.locality.revenue_share_rate)
#     mw = int(simulation.project_size)
#     interest_rate = int(simulation.locality.discount_rate) *.01
#     property_rate = simulation.locality.real_propery_rate
#     mt_rate = simulation.locality.mt_tax_rate
#     scc_depreciation = [.9, .9, .9, .9, .9, .87, .85, .82, .79, .76, .73, .69, .66, .62, .58, .53, .49, .44, .38, .33, .27, .21, .14, .10, .10, .10, .10, .10, .10, .10, .10]
    
    
#     # total_acerage = 2354
#     # inside_acerage = 910
#     # outside_acerage = total_acerage - inside_acerage
#     # baseline_value = 1277.16
#     # inside_fence_value = 10000
#     # outside_fence_value = 1277
#     # fmv_increase = 1.2
#     # yrs_between = 5


#     offset = years - 2020
#     effective_rate = []
#     for i in range(0, offset):
#         effective_rate.append(0)
    
#     for i in range(0, 2050 - years + 1):
#         if(mw >= 20):
#             offset = years-2020
#             effective_rate.append(scc_depreciation[i] * property_rate)
#         else:
#             effective_rate = mt_rate

#     return years, assessed_20, rs_rate, mw, interest_rate, effective_rate

# def performCalculations(simulation, initial_year, investment, rs_rate, mw, interest_rate, effective_rate):
#     #Run each function & extract table of values
#     # print(years, assessed_20, rs_rate, mw, interest_rate, effective_rate)
#     # cas_mt = total_cashflow_mt(years, assessed_20, effective_rate)
#     # print(cas_mt)
#     # cas_rs = total_cashflow_rs(years, rs_rate, mw, interest_rate)
#     # tot_mt = total_adj_rev_mt(years, assessed_20, effective_rate, interest_rate)
#     # tot_mt_sum = sum(tot_mt)
#     # tot_rs = total_adj_rev_rs(years, rs_rate, mw, interest_rate)
#     # tot_rs_sum = sum(tot_rs)
    

#     # #Revenue Share Works
#     cas_rs = total_cashflow_rs(rs_rate, mw, initial_year)
#     tot_rs = total_adj_rev(cas_rs, interest_rate)
#     tot_rs_sum = int(sum(tot_rs))

#     #Revenue Share with Land Works
#     cas_mt = total_cashflow_mt(initial_year, investment, effective_rate)
#     # cas_mt_land = add_land(cas_mt, land_difference, land_baseline, property_rate)
#     # print(cas_mt_land)
#     tot_mt = total_adj_rev(cas_mt, interest_rate)
#     tot_mt_sum = int(sum(tot_mt))
#     # print(tot_rs_sum, tot_mt_sum)

#     try:
#         sim = simulation.calculations
#         calc = Calculations.objects.get(simulation=simulation)
#         calc.cas_mt = cas_mt
#         calc.cas_rs = cas_rs
#         calc.tot_mt = tot_mt
#         calc.tot_rs = tot_rs
#     except Calculations.DoesNotExist:
#         calc = Calculations.objects.create(simulation=simulation, cas_mt = cas_mt, cas_rs=cas_rs, tot_mt=tot_mt, tot_rs=tot_rs)
#     return calc


# # def land_value(baseline_value, inside_fence_value, outside_fence_value_, fmv_increase, yrs, total_acerage, inside_acerage, outside_acerage):
# #     baseline=[]
# #     for i in range(31):
# #         baseline.append(baseline_value * total_acerage)
# #     return baseline



# def total_cashflow_mt(year, assessed_20, effective_rate_list):
#     '''
#         :year: Starting year of solar project
#         :assessed_20: Initial investment into solar project
#         :effective_rate_list: List of effective rates of m&t over the course of a 30 year period
#         :return: list of M&T tax revenue generated each year from 2020-2050, nominal $
#     '''
#     effective_rate_ext(effective_rate_list)
#     # print(assessed_20)
#     print(effective_rate_list)
#     yearly_rev_mt = []
#     for i in range(0, 31):
#         if(i + 2020 >= year):
#             if i+2020 - year < 5:
#                 revenue = ((assessed_20 * .2 * effective_rate_list[i])/100)/1000
#                 yearly_rev_mt.append(revenue)
#             elif (i + 2020 - year) >= 5 and (i + 2020 - year) < 10:
#                 revenue = ((assessed_20 * .3 * effective_rate_list[i])/100)/1000
#                 yearly_rev_mt.append(revenue)
#             elif (i + 2020 - year) >= 10:
#                 revenue = ((assessed_20 * .4 * effective_rate_list[i])/100)/1000
#                 yearly_rev_mt.append(revenue)
#         else:
#             yearly_rev_mt.append(0)
#     return yearly_rev_mt

# def total_cashflow_rs(revenue_share_rate, megawatts, year):
#     '''
#         :revenue_share_rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
#         :megawatts: Size of solar project
#         :year: Starting year of the solar project
#         :return: A list of reveneue share revenue generated during each year from 2020-2050, nominal $
#     '''
#     cashflow_rev = []
#     for i in range(0, 31):
#         if(i + 2020 >= year):
#             cashflow_rev.append((revenue_share_rate * megawatts)/1000) # If the index is at or past the initial year of project
#         else:
#             cashflow_rev.append(0) #If the index is before the initial year of project
#     return cashflow_rev


# def total_adj_rev(cas, discount_rate):
#     '''
#         :cas_rs: List of revenue generate during each year from 2020-2050, nominal $
#         :discount_rate: rate at which revenue values will be discounted
#         :return: A list of revenue generated during each year from 2020-2050, 2020 $
#     '''
#     tot_rs = []
#     for i in range(len(cas)):
#         tot_rs.append(cas[i] / ((1 + discount_rate)**(i + 1))) # Present value formula
#     return tot_rs

# def land_value(total_acerage, inside_acerage, outside_acerage, baseline_value, inside_fence_value, outside_fence_value, fmv_increase, yrs_between, starting_year):
#     baseline=[]
#     inside = []
#     outside = []
#     difference = []

#     offset = starting_year - 2020
#     for i in range(0, offset):
#         baseline.append(0)
#         inside.append(0)
#         outside.append(0)


#     for i in range(0, 2050-starting_year+1):
#         if( i % 5 == 0):
#             baseline.append(int(baseline_value * total_acerage * ((1.012)**(i+1))))
#         else:
#             baseline.append(baseline[i + offset-1])
#         if( i % 6 == 0):
#             inside.append(int(inside_fence_value * inside_acerage * ((1.012)**(i+1))))
#             outside.append(int(outside_fence_value * outside_acerage * ((1.012)**(i+1))))
#         else:
#             inside.append(inside[i + offset-1])
#             outside.append(outside[i + offset-1])
    
#     for i in range(len(baseline)):
#         difference.append(inside[i] + outside[i] - baseline[i])
#     return difference, baseline

# def add_land(cas_mt, land_difference, land_baseline, property_rate):
#     # print("Difference in land values " + str(land_difference))
#     # print("M&T with no Land " + str(cas_mt))
#     cas_mt_land = []
#     for i in range(len(cas_mt)):
#         land_value_by_year = int((land_difference[i]/100 * property_rate)) + int((land_baseline[i]/100 * property_rate))
#         cas_mt_land.append(cas_mt[i] + land_value_by_year)
#     return cas_mt_land

# total_acerage = 2354
# inside_acerage = 910
# outside_acerage = total_acerage - inside_acerage
# baseline_value = 1277.16
# inside_fence_value = 10000
# outside_fence_value = 1277
# fmv_increase = 1.2
# yrs_between = 5

# initial_year = 2020
# investment = 140000000
# rs_rate = 1400
# mt_rate = [0.63]
# property_rate = 0.5
# mw = 100
# interest_rate = 0.06
# scc_depreciation = [.9, .9, .9, .9, .9, .87, .85, .82, .79, .76, .73, .69, .66, .62, .58, .53, .49, .44, .38, .33, .27, .21, .14, .10, .10, .10, .10, .10, .10, .10, .10]

# if(mw >= 20):
#     effective_rate = []
#     for i in range(len(scc_depreciation)):
#         effective_rate.append(scc_depreciation[i] * property_rate)
#     # effective_rate = [property_rate]
# else:
#     effective_rate = mt_rate

# land_values = land_value(total_acerage, inside_acerage, outside_acerage, baseline_value, inside_fence_value, outside_fence_value, fmv_increase, yrs_between, 2020)
# land_difference = land_values[0]
# land_baseline = land_values[1]




# #Revenue Share Works
# cas_rs = total_cashflow_rs(rs_rate, mw, initial_year)
# tot_rs = total_adj_rev(cas_rs, interest_rate)
# tot_rs_sum = int(sum(tot_rs))

# #Revenue Share with Land Works
# cas_mt = total_cashflow_mt(initial_year, investment, effective_rate)
# cas_mt_land = add_land(cas_mt, land_difference, land_baseline, property_rate)
# print(cas_mt_land)
# tot_mt = total_adj_rev(cas_mt_land, interest_rate)
# tot_mt_sum = int(sum(tot_mt))
# print(tot_rs_sum, tot_mt_sum)



'''
Calculations
'''
def effective_rate_ext (effective_rate_list):
    '''
    Takes in schedule of effective rates for county + year of initial build
    Extends list with final effective rate to be available for calculations out to 2050
    '''
    last_rate = effective_rate_list[-1]
    while len(effective_rate_list) <= 32:
        effective_rate_list.append(last_rate)
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# M&T functions
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# def lifetime_adj_rev_mt(year, assessed_20, effective_rate_list, interest_rate):
#     '''
#     :param year: calendar year in which the investment is being made
#     :param assessed_20: assessed value of all new solar projects built in locality during particular calendar year
#     :param effective_rate_list: schedule of a locality's effective M&T tax rate
#     :param interest_rate: rate at which values will be discounted
#     :return: total lifetime tax revenue from new builds in year y under M&T tax, in year y dollars
#     '''
#     effective_rate_ext(effective_rate_list)
#     rev_year_y = [] # start a list to fill with lifetime cashflows from projects built in year year
#     for y in range(0, year - 2019): # fill list with zeros for before project existed
#         rev_year_y.append(0)
#     for n in range(0, 5):  # tax revenue from first 5 years
#         revenue = (assessed_20 * .2 * effective_rate_list[n]) / 100 # (Project value * Taxable percentage * M&T tax rate) / 100 = M&T revenue Divide by 100 as M&T is calculated per 100 valuation.
#         year_adj_revenue = revenue / ((1 + interest_rate) ** n) 
#         rev_year_y.append(year_adj_revenue)
#     for n in range(5, 10):  # tax revenue from second 5 years
#         revenue = (assessed_20 * .3 * effective_rate_list[n]) / 100
#         year_adj_revenue = revenue / ((1 + interest_rate) ** n)
#         rev_year_y.append(year_adj_revenue)
#     for n in range(10, 31):  # tax revenue from end of 10 years through 2050
#         revenue = (assessed_20 * .4 * effective_rate_list[n]) / 100
#         year_adj_revenue = revenue / ((1 + interest_rate) ** n)
#         rev_year_y.append(year_adj_revenue)
#     return rev_year_y
# def total_adj_rev_mt(years, investments_20, outer_effective_rate_list, outer_interest_rate):
#     '''
#     :param years: list of years in which there is expected to be new investments in solar for a locality
#     :param investments_20: list of total assessed values of investments in locality for each year
#     :param outer_effective_rate_list: schedule of a locality's effective M&T tax rate
#     :param outer_interest_rate:  rate at which values will be discounted
#     :return: total tax revenue from new solar projects >20MW built in a locality out to 2050
#     '''
#     total = []  # list to add cashflows from each year to
#     for n in range(0, 32):
#         # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
#         total.append(0)
#     for yr in range(0, len(years)):
#         # selecting matching pair of year and its corresponding assessed value of new solar >20MW
#         year_y = years[yr]
#         assessed_year_y = investments_20[yr]
#         # calculate total lifetime tax revenue from new builds in year y under M&T tax, in year y dollars
#         year_y_lifetime_cash = lifetime_adj_rev_mt(year_y, assessed_year_y, outer_effective_rate_list,
#                                                    outer_interest_rate)
#         # calculate year_y_lifetime_rev in 2020 $$$
#         for n in range(0, 32):
#             y_life_pv = year_y_lifetime_cash[n] / ((1 + outer_interest_rate) ** (year_y - 2020))
#             # add value from year y to total
#             total[n] = total[n] + y_life_pv
#     total.pop(0)
    
#     for val in range(0, len(total)): # round final numbers to nearest thousand
#         total[val] = round(total[val] / 1000)
    
#     return total
# def yearly_cashflow_mt(year, assessed_20, effective_rate_list):
#     '''
#     :param year: calendar year in which the investment is being made
#     :param assessed_20: assessed value of all new solar projects >20MW built in locality during particular calendar year
#     :param effective_rate_list: schedule of a locality's effective M&T tax rate
#     :param interest_rate: rate at which values will be discounted
#     :return: list of revenues from solar projects >20MW built in indicated year for 30 years
#     '''
#     effective_rate_ext(effective_rate_list)
#     rev_year_y = [] # start a list to fill with lifetime cashflows from projects built in year year
#     for y in range(0, year - 2019): # fill list with zeros for period before project is built
#         rev_year_y.append(0)
#     for n in range(0, 5):  # tax revenue from first 5 years
#         revenue = (assessed_20 * .2 * effective_rate_list[n]) / 100
#         rev_year_y.append(revenue)
#     for n in range(5, 10):  # tax revenue from second 5 years
#         revenue = (assessed_20 * .3 * effective_rate_list[n]) / 100
#         rev_year_y.append(revenue)
#     for n in range(10, 31):  # tax revenue from end of 10 years through 2050
#         revenue = (assessed_20 * .4 * effective_rate_list[n]) / 100
#         rev_year_y.append(revenue)
#     return rev_year_y
# def total_cashflow_mt(years, investments_20, outer_effective_rate_list):
#     '''
#     :param years: list of years in which there is expected to be new investments in solar for a locality
#     :param investments_20: list of assessed values of solar investments >20MW in locality for each indicated year
#     :param outer_effective_rate_list: schedule of a locality's effective M&T tax rate
#     :param outer_interest_rate: rate at which values will be discounted
#     :return: list of yearly tax revenue from solar projects >20MW built in a locality out to 2050
#     '''
#     total = []  # list for storing annual cashflows
#     for n in range(0, 32):
#         # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
#         total.append(0)
#     for yr in range(0, len(years)):
#         # selecting matching pair of year and its corresponding assessed value of new solar >20MW
#         year_y = years[yr]
#         assessed_year_y = investments_20[yr]
#         # calculate total lifetime tax revenue from new builds in year y under M&T tax, in year y dollars
#         year_y_lifetime_cash = yearly_cashflow_mt(year_y, assessed_year_y, outer_effective_rate_list
#                                                    )
#         # calculate year_y_lifetime_rev in 2020 $$$
#         for n in range(0, 32):
#             y_life_pv = year_y_lifetime_cash[n] / ((1 + 0) ** (2020 - 2020))
#             # add value from year y to total
#             total[n] = total[n] + y_life_pv
#     total.pop(0)
    
#     for val in range(0, len(total)): # round final numbers to nearest thousand
#         total[val] = round(total[val] / 1000)
#     return total
    









# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Revenue Share functions
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# def lifetime_adj_rev_rs(rate, megawatts, year, interest_rate):
#     '''
#     :param rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
#     :param megawatts:
#     :param year:
#     :param interest_rate:
#     :return:
#     '''
#     rev_year_y = []
#     for y in range(0, year - 2019):
#         rev_year_y.append(0)
#     for n in range(0, 2051 - year):  # tax revenue from end of 10 years through 2050
#         revenue = (float(rate * megawatts))
#         year_adj_revenue = revenue / ((1 + interest_rate) ** n)
#         rev_year_y.append(year_adj_revenue)
#     return rev_year_y
# def total_adj_rev_rs(years, rate, megawatts, interest_rate):
#     '''
#     :param years:
#     :param rate:
#     :param megawatts:
#     :param effective_rate_list:
#     :param interest_rate:
#     :return:
#     '''
#     total = []  # bin to add present value of lifetime tax revenue from each year to
#     for n in range(0, 32):
#         # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
#         total.append(0)
#     for yr in range(0, len(years)):
#         # calculate yearly list of cash flows for new builds in year yr
#         year_y = years[yr]
#         megawatts_y = megawatts[yr]
#         year_y_lifetime_cash = lifetime_adj_rev_rs(rate, megawatts_y, year_y, interest_rate)
#         # calculate each year into 2020 $'s and then add to corresponding year on total cashflow
#         for n in range(0, len(year_y_lifetime_cash)):
#             y_life = year_y_lifetime_cash[n] / ((1 + interest_rate) ** (year_y - 2020))
#             total[n] = total[n] + y_life
#     total.pop(0)
        
#     for val in range(0, len(total)): # round final numbers to nearest thousand
#         total[val] = round(total[val] / 1000)
#     return total
    
    
# def lifetime_cashflow_rs(rate, megawatts, year, interest_rate):
#     '''
#     :param rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
#     :param megawatts: size in MW of all new solar projects >5MW built in locality during particular calendar year
#     :param year: calendar year in which the investment is being made
#     :param interest_rate:  rate at which values will be discounted
#     :return: list of revenues from solar projects >5MW built in indicated year through 2050
#     '''
#     rev_year_y = []
#     for y in range(0, year - 2019):
#         rev_year_y.append(0)
#     for n in range(0, 2051 - year):  # tax revenue from end of 10 years through 2050
#         revenue = (float(rate * megawatts))
#         rev_year_y.append(revenue)
#     return rev_year_y
# def total_cashflow_rs(years, rate, megawatts, interest_rate):
#     '''
#     :param years: list of years in which there is expected to be new investments in solar for a locality
#     :param rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
#     :param megawatts: list of size in MW of total solar investments >5MW in locality for each indicated year 
#     :param interest_rate: rate at which values will be discounted
#     :return:  list of yearly tax revenue from solar projects >5MW built in a locality out to 2050
#     '''
#     total = []  # bin to add present value of lifetime tax revenue from each year to
#     for n in range(0, 32):
#         # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
#         total.append(0)
#     for yr in range(0, len(years)):
#         # calculate yearly list of cash flows for new builds in year yr
#         year_y = years[yr]
#         megawatts_y = megawatts[yr]
#         year_y_lifetime_cash = lifetime_cashflow_rs(rate, megawatts_y, year_y, interest_rate)
#         # calculate each year into 2020 $'s and then add to corresponding year on total cashflow
#         for n in range(0, len(year_y_lifetime_cash)):
#             y_life_pv = year_y_lifetime_cash[n] / ((1 + 0) ** (2020 - 2020))
#             total[n] = total[n] + y_life_pv
            
#     total.pop(0) # remove 2019 place holder
    
#     for val in range(0, len(total)): # round final numbers to nearest thousand
#         total[val] = round(total[val] / 1000)
        
#     return total

stepdown = [.8, .8, .8, .8, .8, .7, .7, .7, .7, .7, .6]
effective_rate_ext(stepdown)
year = 2020
investment = 210000000
depreciation_schedule = [.9, .9, .9, .9, .9, .8729, .8470, .8196, .7906, .7598, .7271, .6925, .6568, .6170, .5758, .5321, .4858, .4367, .3847, .3295, .2711, .2091, .1434, .10, .10, .10, .10, .10, .10, .10, .10]
assessment_ratio = .998
size_mw = 100
real_estate_rate = 0.47
mt_tax_rate = 0.47

#Land Values
total_acerage = 2354
inside_acerage = 910
outside_acerage = total_acerage - inside_acerage
print(outside_acerage)
baseline_value = 1277.16
inside_fence_value = 10000
outside_fence_value = baseline_value
fmv_increase = 1.2
yrs_between = 5

'''
FUNCTIONS TO GET TOTAL MT REVENUE GENERATED BY SOLAR FACILITY

'''


##############################################################
# Functions to determine tax rates for project
##############################################################

'''
    Get the exemption rate for the project. If above 150 MW a solar project does not have any exemptions applied. Otherwise it is the M&T stepdown exemption rate
'''
def get_mt_exemption(size_mw, mt_exemption):
    if(size_mw > 150):
        return 0
    else:
        return mt_exemption

'''
    Get the M&T tax rate for the project. If above 20 MW use the real estate rate for the project, otherwise use the mt_tax_rate
'''
def get_mt_tax_rate(size_mw, mt_tax_rate, real_estate_rate):
    if investment > 20:
        return real_estate_rate
    else:
        return mt_tax_rate

##############################################################
# Calculations for Valuation of Proposed Solar Facility
##############################################################

def solar_facility_valuation(year, investment, mt_exemption, depreciation_schedule, assessment_ratio):
    valuation = []
    for i in range(0, 31):
        if(i + 2020 >= year):
            after_exemption = investment * (1 - mt_exemption[i])
            after_depreciation = after_exemption * depreciation_schedule[i]
            assessed_facility_valuation = after_depreciation * assessment_ratio
            valuation.append(round(assessed_facility_valuation)) # If the index is at or past the initial year of project
        else:
            valuation.append(0) #If the index is before the initial year of project
    return valuation


##############################################################
# Calculations for increase in Land Value
##############################################################

def current_land_value(total_acerage, baseline_value, starting_year):
    baseline = []
    offset = starting_year - 2020
    for i in range(0, offset):
        baseline.append(0)
    for i in range(0, 2050-starting_year+1):
        if(i % 5 == 0):
            baseline.append(round(baseline_value * total_acerage * ((1.012)**(i+1))))
        else:
            baseline.append(baseline[i + offset - 1])
    return baseline

def new_land_value(total_acerage, inside_acerage, outside_acerage, inside_fence_value, outside_fence_value, starting_year):
    total = []
    offset = starting_year - 2020

    for i in range(0, offset):
        total.append(0)

    for i in range(0, 2050-starting_year+1):
        if( i % 6 == 0):
            inside = inside_fence_value * inside_acerage * ((1.012)**(i+1))
            outside = outside_fence_value * outside_acerage * ((1.012)**(i+1))
            total.append(round(inside + outside))
        else:
            total.append(total[i + offset-1])
        
    return total

def increase_in_land_value(current_land_value, new_land_value, assessment_ratio):
    difference = []
    for i in range(0, len(current_land_value)):
        difference.append(round((new_land_value[i] - current_land_value[i]) * assessment_ratio))
    return difference

##############################################################



##############################################################
# Gross Revenue from Project Calculations
##############################################################

def increased_county_gross_revenue_from_project(solar_valuation_list, applied_mt_tax_rate, increase_in_land_value, applied_real_estate_rate):
    gross_revenue_increase = []
    for i in range(0, len(increase_in_land_value)):
        increase_from_solar = (solar_valuation_list[i] * applied_mt_tax_rate)/100
        increase_from_land = (increase_in_land_value[i] * applied_real_estate_rate)/100
        gross_revenue_increase.append(round(increase_from_solar + increase_from_land))
    return gross_revenue_increase

def current_land_revenue(current_land_value, applied_real_estate_rate):
    current_revenue = []
    for i in range(len(current_land_value)):
        current_revenue.append(round(current_land_value[i] * (applied_real_estate_rate/100)))
    return current_revenue

def total_gross_revenue_mt(current_revenue, gross_revenue_increase):
    total_revenue = []
    for i in range(len(current_revenue)):
        total_revenue.append(current_revenue[i] + gross_revenue_increase[i])
    return total_revenue
##############################################################


mt_exemption = get_mt_exemption(size_mw, stepdown)

solar_valuation_list = solar_facility_valuation(year, investment, mt_exemption, depreciation_schedule, assessment_ratio)
project_mt_tax_rate = get_mt_tax_rate(size_mw, mt_tax_rate, real_estate_rate)

current_land_value = current_land_value(total_acerage, baseline_value, year)
new_land_value = new_land_value(total_acerage, inside_acerage, outside_acerage, inside_fence_value, outside_fence_value, year)
increase_in_land_value = increase_in_land_value(current_land_value, new_land_value, assessment_ratio)
project_real_estate_rate = real_estate_rate

increase_gross_revenue = increased_county_gross_revenue_from_project(solar_valuation_list, project_mt_tax_rate, increase_in_land_value, project_real_estate_rate)
current_land_revenue = current_land_revenue(current_land_value, project_real_estate_rate)

total_mt_revenue = total_gross_revenue_mt(current_land_revenue, increase_gross_revenue)
# print(total_mt_revenue)
#print(increased_county_gross_revenue_from_project(solar_valuation_list, applied_mt_tax_rate, increase_in_land_value, applied_real_estate_rate))




'''
FUNCTIONS TO GET TOTAL TAX AVAILABLE TO LOCALITIES FROM MT TAX
'''

def net_total_revenue_from_project(gross_revenue_project, increase_in_local_contribution):
    net_total_revenue = []
    for i in range(len(gross_revenue_project)):
        net_total_revenue.append(round(gross_revenue_project[i] - increase_in_local_contribution[i],))
    return net_total_revenue

def increase_in_local_contribution(pv_required_education_contribution, baseline_required_education_contribution):
    increase_contribution = []
    for i in range(len(pv_required_education_contribution)):
        increase_contribution.append(pv_required_education_contribution[i] - baseline_required_education_contribution[i])
    return increase_contribution

def pv_required_education_contribution(locality_education_budget, budget_escalator, pv_composite_index):
    pv_education_contribution = []
    for i in range(len(pv_composite_index)):
        pv_education_contribution.append(locality_education_budget * ((1+budget_escalator) ** i) * pv_composite_index[i])
    return pv_education_contribution

def baseline_required_education_contribution(locality_education_budget, budget_escalator, baseline_composite_index):
    baseline_education_contribution = []
    for i in range(len(baseline_composite_index)):
        baseline_education_contribution.append(locality_education_budget * ((1+budget_escalator) ** i) * baseline_composite_index[i])
    return baseline_education_contribution

'''
COMPOSITE INDEX FUNCTIONS
'''

def composite_index(adm_composite_index, per_capita_composite_index):
    final_pv_composite_index = []
    for i in range(len(adm_composite_index)):
        local_composite_index = ((2/3) * adm_composite_index[i]) + ((1/3) * per_capita_composite_index[i])
        value = 0.45 * local_composite_index
        final_pv_composite_index.append(value)
    return final_pv_composite_index

def adm_composite_index(true_values_adm, gross_income_adm, retail_sales_adm):
    final_adm_composite_index = []
    for i in range(len(true_values_adm)):
        adm_value = .5 * true_values_adm[i] + .4 * gross_income_adm[i] + .1 * retail_sales_adm[i]
        final_adm_composite_index.append(adm_value)
    return final_adm_composite_index

def per_capita_composite_index(true_values_per_capita, gross_income_per_capita, retail_sales_per_capita):
    final_per_capita_composite_index = []
    for i in range(len(true_values_per_capita)):
        per_capita_value = .5 * true_values_per_capita[i] + .4 * gross_income_per_capita[i] + .1 * retail_sales_per_capita[i]
        final_per_capita_composite_index.append(per_capita_value)
    return final_per_capita_composite_index

'''
TRUE VALUE CALCULATIONS
'''
def get_true_values_adm(local_true_values, divisional_adm, statewide_total_true_values, total_state_adm):
    final_true_values = []
    for i in range(len(local_true_values)):
        numerator = local_true_values[i]/divisional_adm
        denominator = statewide_total_true_values[i]/total_state_adm
        final_true_values.append(numerator/denominator)
    return final_true_values

def get_true_values_per_capita(local_true_values, local_pop, statewide_total_true_values, state_pop):
    final_true_values = []
    for i in range(len(local_true_values)):
        numerator = local_true_values[i]/local_pop
        denominator = statewide_total_true_values[i]/state_pop
        final_true_values.append(numerator/denominator)
    return final_true_values

def get_baseline_true_values_adm(baseline_true_values, divisional_adm, baseline_state_true_values, total_state_adm):
    final_true_values = []
    for i in range(len(baseline_true_values)):
        numerator = baseline_true_values[i]/divisional_adm
        denominator = baseline_state_true_values[i]/total_state_adm
        final_true_values.append(numerator/denominator)
    return final_true_values

def get_baseline_true_values_per_capita(baseline_true_values, local_pop, baseline_state_true_values, state_pop):
    final_true_values = []
    for i in range(len(baseline_true_values)):
        numerator = baseline_true_values[i]/local_pop
        denominator = baseline_state_true_values[i]/state_pop
        final_true_values.append(numerator/denominator)
    return final_true_values

def local_true_values(baseline_true_value, increase_in_taxable_property):
    final_local_true_values = []
    for i in range(len(increase_in_taxable_property)):
        final_local_true_values.append(baseline_true_value + increase_in_taxable_property[i])
    return final_local_true_values

def state_total_true_values(baseline_state_true_value, increase_in_taxable_property):
    final_state_true_values = []
    for i in range(len(increase_in_taxable_property)):
        final_state_true_values.append(baseline_state_true_value + increase_in_taxable_property[i])
    return final_state_true_values

def increase_in_taxable_property(increase_in_land_value, solar_facility_valuation):
    inc_taxable_property = [increase_in_land_value[i] + solar_facility_valuation[i] for i in range(len(solar_facility_valuation))]
    return inc_taxable_property

'''
GROSS INCOME CALCULATIONS
'''
def get_gross_income_adm(adj_gross_income, divisional_adm, statewide_gross_income, total_state_adm):
    final_gross_income = []
    for i in range(31):
        numerator = adj_gross_income/divisional_adm
        denominator = statewide_gross_income/total_state_adm
        final_gross_income.append(numerator/denominator)
    return final_gross_income

def get_gross_income_per_capita(adj_gross_income, local_pop, statewide_gross_income, state_pop):
    final_gross_income = []
    for i in range(31):
        numerator = adj_gross_income/local_pop
        denominator = statewide_gross_income/state_pop
        final_gross_income.append(numerator/denominator)
    return final_gross_income

'''
RETAIL SALES CALCULATIONS
'''
def get_retail_sales_adm(local_taxable_retail_sales, divisional_adm, state_taxable_retail_sales, total_state_adm):
    final_retail_sales = []
    for i in range(31):
        numerator = local_taxable_retail_sales/divisional_adm
        denominator = state_taxable_retail_sales/total_state_adm
        final_retail_sales.append(numerator/denominator)
    return final_retail_sales

def get_retail_sales_per_capita(local_taxable_retail_sales, local_pop, state_taxable_retail_sales, state_pop):
    final_retail_sales = []
    for i in range(31):
        numerator = local_taxable_retail_sales/local_pop
        denominator = state_taxable_retail_sales/state_pop
        final_retail_sales.append(numerator/denominator)
    return final_retail_sales


taxable_property = increase_in_taxable_property(increase_in_land_value, solar_valuation_list)
# print(taxable_property)
local_baseline = [1082405094 for i in range(31)]
local_true = local_true_values(local_baseline[0], taxable_property)
state_baseline = [1170092111099 for i in range(31)]
state_true = state_total_true_values(state_baseline[0], taxable_property)
local_adm = 2092.8
local_gi = 235448294
local_retail_sales = 125684762.78
local_pop = 16261

state_gi = 269067675605
state_adm = 1239781
state_retail_sales = 100207273998.18
state_pop = 8382993
# print(local_true)

test_true_values = get_true_values_adm(local_true, local_adm, state_true, state_adm)
# print(test_true_values)

test_gross_income = get_gross_income_adm(local_gi, local_adm, state_gi, state_adm)
# print(test_gross_income)

test_retail_sales = get_retail_sales_adm(local_retail_sales, local_adm, state_retail_sales, state_adm)
# print(test_retail_sales)

test_adm = adm_composite_index(test_true_values, test_gross_income, test_retail_sales)
# print(test_adm)

true_values_pop = get_true_values_per_capita(local_true, local_pop, state_true, state_pop)
gross_income_pop = get_gross_income_per_capita(local_gi, local_pop, state_gi, state_pop)
retail_sales_pop = get_retail_sales_per_capita(local_retail_sales, local_pop, state_retail_sales, state_pop)

test_local = per_capita_composite_index(true_values_pop, gross_income_pop, retail_sales_pop)

pv_comp_index = composite_index(test_adm, test_local)
# print(pv_comp_index)

baseline_adm_true_values = get_baseline_true_values_adm(local_baseline, local_adm, state_baseline, state_adm)
baseline_per_capita_true_values = get_baseline_true_values_per_capita(local_baseline, local_pop, state_baseline, state_pop)

baseline_adm_comp = adm_composite_index(baseline_adm_true_values, test_gross_income, test_retail_sales)
baseline_local_comp = per_capita_composite_index(baseline_per_capita_true_values, gross_income_pop, retail_sales_pop)
baseline_comp_index = composite_index(baseline_adm_comp, baseline_local_comp)
# print(baseline_comp_index)

required_local_matching = 3754671
education_budget = required_local_matching / baseline_comp_index[0]
#print(education_budget, 0.01, baseline_comp_index[0])
baseline_education_contribution = baseline_required_education_contribution(education_budget, 0.01, baseline_comp_index)
pv_education_contribution = pv_required_education_contribution(education_budget, 0.01, pv_comp_index)
#print(baseline_education_contribution)

local_contribution_increase = increase_in_local_contribution(pv_education_contribution, baseline_education_contribution)
# print(local_contribution_increase)

#print(total_mt_revenue)
net_revenue  = net_total_revenue_from_project(total_mt_revenue, local_contribution_increase)