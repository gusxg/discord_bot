import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from myserver import server_on

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# 🔒 จำกัดช่อง
ALLOWED_CHANNEL_ID = 1493585784039538810 

# 📚 ฐานข้อมูล
exams = {
    "posn": {
            "คณิต": {
                "2561": "files/math2561.pdf",
                "2562": "files/math2562.pdf",
                "2564": "files/math2564.pdf",
                "2565": "files/math2565.pdf",
                "2566": "files/math2566.pdf",
                "2567": "files/math2567.pdf",
                "2568": "files/math2568.pdf"
            },
            "ฟิสิกส์": {
                "2560": "files/phy2560.pdf",
                "2561": "files/phy2561.pdf",
                "2562": "files/phy2562.pdf",
                "2564": "files/phy2564.pdf",
                "2565": "files/phy2565.pdf",
                "2566": "files/phy2566.pdf",
                "2567": "files/phy2567.pdf",
                "2568": "files/phy2568.pdf",
            },
            "เคมี": {
                "2560": "chem/chem60.pdf",
                "2561": "chem/chem61.pdf",
                "2562": "chem/chem62.pdf",
                "2564": "chem/chem64.pdf",
                "2565": "chem/chem65.pdf",
                "2566": "chem/chem66.pdf",
                "2567": "chem/chem67.pdf",
                "2568": "chem/chem68.pdf",
            },
            "ชีวะ": {
                "2560": "bio/bio60.pdf",
                "2561": "bio/bio61.pdf",
                "2562": "bio/bio62.pdf",
                "2564": "bio/bio64.pdf",
                "2565": "bio/bio65.pdf",
                "2566": "bio/bio66.pdf",
                "2567": "bio/bio67.pdf",
                "2568": "bio/bio68.pdf",
            },
            "คอมพิวเตอร์": {
                "2560": "com/com60.pdf",
                "2561": "com/com61.pdf",
                "2562": "com/com62.pdf",
                "2564": "com/com64.pdf",
                "2565": "com/com65.pdf",
                "2566": "com/com66.pdf",
                "2567": "com/com67.pdf",
                "2568": "com/com68.pdf",
            }
    },

    "onet3": {
            "คณิต": {
                "2567": "https://www.niets.or.th/th/content/uploads/editor/files/O-NET/exam_m3_2567/mathM3-67.pdf"
            },
            "ภาษาไทย": {
                "2567": "https://www.niets.or.th/th/content/uploads/editor/files/O-NET/exam_m3_2567/thaiM3-67.pdf"
            },
            "อังกฤษ": {
                "2567": "https://www.niets.or.th/th/content/uploads/editor/files/O-NET/exam_m3_2567/engM3-67.pdf"
            },
            "วิทยาศาสตร์": {
                "2567": "https://www.niets.or.th/th/content/uploads/editor/files/O-NET/exam_m3_2567/sciM3-67.pdf"
            }
    },

    "onet6": {
            "คณิต": {
                "2567": "https://www.niets.or.th/th/content/uploads/editor/files/O-NET/exam_m6_2567/Sample%20O-NET%20M6-maths.pdf"
            },
            "ภาษาไทย": {
                "2567": "https://www.niets.or.th/th/content/uploads/editor/files/O-NET/exam_m6_2567/Sample%20O-NET%20M6-thai.pdf"
            },
            "อังกฤษ": {
                "2567": "https://www.niets.or.th/th/content/uploads/editor/files/O-NET/exam_m6_2567/Sample%20O-NET%20M6-english.pdf"
            },
            "วิทยาศาสตร์": {
                "2567": "https://www.niets.or.th/th/content/uploads/editor/files/O-NET/exam_m6_2567/Sample%20O-NET%20M6-science.pdf"
            }    
    }
}

# 🔽 dropdown หมวดหมู่
exam_types = [
    app_commands.Choice(name="สอวน", value="posn"),
    app_commands.Choice(name="onet3", value="onet3"),
    app_commands.Choice(name="onet6", value="onet6"),
]

# 🔽 dropdown วิชา
subjects = [
    app_commands.Choice(name="คณิต", value="คณิต"),
    app_commands.Choice(name="ฟิสิกส์", value="ฟิสิกส์"),
    app_commands.Choice(name="เคมี", value="เคมี"),
    app_commands.Choice(name="ชีวะ", value="ชีวะ"),
    app_commands.Choice(name="คอมพิวเตอร์", value="คอมพิวเตอร์"),
    app_commands.Choice(name="ภาษาไทย", value="ภาษาไทย"),
    app_commands.Choice(name="อังกฤษ", value="อังกฤษ"),
    app_commands.Choice(name="วิทยาศาสตร์", value="วิทยาศาสตร์")
]

# 🔽 dropdown ปี
years = [
    app_commands.Choice(name="2560", value="2560"),
    app_commands.Choice(name="2561", value="2561"),
    app_commands.Choice(name="2562", value="2562"),
    app_commands.Choice(name="2564", value="2564"),
    app_commands.Choice(name="2565", value="2565"),
    app_commands.Choice(name="2566", value="2566"),
    app_commands.Choice(name="2567", value="2567"),
    app_commands.Choice(name="2568", value="2568"),
]

# 🔥 background task สำหรับลบข้อความหลัง delay วินาที
async def delete_after_delay(interaction: discord.Interaction, delay: int = 300):
    await asyncio.sleep(delay)
    try:
        msg = await interaction.original_response()
        await msg.delete()
    except Exception as e:
        print(f"ลบไม่ได้: {e}")

@bot.event
async def on_ready():
    print(f"ล็อกอินแล้วเป็น {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Sync แล้ว {len(synced)} คำสั่ง")
    except Exception as e:
        print(e)

# 🔍 คำสั่งหลัก
@bot.tree.command(name="posn", description="ค้นหาข้อสอบ สอวน")
@app_commands.describe(exam_type="เลือกประเภท", subject="เลือกวิชา", year="เลือกปี")
@app_commands.choices(exam_type=exam_types, subject=subjects, year=years)
async def posn(
    interaction: discord.Interaction,
    exam_type: app_commands.Choice[str],
    subject: app_commands.Choice[str],
    year: app_commands.Choice[str]
):
    # ❌ ใช้ผิดห้อง
    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(
            "❌ ใช้ได้เฉพาะห้องนี้",
            ephemeral=True
        )
        return

    subject_value = subject.value
    year_value = year.value
    exam_type_value = exam_type.value

    # ❌ ไม่มีข้อมูล
    if exam_type_value not in exams or subject_value not in exams[exam_type_value] or year_value not in exams[exam_type_value][subject_value]:
        await interaction.response.send_message(
            "❌ ไม่พบข้อมูล",
            delete_after=10
        )
        return

    file_path = exams[exam_type_value][subject_value][year_value]

    if file_path.startswith(("http://", "https://")):
        await interaction.response.send_message(
            content=f"📄{exam_type.name} {subject_value} ปี {year_value}\n{file_path}"
        )
    else:
        # ❌ ไฟล์ไม่มีจริง
        if not os.path.exists(file_path):
            await interaction.response.send_message(
                "❌ ไม่พบไฟล์ในเครื่อง",
                delete_after=10
            )
            return

        # ✅ ส่งไฟล์
        file = discord.File(file_path)
        await interaction.response.send_message(
            content=f"📄{exam_type.name} {subject_value} ปี {year_value}",
            file=file
        )

    # ✅ รัน background task ลบข้อความหลัง 5 นาที
    asyncio.create_task(delete_after_delay(interaction, 300))

server_on()

bot.run(os.getenv("TOKEN"))
