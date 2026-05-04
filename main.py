import discord
from discord import app_commands, ui
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import asyncio
import os
import json
import re

# ==========================================
# ⚙️ إعدادات البوت الأساسية
# ==========================================
TOKEN = os.getenv("DISCORD_TOKEN", "MTQ5NjE2MDg4NzYxNzA5Mzc4NA.GF1_dU.m9kbmX6vzbR_HHyp8c5o8svdzX7su8oG3jAR-o").strip()
MAIN_GIF_URL = "https://files.manuscdn.com/user_upload_by_module/session_file/310519663561208676/BzWAJYSxHhIcSUfG.gif"
PANEL_IMAGE_URL = "https://files.manuscdn.com/user_upload_by_module/session_file/310519663590897529/WpsGoScjQVOQeyBf.png"
VIDEO_PATH = "welcome_video.mp4"
KSA_TZ = timezone(timedelta(hours=3))

ALLOWED_SETUP_ROLES = [1496574941246521475, 1497314460627505275]

ROLES = {
    "MONITORING": 1496852706021605436,
    "SUPPORT": 1496852633573523526,
    "MILITARY_CALL_ROLE": 1496591142874251264,
    "INQUIRY_VIEWERS": [1497314460627505275, 1497314837859143803],
    "LEADERSHIP_VIEWERS": [1497314460627505275],
    "INVENTORY_VIEWERS": [1496481118638309567, 1497314460627505275],
    "COMPLAINT_VIEWERS": [1497314460627505275]
}

CHANNELS = {
    "APPLICATIONS": 1497304423733530704,
    "TRIAL_REQUESTS": 1497188041591095366,
    "WELCOME": 1497304423733530704,
    "REPORTS_MONITORING": 1496574125626495036,
    "REPORTS_SUPPORT": 1496574125626495036,
    "MILITARY_CALL": 1496863261579149413,
    "WARNINGS": 1496864245608874075,
    "LOGS": 1496574125626495036
}

# ==========================================
# 📜 محتوى القوانين
# ==========================================
LAWS_CONTENT = {
    "مفاهيم الأفواج الأمنية": (
        "قوات الأفواج الأمنية هي قطاع عسكري تابع لوزارة الداخلية السعودية وتختص بحروب العصابات والمناطق الجبلية والحدودية "
        "ولها صلاحية إلقاء القبض والضبط والتفتيش والمطاردة وإطلاق النار وفق النظام، ومساندة القوات العسكرية."
    ),
    "قوة الدعم والمساندة": (
        "1 - وجب عليك احترام عموم أفراد الفرقة من القيادة الى أقل رتبة بالفرقة.\n"
        "2 - يُمنع الاستهبال والضحك وقت المباشرة، نرجو الالتزام بالجدية الكاملة.\n"
        "3 - يمنع مباشرة الحالات المرورية؛ الاختصاص هو الحالات الجنائية والمداهمات فقط.\n"
        "4 - أنت المسؤول الأول عن المركبة المستلمة وفي حال إهمالها ستتم محاسبتك.\n"
        "5 - يمنع صدم الأشخاص في المطاردات إلا بعد مرور الوقت المعروف للحالات الجنائية.\n"
        "6 - مركز التحكم هو العمليات، وفي حال عدم تواجده فالأقدمية هي المرجع.\n"
        "7 - عند الاستيقاف يجب تقفيل الشارع من المداخل والمخارج لتجنب التدخل الخارجي.\n"
        "8 - يمنع التحدث مع المقبوض عليه؛ التحدث فقط للمحقق الميداني أو المسؤول.\n"
        "9 - عند القبض يجب التوجه لأقرب مركز حكومي لاستكمال الإجراءات بسرعة."
    ),
    "إدارة الرصد والاستجابة": (
        "وحدة الرصد الجوي هي وحدة ميدانية تستخدم الهليكوبتر لدعم العمليات من الجو.\n"
        "1- مراقبة المواقع الحساسة والمناطق المشتبه بها.\n"
        "2- تتبع المطلوبين وتوجيه الدوريات الأرضية لمواقعهم.\n"
        "3- تقديم دعم سريع للقوات الأمنية أثناء الحملات.\n"
        "4- نقل المعلومات الميدانية مباشرة لغرف العمليات.\n"
        "5- كشف الجرائم قبل وقوعها ودعم القوات على الأرض بكفاءة."
    ),
    "قائمة المركبات": (
        "**✅ المركبات المسموحة للأفراد:**\n"
        "كامري، فتك (قديم/جديد)، سيرا، كابرس، ربع (قديم/جديد)، تاهو 11، تشارجر، اف جي، فورد فكتوريا، دورانجو، كامري 14، ترافيس، فورتشر 12، لاند (قديم/جديد)، فتك غمارتين.\n\n"
        "**❌ المركبات غير المسموحة:**\n"
        "لكزس (ضباط)، مرسيدس (ضباط)، تاهو 24 (مسؤولين)، يوكن 11 وتورس (دعم ومساندة)، مدرعة، شاص عيار 50، شاص مقفص 17، هليكوبتر، نقل الأفواج."
    ),
    "المهام والمواقع": (
        "**📌 المهام:**\n"
        "1- ضبط الجرائم الجنائية في الطرق السريعة.\n"
        "2- ضبط قضايا المخدرات والترويج والتهريب.\n"
        "3- لا يسمح بالمركبات السرية إلا لفرقة الدعم والمساندة والحملات.\n"
        "4- إحباط السطو والنهب وسلب المواطنين.\n"
        "5- حماية حياة المواطن في الطرق السريعة والجبال.\n\n"
        "**📍 مواقع التواجد:**\n"
        "الجبال والأودية، منطقة الدمام والرياض وجدة (ما عدا المناطق الممنوعة)."
    ),
    "التعليمات العسكرية": (
        "1- عدم التدخل في أي حالة إلا عن طريق مركز العمليات.\n"
        "2- بين كل بلاغ وبلاغ 5 ثواني كحد أقصى.\n"
        "3- احترام المواطنين والعسكر وتحسين الأسلوب.\n"
        "4- الصدم بإذن العمليات فقط (كل 30 ثانية صدم احترافي في الرفرف الخلفي).\n"
        "5- القيافة العسكرية تكون موحدة.\n"
        "6- التواجد في التردد (6.6) عند تسجيل الحضور.\n"
        "7- في المطاردة 3 وحدات كحد أقصى مع رفع الكود العسكري."
    ),
    "التسلسل الرتبي": (
        "• مسؤول أفراد الأفواج الأمنية\n"
        "• مسؤول قطاع الأفواج الأمنية\n"
        "• نائب قائد وكالة شؤون الأفواج الأمنية\n"
        "• قائد وكالة شؤون الأفواج الأمنية\n"
        "• مساعد قيادة الأمن العام\n"
        "• نائب مدير الأمن العام\n"
        "• مدير الأمن العام"
    )
}

# ==========================================
# 📊 بيانات الاختبار (الرصد)
# ==========================================
MONITORING_QUESTIONS = [
    {
        "q": "ماهي المهمة من اختصاص لوحدة الرصد الجوي عند ملاحقة المركبات الهاربة؟",
        "options": ["تتبع المركبة وتوجيه الدوريات الأرضية لموقعها بدقة.", "اعتراض المركبة الهاربة وإجبارها على التوقف باستخدام الطائرة."]
    },
    {
        "q": "الارتفاع المخصص للطيران؟",
        "options": ["500 متر", "550 متر", "450 متر"]
    },
    {
        "q": "هل يمنع الهبوط أو الاقتراب من سطح الأرض في حالات إطلاق النار أو المداهمات أو الحملات الأمنية؟",
        "options": ["نعم", "لا"]
    },
    {
        "q": "ما هي المواقع المصرح فيها بالهبوط نظاماً؟",
        "options": ["المواقع المصرح بها هي المهابط المعتمدة (H) والمطارات الرسمية فقط.", "يحق الهبوط في أي مكان يراه الطيار مناسباً بشرط أن تكون الأرض مستوية."]
    },
    {
        "q": "هل يُسمح لوحدات الرصد بمباشرة حالات إطلاق النار؟",
        "options": ["لا", "نعم", "في حال إسقاط جميع الوحدات الأرضية"]
    }
]

# ==========================================
# 💾 إدارة البيانات
# ==========================================
DATA_FILE = "bot_data_v7.json"
_cached_data = None

def load_data():
    global _cached_data
    if _cached_data is not None: return _cached_data
    if not os.path.exists(DATA_FILE):
        _cached_data = {"users": {}, "double_multiplier": 1.0, "active_sessions": {}}
        save_data(_cached_data)
    else:
        try:
            with open(DATA_FILE, "r") as f: _cached_data = json.load(f)
        except:
            _cached_data = {"users": {}, "double_multiplier": 1.0, "active_sessions": {}}
            save_data(_cached_data)
    return _cached_data

def save_data(data):
    global _cached_data
    _cached_data = data
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# ==========================================
# 🤖 كلاس البوت الأساسي
# ==========================================
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # ملاحظة: هذه الـ Views يجب أن تكون معرفة في الكود (تم افتراض وجودها كما في الكود الأصلي)
        try:
            self.add_view(DutyView("الرصد", ROLES["MONITORING"]))
            self.add_view(DutyView("الدعم", ROLES["SUPPORT"]))
            self.add_view(ReportView("الرصد"))
            self.add_view(ReportView("الدعم"))
            self.add_view(TicketView())
            self.add_view(TicketControlView())
            self.add_view(LawsView())
            self.add_view(PodcastView())
            self.add_view(TrialRequestView())
            self.add_view(MilitaryCallView())
            self.add_view(ApplyView("الرصد", ROLES["MONITORING"]))
            self.add_view(ApplyView("الدعم", ROLES["SUPPORT"]))
            self.add_view(InventoryButtonsView("الرصد", ROLES["MONITORING"]))
            self.add_view(InventoryButtonsView("الدعم", ROLES["SUPPORT"]))
        except NameError:
            pass # في حال كانت الـ Views معرفة لاحقاً في الكود
        
        await self.tree.sync()
        print(f"--- [SUCCESS] تم تشغيل النسخة النهائية الأسطورية باسم: {self.user} ---")

bot = MyBot()

# ==========================================
# 🛠️ أدوات مساعدة
# ==========================================
async def send_panel(interaction, embed, view):
    embed.set_image(url=PANEL_IMAGE_URL)
    if os.path.exists(VIDEO_PATH):
        file = discord.File(VIDEO_PATH, filename="welcome_video.mp4")
        await interaction.channel.send(file=file, embed=embed, view=view)
    else:
        await interaction.channel.send(embed=embed, view=view)

def is_allowed_setup():
    async def predicate(interaction: discord.Interaction):
        if any(role.id in ALLOWED_SETUP_ROLES for role in interaction.user.roles) or interaction.user.guild_permissions.administrator:
            return True
        await interaction.response.send_message("❌ ليس لديك صلاحية استخدام هذا الأمر.", ephemeral=True)
        return False
    return app_commands.check(predicate)

# ==========================================
# 🚀 أوامر السلاش (Setup)
# ==========================================
@bot.tree.command(name="help", description="عرض قائمة بجميع الأوامر المتاحة")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="📖 دليل أوامر البوت الفخم", color=discord.Color.gold())
    setup_cmds = "`/setup_duty_monitoring`, `/setup_duty_support`, `/setup_reports_monitoring`, `/setup_reports_support`, `/setup_tickets`, `/setup_laws`, `/setup_military`, `/setup_podcast`, `/setup_apply_monitoring`, `/setup_apply_support`, `/set_double_multiplier`, `/setup_inventory_monitoring`, `/setup_inventory_support`"
    embed.add_field(name="⚙️ أوامر الإعداد", value=setup_cmds, inline=False)
    embed.set_image(url=PANEL_IMAGE_URL)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# --- نظام الترحيب ---
@bot.event
async def on_member_join(member):
    ch = member.guild.get_channel(CHANNELS["WELCOME"])
    if not ch: return
    created_at = member.created_at; now = datetime.now(timezone.utc); diff = now - created_at
    account_age = f"{diff.days // 365} years ago" if diff.days > 365 else (f"{diff.days // 30} months ago" if diff.days > 30 else f"{diff.days} days ago")
    inviter_mention = "Unknown"
    try:
        invites = await member.guild.invites()
        for inv in invites:
            if inv.uses > 0: inviter_mention = inv.inviter.mention; break
    except: pass
    embed = discord.Embed(title=f"Welcome To Osten Town RP", description=f"**Member :**\n{member.mention}\n\n**Invited By :**\n{inviter_mention}", color=discord.Color.from_rgb(43, 45, 49))
    embed.set_author(name=f"{member.name} | ! Abu Naif", icon_url=member.display_avatar.url)
    embed.add_field(name="Create Discord :", value=account_age, inline=True); embed.add_field(name="Number :", value=str(member.guild.member_count), inline=True)
    embed.set_image(url=PANEL_IMAGE_URL); embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else None)
    embed.set_footer(text=f"Powered By [ Osten Town dev ] • Today at {datetime.now(KSA_TZ).strftime('%I:%M %p')}", icon_url=member.guild.icon.url if member.guild.icon else None)
    await ch.send(content=f"{member.mention} | ! Abu Naif", embed=embed)

@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        log_ch = after.guild.get_channel(CHANNELS["LOGS"])
        if not log_ch: return
        added_roles = [role for role in after.roles if role not in before.roles]
        removed_roles = [role for role in before.roles if role not in after.roles]
        
        try:
            async for entry in after.guild.audit_logs(limit=5, action=discord.AuditLogAction.member_role_update):
                if entry.target.id == after.id:
                    admin = entry.user
                    for role in added_roles:
                        embed = discord.Embed(title="🎖️ إضافة رتبة", color=discord.Color.blue(), timestamp=datetime.now(KSA_TZ))
                        embed.add_field(name="بواسطة", value=admin.mention); embed.add_field(name="إلى", value=after.mention)
                        embed.add_field(name="الرتبة", value=role.mention); embed.set_thumbnail(url=PANEL_IMAGE_URL); await log_ch.send(embed=embed)
                    for role in removed_roles:
                        embed = discord.Embed(title="🚫 إزالة رتبة", color=discord.Color.red(), timestamp=datetime.now(KSA_TZ))
                        embed.add_field(name="بواسطة", value=admin.mention); embed.add_field(name="من", value=after.mention)
                        embed.add_field(name="الرتبة", value=role.mention); embed.set_thumbnail(url=PANEL_IMAGE_URL); await log_ch.send(embed=embed)
                    break
        except Exception as e:
            print(f"Error in on_member_update logs: {e}")

@bot.event
async def on_ready(): print(f"--- البوت الفخم متصل الآن: {bot.user} ---")

if __name__ == "__main__":
    bot.run(TOKEN)
