import argparse
import os
import requests
from imgurpython import ImgurClient
from datetime import datetime
from termcolor import colored
import time
import webbrowser
import pyperclip

key_file_path = os.path.expanduser('~/.config/imgur-it/keys.txt')

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


IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET = read_keys_from_file(key_file_path)

if not IMGUR_CLIENT_ID or not IMGUR_CLIENT_SECRET:
    say("Imgur API anahtarları okunamadı. Lütfen keys.txt dosyasını kontrol edin.")
    exit(1)

def upload_image(image_path):
    client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
    response = client.upload_from_path(image_path, anon=True)
    imgur_link = response['link']
    return imgur_link

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

def create_html_summary(imgur_links, output_file='summary.html'):
    html_content = '''
    <html>
    <head>
        <title>Imgur Yükleme Özeti</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #fef4f4;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0,0,0,0.2);
            }
            h1 {
                color: #ff6f61;
                text-align: center;
            }
            .image-item {
                margin-bottom: 20px;
                padding: 10px;
                border: 1px solid #ff6f61;
                border-radius: 10px;
                background-color: #ffe4e1;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .image-item img {
                max-width: 100%;
                height: auto;
                border-radius: 10px;
            }
            .image-item a {
                color: #ff6f61;
                text-decoration: none;
                font-weight: bold;
            }
            .image-item a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Imgur Yükleme Özeti</h1>
    '''
    for image_name, link in imgur_links:
        html_content += f'''
        <div class="image-item">
            <h2>{image_name}</h2>
            <a href="{link}" target="_blank">{link}</a><br>
            <img src="{link}" width="300">
        </div>
        '''
    html_content += '''
        </div>
    </body>
    </html>
    '''
    
    with open(output_file, 'w') as file:
        file.write(html_content)
    
    webbrowser.open(f'file://{os.path.abspath(output_file)}')
    say(f"Özet HTML dosyası {output_file} olarak oluşturuldu ve tarayıcıda açıldı.")

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

def download_images_from_file(file_path):
    if not os.path.isfile(file_path):
        say(f"Link dosyası bulunamadı: {file_path}")
        return
    
    with open(file_path, 'r') as file:
        links = file.readlines()

    for idx, link in enumerate(links, start=1):
        link = link.strip()
        if link:
            say(f"{idx}/{len(links)}: {link} indiriliyor...")
            download_image(link, f"downloaded_image_{idx}.png")

parser = argparse.ArgumentParser()
parser.add_argument("image_path", type=str, nargs='?', help="Yüklenecek resim dosyasının yolu")
parser.add_argument("-f", "--folder", type=str, help="Yüklenecek resimlerin bulunduğu klasörün yolu")
parser.add_argument("-w", "--write", type=str, nargs='?', const='', help="Linkleri belirtilen dosyaya yaz (dosya yolu verilmezse varsayılan olarak aynı klasörde links.txt olarak kaydedilir)")
parser.add_argument("-i", "--imgur", type=str, help="Imgur linkinden resmi indir veya bir .txt dosyasından tüm linkleri indir")
parser.add_argument("-s", "--summary", action='store_true', help="Yüklenen resimlerin özetini HTML dosyası olarak oluştur")
args = parser.parse_args()

write_to_file = None
imgur_links = []

if args.imgur:
    if args.imgur.endswith('.txt'):
        download_images_from_file(args.imgur)
    else:
        try:
            download_image(args.imgur, "downloaded_image.png")
        except Exception as e:
            say(f"İndirirken bir hata oluştu: {e}")

elif args.image_path:
    try:
        imgur_link = upload_image(args.image_path)
        pyperclip.copy(imgur_link)
        say("Resim başarılı bir şekilde yüklendi ve panoya kopyalandı:", imgur_link)
        imgur_links.append((os.path.basename(args.image_path), imgur_link))
    except Exception as e:
        say(f"Yükleme sırasında bir hata oluştu: {e}")

elif args.folder:
    if os.path.isdir(args.folder):
        if args.write is not None:
            if args.write == '':
                write_to_file = os.path.join(args.folder, "links.txt")
            else:
                write_to_file = args.write
        imgur_links = upload_images_in_folder(args.folder, write_to_file=write_to_file)
    else:
        say(f"Geçersiz klasör yolu: {args.folder}")

if args.summary and imgur_links:
    create_html_summary(imgur_links)

if not (args.image_path or args.folder or args.imgur or args.summary):
    parser.print_help()
