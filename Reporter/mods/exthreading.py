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


import threading
import sys


class Exthread(threading.Thread):
    def __init__(self, target=None, args=(), daemon=None, exceptioninfo=None):
        self.exceptioninfo = exceptioninfo
        threading.Thread.__init__(self, target=target, args=args, daemon=daemon)

    def run(self):
        try:
            threading.Thread.run(self)
        except:
            self.exceptioninfo.put(sys.exc_info()[1])
            self.exceptioninfo.join()