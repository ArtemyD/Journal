"""
Copyright 2020 Artem Dyachenko

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
import datetime


def str_to_date(input: str):
    return datetime.datetime.strptime(input, '(%Y, %m, %d)').date()


def str_to_date_2(input: str):
    return datetime.datetime.strptime(input, '%Y-%m-%d').date()


def str_to_time(input: str):
    return datetime.datetime.strptime(input,  '%H:%M:%S').time()
