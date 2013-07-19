# REPORTER create reports
# Copyright (C) 2013  AB

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import datetime
# import sqlite3
# import math


def gen_date_list(base, numdays):
    base = datetime.datetime.date(base)
    date_list = [base + datetime.timedelta(days=i) for i in range(numdays)]
    return date_list


def bill_daily_list(park_start, park_end, daily_tariff):
    # convert tariff to datetime
    date_frm = '%Y-%m-%d %H:%M:%S'
    park_start = datetime.datetime.strptime(park_start, date_frm)
    park_end = datetime.datetime.strptime(park_end, date_frm)

    # calculate number of *calendar* parking days
    park_length = park_end.date() - park_start.date()
    park_days = park_length.days + 1  # !!!

    # calculate cartesian product of day list and tariff list
    dl = gen_date_list(park_start, park_days)
    dtl = [[datetime.datetime.combine(i, j[0]), datetime.datetime.combine(i, j[1]), j[2]]
           for i in dl for j in daily_tariff]

    # select tariff intervals intersecting parking interval (not(A and B) = not A or not B)
    pdtl = [i for i in dtl if i[0] < park_end and i[1] > park_start]
    # This can be optimized because the intervals in dtl are ordered set, so you need to find
    # the first and last intersecting intervals of dtl.

    # correct start and end of intervals list
    pdtl[0][0], pdtl[-1][1] = park_start, park_end

    # calculating cost
    cost = 0
    for i in pdtl:
        # cost += math.ceil((i[1] - i[0]).seconds/3600)*i[2]
        cost += i[2]
    return cost


daily_tariff = [[datetime.time(0, 0, 0), datetime.time(6, 0, 0), 10],
                [datetime.time(6, 0, 0), datetime.time(18, 0, 0), 0],
                [datetime.time(18, 0, 0), datetime.time(23, 59, 59), 0]]

# bill_daily('2012-05-11 21:00:00','2012-05-12 03:00:00',daily_tariff)
# bill_daily_list('2012-05-11 22:00:00', '2012-05-13 03:00:00', daily_tariff)
