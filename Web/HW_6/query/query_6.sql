SELECT students.name
FROM students
JOIN groups ON students.group_id = groups.group_id
WHERE groups.name = 'out Group';
