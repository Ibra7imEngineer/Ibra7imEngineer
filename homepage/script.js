// هذا الكود بسيط، يقوم بإظهار تنبيه عند تحميل الصفحة وأيضًا عند النقر على الزر في index.html

// تعريف الدالة التي ستُستدعى عند النقر على الزر في index.html
function showWelcomeAlert() {
    alert("شكرًا لزيارتك موقع استكشاف الفضاء! استمتع بالرحلة.");
}

// دالة يتم تشغيلها عند تحميل محتوى الصفحة بالكامل
document.addEventListener('DOMContentLoaded', function() {
    // يمكنك إضافة المزيد من التفاعلات هنا، مثل تغيير نمط عنصر ما عند التحميل
    console.log("تم تحميل محتوى الموقع بنجاح.");

    // مثال: إضافة تأثير بسيط على عنصر في الصفحة (يجب تحديثه إذا كان العنصر موجوداً في كل الصفحات)
    if (document.querySelector('footer')) {
        document.querySelector('footer').style.fontSize = '0.9rem';
    }
});
