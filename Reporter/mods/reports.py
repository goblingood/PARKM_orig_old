# REPORTER connects guest cards to companies
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
import datetime

try:
    import mods.billalgs as ba
    import mods.savexlsx as sx
except:
    import billalgs as ba
    import savexlsx as sx


def get_companies_list():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=parktime35;UID=sa;PWD=123')
    c = conn.cursor()
    c.execute('''SELECT CM.Name FROM Companies AS CM ORDER BY CM.Name''')
    companies_list = [row.Name for row in c]
    c.close()
    return companies_list


def reports(company, report_path, all_companies, status, rd_start, rd_end):
    if company != 'Все компании':
        reports_company(company, report_path, rd_start, rd_end)
    else:
        for company in all_companies[1:]:
            reports_company(company, report_path, rd_start, rd_end)


def reports_company(company, report_path, rd_start, rd_end):

    daily_tariffs = {'_Постоянные карты': [[datetime.time(0, 0, 0), datetime.time(0, 15, 0), 0],
                     [datetime.time(0, 15, 0), datetime.time(7, 0, 0), 250],
                     [datetime.time(7, 0, 0), datetime.time(23, 59, 59), 0]],
                     '_Всё бесплатно':    [[datetime.time(0, 0, 0), datetime.time(23, 59, 59), 0]]}

    date_frm = '%Y-%m-%d %H:%M:%S'

    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=parktime35;UID=sa;PWD=123')

    c = conn.cursor()
    sql = '''SELECT CM.Name,
                 CS.Name,
                 UPPER(SUBSTRING(MASTER.DBO.FN_VARBINTOHEXSTR(CR.ID), 3, 8)),
                 TRF.Name AS Tariff,
                 T.TimeEntry, T.TimeExit
                 FROM Companies AS CM LEFT JOIN (
                                                 Cards AS CR
                                                 INNER JOIN Transactions AS T ON CR.ID = T.CardID
                                                                              AND T.Type = 2 AND T.TimeEntry < T.TimeExit
                                                                              AND T.TimeEntry > '2000-01-01'
                                                                              AND T.TimeExit BETWEEN ? AND ?
                                                 LEFT JOIN Tariffs AS TRF ON CR.TariffID = TRF.ID
                                                 LEFT JOIN Customers AS CS ON CR.CustomerID = CS.ID
                                                ) ON CM.ID = CR.CompanyID
                 WHERE CR.ID IS NOT NULL AND CM.Name = ?'''  # temporary block empty CR.ID

    c.execute(sql, (rd_start, rd_end, company))

    # r = c.fetchall()
    # rep_data = [list(i) for i in r] # sad but xlsxwriter module require list of list
    # # [i.append(ba.bill_daily_list(datetime.datetime.strftime(i[3], date_frm),datetime.datetime.strftime(i[4], date_frm), daily_tariff)) for i in rep_data]
    # for i in rep_data:
    #   i.append(ba.bill_daily_list(datetime.datetime.strftime(i[3], date_frm),datetime.datetime.strftime(i[4], date_frm), daily_tariff))

    rep_data = [[company], [], ['Компания', 'Сотрудник', 'Номер карты', 'Тариф', 'Время въезда', 'Время выезда', 'Длительность', 'Стоимость']]

    row_count = 0
    for row in c:
        t = list(row)
        t.append(row.TimeExit - row.TimeEntry)
        t.append(ba.bill_daily_list(datetime.datetime.strftime(row.TimeEntry, date_frm),
                 datetime.datetime.strftime(row.TimeExit, date_frm), daily_tariffs[row.Tariff]))
        rep_data.append(t)
        row_count += 1

    c.close()

    rep_data.append(['', '', '', '', '', '', '=SUM(G4:G' + str(row_count + 3) + ')', '=SUM(H4:H' + str(row_count + 3) + ')'])
    print(rep_data)
    sx.save_company_xlsx(report_path + company, rep_data)
