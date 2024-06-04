import requests
import xml.etree.ElementTree as ET
import discord
from discord.ext import commands
import json
from datetime import datetime
import math

# URL data gempa BMKG
url = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.xml"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}

# Bot token Anda
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# Inisialisasi bot dengan intents yang diperbarui
intents = discord.Intents.default()
intents.message_content = True  # Aktifkan intent untuk konten pesan
bot = commands.Bot(command_prefix="$", intents=intents)

# Konstanta yang diberikan
c1 = 1.6856
c2 = 0.9241
c3 = -0.0760
c4 = 0.0057
lnepsilon = 0

# Fungsi untuk menghitung R
def calculate_R(x2, y2, H):
    x1_const = -6.928423976482093
    y1_const = 107.76950682901153
    E = math.sqrt((x2 - x1_const)**2 + (y2 - y1_const)**2)
    R = math.sqrt(E**2 + H**2)
    return R

# Fungsi untuk menghitung percepatan tanah y
def calculate_y(M, R):
    lnR = math.log(R)
    lny = c1 + c2*(M - 6) + c3*(M - 6)**2 - lnR - c4*R + lnepsilon
    y = math.exp(lny)  # Karena lny = ln(y), kita gunakan exp untuk mendapatkan y
    return y

# Fungsi untuk menentukan skala MMI
def calculate_mmi(y):
    if 0 <= y <= 1.45:
        return "I"
    elif 1.46 <= y <= 2.9:
        return "II"
    elif 2.91 <= y <= 31.27:
        return "III"
    elif 31.28 <= y <= 59.64:
        return "IV"
    elif 59.65 <= y <= 88:
        return "V"
    elif 89 <= y <= 167:
        return "VI"
    elif 168 <= y <= 366:
        return "VII"
    elif 367 <= y <= 564:
        return "VIII"
    elif y >= 565:
        return "IX"
    else:
        return "Tidak diketahui"

# Fungsi untuk mendapatkan data gempa dari BMKG
def get_gempa_data():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = ET.fromstring(response.content)
        gempa_info = {
            "Tanggal": data.find(".//Tanggal").text,
            "Jam": data.find(".//Jam").text,
            "DateTime": data.find(".//DateTime").text,
            "Magnitude": float(data.find(".//Magnitude").text),
            "Kedalaman": float(data.find(".//Kedalaman").text.split()[0]),  # Mengambil nilai kedalaman dalam km
            "Koordinat": data.find(".//coordinates").text,
            "Lintang": float(data.find(".//Lintang").text.split()[0]),  # Mengambil nilai lintang
            "Bujur": float(data.find(".//Bujur").text.split()[0]),  # Mengambil nilai bujur
            "Lokasi": data.find(".//Wilayah").text,
            "Dirasakan": data.find(".//Dirasakan").text
        }
        return gempa_info
    else:
        return None

# Fungsi untuk mendapatkan data gempa dari file JSON
def get_fake_gempa_data():
    with open('fake.json', 'r') as file:
        gempa_info = json.load(file)
    return gempa_info

# Command bot untuk menampilkan data gempa asli dan menghitung percepatan tanah
@bot.command()
async def info(ctx):
    gempa_info = get_gempa_data()
    if gempa_info:
        # Hitung R
        R = calculate_R(gempa_info["Lintang"], gempa_info["Bujur"], gempa_info["Kedalaman"])
        # Hitung percepatan tanah y
        y = calculate_y(gempa_info["Magnitude"], R)
        # Tentukan skala MMI
        mmi = calculate_mmi(y)
        
        # Kirim pesan alert berdasarkan skala MMI
        alert_message = ""
        if "III" <= mmi <= "VI":
            alert_message = "!alert1"
        elif "VII" <= mmi <= "VIII":
            alert_message = "!alert2"
        elif mmi == "IX":
            alert_message = "!alert3"
        
        embed = discord.Embed(title="Gempabumi Terbaru", color=0xff0000)
        embed.add_field(name="Tanggal", value=gempa_info["Tanggal"], inline=False)
        embed.add_field(name="Jam", value=gempa_info["Jam"], inline=False)
        embed.add_field(name="DateTime", value=gempa_info["DateTime"], inline=False)
        embed.add_field(name="Magnitudo", value=gempa_info["Magnitude"], inline=False)
        embed.add_field(name="Kedalaman", value=f"{gempa_info['Kedalaman']} km", inline=False)
        embed.add_field(name="Koordinat", value=gempa_info["Koordinat"], inline=False)
        embed.add_field(name="Lintang", value=gempa_info["Lintang"], inline=False)
        embed.add_field(name="Bujur", value=gempa_info["Bujur"], inline=False)
        embed.add_field(name="Lokasi", value=gempa_info["Lokasi"], inline=False)
        embed.add_field(name="Dirasakan", value=gempa_info["Dirasakan"], inline=False)
        embed.add_field(name="Percepatan Tanah (y)", value=f"{y:.2f} gal", inline=False)
        embed.add_field(name="Skala MMI ITB", value=f"{mmi}", inline=False)
        
        await ctx.send(embed=embed)
        
        if alert_message:
            await ctx.send(alert_message)
    else:
        await ctx.send("Gagal mengakses data gempa!")

# Command bot untuk menampilkan data gempa palsu dari file
@bot.command()
async def fake(ctx):
    gempa_info = get_fake_gempa_data()
    if gempa_info:
        now = datetime.now()
        gempa_info["Tanggal"] = now.strftime("%d-%b-%Y")
        gempa_info["Jam"] = now.strftime("%H:%M:%S WIB")
        gempa_info["DateTime"] = now.isoformat()

        embed = discord.Embed(title="Gempabumi Terbaru (Palsu)", color=0xff0000)
        embed.add_field(name="Tanggal", value=gempa_info["Tanggal"], inline=False)
        embed.add_field(name="Jam", value=gempa_info["Jam"], inline=False)
        embed.add_field(name="DateTime", value=gempa_info["DateTime"], inline=False)
        embed.add_field(name="Magnitudo", value=gempa_info["Magnitude"], inline=False)
        embed.add_field(name="Kedalaman", value=gempa_info["Kedalaman"], inline=False)
        embed.add_field(name="Koordinat", value=gempa_info["Koordinat"], inline=False)
        embed.add_field(name="Lintang", value=gempa_info["Lintang"], inline=False)
        embed.add_field(name="Bujur", value=gempa_info["Bujur"], inline=False)
        embed.add_field(name="Lokasi", value=gempa_info["Lokasi"], inline=False)
        embed.add_field(name="Dirasakan", value=gempa_info["Dirasakan"], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Gagal membaca data gempa dari file!")

# Menjalankan bot
bot.run(TOKEN)
