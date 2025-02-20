import random
import time
import requests
from bs4 import BeautifulSoup
import csv

# URL pendaftaran Facebook
FB_REGISTER_URL = "https://www.facebook.com/r.php"

# Daftar proxy Indonesia (contoh proxy Indonesia acak)
proxy_list = [
    "http://103.247.7.82:8080",
    "http://114.4.57.16:8080",
    "http://118.98.178.85:8080",
    "http://180.250.4.54:8080",
    "http://103.19.14.11:8080",
]

# Daftar user-agent Android
user_agents = [
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.66 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Samsung Galaxy S20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; OPPO A53) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Asus ZenFone 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; Vivo V11 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Realme 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Huawei P30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Xiaomi Mi 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36",
]

def generate_random_name(gender):
    first_names_male = ['Budi', 'Agus', 'Joko', 'Rudi', 'Hendra']
    first_names_female = ['Siti', 'Rina', 'Dewi', 'Ani', 'Yuni']
    last_names = ['Santoso', 'Wijaya', 'Prabowo', 'Kurniawan', 'Siregar']
    first_name = random.choice(first_names_male if gender == 'l' else first_names_female)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def generate_random_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return ''.join(random.choice(chars) for _ in range(8))

def generate_random_yopmail_email():
    """Generate a random email address with yopmail.com"""
    email_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    return f"{email_name}@yopmail.com"

def get_random_proxy():
    return random.choice(proxy_list)

def get_random_user_agent():
    return random.choice(user_agents)

def get_csrf_token(session):
    """Mengambil CSRF token dari halaman pendaftaran Facebook"""
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    response = session.get(FB_REGISTER_URL, headers=headers)
    
    # Mengecek status response dan memastikan kita mendapatkan halaman dengan benar
    if response.status_code != 200:
        print(f"Error: Tidak dapat mengakses halaman pendaftaran Facebook. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Menemukan token CSRF yang ada di form
    csrf_token = None
    for input_tag in soup.find_all("input"):
        if "fb_dtsg" in input_tag.get("name", ""):
            csrf_token = input_tag.get("value")
            break
    
    if not csrf_token:
        print("Error: CSRF token tidak ditemukan.")
    
    return csrf_token

def save_results_to_csv(results):
    """Menyimpan hasil pendaftaran ke dalam file CSV"""
    with open('facebook_account_results.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Email', 'Password', 'Confirmation Code'])
        for result in results:
            writer.writerow(result)
    print("Hasil pendaftaran disimpan di facebook_account_results.csv")

def create_facebook_account():
    session = requests.Session()
    results = []  # List untuk menyimpan hasil pendaftaran

    # Meminta input pengguna
    jumlah = int(input("Jumlah akun yang ingin dibuat: "))
    gender = input("Gender (l/p): ").lower()
    nama_type = input("Nama random/manual (r/m): ").lower()
    password_type = input("Password random/manual (r/m): ").lower()
    use_proxy = input("Gunakan proxy? (y/t): ").lower()
    delay = int(input("Masukkan delay (saran 60-120 detik): "))

    # Mengambil CSRF token untuk pendaftaran
    csrf_token = get_csrf_token(session)
    if not csrf_token:
        print("Tidak dapat mengambil CSRF token.")
        return

    # Set proxy jika diperlukan
    proxies = {"http": get_random_proxy(), "https": get_random_proxy()} if use_proxy == 'y' else None

    for _ in range(jumlah):
        if gender == 'r':
            gender = random.choice(['l', 'p'])
        
        # Menghasilkan nama, email, password
        name = generate_random_name(gender) if nama_type == 'r' else input("Masukkan nama: ")
        password = generate_random_password() if password_type == 'r' else input("Masukkan password: ")

        # Menghasilkan email acak
        email = generate_random_yopmail_email()

        # Data untuk pendaftaran
        data = {
            "fb_dtsg": csrf_token,
            "firstname": name.split()[0],
            "lastname": name.split()[1],
            "reg_email__": email,
            "reg_email_confirmation__": email,
            "password": password,
            "birthday_day": "20",
            "birthday_month": "2",
            "birthday_year": "2000",
            "sex": '2' if gender == 'l' else '1',  # 1 = Female, 2 = Male
            "agree": "on",
            "source": "user_registered",
            "ref": "",
            "hsi": "0",
        }

        # Mengirimkan permintaan POST untuk membuat akun
        try:
            headers = {
                "User-Agent": get_random_user_agent(),
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response = session.post(FB_REGISTER_URL, headers=headers, data=data, proxies=proxies)
            print(f"Response dari server: {response.status_code}")
            if response.status_code == 200:
                print("Akun berhasil dibuat dengan email:", email)
                # Simpan hasil pendaftaran ke list
                results.append([name, email, password, 'Belum ada konfirmasi'])
            else:
                print(f"Gagal membuat akun untuk email {email}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        
        time.sleep(delay)

    # Menyimpan hasil pendaftaran ke CSV
    save_results_to_csv(results)
    print("Proses pembuatan akun selesai.")

if __name__ == "__main__":
    create_facebook_account()
