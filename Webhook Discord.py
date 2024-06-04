import requests
import xml.etree.ElementTree as ET
from apscheduler.schedulers.blocking import BlockingScheduler
import math

# URL data gempa BMKG
url = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.xml"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}

# Webhook URL Anda
WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'

# Fungsi untuk mendapatkan data gempa
def get_gempa_data():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = ET.fromstring(response.content)
        gempa_info = {
            "Tanggal": data.find(".//Tanggal").text,
            "Jam": data.find(".//Jam").text,
            "DateTime": data.find(".//DateTime").text,
            "Magnitude": data.find(".//Magnitude").text,
            "Kedalaman": data.find(".//Kedalaman").text,
            "Koordinat": data.find(".//coordinates").text,
            "Lintang": data.find(".//Lintang").text,
            "Bujur": data.find(".//Bujur").text,
            "Lokasi": data.find(".//Wilayah").text,
            "Dirasakan": data.find(".//Dirasakan").text
        }
        return gempa_info
    else:
        return None

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
    


# Fungsi untuk mengirim pesan ke Discord menggunakan webhook
def send_gempa_info():
    gempa_info = get_gempa_data()
    if gempa_info:
        # Konversi data yang diperlukan menjadi float
        lintang = float(gempa_info["Lintang"].replace(" LS", "").replace(" LU", ""))
        bujur = float(gempa_info["Bujur"].replace(" BT", "").replace(" BB", ""))
        kedalaman = float(gempa_info["Kedalaman"].replace(" km", ""))
        magnitude = float(gempa_info["Magnitude"])

        # Hitung R
        R = calculate_R(lintang, bujur, kedalaman)
        # Hitung percepatan tanah y
        y = calculate_y(magnitude, R)
        # Tentukan skala MMI
        mmi = calculate_mmi(y)

        embed = {
            "title": "Gempabumi Terbaru",
            "color": 16711680,  # Warna merah dalam format desimal
            "fields": [
                {"name": "Tanggal", "value": gempa_info["Tanggal"], "inline": False},
                {"name": "Jam", "value": gempa_info["Jam"], "inline": False},
                {"name": "DateTime", "value": gempa_info["DateTime"], "inline": False},
                {"name": "Magnitudo", "value": gempa_info["Magnitude"], "inline": False},
                {"name": "Kedalaman", "value": gempa_info["Kedalaman"], "inline": False},
                {"name": "Koordinat", "value": gempa_info["Koordinat"], "inline": False},
                {"name": "Lintang", "value": gempa_info["Lintang"], "inline": False},
                {"name": "Bujur", "value": gempa_info["Bujur"], "inline": False},
                {"name": "Lokasi", "value": gempa_info["Lokasi"], "inline": False},
                {"name": "Dirasakan", "value": gempa_info["Dirasakan"], "inline": False},
                {"name": "Percepatan Tanah (y)", "value": str(y), "inline": False},
                {"name": "MMI ITB", "value": mmi, "inline": False},
            ]
        }

        payload = {
            "embeds": [embed]
        }

        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("Pesan berhasil dikirim!")
        else:
            print(f"Gagal mengirim pesan: {response.status_code}")
    else:
        print("Gagal mengakses data gempa!")

# Scheduler untuk mengirim pesan setiap 2 jam
scheduler = BlockingScheduler()
scheduler.add_job(send_gempa_info, 'interval', hours=2)

# Mulai scheduler
print("Scheduler dimulai, mengirim pesan setiap 2 jam...")
scheduler.start()
