# Florina's Imgur ✨

Linux terminalinde Imgur ile resim yükleme, bağlantıları yönetme ve indirme işlemlerini kolaylaştıran bir Python betiğidir. Bu araç, komut satırından basitçe `imgur` komutunu kullanarak Imgur işlemlerinizi gerçekleştirmenizi sağlar.
 
## Özellikler 🌸

- Tek bir resmi veya bir klasördeki tüm resimleri Imgur'a yükleyin.
- Yüklenen resimlerin bağlantılarını `links.txt` dosyasına kaydedin.
- Imgur bağlantılarından resim indirin. (Çalışmıyor sanırım ?_?)
- Python bağımlılıkları ve API anahtarlarını yönetin.

## Kurulum 💖

1. **Projeyi klonlayın:**
   ```bash
   git clone https://github.com/FlorinaAI/imgur.git
   ```

2. **Terminali açın ve proje klasörüne gidin:**
   ```bash
   cd imgur
   ```

3. **Kurulum betiğini çalıştırın:**
    ```bash
    ./install.sh
    ```
4. **Kurulum sırasında sizden Imgur API anahtarlarınızı girmeniz istenecektir. [Client oluşturun](https://api.imgur.com/oauth2/addclient)**
   
Kurulum başarıyla tamamlandığında, `imgur` komutunu terminalden kullanabilirsiniz.

## Kullanım 🎀

1. **Tek bir resim yükleme**

   Belirtilen resim dosyasını Imgur'a yüklemek için:

   ```bash
   imgur /path/to/image.png
   ```

2. **Klasördeki tüm resimleri yükleme**

   Belirtilen klasördeki tüm resimleri Imgur'a yüklemek için:

   ```bash
   imgur -f /path/to/folder/
   ```

3. **Linkleri .txt dosyasına kaydetme**

   Yüklenen resimlerin bağlantılarını .txt dosyasına kaydetmek için:

   ```bash
   imgur -f /path/to/folder/ -w
   ```
   .txt dosyasının konumunu belirtmek için:

   ```bash
   imgur -f /path/to/folder/ -w /path/to/txt.txt
   ```

4. **Resim İndirme (Hatalı)**

   Yüklenen resimlerin bağlantılarını .txt dosyasına kaydetmek için:

   ```bash
   imgur -i https://imgur.com/examplelink
   ```
