SELECT s.name
FROM subjects s
JOIN teachers t ON t.teacher_id = s.teacher_id
WHERE t.name = 'Sara Ford';
