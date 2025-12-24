#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TASKS 100

// تعريف هيكل المهمة
typedef struct {
    char description[100];
} Task;

// مصفوفة لتخزين المهام ومتغير لمتابعة عددها
Task tasks[MAX_TASKS];
int taskCount = 0;

// الإعلان عن الدوال
void addTask();
void viewTasks();

int main(void) {
    // عرض بياناتك الشخصية
    printf("===============================================\n");
    printf("Project Title: CLI Task Manager\n");
    printf("Name: Ibrahim Mohamed Bassiouni\n");
    printf("GitHub: Ibra7imEngineer\n");
    printf("edX ID: ibrahim_engineer\n");
    printf("City/Country: Kafr El Sheikh, Egypt\n");
    printf("Date: December 2025\n");
    printf("===============================================\n\n");

    int choice;

    while (1) {
        printf("\n--- مدير المهام البسيط ---\n");
        printf("1. إضافة مهمة جديدة\n");
        printf("2. عرض جميع المهام\n");
        printf("3. خروج\n");
        printf("اختر عملية: ");

        // التحقق من صحة المدخلات
        if (scanf("%d", &choice) != 1) {
            printf("خطأ: يرجى إدخال رقم صحيح.\n");
            while(getchar() != '\n'); // تنظيف بفر الإدخال
            continue;
        }
        getchar(); // التخلص من رمز السطر الجديد المتبقي

        switch (choice) {
            case 1:
                addTask();
                break;
            case 2:
                viewTasks();
                break;
            case 3:
                printf("جاري الخروج... وداعاً!\n");
                return 0;
            default:
                printf("اختيار غير صحيح، حاول مرة أخرى.\n");
        }
    }

    return 0;
}

// دالة إضافة مهمة
void addTask() {
    if (taskCount < MAX_TASKS) {
        printf("أدخل وصف المهمة: ");
        fgets(tasks[taskCount].description, 100, stdin);

        // إزالة حرف السطر الجديد من نهاية النص
        tasks[taskCount].description[strcspn(tasks[taskCount].description, "\n")] = 0;

        taskCount++;
        printf("تمت إضافة المهمة بنجاح!\n");
    } else {
        printf("قائمة المهام ممتلئة!\n");
    }
}

// دالة عرض المهام
void viewTasks() {
    if (taskCount == 0) {
        printf("\nلا توجد مهام لعرضها حالياً.\n");
        return;
    }

    printf("\n--- قائمة المهام الحالية ---\n");
    for (int i = 0; i < taskCount; i++) {
        printf("%d. %s\n", i + 1, tasks[i].description);
    }
}
