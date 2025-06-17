from mydatabase import conn, cursor

def get_student_by_name(name):
    cursor.execute('SELECT name, age, grade FROM students WHERE name = ?', (name,))
    result = cursor.fetchone()
    if result:
        return {'name': result[0], 'age': result[1], 'grade': result[2]}
    else:
        return None

def update_student_grade(name, new_grade):
    cursor.execute('UPDATE students SET grade = ? WHERE name = ?', (new_grade, name))
    conn.commit()
    return cursor.rowcount

def delete_student(name):
    cursor.execute('DELETE FROM students WHERE name = ?', (name,))
    conn.commit()
    return cursor.rowcount


if __name__ == '__main__':
    print(get_student_by_name('Alice'))      # {'name': 'Alice', 'age': 20, 'grade': 'A'}
    update_student_grade('Bob', 'A-')
    print(get_student_by_name('Bob'))        # {'name': 'Bob', 'age': 22, 'grade': 'A-'}
    delete_student('Charlie')
    print(get_student_by_name('Charlie'))    # None

    conn.close()
