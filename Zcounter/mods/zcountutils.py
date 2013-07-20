# ZCOUNTER counts busy/total
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


import pyodbc
import sqlite3
import datetime


def query_count():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=parktime35;UID=sa;PWD=123')
    c = conn.cursor()
    sql = """SELECT PARK.Name, CNT_PARK, CNT_FULL
             FROM (SELECT CM.Name, COUNT(CR.ID) AS CNT_PARK FROM Companies AS CM
                       LEFT JOIN Cards AS CR ON CM.ID = CR.CompanyID AND ZoneID=1 GROUP BY CM.Name) AS PARK
                   INNER JOIN
                  (SELECT CM.Name, COUNT(CR.ID) AS CNT_FULL FROM Companies AS CM
                       LEFT JOIN Cards AS CR ON CM.ID = CR.CompanyID GROUP BY CM.Name) AS TOTAL
                   ON PARK.name = TOTAL.name
             ORDER BY PARK.Name"""

    c.execute(sql)
    counter_data = [list(row) for row in c]
    c.close()
    return counter_data


def query_company_inpark(company):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=parktime35;UID=sa;PWD=123')
    c = conn.cursor()
    sql = """SELECT UPPER(SUBSTRING(MASTER.DBO.FN_VARBINTOHEXSTR(CR.ID), 3, 8)) , CS.Name, CR.TimeEntry
             FROM Companies AS CM JOIN (
                                        CARDS AS CR
                                        LEFT JOIN Customers AS CS ON CR.CustomerID = CS.ID
                                       ) ON CM.ID = CR.CompanyID and ZoneID=1
             WHERE CM.Name = ?
             ORDER BY CR.TimeEntry ASC"""

    c.execute(sql, company)
    inpark_data = [list(row) for row in c]
    c.close()
    return inpark_data
