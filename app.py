from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Flash mesajları için gerekli
app.config['UPLOAD_FOLDER'] = 'static/photos'  # Fotoğraflar static/photos klasörüne yüklenecek
app.config['MOOD_FILE'] = 'moods.json'

# İzin verilen dosya uzantıları
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Türkçe Ay İsimleri Haritası
MONTH_MAPPING = {
    1: 'Ocak', 2: 'Şubat', 3: 'Mart', 4: 'Nisan', 5: 'Mayıs', 6: 'Haziran',
    7: 'Temmuz', 8: 'Ağustos', 9: 'Eylül', 10: 'Ekim', 11: 'Kasım', 12: 'Aralık'
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ana Sayfa (Direkt erişim)
@app.route('/')
def index():
    return render_template('index.html')

# Galeri Sayfası
@app.route('/gallery')
def gallery():
    # Şu anki tarihi YYYY-MM formatında al (Date picker varsayılan değeri için)
    now = datetime.now()
    current_date = f"{now.year}-{now.month:02d}"

    # Klasördeki fotoğrafları aylara göre listele
    photos = {}
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        # Klasörleri ters sırala (En yeni tarih en üstte olsun: 2026-01 > 2025-12)
        sorted_months = sorted(os.listdir(app.config['UPLOAD_FOLDER']), reverse=True)
        
        for folder_name in sorted_months:
            month_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
            if os.path.isdir(month_path):
                # Ekranda görünecek isim (Sadece 'Ocak', 'Aralık' vb. kısmı al)
                # Format: YYYY-MM-AyAdi -> Split ile son parçayı al
                parts = folder_name.split('-')
                display_name = parts[-1] if len(parts) > 2 else folder_name
                
                month_images = []
                for filename in os.listdir(month_path):
                    if allowed_file(filename):
                        # Dosya yolunu 'YYYY-MM-Ay/dosya.jpg' formatında sakla
                        relative_path = os.path.join(folder_name, filename).replace('\\', '/')
                        month_images.append(relative_path)
                
                if month_images:
                    photos[display_name] = month_images
    
    return render_template('gallery.html', photos=photos, current_date=current_date)

# Fotoğraf Yükleme
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('gallery'))
    
    file = request.files['file']
    upload_date = request.form.get('upload_date') # Formdan tarihi al
    
    if file.filename == '':
        return redirect(url_for('gallery'))
    
    if file and allowed_file(file.filename):
        # Eğer formdan tarih geldiyse onu kullan, yoksa şu anı kullan
        if upload_date:
            try:
                year, month = map(int, upload_date.split('-'))
            except ValueError:
                now = datetime.now()
                year, month = now.year, now.month
        else:
            now = datetime.now()
            year, month = now.year, now.month
            
        month_name = MONTH_MAPPING.get(month, 'Genel')
        
        # Format: YYYY-MM-AyAdi (Örn: 2026-02-Şubat)
        folder_name = f"{year}-{month:02d}-{month_name}"
        
        # Ay klasörünü oluştur (yoksa)
        target_dir = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        filename = file.filename
        file.save(os.path.join(target_dir, filename))
        return redirect(url_for('gallery'))

    return redirect(url_for('gallery'))

# Ruh Hali Sayfası
@app.route('/mood')
def mood():
    # JSON dosyasından verileri oku
    if os.path.exists(app.config['MOOD_FILE']):
        with open(app.config['MOOD_FILE'], 'r', encoding='utf-8') as f:
            moods = json.load(f)
    else:
        # Dosya yoksa varsayılanları oluştur
        moods = {
            "Osman": {"level": 5, "last_updated": datetime.now().strftime("%d.%m.%Y")},
            "Zeynep": {"level": 5, "last_updated": datetime.now().strftime("%d.%m.%Y")}
        }
        with open(app.config['MOOD_FILE'], 'w', encoding='utf-8') as f:
            json.dump(moods, f, indent=4)
            
    return render_template('mood.html', moods=moods)

# Ruh Hali Güncelleme
@app.route('/update_mood', methods=['POST'])
def update_mood():
    user = request.form.get('user')
    mood_level = int(request.form.get('mood_level'))
    # password = request.form.get('password') # Şifre kaldırıldı
    
    # Verileri Güncelle
    if os.path.exists(app.config['MOOD_FILE']):
        with open(app.config['MOOD_FILE'], 'r', encoding='utf-8') as f:
            moods = json.load(f)
            
        moods[user] = {
            "level": mood_level,
            "last_updated": datetime.now().strftime("%d.%m.%Y")
        }
        
        with open(app.config['MOOD_FILE'], 'w', encoding='utf-8') as f:
            json.dump(moods, f, indent=4)
            
    return redirect(url_for('mood'))

if __name__ == '__main__':
    # Klasör yoksa oluştur
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True, host='0.0.0.0', port=5000)
