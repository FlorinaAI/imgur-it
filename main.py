import argparse
import os
import requests
from imgurpython import ImgurClient
from datetime import datetime
from termcolor import colored
import time

def say(message, link=None):
    current_time = datetime.now().strftime("%H:%M")
    formatted_time = f"[{colored(current_time, 'magenta')}]"
    formatted_message = colored(message, 'cyan')
    if link:
        formatted_message += colored(f" {link}", 'red')
    print(f"{formatted_time} {formatted_message}")


def read_keys_from_file(file_path):
  try:
    with open(file_path, 'r') as file:
      lines = file.readlines()
      for line in lines:
        if line.startswith('IMGUR_CLIENT_ID'):
          IMGUR_CLIENT_ID = line.split('=')[1].strip()
        elif line.startswith('IMGUR_CLIENT_SECRET'):
          IMGUR_CLIENT_SECRET = line.split('=')[1].strip()

      return IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET
  except FileNotFoundError:
    say(f"Dosya bulunamadı: {file_path}")
    return None, None

key_file_path = os.path.expanduser('~/.config/florinasimgur/keys.txt')


IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET = read_keys_from_file(key_file_path)

if not IMGUR_CLIENT_ID or not IMGUR_CLIENT_SECRET:
  say("Imgur API anahtarları okunamadı. Lütfen keys.txt dosyasını kontrol edin.")
  exit(1)

def upload_image(image_path):
    client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
    response = client.upload_from_path(image_path, anon=True)
    return response['link']

def upload_images_in_folder(folder_path, write_to_file=None):
    imgur_links = []
    image_files = [os.path.join(root, file)
                   for root, dirs, files in os.walk(folder_path)
                   for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    say(f"{len(image_files)} tane resim bulundu. Yükleme başlıyor...")
    
    for idx, image_path in enumerate(image_files, start=1):
        try:
            say(f"{idx}/{len(image_files)}: {image_path} yükleniyor...")
            imgur_link = upload_image(image_path)
            imgur_links.append((os.path.basename(image_path), imgur_link))
            say("Resim başarılı bir şekilde yüklendi:", imgur_link)
        except Exception as e:
            say(f"Yükleme sırasında bir hata oluştu ({image_path}): {e}")
    
    if write_to_file:
        with open(write_to_file, 'w') as file:
            for image_name, link in imgur_links:
                file.write(f"{image_name} : {link}\n")
        say(f"Tüm linkler {write_to_file} dosyasına yazıldı.")
    
    return imgur_links

def download_image(imgur_link, download_path):
    headers = {'User-Agent': 'Mozilla/5.0'}
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(imgur_link, headers=headers, timeout=10)
            if response.status_code == 200:
                with open(download_path, 'wb') as file:
                    file.write(response.content)
                say(f"Resim başarıyla {download_path} olarak indirildi.")
                return
            elif response.status_code == 429:
                say("Rate limit hatası alındı. Bir süre bekleniyor...")
                time.sleep(60)
            else:
                say(f"Resim indirilemedi. HTTP durum kodu: {response.status_code}")
                return
        except requests.RequestException as e:
            say(f"Resim indirirken bir hata oluştu: {e}")
            return
    say("Maksimum deneme sayısına ulaşıldı. Resim indirilemedi.")

parser = argparse.ArgumentParser()
parser.add_argument("image_path", type=str, nargs='?', help="Yüklenecek resim dosyasının yolu")
parser.add_argument("-f", "--folder", type=str, help="Yüklenecek resimlerin bulunduğu klasörün yolu")
parser.add_argument("-w", "--write", type=str, nargs='?', const='', help="Linkleri belirtilen dosyaya yaz (dosya yolu verilmezse varsayılan olarak aynı klasörde links.txt olarak kaydedilir)")
parser.add_argument("-i", "--imgur", type=str, help="Imgur linkinden resmi indir")
args = parser.parse_args()

write_to_file = None

if args.imgur:
    try:
        download_image(args.imgur, "downloaded_image.png")
    except Exception as e:
        say(f"İndirirken bir hata oluştu: {e}")

elif args.image_path:
    try:
        imgur_link = upload_image(args.image_path)
        say("Resim başarılı bir şekilde yüklendi:", imgur_link)
    except Exception as e:
        say(f"Yükleme sırasında bir hata oluştu: {e}")

elif args.folder:
    if os.path.isdir(args.folder):
        if args.write is not None:
            if args.write == '':               
                write_to_file = os.path.join(args.folder, "links.txt")
            else:
                write_to_file = args.write
        upload_images_in_folder(args.folder, write_to_file)
    else:
        say(f"Geçersiz klasör yolu: {args.folder}")

else:
    say("Bir resim dosyası yolu veya klasör yolu belirtmelisiniz.")
