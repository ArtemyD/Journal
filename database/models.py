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

import numpy as np
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy.orm import relationship

from transform.date import str_to_date, str_to_date_2, str_to_time
from transform.msg_error import bd_error

Base = declarative_base()


def get_user_password(session, login):
    user = session.query(Users).filter_by(login=login).first()

    try:
        return user

    except:
        return None


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)


class Discipline(Base):
    __tablename__ = 'discipline'
    id_discipline = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def show_all(self, session):
        try:
            list_name = session.query(Discipline.name).all()
            return list_name
        except Exception as e:
            session.rollback()
            print(str(e))

    def show_name(self, session):
        try:
            list_all = session.query(Discipline).all()
            ls = []
            for i in list_all:
                ls.append(i.name)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    def add(self, session, name):
        new_discipline = Discipline(name=name)
        session.add(new_discipline)
        session.commit()
        session.flush()

    def update(self, session, old_name, new_name):
        s = session.query(Discipline).filter_by(name=old_name)
        s.update({Discipline.name: new_name})
        session.commit()

    def delete(self, session, name):
        try:
            s = session.query(Discipline).filter_by(name=name)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()


class Specialty(Base):
    __tablename__ = 'specialty'
    id_specialty = Column(Integer, primary_key=True)
    code = Column(String(20), nullable=False)
    name = Column(String(255), nullable=False)

    def show_all(self, session):
        try:
            list_all = session.query(Specialty).all()
            return list_all

        except Exception as e:
            session.rollback()
            print(str(e))

    def show_name(self, session):
        try:
            list_all = session.query(Specialty).all()
            ls_name = []
            for i in list_all:
                ls_name.append(i.name)

            return ls_name

        except Exception as e:
            session.rollback()
            print(str(e))

    def add(self, session, code, name):
        try:
            new_specialty = Specialty(code=code, name=name)
            session.add(new_specialty)
            session.commit()
            session.flush()
        except Exception as e:
            session.rollback()

    def update(self,session, old_code, code, name):
        s = session.query(Specialty).filter_by(code=old_code)
        s.update({Specialty.name: name, Specialty.code: code})
        session.commit()

    def delete(self, session, name):
        try:
            s = session.query(Specialty).filter_by(name=name)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()


class Group(Base):
    __tablename__ = 'app_group'
    id_group = Column(Integer, primary_key=True)
    number = Column(String(100), nullable=False)
    note = Column(String(255), nullable=True)
    id_specialty = Column(Integer, ForeignKey('specialty.id_specialty'), nullable=False, primary_key=True)
    specialty = relationship(Specialty, primaryjoin=id_specialty == Specialty.id_specialty, backref="p_specialty")

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.number, self.note, self.specialty.name)

    def show_all(self, session):
        try:
            list = session.query(Group).all()
            ls = []
            for i in list:
                ls1 = []
                ls1.append(i.specialty.name)
                ls1.append(i.number)

                if i.note is None:
                    ls1.append('')
                else:
                    ls1.append(i.note)
                ls.append(ls1)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    def show_name(self, session):
        try:
            list_all = session.query(Group).all()
            ls = []
            for i in list_all:
                ls.append(i.number)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    def add(self, session, number, note, spec):
        try:
            s = session.query(Specialty).filter_by(name=spec).first()
            id_spec = s.id_specialty
            new_group = Group(number=number, note=note, id_specialty=id_spec)
            session.add(new_group)
            session.commit()
            session.flush()
        except Exception as e:
            bd_error()

    def update(self, session, old_number, number, note, spec):
        try:
            s = session.query(Specialty).filter_by(name=spec).first()
            id_spec = s.id_specialty
            g = session.query(Group).filter_by(number=old_number)
            g.update({Group.number: number, Group.note: note, Group.id_specialty: id_spec})
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()

    def delete(self, session, number):
        try:
            s = session.query(Group).filter_by(number=number)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()


class Student(Base):
    __tablename__ = 'student'
    id_student = Column(Integer, primary_key=True)
    fio = Column(String(255), nullable=True)
    number = Column(String(100), nullable=False)
    note = Column(String(255), nullable=True)
    id_group = Column(Integer, ForeignKey('app_group.id_group'), nullable=False, primary_key=True)
    group = relationship(Group, primaryjoin=id_group == Group.id_group, backref="p_group")

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.number, self.note, self.group.number)

    @staticmethod
    def show_all(session, group_number: str):
        try:
            student_list: list = session.query(Student).all()
            ls: list = []
            for i in student_list:
                if i.group.number == group_number:
                    ls1: list = []
                    ls1.append(i.fio)
                    ls1.append(i.number)

                    if i.note is None:
                        ls1.append('')
                    else:
                        ls1.append(i.note)
                    ls.append(ls1)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def show_name(session, group_number: str):
        try:
            student_list: list = session.query(Student).all()
            ls: list = []
            for i in student_list:
                if i.group.number == group_number:
                    ls.append(i.fio)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def delete(session, number):
        try:
            s = session.query(Student).filter_by(number=number)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def add(session, fio, number, note, group_number):
        try:
            g = session.query(Group).filter_by(number=group_number).first()
            id_group = g.id_group
            new_student = Student(fio=fio, number=number, note=note, id_group=id_group)
            session.add(new_student)
            session.commit()
            session.flush()

        except Exception as e:
            bd_error()

    @staticmethod
    def update(session, old_number, fio, number, note):
        try:
            s = session.query(Student).filter_by(number=old_number)
            s.update({Student.number: number, Student.note: note, Student.fio: fio})
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()


class GradeScale(Base):
    __tablename__ = 'grade_scale'
    id_grade_scale = Column(Integer, primary_key=True)
    min = Column(Integer, nullable=False)
    max = Column(Integer, nullable=False)

    @staticmethod
    def all(session):
        try:
            grade_scale_list: list = session.query(GradeScale).all()
            ls: list = []
            for i in grade_scale_list:
                min = str(i.min)
                max = str(i.max)
                value = min + "-" + max
                ls.append(value)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()


class Work(Base):
    __tablename__ = 'work'
    id_work = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    task = Column(String(500), nullable=True)
    note = Column(String(255), nullable=True)
    isdeadline = Column(Boolean)
    deadline = Column(Date, nullable=True)
    id_group = Column(Integer, ForeignKey('app_group.id_group'), nullable=False, primary_key=True)
    group = relationship(Group, primaryjoin=id_group == Group.id_group, backref="p_work_group")
    id_discipline = Column(Integer, ForeignKey('discipline.id_discipline'), nullable=False, primary_key=True)
    discipline = relationship(Discipline, primaryjoin=id_discipline == Discipline.id_discipline, backref="p_discipline")
    id_grade_scale = Column(Integer, ForeignKey('grade_scale.id_grade_scale'), nullable=False, primary_key=True)
    grade_scale = relationship(GradeScale, primaryjoin=id_grade_scale == GradeScale.id_grade_scale,
                               backref="p_work_grade_scale")

    def __repr__(self):
        return "<User('%s')>" % self.name

    @staticmethod
    def show_name(session, group_number: str, discipline_name: str, flag_header=False):
        try:
            work_all: list = session.query(Work).join(Group).join(Discipline).filter(
                Group.number == group_number).filter(
                Discipline.name == discipline_name).order_by(Work.id_work).all()

            work_count: int = len(work_all)

            if flag_header:
                ls = []
                ls.append('ФИО студента')
            else:
                ls = []

            # Заполняем шапку таблицы
            for i in range(work_count):
                ls.append(work_all[i].name)
                if flag_header:
                    ls.append('Дата защиты')
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def get(session, group_number, discipline_name, work_choosen):
        try:
            w = session.query(Work).join(Group).join(Discipline).filter(
                Group.number == group_number).filter(
                Discipline.name == discipline_name).filter(Work.name == work_choosen).first()
            return w

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def get_from_id(session, id_work):
        try:
            w = session.query(Work).filter_by(id_work=id_work).first()
            return w

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def add(session, discipline_name, group_number, name, task, note, grade_scale, new_date, isdeadline):
        try:
            new_date = str_to_date(new_date)
            g = session.query(Group).filter_by(number=group_number).first()
            id_group = g.id_group
            d = session.query(Discipline).filter_by(name=discipline_name).first()
            id_discipline = d.id_discipline
            max = grade_scale.split('-', 1)
            max = max[1]
            gr = session.query(GradeScale).filter_by(max=max).first()
            id_grade_scale = gr.id_grade_scale
            new_work = Work(id_group=id_group, id_discipline=id_discipline, id_grade_scale=id_grade_scale, name=name,
                            task=task, note=note, deadline=new_date, isdeadline=isdeadline)
            session.add(new_work)
            session.commit()
            session.flush()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def update(session, id_work, name, task, note, grade_scale, new_date, isdeadline):
        try:
            new_date = str_to_date(new_date)
            max = grade_scale.split('-', 1)
            max = max[1]
            gr = session.query(GradeScale).filter_by(max=max).first()
            id_grade_scale = gr.id_grade_scale

            s = session.query(Work).filter_by(id_work=id_work)
            s.update({Work.name: name, Work.task: task, Work.note: note, Work.deadline: new_date,
                      Work.isdeadline: isdeadline,
                      Work.id_grade_scale: id_grade_scale})
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def delete(session, id_work):
        try:
            grade = session.query(Grade).join(Work).filter(Work.id_work == id_work).all()
            for i in grade:
                id_grade = i.id_grade
                s = session.query(Grade).filter_by(id_grade=id_grade)
                s.delete()

            s = session.query(Work).filter_by(id_work=id_work)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()


class Grade(Base):
    __tablename__ = 'grade'
    id_grade = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    feedback = Column(String(500), nullable=True)
    note = Column(String(255), nullable=True)
    path_file = Column(String(255), nullable=True)
    id_work = Column(Integer, ForeignKey('work.id_work'), nullable=False, primary_key=True)
    work = relationship(Work, primaryjoin=id_work == Work.id_work, backref="parent_grade_work")
    id_student = Column(Integer, ForeignKey('student.id_student'), nullable=False, primary_key=True)
    student = relationship(Student, primaryjoin=id_student == Student.id_student, backref="parent_grade_student")

    @staticmethod
    def all(session, discipline, group_number):
        try:
            student_all: list = session.query(Student).join(Group).filter(Group.number == group_number).order_by(
                Student.fio).all()

            work_all: list = session.query(Work).join(Group).join(Discipline).filter(
                Group.number == group_number).filter(Discipline.name == discipline).order_by(Work.id_work).all()

            ls = []

            for i in student_all:
                row = []
                row.append(i.fio)

                for j in work_all:
                    grade = session.query(Grade).join(Student).join(Work). \
                        filter(Student.id_student == i.id_student).filter(Work.id_work == j.id_work).first()

                    if grade:
                        row.append(str(grade.value))
                        row.append(str(grade.date))
                    else:
                        row.append('')
                        row.append('')

                ls.append(row)

            ls = np.array(ls)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def get(session, id_work, student_name):
        try:
            g = session.query(Grade).join(Work).join(Student).filter(
                Work.id_work == id_work).filter(
                Student.fio == student_name).first()
            return g

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def add(session, id_work, student, value, new_date, new_path_file, note, feedback):
        try:
            st = session.query(Student).filter(Student.fio == student).first()
            id_student = st.id_student

            date = str_to_date(new_date)

            new_grade = Grade(date=date, id_student=id_student, id_work=id_work, value=value, path_file=new_path_file,
                              note=note, feedback=feedback)
            session.add(new_grade)
            session.commit()
            session.flush()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def update(session, id_grade, value, new_date, new_path_file, note, feedback):
        try:
            new_date = str_to_date(new_date)
            s = session.query(Grade).filter_by(id_grade=id_grade)
            if new_path_file == '':
                s.update(
                    {Grade.value: value, Grade.note: note, Grade.feedback: feedback,
                     Grade.date: new_date})
            else:
                s.update(
                    {Grade.value: value, Grade.path_file: new_path_file, Grade.note: note, Grade.feedback: feedback,
                     Grade.date: new_date})
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def delete(session, id_grade):
        try:
            s = session.query(Grade).filter_by(id_grade=id_grade)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()


class HistoryGrade(Base):
    __tablename__ = 'history_grade'
    id_history_grade = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    action = Column(String(15), nullable=True)
    id_work = Column(Integer, ForeignKey('work.id_work'), nullable=False, primary_key=True)
    work = relationship(Work, primaryjoin=id_work == Work.id_work, backref="parent_history_work")
    id_student = Column(Integer, ForeignKey('student.id_student'), nullable=False, primary_key=True)
    student = relationship(Student, primaryjoin=id_student == Student.id_student, backref="parent_history_student")

    @staticmethod
    def add(session, id_work, student, value, action, date):
        try:
            st = session.query(Student).filter(Student.fio == student).first()
            id_student = st.id_student

            date = str_to_date(date)

            new_history_grade = HistoryGrade(date=date, id_student=id_student, id_work=id_work, value=value,
                                             action=action)
            session.add(new_history_grade)
            session.commit()
            session.flush()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def all(session, discipline, group_number):
        try:
            student_all: list = session.query(Student).join(Group).filter(Group.number == group_number).order_by(
                Student.fio).all()

            work_all: list = session.query(Work).join(Group).join(Discipline).filter(
                Group.number == group_number).filter(
                Discipline.name == discipline).all()

            ls = []

            history_all: list = session.query(HistoryGrade).all()

            for i in history_all:
                for j in work_all:
                    if i.id_work == j.id_work:
                        for k in student_all:
                            if i.id_student == k.id_student:
                                row = []
                                row.append(k.fio)
                                row.append(j.name)
                                row.append(i.action)
                                row.append(str(i.date))
                                row.append(i.value)

                                ls.append(row)

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()


# Тема инструктажа
class Safety(Base):
    __tablename__ = 'safety'
    id_safety = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    id_group = Column(Integer, ForeignKey('app_group.id_group'), nullable=False, primary_key=True)
    group = relationship(Group, primaryjoin=id_group == Group.id_group, backref="p_safety_group")
    id_discipline = Column(Integer, ForeignKey('discipline.id_discipline'), nullable=False, primary_key=True)
    discipline = relationship(Discipline, primaryjoin=id_discipline == Discipline.id_discipline,
                              backref="p_safety_discipline")

    @staticmethod
    def all_name(session, discipline, group_number, flag_header=False):
        try:
            safety_all: list = session.query(Safety).join(Group).join(Discipline).filter(
                Group.number == group_number).filter(
                Discipline.name == discipline).all()

            safety_count: int = len(safety_all)

            if flag_header:
                ls = []
                ls.append('ФИО студента')
            else:
                ls = []

            # Заполняем шапку таблицы
            for i in range(safety_count):
                ls.append(safety_all[i].name)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def add(session, discipline, group_number, name):
        try:
            g = session.query(Group).filter_by(number=group_number).first()
            id_group = g.id_group
            d = session.query(Discipline).filter_by(name=discipline).first()
            id_discipline = d.id_discipline
            new_safety = Safety(name=name, id_group=id_group, id_discipline=id_discipline)
            session.add(new_safety)
            session.commit()
            session.flush()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def delete(session, choosen_safe, discipline_name, group_number):
        try:
            s = session.query(Safety).join(Discipline).join(Group).filter(Discipline.name == discipline_name) \
                .filter(Group.number == group_number).filter(Safety.name == choosen_safe).first()
            id_safety = s.id_safety

            pass_safety = session.query(PassSafety).join(Safety).filter(Safety.id_safety == id_safety).all()
            for i in pass_safety:
                id_pass_safety = i.id_pass_safety
                s = session.query(PassSafety).filter_by(id_pass_safety=id_pass_safety)
                s.delete()

            s = session.query(Safety).filter_by(id_safety=id_safety)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()


# Инструктаж
class PassSafety(Base):
    __tablename__ = 'pass_safety'
    id_pass_safety = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    id_student = Column(Integer, ForeignKey('student.id_student'), nullable=False, primary_key=True)
    student = relationship(Student, primaryjoin=id_student == Student.id_student, backref="p_pass_student")
    id_safety = Column(Integer, ForeignKey('safety.id_safety'), nullable=False, primary_key=True)
    safety = relationship(Safety, primaryjoin=id_safety == Safety.id_safety,
                          backref="p_pass_safety")

    @staticmethod
    def add(session, student, safety, date, discipline, group_number):
        try:
            s = session.query(Safety).join(Group).filter(Group.number == group_number). \
                filter(Discipline.name == discipline).filter(Safety.name == safety).first()

            id_safety = s.id_safety
            st = session.query(Student).filter(Student.fio == student).first()
            id_student = st.id_student

            date = str_to_date(date)

            new_pass_safety = PassSafety(date=date, id_student=id_student, id_safety=id_safety)
            session.add(new_pass_safety)
            session.commit()
            session.flush()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def all(session, discipline, group_number):
        try:
            student_all: list = session.query(Student).join(Group).filter(Group.number == group_number).order_by(
                Student.fio).all()

            safety_all: list = session.query(Safety).join(Group).join(Discipline).filter(
                Group.number == group_number).filter(
                Discipline.name == discipline).all()

            ls = []

            for i in student_all:
                row = []
                row.append(i.fio)

                for j in safety_all:
                    pass_safety = session.query(PassSafety).join(Student).join(Safety). \
                        filter(Student.id_student == i.id_student).filter(Safety.id_safety == j.id_safety).first()

                    if pass_safety:
                        row.append(str(pass_safety.date))
                    else:
                        row.append('')

                ls.append(row)

            ls = np.array(ls)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def update(session, fio, safety, new_date, discipline_name, group_number):
        try:
            s = session.query(PassSafety).join(Safety).join(Discipline).join(Group).join(Student).filter(
                Discipline.name == discipline_name) \
                .filter(Group.number == group_number).filter(Safety.name == safety).filter(Student.fio == fio).first()
            id = s.id_pass_safety

            s = session.query(PassSafety).filter_by(id_pass_safety=id)
            new_date = str_to_date(new_date)
            s.update({PassSafety.date: new_date})
            session.commit()

        except Exception as e:
            print(e)
            session.rollback()
            bd_error()


# Аудитории
class Audience(Base):
    __tablename__ = 'audience'
    id_audience = Column(Integer, primary_key=True)
    corps = Column(String(20), nullable=False)
    number = Column(String(20), nullable=False)

    @staticmethod
    def show_all(session):
        try:
            list = session.query(Audience).all()
            ls = []
            for i in list:
                ls1 = []
                ls1.append(i.corps)
                ls1.append(i.number)
                ls.append(ls1)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def show_name(session):
        try:
            list_all = session.query(Audience).order_by(Audience.corps).all()
            ls = []
            for i in list_all:
                value = i.corps + ' ' + i.number
                ls.append(value)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def add(session, corps, number):
        try:
            new_audience = Audience(corps=corps, number=number)
            session.add(new_audience)
            session.commit()
            session.flush()
        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def update(session, old_number, corps, number):
        try:
            s = session.query(Audience).filter_by(number=old_number)
            s.update({Audience.corps: corps, Audience.number: number})
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def delete(session, number):
        try:
            s = session.query(Audience).filter_by(number=number)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()


# Формат занятий
class ClassFormat(Base):
    __tablename__ = 'class_format'
    id_class_format = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    @staticmethod
    def show_all(session):
        try:
            list = session.query(ClassFormat).all()
            ls = []
            for i in list:
                ls1 = []
                ls1.append(i.name)
                ls.append(ls1)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def show_name(session):
        try:
            list_all = session.query(ClassFormat).all()
            ls = []
            for i in list_all:
                ls.append(i.name)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def add(session, name):
        try:
            new = ClassFormat(name=name)
            session.add(new)
            session.commit()
            session.flush()
        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def update(session, old_name, name):
        try:
            s = session.query(ClassFormat).filter_by(name=old_name)
            s.update({ClassFormat.name: name})
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def delete(session, name):
        try:
            s = session.query(ClassFormat).filter_by(name=name)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()


# Настройки формата расписания
class Settings(Base):
    __tablename__ = 'settings'
    id_schedule_format = Column(Integer, primary_key=True)
    schedule_format = Column(Boolean)

    @staticmethod
    def get(session):
        try:
            settings = session.query(Settings).first()
            return settings.schedule_format

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def set(session, new_value):
        try:
            s = session.query(Settings)
            s.update({Settings.schedule_format: new_value})
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()


# День в расписании
class ScheduledDay(Base):
    __tablename__ = 'scheduled_day'
    id_scheduled_day = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    week_number = Column(Boolean)

    @staticmethod
    def add_day_from_period(session, date_begin, date_end):
        day_begin = int(date_begin.split(',')[2].split(')')[0])
        month_begin = int(date_begin.split(',')[1])
        year_begin = int(date_begin.split(',')[0].split('(')[1])

        day_end = int(date_end.split(',')[2].split(')')[0])
        month_end = int(date_end.split(',')[1])
        year_end = int(date_end.split(',')[0].split('(')[1])

        begin = datetime.date(year_begin, month_begin, day_begin)
        end = datetime.date(year_end, month_end, day_end)

        day = begin
        week_flag = False
        while day != end:
            weekday = day.weekday()
            if weekday != 6:
                new = ScheduledDay(date=day, week_number=week_flag)
                session.add(new)
                session.commit()
                session.flush()
            else:
                if week_flag == False:
                    week_flag = True
                else:
                    week_flag = False

            day += datetime.timedelta(days=1)


# Занятие
class Occupation(Base):
    __tablename__ = 'occup'
    id_occup = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(String(10), nullable=False)
    id_scheduled_day = Column(Integer, ForeignKey('scheduled_day.id_scheduled_day'), nullable=False, primary_key=True)
    scheduled_day = relationship(ScheduledDay, primaryjoin=id_scheduled_day == ScheduledDay.id_scheduled_day, backref="p_scheduled_day_occupation")
    id_discipline = Column(Integer, ForeignKey('discipline.id_discipline'), nullable=False, primary_key=True)
    discipline = relationship(Discipline, primaryjoin=id_discipline == Discipline.id_discipline,
                          backref="p_discipline_occupation")
    id_class_format = Column(Integer, ForeignKey('class_format.id_class_format'), nullable=False, primary_key=True)
    class_format = relationship(ClassFormat, primaryjoin=id_class_format == ClassFormat.id_class_format,
                              backref="p_class_format_occupation")
    id_group = Column(Integer, ForeignKey('app_group.id_group'), nullable=False, primary_key=True)
    group = relationship(Group, primaryjoin=id_group == Group.id_group, backref="p_group_occupation")
    id_audience = Column(Integer, ForeignKey('audience.id_audience'), nullable=False, primary_key=True)
    audience = relationship(Audience, primaryjoin=id_audience == Audience.id_audience, backref="p_audience_occupation")

    @staticmethod
    def add_once(session, discipline, format, audience, group, date, time):
        try:
            d = session.query(Discipline).filter(Discipline.name == discipline).first()
            f = session.query(ClassFormat).filter(ClassFormat.name == format).first()
            corps = audience.split(' ')[0]
            number = audience.split(' ')[1]
            a = session.query(Audience).filter(Audience.corps == corps).filter(Audience.number == number).first()
            g = session.query(Group).filter(Group.number == group).first()

            id_discipline = d.id_discipline
            id_class_format = f.id_class_format
            id_audience = a.id_audience
            id_group = g.id_group

            date = str(date)
            date = str_to_date(date)

            s = session.query(ScheduledDay).filter_by(date=date).first()
            id_scheduled_day = s.id_scheduled_day
            # session.rollback()

            new_occupation = Occupation(time=time, id_scheduled_day=id_scheduled_day, id_discipline=id_discipline,
                                        id_class_format=id_class_format, id_audience=id_audience, id_group=id_group)

            session.add(new_occupation)
            session.commit()
            # session.flush()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def add(session, discipline, format, audience, group, date_begin, date_end, time, weekday, period):
        try:
            d = session.query(Discipline).filter(Discipline.name == discipline).first()
            f = session.query(ClassFormat).filter(ClassFormat.name == format).first()
            corps = audience.split(' ')[0]
            number = audience.split(' ')[1]
            a = session.query(Audience).filter(Audience.corps == corps).filter(Audience.number == number).first()
            g = session.query(Group).filter(Group.number == group).first()

            id_discipline = d.id_discipline
            id_class_format = f.id_class_format
            id_audience = a.id_audience
            id_group = g.id_group

            begin = datetime.date(date_begin[0], date_begin[1], date_begin[2])
            end = datetime.date(date_end[0], date_end[1], date_end[2])

            day = begin
            while day != end:
                d = day.weekday()
                if d == weekday:
                    s = session.query(ScheduledDay).filter_by(date=day).first()
                    id_scheduled_day = s.id_scheduled_day
                    week_number = s.week_number
                    if period == "Каждую неделю":
                        new_occupation = Occupation(time=time, id_scheduled_day=id_scheduled_day,
                                                    id_discipline=id_discipline,
                                                    id_class_format=id_class_format, id_audience=id_audience,
                                                    id_group=id_group)
                        session.add(new_occupation)
                        session.commit()
                        session.flush()
                    elif period == '1-ая неделя':
                        if week_number == False:
                            new_occupation = Occupation(time=time, id_scheduled_day=id_scheduled_day,
                                                        id_discipline=id_discipline,
                                                        id_class_format=id_class_format, id_audience=id_audience,
                                                        id_group=id_group)
                            session.add(new_occupation)
                            session.commit()
                            session.flush()
                    else:
                        if week_number == True:
                            new_occupation = Occupation(time=time, id_scheduled_day=id_scheduled_day,
                                                        id_discipline=id_discipline,
                                                        id_class_format=id_class_format, id_audience=id_audience,
                                                        id_group=id_group)
                            session.add(new_occupation)
                            session.commit()
                            session.flush()
                day += datetime.timedelta(days=1)

        except Exception as e:
            session.rollback()
            bd_error()


    @staticmethod
    def show_all(session, date):
        try:
            s = session.query(ScheduledDay).filter_by(date=date).first()
            id_scheduled_day = s.id_scheduled_day

            o_list = session.query(Occupation).join(ScheduledDay).filter(ScheduledDay.id_scheduled_day == id_scheduled_day).\
                order_by(Occupation.time).all()
            ls = []
            for i in o_list:
                ls1 = []
                time = str(i.time)
                time_1 = time.split(':')[0]
                time_2 = time.split(':')[1]
                time = time_1 + ':' + time_2
                ls1.append(str(time))
                ls1.append(i.discipline.name)
                ls1.append(i.class_format.name)
                ls1.append(i.group.number)
                ls1.append(i.audience.corps + " " + i.audience.number)
                ls.append(ls1)

            return ls

        except Exception as e:
            session.rollback()
            return []

    @staticmethod
    def delete(session, time, discipline, group):
        try:
            d = session.query(Discipline).filter_by(name=discipline).first()
            id_discipline = d.id_discipline

            g = session.query(Group).filter_by(number=group).first()
            id_group = g.id_group

            t = session.query(Occupation).filter_by(id_group=id_group).filter_by(id_discipline=id_discipline)
            t.delete()
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def get(session, time, discipline, group):
        try:
            d = session.query(Discipline).filter_by(name=discipline).first()
            id_discipline = d.id_discipline

            g = session.query(Group).filter_by(number=group).first()
            id_group = g.id_group

            t = session.query(Occupation).filter_by(id_group=id_group).filter_by(id_discipline=id_discipline).first()
            return t

        except Exception as e:
            session.rollback()
            bd_error()


    @staticmethod
    def update(session, discipline_old, group_old, class_format_old, discipline, group,
                 class_format, audience):
        try:
            d_old = session.query(Discipline).filter_by(name=discipline_old).first()
            id_discipline_old = d_old.id_discipline
            d = session.query(Discipline).filter_by(name=discipline).first()
            id_discipline = d.id_discipline

            g_old = session.query(Group).filter_by(number=group_old).first()
            id_group_old = g_old.id_group
            g = session.query(Group).filter_by(number=group).first()
            id_group = g.id_group

            c_old = session.query(ClassFormat).filter_by(name=class_format_old).first()
            id_class_format_old = c_old.id_class_format
            c = session.query(ClassFormat).filter_by(name=class_format).first()
            id_class_format = c.id_class_format

            corps = audience.split(' ')[0]
            number = audience.split(' ')[1]
            a = session.query(Audience).filter(Audience.corps == corps).filter(Audience.number == number).first()
            id_audience = a.id_audience

            t = session.query(Occupation).filter_by(id_group=id_group_old).filter_by(id_discipline=id_discipline_old).\
                filter_by(id_class_format=id_class_format_old)
            t.update({Occupation.id_group: id_group, Occupation.id_discipline: id_discipline,
                      Occupation.id_class_format: id_class_format, Occupation.id_audience: id_audience})
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()


# Посещение
class Attendance(Base):
    __tablename__ = 'attendance'
    id_attendance = Column(Integer, primary_key=True)
    attended = Column(Boolean)
    id_occupation = Column(Integer, ForeignKey('occup.id_occup'), nullable=False, primary_key=True)
    occupation = relationship(Occupation, primaryjoin=id_occupation == Occupation.id_occup,
                              backref="p_occupation_attendance")
    id_student = Column(Integer, ForeignKey('student.id_student'), nullable=False, primary_key=True)
    student = relationship(Student, primaryjoin=id_student == Student.id_student,
                          backref="p_student_attendance")

    @staticmethod
    def show_name(session, group_number, discipline_name, flag_header=False):
        try:
            occupation_all: list = session.query(Occupation).join(Group).join(Discipline).join(ScheduledDay).filter(
                Group.number == group_number).filter(
                Discipline.name == discipline_name).order_by(ScheduledDay.date).all()

            occupation_count: int = len(occupation_all)

            if flag_header:
                ls = []
                ls.append('ФИО студента')
            else:
                ls = []

            # Заполняем шапку таблицы
            for i in range(occupation_count):
                value = str(occupation_all[i].scheduled_day.date)
                value += "|" + occupation_all[i].class_format.name
                ls.append(value)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def all(session, discipline_name, group_number):
        try:
            student_all: list = session.query(Student).join(Group).filter(Group.number == group_number).order_by(
                Student.fio).all()

            occupation_all: list = session.query(Occupation).join(Group).join(Discipline).join(ScheduledDay).filter(
                Group.number == group_number).filter(
                Discipline.name == discipline_name).order_by(ScheduledDay.date).all()

            ls = []

            for i in student_all:
                row = []
                row.append(i.fio)
                id_student = i.id_student

                for j in occupation_all:
                    id_occup = j.id_occup
                    try:
                        a = session.query(Attendance).filter(Attendance.id_occupation==id_occup).filter(Attendance.id_student==id_student).first()
                    except:
                        a = []

                    if a == None:
                        row.append(' ')
                    elif a.attended == False:
                        row.append('Н')
                    else:
                        row.append(' ')

                ls.append(row)

            ls = np.array(ls)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def update(session, date, class_format, student):
        try:
            c = session.query(ClassFormat).filter_by(name=class_format).first()
            id_class_format = c.id_class_format
            s = session.query(Student).filter_by(fio=student).first()
            id_student = s.id_student
            date = str_to_date_2(date)
            sc = session.query(ScheduledDay).filter_by(date=date).first()
            id_scheduled_day = sc.id_scheduled_day

            o = session.query(Occupation).join(ScheduledDay).filter(Occupation.id_class_format == id_class_format).\
                filter(Occupation.id_scheduled_day == id_scheduled_day).first()
            id_occupation = o.id_occup
            au = session.query(Attendance).filter(Attendance.id_occupation==id_occupation).filter(Attendance.id_student==id_student)
            auu = session.query(Attendance).filter(Attendance.id_occupation==id_occupation).filter(Attendance.id_student==id_student).first()

            if auu == None:
                new_attendance = Attendance(attended=False, id_occupation=id_occupation, id_student=id_student)
                session.add(new_attendance)
                session.commit()
                session.flush()
            else:
                if auu.attended == True:
                    au.update({Attendance.attended: False})
                    session.commit()
                else:
                    au.update({Attendance.attended: True})
                    session.commit()

        except Exception as e:
            session.rollback()
            bd_error()
