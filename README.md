````markdown
# 🤖 فرفوش - Telegram Bot الجنان

<div align="center">

**بوت تليجرام ذكي ومرح مع شخصية كوميدية متقلبة المزاج** 😂🎉

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=flat-square&logo=telegram)
![Google Gemini](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-green?style=flat-square)

</div>

---

## 🎭 عن البوت

**فرفوش** هو بوت تليجرام ذكي ومتقدم مكتوب بـ Python، يتميز بـ:

✨ **شخصية فريدة**: صديق بشري مرح وعصبي بنفس الوقت  
💬 **محادثة ذكية**: يستخدم Google Gemini 2.0 Flash AI  
🎨 **إنشاء صور**: من خلال أوصاف نصية  
🎤 **تحويل نص لصوت**: استخدام gTTS  
🎬 **طلب الفيديوهات**: بأسلوب حماسي ومرح  
🚀 **استضافة مجانية**: يعمل 24/7 على Render.com  

---

## 🚀 البدء السريع

### المتطلبات الأساسية

- Python 3.11 أو أحدث
- حساب Telegram و BotFather
- API Key من Google Gemini

### الخطوة 1: استنساخ المستودع

```bash
git clone https://github.com/karimhajj83-code/telegram-bot-farfosh.git
cd telegram-bot-farfosh
```

### الخطوة 2: تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### الخطوة 3: إعداد متغيرات البيئة

انسخ ملف `.env.example` وأنشئ ملف `.env`:

```bash
cp .env.example .env
```

ثم عدّل الملف وأضف:

```env
BOT_TOKEN=8471634275:AAFKFFXTpJn1ZuzViUXgGxhf_MIv367mXuc
GEMINI_API_KEY=your_actual_gemini_api_key
```

### الخطوة 4: تشغيل البوت محلياً

```bash
python main.py
```

يجب أن ترى رسالة مثل:
```
✅ Bot Connected: @farfosh_bot
✅ Bot Name: فرفوش
✅ Bot ID: 1234567890
🔄 Starting polling... Bot is LIVE! 🎉
```

---

## 📡 نشر على Render.com

### الخطوة 1: إنشاء حساب Render

1. اذهب إلى [render.com](https://render.com)
2. سجل حساب جديد
3. ربط حسابك بـ GitHub

### الخطوة 2: إنشاء Web Service

1. اضغط على "New +" → "Web Service"
2. اختر مستودع `telegram-bot-farfosh`
3. املأ البيانات:
   - **Name**: `farfosh-bot`
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

### الخطوة 3: إضافة متغيرات البيئة

في صفحة الـ Web Service:

1. اضغط على "Environment"
2. أضف المتغيرات:
   - `BOT_TOKEN`: `8471634275:AAFKFFXTpJn1ZuzViUXgGxhf_MIv367mXuc`
   - `GEMINI_API_KEY`: API Key من Google

### الخطوة 4: نشر البوت

اضغط "Create Web Service" والبوت سيبدأ في الاشتغال فوراً! 🚀

---

## 📋 الأوامر المتاحة

### أوامر البوت

| الأمر | الوصف | المثال |
|------|-------|--------|
| `/start` | رسالة الترحيب والبدايات | `/start` |
| `/image` | إنشاء صورة من وصف | `/image رسمة جبل جميل` |
| `/tts` | تحويل نص إلى صوت | `/tts السلام عليكم ورحمة الله` |
| `/video` | طلب فيديو | `/video فيديو مضحك عن البرمجة` |
| `/help` | قائمة الأوامر | `/help` |
| `/about` | معلومات عن البوت | `/about` |

### الرسائل العادية

أرسل أي رسالة نصية والبوت سيجيب بأسلوب فرفوش المرح! 😂

```
أنت: السلام عليكم، كيف حالك؟
البوت: وعليكم السلام يا جماعة! ههههه أنا تمام الثلج يا صاحبي! 😂
```

---

## 🎭 شخصية البوت

### نبرة الحديث

فرفوش يتحدث بـ:
- ✅ اللهجة العربية العامية الشبابية (الشامية/اللبنانية)
- ✅ أسلوب مرح وكوميدي
- ✅ عصبية درامية سخيفة 😤
- ✅ ضحك بكثرة (هههههه، خخخخ) 😂
- ✅ إيموجيات متنوعة

### أمثلة على الردود

```
المستخدم: شو أخبارك؟
فرفوش: ولك ياااه! تمام يا حبيبي هههه 😂 أنا كل يوم مرح وعصبي بنفس الوقت! 
شو أخبارك أنت؟ قول لي بتبي إيه! 🔥

المستخدم: 2 + 2 كم؟
فرفوش: يا إلهي! هالسؤال البسيط اللي بيجلط! ههههههه 😤😂 
الإجابة هي 4 يا عم! بس يا رب ما تسأل أسئلة أبسط من هيك ولا رح أصرخ! 
💀💀💀
```

---

## 🛠️ البناء التقني

### المكتبات المستخدمة

| المكتبة | الإصدار | الاستخدام |
|--------|---------|----------|
| `pyTelegramBotAPI` | 4.20.0 | تفاعل Telegram |
| `google-genai` | 0.3.0 | Google Gemini 2.0 Flash |
| `Pillow` | 10.1.0 | إنشاء الصور |
| `gTTS` | 2.4.0 | تحويل النص لصوت |
| `requests` | 2.31.0 | طلبات HTTP |
| `python-dotenv` | 1.0.0 | متغيرات البيئة |

### هيكل المشروع

```
telegram-bot-farfosh/
├── main.py              # الملف الرئيسي للبوت
├── requirements.txt     # المكتبات المطلوبة
├── Procfile            # إعدادات Render.com
├── runtime.txt         # إصدار Python
├── .env.example        # متغيرات البيئة (مثال)
├── .env                # متغيرات البيئة (محلي فقط)
├── .gitignore          # ملفات مستثناة من Git
└── README.md           # هذا الملف
```

---

## ⚙️ الإعدادات المتقدمة

### تعديل شخصية البوت

في ملف `main.py`، عدّل المتغير `SYSTEM_PROMPT`:

```python
SYSTEM_PROMPT = """أنت بوت تليجرام اسمه "فرفوش"...
(اكتب وصفك الخاص هنا)
"""
```

### تحسين جودة الصور

في دالة `generate_image_from_text()`:

```python
img = Image.new('RGB', (1024, 768), color=(20, 20, 40))  # غير الحجم والألوان
```

### تغيير لغة الصوت

في دالة `text_to_speech()`:

```python
tts = gTTS(text=text, lang='ar', slow=False)  # غير 'ar' للغة أخرى
```

---

## 🐛 استكشاف الأخطاء

### المشكلة: "GEMINI_API_KEY environment variable not set"

**الحل:**
1. تأكد من إضافة المتغير في `.env`
2. في Render، أضفه في "Environment" settings
3. أعد تشغيل البوت

### المشكلة: "Bot stopped responding"

**الحل:**
1. تحقق من اتصال الإنترنت
2. أعد تشغيل الخدمة في Render
3. افحص السجلات: `Logs` في Render dashboard

### المشكلة: الصور لا تُنشأ

**الحل:**
1. تأكد من وجود مساحة كافية في السيرفر
2. اختصر وصف الصورة
3. جرب صورة بسيطة أولاً

---

## 📊 الإحصائيات والمراقبة

يسجل البوت تلقائياً:
- ✅ كل أمر يتم استخدامه
- ✅ كل رسالة من المستخدمين
- ✅ الأخطاء والمشاكل التقنية
- ✅ وقت الاستجابة

افحص السجلات في:
```bash
# محلياً
tail -f botlogs.log

# على Render
داخل لوحة التحكم → Logs tab
```

---

## 🤝 المساهمة

تريد تحسين البوت؟ 🚀

1. اعمل Fork للمشروع
2. اشتغل على Branch جديد (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push للـ Branch (`git push origin feature/amazing-feature`)
5. افتح Pull Request

---

## 📝 الترخيص

هذا المشروع مرخص تحت MIT License - شوف ملف [LICENSE](LICENSE) للتفاصيل.

---

## 👨‍💻 المطور

<div align="center">

**كريم** 🧠  
Full-Stack Developer | AI Enthusiast

[![GitHub](https://img.shields.io/badge/GitHub-karimhajj83--code-black?style=for-the-badge&logo=github)](https://github.com/karimhajj83-code)

</div>

---

## 📞 للتواصل والدعم

- 📧 البريد الإلكتروني: [تواصل عبر GitHub]
- 🐙 GitHub: [@karimhajj83-code](https://github.com/karimhajj83-code)
- 💬 Telegram: [@fafosh_bot](https://t.me/fafosh_bot)

---

## 🎯 خريطة الطريق المستقبلية

- [ ] إضافة قاعدة بيانات للذاكرة طويلة المدى
- [ ] الألعاب التفاعلية
- [ ] البحث عن المعلومات عبر الإنترنت
- [ ] معالجة الصور الملتقطة
- [ ] تحويل الفيديو للصوت
- [ ] دعم لغات متعددة
- [ ] نظام المكافآت والنقاط

---

<div align="center">

**شكراً لاستخدام فرفوش! 🎉**

لا تنسى تعطيه ⭐ إذا أعجبك! 😂

</div>
````
