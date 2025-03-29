let map;
let clickCount = 0;
let fromMarker, toMarker, routeLine;

// Инициализация карты
function initLeafletMap() {
    map = L.map('leafletMap').setView([50.5954, 36.5872], 13); // Белгородская область

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Клик по карте (способ 1 + форма)
    map.on('click', function (e) {
        const method = document.getElementById("methodSelector").value;
        if (method !== "1") return;

        if (clickCount === 0) {
            clearMap();
            fromMarker = L.marker(e.latlng).addTo(map).bindPopup("Точка A").openPopup();
            document.getElementById("from_lat").value = e.latlng.lat.toFixed(6);
            document.getElementById("from_lon").value = e.latlng.lng.toFixed(6);
            clickCount++;
        } else if (clickCount === 1) {
            toMarker = L.marker(e.latlng).addTo(map).bindPopup("Точка B").openPopup();
            document.getElementById("to_lat").value = e.latlng.lat.toFixed(6);
            document.getElementById("to_lon").value = e.latlng.lng.toFixed(6);
            clickCount++;
        }
    });
}

// Очистка карты и маркеров
function clearMap() {
    if (fromMarker) map.removeLayer(fromMarker);
    if (toMarker) map.removeLayer(toMarker);
    if (routeLine) map.removeLayer(routeLine);
    fromMarker = null;
    toMarker = null;
    routeLine = null;
    clickCount = 0;
}

// Полный сброс
function resetLeafletMap() {
    map.remove();
    document.getElementById("leafletMap").innerHTML = "";
    clearMap();
    initLeafletMap();
    resetFormFields();
}

// Очистка значений формы координат
function resetFormFields() {
    const ids = ["from_lat", "from_lon", "to_lat", "to_lon"];
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
    });
}

// Рисуем маршрут по координатам
async function fetchAndDrawRoute(fromLat, fromLon, toLat, toLon, mode = "car") {
    const url = `/map/interactive-data?from_lat=${fromLat}&from_lon=${fromLon}&to_lat=${toLat}&to_lon=${toLon}&mode=${mode}`;
    const response = await fetch(url);
    const geo = await response.json();

    if (geo && geo.geometry) {
        routeLine = L.geoJSON(geo, {
            style: { color: 'blue', weight: 5 }
        }).addTo(map);
        map.fitBounds(routeLine.getBounds());
    } else {
        alert("Маршрут не найден.");
    }
}

// === Форма: координаты и клик ===
function setupCoordsForm() {
    const coordForm = document.getElementById('coordForm');
    if (!coordForm) return;

    coordForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        clearMap();

        const fromLat = parseFloat(this.from_lat.value);
        const fromLon = parseFloat(this.from_lon.value);
        const toLat = parseFloat(this.to_lat.value);
        const toLon = parseFloat(this.to_lon.value);
        const mode = this.mode.value;

        fromMarker = L.marker([fromLat, fromLon]).addTo(map).bindPopup("Точка A").openPopup();
        toMarker = L.marker([toLat, toLon]).addTo(map).bindPopup("Точка B").openPopup();

        await fetchAndDrawRoute(fromLat, fromLon, toLat, toLon, mode);
    });
}

// === Форма: названия адресов ===
function setupNameForm() {
    const nameForm = document.getElementById("routeByNamesForm");
    if (!nameForm) return;

    nameForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        clearMap();

        const fromAddress = document.getElementById("from_address").value;
        const toAddress = document.getElementById("to_address").value;
        const mode = document.getElementById("mode_select").value;

        const geoFrom = await fetch(`/geocode?q=${encodeURIComponent(fromAddress)}`).then(r => r.json());
        const geoTo = await fetch(`/geocode?q=${encodeURIComponent(toAddress)}`).then(r => r.json());

        if (!geoFrom || !geoTo || !geoFrom.lat || !geoTo.lat) {
            alert("Не удалось найти координаты.");
            return;
        }

        const fromLat = parseFloat(geoFrom.lat);
        const fromLon = parseFloat(geoFrom.lon);
        const toLat = parseFloat(geoTo.lat);
        const toLon = parseFloat(geoTo.lon);

        fromMarker = L.marker([fromLat, fromLon]).addTo(map).bindPopup("Откуда").openPopup();
        toMarker = L.marker([toLat, toLon]).addTo(map).bindPopup("Куда").openPopup();

        await fetchAndDrawRoute(fromLat, fromLon, toLat, toLon, mode);
    });
}

// === Инициализация ===
document.addEventListener("DOMContentLoaded", function () {
    initLeafletMap();
    setupCoordsForm();
    setupNameForm();
});
