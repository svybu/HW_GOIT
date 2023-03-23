SELECT students.name, AVG(grades.grade) AS average_grade
FROM students
JOIN grades ON students.student_id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.subject_id
WHERE subjects.name = 'office'
GROUP BY students.name
ORDER BY average_grade DESC
LIMIT 1;
