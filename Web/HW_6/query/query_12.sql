SELECT s.name AS student_name, g.name AS group_name, grades.grade, grades.date_received
FROM grades
JOIN students s ON grades.student_id = s.student_id
JOIN groups g ON s.group_id = g.group_id
JOIN subjects sub ON grades.subject_id = sub.subject_id
WHERE sub.name = 'tough'
AND g.name = 'out Group'
AND grades.date_received = (SELECT MAX(date_received) FROM grades)
