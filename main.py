import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio
import os
import shutil
from flask import Flask
from threading import Thread

# --- 1. نظام البقاء حياً (للاستضافات المجانية) ---
app = Flask('')

@app.route('/')
def home():
    return "Elite FS Bot is Running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- 2. الإعدادات الأساسية ---
# يتم جلب التوكن من إعدادات الموقع (Environment Variables) للأمان
TOKEN = os.getenv('DISCORD_TOKEN')

VERIFY_ROLE_ID = 1435976172633849908 
LOG_CHANNEL_ID = 1472969983582540012 
CLAN_TAG = "FS"

# كاشف تلقائي لمسار الصوت (FFmpeg)
FFMPEG_EXE = shutil.which("ffmpeg") or r'C:\ffmpeg\bin\ffmpeg.exe'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# --- 3. محرك الموسيقى الفخم ---
yt_dlp.utils.bug_reports_message = lambda *args, **kwargs: ''
ytdl_format_options = {
    'format': 'bestaudio/best', 'restrictfilenames': True, 'noplaylist': True,
    'nocheckcertificate': True, 'ignoreerrors': False, 'logtostderr': False,
    'quiet': True, 'no_warnings': True, 'default_search': 'auto', 'source_address': '0.0.0.0'
}
ffmpeg_options = {
    'options': '-vn', 
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data: data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, executable=FFMPEG_EXE, **ffmpeg_options), data=data)

# --- 4. نظام التذاكر (Ticket System) ---
class TicketControl(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close / إغلاق", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_tkt")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        emb = discord.Embed(description="🔒 **Ticket deletion in progress...**\n🔒 **جاري أرشفة وإغلاق التذكرة نهائياً.**", color=discord.Color.red())
        await interaction.response.send_message(embed=emb)
        await asyncio.sleep(5)
        await interaction.channel.delete()

class TicketLauncher(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket / فتح تذكرة", style=discord.ButtonStyle.secondary, emoji="📩", custom_id="open_tkt")
    async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(f'🎫-{interaction.user.name}', overwrites=overwrites)
        
        embed = discord.Embed(title="🔱 FS SUPPORT | الدعم الإداري", color=discord.Color.gold())
        embed.description = f"Welcome {interaction.user.mention}\nPlease state your request, and the administration will reply soon.\n\nمرحباً بك، يرجى كتابة طلبك وسيتم الرد عليك من قبل الإدارة."
        embed.set_footer(text=f"FS Clan Elite System")
        
        await channel.send(embed=embed, view=TicketControl())
        await interaction.response.send_message(f"✅ **Ticket Created:** {channel.mention}", ephemeral=True)

# --- 5. نظام التفعيل (Verification System) ---
class RegistrationModal(discord.ui.Modal, title='Clan Membership | طلب انضمام'):
    name = discord.ui.TextInput(label='Full Name | الاسم الكامل', placeholder='Type your name...', required=True, min_length=3)
    age = discord.ui.TextInput(label='Age | العمر', placeholder='Type your age...', required=True, max_length=2)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        new_nick = f"{self.name.value} | {CLAN_TAG}"
        
        try: await interaction.user.edit(nick=new_nick)
        except: pass
        
        role = interaction.guild.get_role(VERIFY_ROLE_ID)
        if role: await interaction.user.add_roles(role)
        
        log_ch = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_ch:
            embed = discord.Embed(title="🔱 NEW WARRIOR JOINED | محارب جديد", color=0xdaa520)
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            embed.add_field(name="User / العضو", value=interaction.user.mention, inline=True)
            embed.add_field(name="Identity / الهوية", value=f"**{self.name.value}**", inline=True)
            embed.add_field(name="Age / العمر", value=f"**{self.age.value}**", inline=True)
            embed.set_image(url="https://media.discordapp.net/attachments/1086036284693160047/1105944569837699122/line.gif")
            await log_ch.send(embed=embed)
        
        success_emb = discord.Embed(description="✅ **Welcome to the Elite ranks of FS Clan!**\n✅ **تم تفعيل عضويتك بنجاح. مرحباً بك في الصفوف!**", color=discord.Color.green())
        await interaction.followup.send(embed=success_emb, ephemeral=True)

class VerifyLauncher(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Verify / تفعيل", style=discord.ButtonStyle.success, emoji="⚔️", custom_id="verify_btn")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RegistrationModal())

# --- 6. الأوامر والأحداث ---
@bot.event
async def on_ready():
    bot.add_view(VerifyLauncher())
    bot.add_view(TicketLauncher())
    bot.add_view(TicketControl())
    await bot.tree.sync()
    print(f'>>> Elite FS Bot is Online: {bot.user}')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    await ctx.message.delete()
    
    # لوحة التفعيل
    v_emb = discord.Embed(title="🛡️ CLAN VERIFICATION | تفعيل العضوية", color=discord.Color.dark_red())
    v_emb.description = "Greetings! Click below to start your registration process.\n\nتحية طيبة! يرجى الضغط على الزر أدناه للبدء في إجراءات التفعيل."
    v_emb.set_image(url="https://media.discordapp.net/attachments/1086036284693160047/1105944569837699122/line.gif")
    await ctx.send(embed=v_emb, view=VerifyLauncher())
    
    # لوحة التذاكر
    t_emb = discord.Embed(title="📩 SUPPORT CENTER | مركز الدعم", color=discord.Color.blue())
    t_emb.description = "Need help? Open a support ticket to reach the administration.\n\nتحتاج للمساعدة؟ افتح تذكرة دعم فني للتواصل مع الإدارة."
    await ctx.send(embed=t_emb, view=TicketLauncher())

@bot.tree.command(name="play", description="Stream audio from YouTube | بث صوتي")
async def play(interaction: discord.Interaction, search: str):
    await interaction.response.defer()
    if not interaction.user.voice:
        return await interaction.followup.send("⚠️ **Please join a voice channel.**\n⚠️ **يرجى الانضمام لروم صوتي أولاً.**")
    
    vc = interaction.guild.voice_client or await interaction.user.voice.channel.connect()
    try:
        player = await YTDLSource.from_url(search, loop=bot.loop, stream=True)
        if vc.is_playing(): vc.stop()
        vc.play(player)
        embed = discord.Embed(title="🎶 Now Playing | جاري البث", description=f"**{player.title}**", color=discord.Color.purple())
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send("❌ **Error: Streaming service unavailable.**")

@bot.tree.command(name="stop", description="Stop music and leave | إيقاف ومغادرة")
async def stop(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("⏹️ **Disconnected.**")
    else:
        await interaction.response.send_message("❌ **Not connected to any voice channel.**", ephemeral=True)

# --- 7. تشغيل البوت ---
if __name__ == "__main__":
    if TOKEN:
        keep_alive()  # تشغيل خادم الويب للبقاء حياً
        bot.run(TOKEN)
    else:
        print("CRITICAL ERROR: 'DISCORD_TOKEN' NOT FOUND!")
