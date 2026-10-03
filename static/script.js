// Yağmur animasyonu
document.addEventListener("DOMContentLoaded", function() {
    // Yağmur damlaları oluştur
    const bgContainer = document.querySelector('.background-hearts');
    if (bgContainer) {
        function createRaindrops() {
            for (let i = 0; i < 80; i++) {
                const drop = document.createElement('div');
                drop.className = 'raindrop';
                drop.style.left = Math.random() * 100 + '%';
                drop.style.height = (15 + Math.random() * 30) + 'px';
                drop.style.animationDuration = (1.5 + Math.random() * 2) + 's';
                drop.style.animationDelay = Math.random() * 3 + 's';
                bgContainer.appendChild(drop);
            }
        }
        createRaindrops();
    }

    // Sayaç alanı varsa, durdur (eski kodun devamı)
    const daysEl = document.getElementById("days");
    const hoursEl = document.getElementById("hours");
    const minutesEl = document.getElementById("minutes");
    const secondsEl = document.getElementById("seconds");

    if (daysEl) daysEl.innerText = "–";
    if (hoursEl) hoursEl.innerText = "–";
    if (minutesEl) minutesEl.innerText = "–";
    if (secondsEl) secondsEl.innerText = "–";

    const label = document.querySelector('.start-date');
    if (label) {
        label.innerText = "Sayaç durduruldu.";
    }
});
