from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Flash mesajları için gerekli
app.config['UPLOAD_FOLDER'] = 'static/photos'  # Fotoğraflar static/photos klasörüne yüklenecek
app.config['MOOD_FILE'] = 'moods.json'

# İzin verilen dosya uzantıları (fotoğraf + video + iphone heic/heif)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mov', 'avi', 'webm', 'mkv', '3gp', 'heic', 'heif'}
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2 GB toplu yükleme kapasitesi

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

# Buluşma Takvimi Sayfası (Aradayız - Gizli)
@app.route('/meeting')
def meeting():
    return redirect(url_for('index'))

# Galeri Sayfası (Tüm anılar tek ve toplu galeri)
@app.route('/gallery')
def gallery():
    all_media = []
    VIDEO_EXTS = {'mp4', 'mov', 'avi', 'webm', 'mkv', '3gp'}
    upload_dir = app.config['UPLOAD_FOLDER']

    if os.path.exists(upload_dir):
        for root, _, files in os.walk(upload_dir):
            for file in files:
                if allowed_file(file):
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, upload_dir).replace('\\', '/')
                    ext = file.rsplit('.', 1)[-1].lower() if '.' in file else ''
                    is_video = ext in VIDEO_EXTS
                    try:
                        mtime = os.path.getmtime(abs_path)
                    except OSError:
                        mtime = 0

                    all_media.append({
                        'path': rel_path,
                        'name': file,
                        'is_video': is_video,
                        'mtime': mtime
                    })

        # Tarihe / eklenme sırasına göre en yeni olanlar önce gelecek şekilde sırala
        all_media.sort(key=lambda x: (x['mtime'], x['name']), reverse=True)

    return render_template('gallery.html', all_media=all_media)


# Fotoğraf & Video Toplu Yükleme (Telefondan kolay yükleme için)
@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('files')
    if not files or (len(files) == 1 and files[0].filename == ''):
        files = request.files.getlist('file')

    if not files or (len(files) == 1 and files[0].filename == ''):
        return redirect(url_for('gallery'))

    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    for f in files:
        if f and f.filename != '' and allowed_file(f.filename):
            filename = f.filename
            # Dosya adı çakışmasını önle
            base, ext = os.path.splitext(filename)
            dest_name = filename
            counter = 1
            while os.path.exists(os.path.join(upload_dir, dest_name)):
                dest_name = f"{base}_{counter}{ext}"
                counter += 1
            f.save(os.path.join(upload_dir, dest_name))

    return redirect(url_for('gallery'))

# Ruh Hali Sayfası (Aradayız - Gizli)
@app.route('/mood')
def mood():
    return redirect(url_for('index'))

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
