# GCARDS connects guest cards to companies
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
import os
import datetime


def tohex(val):
    return hex((val + (1 << 32)) % (1 << 32))[2:].zfill(8).upper()


def toint(val):
    t = int(val, 16)
    if t > 0x7FFFFFFF:
        t -= 0x100000000
    return t


def get_companies_list():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=parktime35;UID=sa;PWD=123')
    c = conn.cursor()
    c.execute("""SELECT CM.Name FROM Companies AS CM ORDER BY CM.Name""")
    companies_list = [row.Name for row in c]
    c.close()
    return companies_list


def get_gcards_list(company):
    gcards_list = []

    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=parktime35;UID=sa;PWD=123')
    c = conn.cursor()
    if company == 'Непривязанные':
        sql = """SELECT CR.ID FROM Cards AS CR
                 WHERE CR.CompanyID = -1 AND CR.CustomerID = -1
                    AND CR.ID NOT IN (SELECT CardID FROM gcards.dbo.gcards)
                 ORDER BY CR.ID"""
        c.execute(sql)
    else:
        sql = """SELECT CR.CardID AS ID
                 FROM gcards.dbo.gcards AS CR JOIN Companies AS CM ON CM.ID = CR.CompanyID
                 WHERE CM.Name=?
                 ORDER BY CR.ID"""
        c.execute(sql, company)
    gcards_list = [tohex(row.ID) for row in c]
    c.close()
    return gcards_list


def register_gcards(gcards, cur, new):
    if cur == new or not gcards:
        return

    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=gcards;UID=sa;PWD=123')
    c = conn.cursor()
    sconn = sqlite3.connect('mods\gcards.db')
    sql = """SELECT ID FROM parktime35.dbo.Companies AS CM WHERE CM.Name = ?"""
    c.execute(sql, new)
    newID = c.fetchone()

    if cur == 'Непривязанные':
        sql = """INSERT INTO gcards (CardID, CompanyID) VALUES (?, ?)"""
        rows = [(toint(i), newID[0]) for i in gcards]
        c.executemany(sql, rows)
        sconn.executemany(sql, rows)
    elif new == 'Непривязанные':
        sql = """DELETE FROM gcards WHERE CardID = ?"""
        rows = [(toint(i),) for i in gcards]
        c.executemany(sql, rows)
        sconn.executemany(sql, rows)
    else:
        sql = """UPDATE gcards SET CompanyID = ? WHERE CardID = ?"""
        rows = [(newID[0], toint(i)) for i in gcards]
        c.executemany(sql, rows)
        sconn.executemany(sql, rows)

    c.commit()
    c.close()
    sconn.commit()
    sconn.close()


def init_sqlitedb(dbpath='mods\gcards.db'):
    # can use (SELECT count(*) FROM sqlite_master WHERE type='table' AND name='table_name')
    # try:
    #     with open(dbpath):  # can without 'with'
    #         pass
    # except IOError:
    #     conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=gcards;UID=sa;PWD=123')
    #     c = conn.cursor()
    #     sconn = sqlite3.connect(dbpath)
    #     sql = """CREATE TABLE IF NOT EXISTS gcards (CardID INTEGER PRIMARY KEY, CompanyID INTEGER NOT NULL,
    #                                                 RecordDate INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP, Active INTEGER DEFAULT 1, Reserved INTEGER)"""
    #     sconn.execute(sql)
    #     sql = """SELECT CardID, CompanyID, RecordDate, Active FROM gcards"""
    #     init_data = c.execute(sql).fetchall()

    #     print(init_data)
    #     sql = """INSERT INTO gcards (CardID, CompanyID, RecordDate, Active) VALUES(?, ?, ?, ?)"""
    #     sconn.executemany(sql, init_data)

    #     c.close()
    #     sconn.commit()
    #     sconn.close()
    # improved I think:
    sconn = sqlite3.connect(dbpath)
    sql = """SELECT COUNT(*) AS CNT FROM sqlite_master WHERE type='table' AND name='gcards'"""
    if sconn.execute(sql).fetchone()[0] == 0:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=gcards;UID=sa;PWD=123')
        c = conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS gcards (CardID INTEGER PRIMARY KEY, CompanyID INTEGER NOT NULL,
                                                    RecordDate INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP, Active INTEGER DEFAULT 1, Reserved INTEGER)"""
        sconn.execute(sql)
        sql = """SELECT CardID, CompanyID, RecordDate, Active FROM gcards"""
        init_data = c.execute(sql).fetchall()

        print(init_data)
        sql = """INSERT INTO gcards (CardID, CompanyID, RecordDate, Active) VALUES(?, ?, ?, ?)"""
        sconn.executemany(sql, init_data)

        c.close()
        sconn.commit()
        sconn.close()


def purge_deleted(isdel):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=gcards;UID=sa;PWD=123')
    c = conn.cursor()

    if isdel:
        # can simple delete but keep history
        # sql = """DELETE FROM gcards WHERE CardID NOT IN (SELECT CR.ID FROM parktime35.dbo.Cards AS CR
        #                                                  WHERE CR.CompanyID = -1 AND CR.CustomerID = -1)"""
        sql = """UPDATE gcards SET Active = 0 WHERE CardID NOT IN (SELECT CR.ID FROM parktime35.dbo.Cards AS CR
                                                                   WHERE CR.CompanyID = -1 AND CR.CustomerID = -1)"""
        c.execute(sql)
        # try:
        os.rename('mods\gcards.db', 'mods\gcards_' + datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H.%M.%S') + '.db')
        init_sqlitedb()
        # except:
        #     print(E)
        #     exit()
    else:
        sconn = sqlite3.connect('mods\gcards.db')
        sql = """SELECT CR.ID FROM parktime35.dbo.Cards AS CR WHERE CR.CompanyID = -1 AND CR.CustomerID = -1"""
        c.execute(sql)
        existing_gcards = [(row.ID,) for row in c]
        print(existing_gcards)
        # some hack (cant use IN!)
        sql = """UPDATE gcards SET Active = 0 WHERE CardID <> ?"""
        c.executemany(sql, existing_gcards)
        sconn.executemany(sql, existing_gcards)
        c.commit()
        sconn.commit()
        sconn.close()

    c.close()


"""
##############################################################################
#MSSQL#

CREATE TABLE gcards.dbo.gcards(
    ID int IDENTITY(1,1) NOT NULL,
    CardID int NOT NULL,
    CompanyID int NOT NULL,
    RecordDate datetime NOT NULL DEFAULT GETUTCDATE(),
    Active int NOT NULL DEFAULT 1,
 CONSTRAINT PK_gcards PRIMARY KEY CLUSTERED (ID)
)


##############################################################################
#SQLITE#

CREATE TABLE gcards (CardID INTEGER PRIMARY KEY, CompanyID INTEGER NOT NULL,
                     RecordDate TEXT NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), Active INTEGER DEFAULT 1, Reserved INTEGER)

"""
