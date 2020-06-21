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
import numpy as np
from database.models import Users


def query_to_list_of_name(query):
    result_list =[]

    try:
        for i in query:
            value = i.name
            result_list.append(value)

    except:
        pass

    return result_list


def query_to_list_of_specialty_all(query):
    result_list = []

    try:
        for i in query:
            list_i = []
            code: str = i.code
            name: str = i.name
            list_i.append(code)
            list_i.append(name)

            result_list.append(list_i)

    except:
        pass

    result_list = np.array(result_list)

    return result_list


def query_to_list_of_group_all(query):
    result_list = []

    try:
        for i in query:
            list_i = []
            number: str = i.number
            note: str = i.note

            list_i.append(number)
            list_i.append(note)

            result_list.append(list_i)

    except:
        pass

    result_list = np.array(result_list)

    return result_list


def get_user_or_None(session, login):
    try:
        user = session.query(Users).filter_by(login=login).first()
        return user

    except:
        return None
