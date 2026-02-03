// Sevgililik Başlangıç Tarihi: 13 Nisan 2025
// NOT: Gelecek bir tarih olduğu için sayaç şu an "Geri Sayım" gibi çalışacak,
// tarih geçtiğinde ise "Geçen Süre" olarak devam edecek.
// Kullanıcının isteği: "13.04.2025'ten bugüne saysın" (gelecek tarih olduğu için mantıken 0 gösterecek veya geri sayacak)
// Ancak test edebilmek için şimdilik geri sayım mantığı kuralım, tarih gelince pozitife döner.

const startDate = new Date("2025-04-13T00:00:00").getTime();

function updateCounter() {
    const now = new Date().getTime();
    
    // Tarih farkını mutlak değer olarak alıyoruz ki hem geri sayım hem geçen süre için çalışsın
    let diff = now - startDate;
    
    // Eğer gelecek tarihse (henüz 13.04.2025 olmadıysa)
    // Kullanıcı "bugüne saysın" dedi, belki geçmiş bir tarih kastetti ama "2025" yazdı.
    // Eğer yanlışlıkla 2025 yazdıysa (2024 yerine), bunu belirtmeliyim. 
    // Ama "13.04.2025" dediği için aynen uyguluyorum.
    
    // Negatifse (tarih gelecekteyse) - Gösterim tercihine göre 0 veya geri sayım
    // Biz 'since' mantığı kurduk ama tarih gelecekte. 
    // Şık durması için mutlak farkı gösterelim, başlık değişsin.
    
    const isFuture = diff < 0;
    diff = Math.abs(diff);

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    document.getElementById("days").innerText = days;
    document.getElementById("hours").innerText = hours;
    document.getElementById("minutes").innerText = minutes;
    document.getElementById("seconds").innerText = seconds;
    
    // Tarih gelecekteyse metni güncelle (Opsiyonel)
    const label = document.querySelector('.start-date');
    if (isFuture) {
        label.innerText = "13 Nisan 2025'e kalan süre...";
    } else {
        label.innerText = "13 Nisan 2025'ten beri...";
    }
}

// Her saniye güncelle
setInterval(updateCounter, 1000);
updateCounter(); // İlk yüklemede çalıştır
