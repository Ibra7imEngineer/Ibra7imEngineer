import csv
import sys


def main():

    # 1. TODO: Check for command-line usage
    # يجب أن يقبل البرنامج وسيطي سطر أوامر: اسم ملف قاعدة البيانات واسم ملف تسلسل الحمض النووي
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # تحديد أسماء الملفات من وسائط سطر الأوامر
    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    # 2. TODO: Read database file into a variable
    database = []
    # يجب فتح ملف قاعدة البيانات (CSV) وقراءته
    try:
        with open(database_file, 'r') as file:
            reader = csv.DictReader(file)
            # تخزين البيانات في قائمة من القواميس
            database = list(reader)
    except FileNotFoundError:
        print(f"Error: Database file not found at {database_file}")
        sys.exit(1)

    # استخراج قائمة STRs (رؤوس الأعمدة باستثناء 'name')
    # هذا يضمن أننا لا نحتاج إلى ترميز STRs يدوياً
    # يتم تجاهل أول عمود 'name'
    strs_headers = list(database[0].keys())[1:]

    # 3. TODO: Read DNA sequence file into a variable
    sequence = ""
    # يجب فتح ملف التسلسل (TXT) وقراءة التسلسل كاملاً
    try:
        with open(sequence_file, 'r') as file:
            sequence = file.read().strip()  # .strip() لإزالة أي مسافات أو أسطر جديدة
    except FileNotFoundError:
        print(f"Error: Sequence file not found at {sequence_file}")
        sys.exit(1)

    # 4. TODO: Find longest match of each STR in DNA sequence
    # تخزين أطول عدد تكرارات لكل STR
    str_counts = {}

    for str_key in strs_headers:
        # استخدام الدالة المساعدة longest_match() لحساب أطول تكرار
        count = longest_match(sequence, str_key)
        # تخزين النتيجة كـ سلسلة نصية (لأن القيم في قاعدة البيانات هي سلاسل نصية)
        str_counts[str_key] = str(count)

    # 5. TODO: Check database for matching profiles
    # المرور على كل شخص في قاعدة البيانات ومقارنة نتائج الـ STRs المحسوبة

    for person in database:
        # متغير منطقي لتتبع ما إذا كان الشخص مطابقاً
        is_match = True

        # مقارنة كل STR في headers
        for str_key in strs_headers:
            # مقارنة العدد المحسوب (في str_counts) مع العدد المخزن في قاعدة البيانات (person)
            if str_counts[str_key] != person[str_key]:
                is_match = False
                break  # إذا لم يتطابق أي STR، انتقل للشخص التالي

        # إذا كانت is_match لا تزال True بعد فحص جميع الـ STRs، فهذا هو الشخص المطابق
        if is_match:
            print(person['name'])
            sys.exit(0)  # الخروج فوراً بعد العثور على المطابقة

    # إذا لم يتم العثور على أي مطابقة بعد المرور على قاعدة البيانات بالكامل
    print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
