#include "helpers.h"
#include <math.h> // مطلوب لاستخدام الدالة round()

// دالة مساعدة لتحديد القيمة القصوى (clamp) لضمان عدم تجاوز 255
int clamp(int value)
{
    return (value > 255) ? 255 : value;
}

// 1. التدرج الرمادي (Grayscale)
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // قراءة القيم الأصلية
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            // حساب المتوسط وتقريبه (استخدام 3.0 لضمان القسمة العشرية)
            int average = round((originalRed + originalGreen + originalBlue) / 3.0);

            // تعيين القيمة الجديدة لجميع الألوان
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// 2. اللون البني الداكن (Sepia)
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            // تطبيق المعادلات والتقريب وتحديد الحد الأقصى باستخدام دالة clamp
            int sepiaRed =
                clamp(round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue));
            int sepiaGreen =
                clamp(round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue));
            int sepiaBlue =
                clamp(round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue));

            // تعيين القيم الجديدة
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// 3. الانعكاس الأفقي (Reflect)
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        // حلقة حتى منتصف العرض فقط
        for (int j = 0; j < width / 2; j++)
        {
            // استخدام RGBTRIPLE كمتغير مؤقت للتبديل
            RGBTRIPLE temp = image[i][j];

            // تبديل البكسل الأيسر بالبكسل الأيمن المقابل
            image[i][j] = image[i][width - 1 - j];

            // تعيين البكسل الأيمن المقابل للقيمة الأصلية
            image[i][width - 1 - j] = temp;
        }
    }
    return;
}

// 4. التمويه/التشويش (Blur)
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // 1. إنشاء نسخة مؤقتة (VLA) ونسخ الصورة الأصلية إليها للقراءة منها
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // 2. معالجة كل بكسل
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;
            int counter = 0;

            // 3. التنقل في شبكة 3x3 (الصف: i-1 إلى i+1)
            for (int row = i - 1; row <= i + 1; row++)
            {
                // العمود: j-1 إلى j+1
                for (int col = j - 1; col <= j + 1; col++)
                {
                    // 4. التحقق من الحدود (عدم الخروج عن نطاق الصورة)
                    if (row >= 0 && row < height && col >= 0 && col < width)
                    {
                        // التجميع من الصورة المؤقتة (الأصلية)
                        sumRed += temp[row][col].rgbtRed;
                        sumGreen += temp[row][col].rgbtGreen;
                        sumBlue += temp[row][col].rgbtBlue;
                        counter++;
                    }
                }
            }

            // 5. حساب المتوسط وتعيين القيم الجديدة (باستخدام float للقسمة)
            image[i][j].rgbtRed = round((float) sumRed / counter);
            image[i][j].rgbtGreen = round((float) sumGreen / counter);
            image[i][j].rgbtBlue = round((float) sumBlue / counter);
        }
    }
    return;
}
