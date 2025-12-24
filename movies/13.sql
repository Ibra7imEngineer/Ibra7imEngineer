SELECT DISTINCT people.name
FROM people
JOIN stars ON people.id = stars.person_id
WHERE stars.movie_id IN (
    -- 1. ابحث عن ID الأفلام التي مثل فيها كيفن بيكون 1958
    SELECT stars.movie_id
    FROM stars
    JOIN people ON stars.person_id = people.id
    WHERE people.name = 'Kevin Bacon' AND people.birth = 1958
)
AND people.name != 'Kevin Bacon'; -- 2. استبعاد كيفن بيكون نفسه من النتائج
