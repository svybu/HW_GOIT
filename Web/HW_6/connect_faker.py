from sqlalchemy import create_engine, text
from faker import  Faker

host = 'localhost'
port = '5432'
database = 'postgres'
user = 'postgres'
password = '1234'

url = f'postgresql://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(url)

class Test_inf():
    def __init__(self):
        self.fake = Faker()
        self.engine = create_engine(url)
        #print('done ')

    def add_groups(self, num_records=30):
        with self.engine.connect() as connection:
            for i in range(num_records):
                name = self.fake.word() + ' Group'
                query = "INSERT INTO groups (name) VALUES (:name)"
                print(name)
                connection.execute(text(query), {"name": name})
            connection.commit()
        print(f'{num_records} записів додано до таблиці groups')

    def add_students(self, num_records=30):
        with self.engine.connect() as connection:
            for i in range(num_records):
                name = self.fake.name()
                group_id = self.fake.random_int(1, 10)
                print(f'{name}, {group_id}')
                query = "INSERT INTO students (name, group_id) VALUES (:name, :group_id)"
                connection.execute(text(query), {"name": name, "group_id": group_id})
            connection.commit()
        print(f'{num_records} записів додано до таблиці students')

    def add_teachers(self, num_records=30):
        with self.engine.connect() as connection:
            for i in range(num_records):
                name = self.fake.name()
                print(f'{name},')
                query = "INSERT INTO teachers (name) VALUES (:name)"
                connection.execute(text(query), {"name": name})
            connection.commit()
        print(f'{num_records} записів додано до таблиці teachers')

    def add_subjects(self, num_records=30):
        with self.engine.connect() as connection:
            for i in range(num_records):
                name = self.fake.word()
                teacher_id = self.fake.random_int(1, 10)
                query = "INSERT INTO subjects (name, teacher_id) VALUES (:name, :teacher_id)"
                connection.execute(text(query), {"name": name, "teacher_id": teacher_id})
            connection.commit()
        print(f'{num_records} записів додано до таблиці subjects')

    def add_grades(self, num_records=30):
        with self.engine.connect() as connection:
            for i in range(num_records):
                student_id = self.fake.random_int(1, 30)
                subject_id = self.fake.random_int(1, 30)
                grade = self.fake.random_int(1, 100)
                date_received = self.fake.date_between(start_date='-1y', end_date='today')
                query = "INSERT INTO grades (student_id, subject_id, grade, date_received) VALUES (:student_id, :subject_id, :grade, :date_received)"
                connection.execute(text(query), {"student_id": student_id, "subject_id": subject_id, "grade": grade, "date_received": date_received})
            connection.commit()
        print(f'{num_records} записів додано до таблиці grades')

    def add_all(self):
        self.add_groups()
        self.add_students()
        self.add_teachers()
        self.add_subjects()
        self.add_grades()

    def select_groups(self):
        with self.engine.connect() as connection:
            query = text("SELECT * FROM groups")
            result = connection.execute(query)
            for row in result:
                print(row)


test = Test_inf()
test.add_all()
test.select_groups()