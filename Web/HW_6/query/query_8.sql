SELECT AVG(grade) AS avg_grade
FROM grades
INNER JOIN subjects ON grades.subject_id = subjects.subject_id
INNER JOIN teachers ON subjects.teacher_id = teachers.teacher_id
WHERE teachers.name = 'Sara Ford';
