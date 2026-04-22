    def join_query(self, join_type, other_table, on_condition, columns='*', filters=None):
        cursor = self._get_cursor(dictionary=True)
        try:
            query = f"SELECT {columns} FROM {self.table_name} {join_type} {other_table} ON {on_condition}"
            where_clause, params = self._build_where(filters)
            query += f" {where_clause}" if where_clause else ""
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка: {e}")
            return []
        finally:
            cursor.close()

    def union_query(self, other_table, columns='*', distinct=True, filters1=None, filters2=None):
        cursor = self._get_cursor(dictionary=True)
        try:
            op = "UNION" if distinct else "UNION ALL"
            where1, params1 = self._build_where(filters1)
            where2, params2 = self._build_where(filters2)
            query = f"SELECT {columns} FROM {self.table_name} {where1} {op} SELECT {columns} FROM {other_table} {where2}"
            cursor.execute(query, params1 + params2)
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка: {e}")
            return []
        finally:
            cursor.close()

db_config = {
    'host': 'srv221-h-st.jino.ru',
    'user': 'j30084097_13418',
    'password': 'pPS090207/()',
    'database': 'j30084097_13418',
    'port': 3306
}

if __name__ == "__main__":
    TBL_STUDENTS = 'test_students'
    TBL_COURSES = 'test_courses'
    TBL_ARCHIVES = 'test_archives'

    db = SQLTable(db_config, TBL_STUDENTS, db_type='mysql')
    db.drop_table()
    db.create_table('id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), mark INT')

    db.insert({'name': 'Aleksey', 'mark': 5})
    db.insert({'name': 'Prudnikov', 'mark': 2})
    db.insert({'name': 'Vladimirovich', 'mark': 3})
    print("\nСтуденты с оценкой > 4:")
    for s in db.select(condition="mark > 4"):
        print(s)

    db_courses = SQLTable(db_config, TBL_COURSES, db_type='mysql')
    db_courses.drop_table()
    db_courses.create_table('id INT AUTO_INCREMENT PRIMARY KEY, student_id INT, subject VARCHAR(50)')

    db_courses.insert({'student_id': 1, 'subject': 'Spo_bd'})
    db_courses.insert({'student_id': 2, 'subject': 'Programming'})


    print("\nINNER JOIN:")
    join_res = db.join_query(
        join_type='INNER JOIN',
        other_table=TBL_COURSES,
        on_condition=f'{TBL_STUDENTS}.id = {TBL_COURSES}.student_id',
        columns=f'{TBL_STUDENTS}.name, {TBL_COURSES}.subject'
    )

    db_archives = SQLTable(db_config, TBL_ARCHIVES, db_type='mysql')
    db_archives.drop_table()
    db_archives.create_table('id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), mark INT')
    db_archives.insert({'name': 'Katerina', 'mark': 3})
    db_archives.insert({'name': 'Irina', 'mark': 4})

    print("\nUNION (студенты + архив):")
    union_res = db.union_query(
        other_table=TBL_ARCHIVES,
        columns='name, mark',
        distinct=True
    )
    for r in union_res:
        print(r)
    db_archives.drop_table()
    db_courses.drop_table()
    db.drop_table()
    db.disconnect()
