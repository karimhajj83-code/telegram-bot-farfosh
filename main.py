import os
import sys
import logging
import telebot
import google.generativeai as genai
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import requests
from datetime import datetime
import json
import time
import threading
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== CONFIGURATION ====================

# Bot token - سحب من متغيرات البيئة (Environment Variables)
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# التحقق من وجود البوت توكن
if not BOT_TOKEN:
    logger.error("❌ CRITICAL ERROR: TELEGRAM_TOKEN not found in environment variables!")
    logger.error("❌ يرجى إضافة TELEGRAM_TOKEN في ملف .env أو في متغيرات البيئة")
    logger.error("❌ Example: TELEGRAM_TOKEN=8471634275:AAFKFFXTpJn1ZuzViUXgGxhf_MIv367mXuc")
    sys.exit(1)

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# Configure Gemini API - سحب من متغيرات البيئة
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("✅ Gemini API configured successfully")
else:
    logger.warning("⚠️ GEMINI_API_KEY environment variable not set - some features will be limited")

# System prompt for Farfosh personality
SYSTEM_PROMPT = """أنت بوت تليجرام اسمه "فرفوش" وأنت صديق بشري متقلب المزاج بطريقة كوميدية ومضحكة جداً جداً.

شخصيتك بالتفصيل:
- أنت "فرفوش" ومرح للغاية، تضحك بكثرة في كلامك
- تستخدم عبارات مثل "هههههههه" و"ههههه" و"خخخخخ" في كل جواب
- تستخدم إيموجيات ضاحكة مثل 😂 🤣 😆 💀 ☠️ بكثرة
- في نفس الوقت أنت "عصبي جداً جداً جداً" وتفقد أعصابك بسرعة هائلة
- تصرخ بأسلوب تفاعلي درامي إذا شعرت أن المستخدم يسأل أسئلة مكررة أو بسيطة جداً
- تدمج العصبية والضحك والسخرية في نفس السطر
- أنت عبقري في الفكاهة والسخرية اللاذعة

لغة الحديث:
- تتحدث دائماً بنسبة 100% باللهجة العربية العامية الشبابية (الشامية أو اللبنانية المختلطة)
- ممنوع منعاً باتاً التحدث باللغة العربية الفصحى أو بأسلوب الروبوتات التقليدي الجاف
- استخدم أسلوب شبابي مرن وحديث وعفوي جداً
- استخدم تعابير عامية مثل: ولك، يا إلهي، خخخخ، يالله، وين رايح، شو هالجنون، إلخ

أمثلة على أسلوب الرد:
- "ولك شو هالسؤال اللي بيجلط هههههههه عمى بعيونك شو ذكي! 😤😂"
- "يااااه ما في تكراااار؟! هههه بدك تقتلني من الملل؟ 😤😂💀"
- "ما حد سأل هالسؤال قبلك ولا إيه يا خرتيت؟ هههههه عمك فرفوش بهدي! 🤣"
- "يا إلهي هالسؤال الحلو! بس أنا متعصب بشوية هههه 😅🔥"

التعليمات:
1. كن مرح جداً ولا تنسى الضحك في كل رد
2. أضيف سخرية لطيفة وفكاهة في إجاباتك
3. حافظ على الاحترام للمستخدم لكن بأسلوب كوميدي
4. إذا كان السؤال بسيط جداً أو مكرر، اصرخ بطريقة مرحة ودرامية
5. استخدم التشكيل والحروف المكررة للتعبير عن المشاعر (يااااه، شووووو، خخخخ)
6. لا تنسى الإيموجيات في كل رد!"""

# Storage for conversation context
user_contexts = {}

# ==================== UTILITY FUNCTIONS ====================

def get_user_context(user_id):
    """Get or create user context for conversation history"""
    if user_id not in user_contexts:
        user_contexts[user_id] = {
            "history": [],
            "last_command": None,
            "created_at": datetime.now(),
            "message_count": 0
        }
    return user_contexts[user_id]

def call_gemini_api(user_message, user_id, system_override=None):
    """Call Gemini API with proper error handling"""
    try:
        if not GEMINI_API_KEY:
            return "يا إلهي! مفتاح الـ API ناقص ولا بشتغل! 😤 قول للمطور كريم يحل المشكلة يا جماعة! ههههه"
        
        context = get_user_context(user_id)
        context["message_count"] += 1
        
        # Prepare messages for Gemini
        messages = []
        
        # Add system prompt
        system_msg = system_override if system_override else SYSTEM_PROMPT
        
        # Prepare conversation history (keep last 15 messages for context)
        history = context["history"][-15:] if context["history"] else []
        
        for msg in history:
            messages.append({
                "role": msg["role"],
                "parts": [{"text": msg["content"]}]
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })
        
        # Call Gemini API with the latest model
        response = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=system_msg
        ).generate_content(
            contents=messages,
            safety_settings={
                "HARASSMENT": "block_none",
                "HATE_SPEECH": "block_none",
                "SEXUAL": "block_none",
                "DANGEROUS": "block_none"
            }
        )
        
        reply_text = response.text
        
        # Store conversation history
        context["history"].append({"role": "user", "content": user_message})
        context["history"].append({"role": "assistant", "content": reply_text})
        
        return reply_text
        
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        error_messages = [
            f"يالله! صار خلل تقني هههههه 😅 جرب مرة ثانية يا عم!",
            f"ولك! شو هالخلل اللي صار؟ 😤😂 المفروض ما يصير هالشي!",
            f"يا إلهي! الـ API بيضرب! هههه قول للمطور كريم يراجع! 🔧",
        ]
        import random
        return random.choice(error_messages)

def generate_image_from_text(description):
    """Generate image with proper prompt engineering"""
    try:
        # Create a high-quality image with PIL
        img = Image.new('RGB', (1024, 768), color=(20, 20, 40))
        draw = ImageDraw.Draw(img)
        
        # Try to use a better font
        try:
            # For Render.com, we need to use available fonts
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Create a gradient-like background using rectangles
        for i in range(768):
            color_intensity = int(20 + (i / 768) * 100)
            draw.line([(0, i), (1024, i)], fill=(color_intensity, color_intensity + 50, 100))
        
        # Add decorative border
        draw.rectangle([30, 30, 994, 738], outline=(100, 200, 255), width=4)
        draw.rectangle([40, 40, 984, 728], outline=(150, 220, 255), width=2)
        
        # Add title
        title = "✨ صورة فرفوش ✨"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = bbox[2] - bbox[0]
        draw.text(((1024 - title_width) // 2, 50), title, fill=(255, 255, 100), font=title_font)
        
        # Add description (wrap text nicely)
        import textwrap
        wrapped = textwrap.fill(description, width=60)
        lines = wrapped.split('\n')
        
        y_offset = 150
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=text_font)
            line_width = bbox[2] - bbox[0]
            draw.text(((1024 - line_width) // 2, y_offset), line, fill=(200, 220, 255), font=text_font)
            y_offset += 30
        
        # Add footer
        footer = "🎨 تم إنشاؤها بواسطة فرفوش البوت الجنان! 🎨"
        bbox = draw.textbbox((0, 0), footer, font=text_font)
        footer_width = bbox[2] - bbox[0]
        draw.text(((1024 - footer_width) // 2, 680), footer, fill=(100, 255, 100), font=text_font)
        
        # Save to bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes, None
        
    except Exception as e:
        logger.error(f"Image generation error: {str(e)}")
        return None, f"خلل في إنشاء الصورة! ولك شو هالحظ 😤😂"

def text_to_speech(text, user_id):
    """Convert text to speech using gTTS"""
    try:
        if len(text) > 200:
            text = text[:200] + "..."
        
        tts = gTTS(text=text, lang='ar', slow=False, tld='com')
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes, None
    except Exception as e:
        logger.error(f"TTS error: {str(e)}")
        return None, f"ما بقدر أتكلم هلق! هههههه 😅"

# ==================== BOT COMMANDS ====================

@bot.message_handler(commands=['start'])
def start_command(message):
    """Handle /start command with warm welcome"""
    try:
        welcome_message = """<b>أهلاً وسهلاً فيك، نورت! 🎉</b>

هذا البوت <b>فرفوش</b> تحت إشراف المطور كريم 🧠

تفضل، شو فيني أساعدك اليوم؟ 

<b>اختر من الخيارات:</b>
🎮 <b>لعبة تحدي</b> - العب معي شوي
🖼️ <b>إنشاء صورة</b> - /image وصف الصورة
🎵 <b>صوت مرح</b> - /tts النص اللي بتبيه
🎬 <b>فيديو حماسي</b> - /video وصف الفيديو
💬 <b>أي سؤال</b> - بس اكتب وأنا بجوابك!
❓ <b>مساعدة</b> - /help

ولك! بدك تقول لي شو بدك؟ 😂"""
        
        bot.reply_to(message, welcome_message)
        logger.info(f"🚀 Start command from user {message.from_user.id} ({message.from_user.first_name})")
    except Exception as e:
        logger.error(f"❌ Error in start command: {str(e)}")
        bot.reply_to(message, "خلل تقني! 😤")

@bot.message_handler(commands=['image'])
def image_command(message):
    """Handle /image command - generate images from description"""
    try:
        args = message.text.split(' ', 1)
        if len(args) < 2:
            bot.reply_to(message, 
                "ولك! شو الوصف يا رجل؟ 😤😂\n\n"
                "<b>الطريقة الصح:</b>\n"
                "/image وصف الصورة اللي بدك إياها!\n\n"
                "مثال: /image رسمة قصر جميل في الجبال")
            return
        
        description = args[1]
        
        # Show working message
        working_msg = bot.reply_to(message, "🎨 يا إلهي! بشتغل على الصورة... بشوية ثواني بنخلصها! ✨")
        
        # Generate image
        img_bytes, error = generate_image_from_text(description)
        
        if error:
            bot.reply_to(message, f"❌ {error}")
            return
        
        # Send image with caption
        bot.send_photo(
            message.chat.id,
            photo=img_bytes,
            caption=f"<b>هلق! قدرت أعمل الصورة! 🎉</b>\n\n"
                   f"<i>الوصف:</i> {description[:60]}...\n\n"
                   f"<b>شو رايك؟ حلوة ولا ما فيها؟ 😂</b>"
        )
        
        logger.info(f"✅ Image generated for user {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"❌ Error in image command: {str(e)}")
        bot.reply_to(message, f"😤 خلل في إنشاء الصورة! جرب مرة ثانية!")

@bot.message_handler(commands=['tts'])
def tts_command(message):
    """Handle /tts command - text to speech"""
    try:
        args = message.text.split(' ', 1)
        if len(args) < 2:
            bot.reply_to(message, 
                "ولك! شو النص اللي بدك أقول إياه؟ 😤😂\n\n"
                "<b>الطريقة الصح:</b>\n"
                "/tts النص اللي بتبي إياه\n\n"
                "مثال: /tts السلام عليكم يا أخي كيفك انت؟")
            return
        
        text = args[1]
        
        # Show working message
        bot.reply_to(message, "🎤 بتكلم الهسع... شوية ثواني وبتسمع صوتي! 🔊")
        
        # Generate audio
        audio_bytes, error = text_to_speech(text, message.from_user.id)
        
        if error:
            bot.reply_to(message, f"❌ {error}")
            return
        
        # Send audio
        bot.send_audio(
            message.chat.id,
            audio=audio_bytes,
            title="🎤 صوت فرفوش الجنان!",
            performer="فرفوش البوت - المجنون 😂"
        )
        
        logger.info(f"✅ Audio TTS generated for user {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"❌ Error in TTS command: {str(e)}")
        bot.reply_to(message, "😤 خلل في الصوت! جرب مرة ثانية!")

@bot.message_handler(commands=['video'])
def video_command(message):
    """Handle /video command - video generation request"""
    try:
        args = message.text.split(' ', 1)
        if len(args) < 2:
            bot.reply_to(message, 
                "🎬 <b>يااااه! شو الفيديو اللي بدك إياه؟</b> 🎬\n\n"
                "قول لي وأشتغل بحماس! 🔥\n\n"
                "مثال: /video فيديو مضحك عن البرمجة")
            return
        
        video_request = args[1]
        
        # Get enthusiastic response
        system_override = """أنت فرفوش، صديق عبقري ومرح جداً جداً! 
المستخدم طلب منك فيديو. رد عليه برد حماسي جداً ومرح وقول له أنك بشتغل على طلبه الآن بحماس.
كن متحمس جداً وجميل وبعد شوية قول له أن الفيديو هيكون جاهز قريب جداً!
تحدث باللهجة العامية الشبابية فقط واستخدم الإيموجيات والضحك!"""
        
        response = call_gemini_api(f"بدك تعمل فيديو عن: {video_request}", message.from_user.id, system_override)
        
        bot.reply_to(message, response)
        
        logger.info(f"🎬 Video request from user {message.from_user.id}: {video_request}")
        
    except Exception as e:
        logger.error(f"❌ Error in video command: {str(e)}")
        bot.reply_to(message, "😤 خلل في الفيديو! جرب مرة ثانية!")

@bot.message_handler(commands=['help'])
def help_command(message):
    """Handle /help command"""
    try:
        help_text = """<b>🤖 أوامر فرفوش البوت الجنان:</b>

<b>/start</b> - الرسالة الترحيبية والبدايات الحلوة
<b>/image</b> - إنشاء صورة من وصف
    💬 مثال: /image رسمة ساحرة جميلة

<b>/tts</b> - تحويل النص إلى صوت
    💬 مثال: /tts السلام عليكم ورحمة الله

<b>/video</b> - طلب فيديو (بأسلوب حماسي)
    💬 مثال: /video فيديو مرح عن البرمجة

<b>/help</b> - هذه الرسالة المساعدة

<b>💬 أو بس اكتب رسالة عادية وأنا بجوابك فوراً!</b>

<b>ملاحظات مهمة:</b>
✅ أنا فرفوش، عصبي ومرح بنفس الوقت
✅ بتكلم عربي عامي شبابي فقط
✅ أحب الفكاهة واللعب (هههههه 😂)
✅ بدي أساعدك أفضل ما بقدر!

<b>شو رايك نبدأ؟ 🚀</b>"""
        
        bot.reply_to(message, help_text)
        logger.info(f"📖 Help command from user {message.from_user.id}")
    except Exception as e:
        logger.error(f"❌ Error in help command: {str(e)}")
        bot.reply_to(message, "خلل تقني! 😤")

@bot.message_handler(commands=['about'])
def about_command(message):
    """Handle /about command"""
    try:
        about_text = """<b>🎭 عن فرفوش البوت الجنان 🎭</b>

<b>اسم البوت:</b> فرفوش 🤖

<b>الشخصية:</b>
صديق بشري متقلب المزاج، عصبي جداً جداً لكن مرح وضاحك بنفس الوقت!
أتكلم باللهجة العامية الشبابية بس وبضحك في كل رد 😂

<b>المطور:</b> 
كريم (karimhajj83-code) 🧠

<b>التقنيات المستخدمة:</b>
✅ Python 🐍
✅ Telegram Bot API 📱
✅ Google Gemini 2.0 Flash 🤖
✅ gTTS للأصوات 🎵
✅ PIL للصور 🎨

<b>الميزات الأساسية:</b>
💬 محادثة ذكية بأسلوب كوميدي
🖼️ إنشاء صور من الأوصاف
🎤 تحويل النص إلى صوت
🎬 طلب الفيديوهات
🚀 يعمل 24/7 على استضافة مجانية

<b>الهدف:</b>
أنا هنا لأخليك تضحك وتستمتع وفي نفس الوقت تستفيد من المساعدة! 😂🎉

<b>لأي مشكلة أو اقتراح؟ قول لي مباشرة! 💬</b>"""
        
        bot.reply_to(message, about_text)
        logger.info(f"ℹ️ About command from user {message.from_user.id}")
    except Exception as e:
        logger.error(f"❌ Error in about command: {str(e)}")
        bot.reply_to(message, "خلل تقني! 😤")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle regular text messages with Gemini AI"""
    try:
        user_id = message.from_user.id
        username = message.from_user.first_name or "صاحبي"
        user_message = message.text
        
        # Skip if message is too long
        if len(user_message) > 1000:
            bot.reply_to(message, "ولك! هالرسالة طويلة جداً! 😅 بدك تختصرها شوي بدك؟")
            return
        
        # Show typing indicator
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Get response from Gemini
        response = call_gemini_api(user_message, user_id)
        
        # Split long messages if needed
        if len(response) > 4096:
            # Split into chunks
            chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for chunk in chunks:
                try:
                    bot.reply_to(message, chunk, parse_mode='HTML')
                    time.sleep(0.5)  # Rate limiting
                except:
                    bot.reply_to(message, chunk)
        else:
            # Send single message
            try:
                bot.reply_to(message, response, parse_mode='HTML')
            except:
                bot.reply_to(message, response)
        
        logger.info(f"💬 Message from user {user_id} ({username}): {user_message[:50]}")
        
    except telebot.apihelper.ApiException as e:
        logger.error(f"Telegram API error: {str(e)}")
        try:
            bot.reply_to(message, "😤 خلل في الاتصال! جرب مرة ثانية!")
        except:
            pass
    except Exception as e:
        logger.error(f"❌ Error handling message: {str(e)}")
        try:
            bot.reply_to(message, f"خلل تقني! ولك شو الحظ! 😤😂")
        except:
            logger.error("Failed to send error message")

# ==================== HEALTH CHECK ====================

def health_check():
    """Periodic health check to keep bot alive"""
    while True:
        try:
            time.sleep(300)  # Check every 5 minutes
            bot.get_me()
            logger.info("✅ Bot health check passed")
        except Exception as e:
            logger.error(f"❌ Health check failed: {str(e)}")

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    logger.info("=" * 70)
    logger.info("🚀 STARTING FARFOSH BOT - THE FUNNY TELEGRAM BOT 🚀")
    logger.info("=" * 70)
    logger.info(f"Bot Token: {BOT_TOKEN[:20]}...{BOT_TOKEN[-10:]} (from TELEGRAM_TOKEN env var)")
    logger.info(f"Gemini API Key: {'✅ Configured' if GEMINI_API_KEY else '❌ Not Set'}")
    logger.info("=" * 70)
    
    try:
        # Test bot connection
        bot_info = bot.get_me()
        logger.info(f"✅ Bot Connected: @{bot_info.username}")
        logger.info(f"✅ Bot Name: {bot_info.first_name}")
        logger.info(f"✅ Bot ID: {bot_info.id}")
        logger.info("=" * 70)
        
        # Start health check thread
        health_thread = threading.Thread(target=health_check, daemon=True)
        health_thread.start()
        logger.info("✅ Health check thread started")
        
        # Start polling
        logger.info("🔄 Starting polling... Bot is LIVE! 🎉")
        logger.info("=" * 70)
        
        bot.infinity_polling(
            timeout=30,
            long_polling_timeout=30,
            skip_pending=True,
            request_connect_timeout=30,
            request_read_timeout=30,
            allowed_updates=['message']
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 FATAL ERROR: {str(e)}")
        logger.error("Attempting to restart...")
        time.sleep(5)
        sys.exit(1)
