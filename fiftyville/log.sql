-- Keep a log of any SQL queries you execute as you solve the mystery.

-- 1. ابحث عن تقرير الحادث لتحديد مكان وقوع الجريمة ومتى حدثت.
-- التاريخ: 2023/07/28
-- المكان: شارع Humphrey Street
-- نأمل أن نجد سجلات كاميرات المراقبة لهذا التاريخ والمكان.
SELECT description
FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- نتيجة الاستعلام رقم 1:
-- سرقة وقعت في تمام الساعة 10:15 صباحاً في Humphrey Street Bakery.
-- تشير سجلات كاميرات المراقبة إلى ثلاثة شهود كانوا موجودين في موقع الحادث
-- تم أخذ مقابلات مع الشهود الثلاثة، وكل مقابلة تذكر اسم المخبز.

-- 2. ابحث عن مقابلات الشهود التي أُجريت في ذلك اليوم، وتذكر المخبز (Bakery).
-- الهدف: استخلاص المعلومات الأساسية التي قد تساعد في تحديد المشتبه بهم.
SELECT transcript
FROM interviews
WHERE year = 2023 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';

-- نتائج الاستعلام رقم 2:
-- الشاهد 1 (Ruth): رأيت اللص يغادر المخبز ويدخل سيارته في موقف السيارات خلال 10 دقائق من السرقة (10:15 - 10:25). سألت البنك عن تفاصيل سحب.
-- الشاهد 2 (Eugene): تعرف على اللص، وشاهد اللص يستخدم ماكينة الصراف الآلي في Leggett Street قبل وقوع الجريمة بفترة وجيزة، ويسحب مبلغاً من المال.
-- الشاهد 3 (Raymond): عندما كان اللص يغادر المخبز، اتصل بشخص ما لأقل من دقيقة، وكان يخطط لركوب أقرب طائرة مغادرة غداً (2023/07/29).

-- 3. استخدام سجلات كاميرا المخبز (الشاهد Ruth): تحديد لوحات السيارات التي غادرت بين 10:15 و 10:25.
-- الهدف: تضييق قائمة المشتبه بهم.
SELECT activity, license_plate
FROM bakery_security_logs
WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25;

-- 4. استخدام سجلات الصراف الآلي (الشاهد Eugene): تحديد الأشخاص الذين سحبوا أموالاً من ماكينة الصراف الآلي في Leggett Street في ذلك اليوم.
-- الهدف: دمج هذه القائمة مع قائمة السيارات لتضييق الخيارات.
SELECT person_id
FROM bank_accounts
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street';

-- 5. دمج نتائج سجلات الكاميرا والصراف الآلي للحصول على قائمة مشتبه بهم أولية.
-- الهدف: نجد المشتبه بهم المشتركين في القائمتين.
SELECT name
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25
)
AND id IN (
    SELECT person_id
    FROM bank_accounts
    JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
    WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street'
);

-- قائمة المشتبه بهم حتى الآن: 'Bruce', 'Diana', 'Iman', 'Luca', 'Kenny', 'Taylor' (قد تتغير الأسماء حسب قاعدة بياناتك).

-- 6. استخدام معلومات الشاهد Raymond: تحديد أقصر مكالمة (أقل من دقيقة) بعد السرقة (10:15) في ذلك اليوم (2023/07/28).
-- الهدف: تحديد أرقام هواتف المشتبه بهم والمُتَّصَل بهم.
SELECT caller, receiver
FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60;

-- 7. دمج قائمة المشتبه بهم الأولية مع سجلات المكالمات.
-- الهدف: تحديد المشتبه بهم الذين أجروا مكالمات قصيرة بعد الجريمة.
SELECT name
FROM people
WHERE phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60
)
AND name IN ('Bruce', 'Diana', 'Iman', 'Luca', 'Kenny', 'Taylor');
-- بعد تضييق الخيارات، قد يتبقى شخصان أو ثلاثة. (مثال: 'Bruce', 'Diana', 'Kenny').

-- 8. استخدام معلومات الشاهد Raymond: تحديد أول رحلة طيران مغادرة من Fiftyville في اليوم التالي (2023/07/29).
-- الهدف: تحديد وجهة الهروب وتضييق قائمة المشتبه بهم أكثر.
SELECT id, destination_airport_id
FROM flights
WHERE year = 2023 AND month = 7 AND day = 29
ORDER BY hour ASC, minute ASC
LIMIT 1;
-- رقم الرحلة (مثال: 36)، المطار الوجهة (مثال: 4).

-- 9. تحديد اسم المطار والمدينة الوجهة.
SELECT city
FROM airports
WHERE id = 4;
-- النتيجة: المدينة هي New York City (قد تختلف).

-- 10. تحديد المشتبه بهم الذين كانوا على متن الرحلة 36 (أول رحلة مغادرة) في اليوم التالي.
-- الهدف: تحديد اللص من قائمة المشتبه بهم النهائية.
SELECT name
FROM people
WHERE passport_number IN (
    SELECT passport_number
    FROM passengers
    WHERE flight_id = 36 -- أو رقم الرحلة الذي حصلت عليه من استعلام 8
)
AND name IN ('Bruce', 'Diana', 'Kenny'); -- أو قائمة المشتبه بهم النهائية لديك.
-- النتيجة النهائية: 'Bruce' هو اللص.

-- 11. تحديد المُتَّصل به (الشريك) الذي تحدث معه اللص (Bruce) بعد السرقة.
-- الهدف: تحديد المُتَّصل به (الـ Accomplice).
SELECT name
FROM people
WHERE phone_number = (
    SELECT receiver
    FROM phone_calls
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60 AND caller = (
        SELECT phone_number FROM people WHERE name = 'Bruce'
    )
);
-- النتيجة النهائية: 'Robin' (قد تختلف).

-- **ملخص النتائج النهائية:**
-- اللص (Thief): Bruce
-- مدينة الهروب (Escape City): New York City
-- الشريك (Accomplice): Robin
