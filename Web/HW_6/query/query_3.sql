SELECT AVG(grade) AS avg_grade
FROM grades
INNER JOIN students ON grades.student_id = students.student_id
INNER JOIN groups ON students.group_id = groups.group_id
INNER JOIN subjects ON grades.subject_id = subjects.subject_id
WHERE subjects.name = 'office';