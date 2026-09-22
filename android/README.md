# موسوعة السوق — مشروع Android Studio

هذا مجلد **مشروع أندرويد جاهز للفتح والبناء**. التطبيق الأصلي في `Souq/` لم يُحذف؛ نُسخت ملفات التشغيل إلى `app/src/main/assets/`.

## الفتح في Android Studio

1. ثبّت [Android Studio](https://developer.android.com/studio) (Hedgehog أو أحدث) و **JDK 17**.
2. **File → Open** واختر المجلد:
   ```
   sell/android
   ```
   وليس جذر `sell` كله.
3. انتظر مزامنة Gradle (أول مرة ينزّل المكتبات).
4. وصّل هاتفاً أو شغّل محاكياً.
5. اضغط **Run** (▶) أو من الطرفية:
   ```bash
   cd android
   ./gradlew assembleDebug
   ```
   ملف APK يظهر في:
   `android/app/build/outputs/apk/debug/app-debug.apk`

## ملاحظات

- `applicationId`: `com.souq.app`
- المحتوى يعمل **بدون إنترنت** (WebView + أصول محلية).
- إذن الإنترنت موجود فقط لآلية تحميل الأصول المحلية (WebViewAssetLoader)، وليس لاعتماد السحابة.
- بعد تعديل ملفات `Souq/` انسخها من جديد إلى `android/app/src/main/assets/` ثم أعد البناء.

## المتطلبات

- Android Studio + Android SDK 34
- minSdk 24 (أندرويد 7)
- Kotlin + Gradle 8.5
