SELECT s.name AS student_name, t.name AS teacher_name, sub.name AS subject_name
FROM students s
JOIN grades g ON s.student_id = g.student_id
JOIN subjects sub ON g.subject_id = sub.subject_id
JOIN teachers t ON sub.teacher_id = t.teacher_id
WHERE s.name = 'David Mcdaniel' AND t.name = 'Sara Ford';
