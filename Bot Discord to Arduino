import discord
import serial
import time

# Mengonfigurasi intents
intents = discord.Intents.default()
intents.message_content = True  # Mengaktifkan intent untuk konten pesan

# Buat instance dari Client Discord dengan intents
client = discord.Client(intents=intents)

# Hubungkan ke Arduino melalui port serial (sesuaikan dengan port Anda)
arduino = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)  # Tunggu sejenak untuk memastikan koneksi serial terbentuk

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!alert1'):
        print("Sending alert to Arduino")
        arduino.write(b'ALERT1\n')  # Mengirimkan teks 'ALERT' ke Arduino
        time.sleep(1)  # Tunggu sejenak agar pesan dikirimkan
        await message.channel.send('Alert sent to Arduino!')

    if message.content.startswith('!alert2'):
        print("Sending alert to Arduino")
        arduino.write(b'ALERT2\n')  # Mengirimkan teks 'ALERT' ke Arduino
        time.sleep(1)  # Tunggu sejenak agar pesan dikirimkan
        await message.channel.send('Alert2 sent to Arduino!')

    if message.content.startswith('!alert3'):
        print("Sending alert3 to Arduino")
        arduino.write(b'ALERT3\n')  # Mengirimkan teks 'ALERT' ke Arduino
        time.sleep(1)  # Tunggu sejenak agar pesan dikirimkan
        await message.channel.send('Alert3 sent to Arduino!')

# Ganti 'YOUR_DISCORD_BOT_TOKEN' dengan token bot yang Anda dapatkan
client.run('YOUR_DISCORD_BOT_TOKEN')
