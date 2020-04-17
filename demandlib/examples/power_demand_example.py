# -*- coding: utf-8 -*-
"""
Creating power demand profiles using bdew profiles.

Installation requirements
-------------------------
This example requires at least version v0.1.4 of the oemof demandlib. Install
by:
    pip install 'demandlib>=0.1.4,<0.2'
Optional:
    pip install matplotlib

"""

import datetime
import demandlib.bdew as bdew
import demandlib.particular_profiles as profiles
from datetime import time as settime
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# The following dictionary is create by "workalendar"
# pip3 install workalendar
# >>> from workalendar.europe import Germany
# >>> cal = Germany()
# >>> holidays = dict(cal.holidays(2010))

holidays = {
    datetime.date(2010, 5, 24): 'Whit Monday',
    datetime.date(2010, 4, 5): 'Easter Monday',
    datetime.date(2010, 5, 13): 'Ascension Thursday',
    datetime.date(2010, 1, 1): 'New year',
    datetime.date(2010, 10, 3): 'Day of German Unity',
    datetime.date(2010, 12, 25): 'Christmas Day',
    datetime.date(2010, 5, 1): 'Labour Day',
    datetime.date(2010, 4, 2): 'Good Friday',
    datetime.date(2010, 12, 26): 'Second Christmas Day'}


def power_example():
    year = 2010

    ann_el_demand_per_sector = {
        'g0': 3000,
        'h0': 3000,
        'i0': 3000,
        'i1': 5000,
        'i2': 6000,
        'g6': 5000}

    # read standard load profiles
    e_slp = bdew.ElecSlp(year, holidays=holidays)

    # multiply given annual demand with timeseries
    elec_demand = e_slp.get_profile(ann_el_demand_per_sector,
                                    dyn_function_h0=True)

    # Add the slp for the industrial group
    ilp = profiles.IndustrialLoadProfile(e_slp.date_time_index,
                                         holidays=holidays)

    # Beginning and end of workday, weekdays and weekend days, and scaling
    # factors by default
    elec_demand['i0'] = ilp.simple_profile(ann_el_demand_per_sector['i0'])

    # Set beginning of workday to 9 am
    elec_demand['i1'] = ilp.simple_profile(ann_el_demand_per_sector['i1'],
                                           am=settime(9, 0, 0))

    # Change scaling factors
    elec_demand['i2'] = ilp.simple_profile(
        ann_el_demand_per_sector['i2'],
        profile_factors={'week': {'day': 1.0, 'night': 0.8},
                         'weekend': {'day': 0.8, 'night': 0.6}})

    print("Be aware that the values in the DataFrame are 15minute values with "
          "a power unit. If you sum up a table with 15min values the result "
          "will be of the unit 'kW15minutes'.")
    print(elec_demand.sum())

    print("You will have to divide the result by 4 to get kWh.")
    print(elec_demand.sum() / 4)

    print("Or resample the DataFrame to hourly values using the mean() "
          "method.")

    # Resample 15-minute values to hourly values.
    elec_demand = elec_demand.resample('H').mean()
    print(elec_demand.sum())

    if plt is not None:
        # Plot demand
        ax = elec_demand.plot()
        ax.set_xlabel("Date")
        ax.set_ylabel("Power demand")
        plt.show()


if __name__ == '__main__':
    power_example()
