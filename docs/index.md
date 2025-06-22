# Artists Gallery

<!-- Map of Israel -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<div id="artist-map" style="height: 350px; margin-bottom: 32px; border-radius: 8px; overflow: hidden;"></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
var map, markers = [], artistData;
document.addEventListener('DOMContentLoaded', function() {
  map = L.map('artist-map').setView([31.5, 34.8], 8); // Center on Israel
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);
  artistData = [];
  artistData.forEach(function(artist) {
    var marker = L.marker([artist.lat, artist.lon]).addTo(map);
    marker.bindPopup('<b>' + artist.artist_name + '</b><br>' + (artist.city || '') + (artist.area ? ', ' + artist.area : ''));
    marker.on('click', function() {
      filterArtistsByLocation(artist.lat, artist.lon);
    });
    markers.push({ marker: marker, lat: artist.lat, lon: artist.lon, city: artist.city, area: artist.area });
  });
  window.resetArtistFilter = function() {
    document.getElementById('city-filter').value = '';
    document.getElementById('area-filter').value = '';
    filterArtists();
    map.setView([31.5, 34.8], 8);
  }
});
function filterArtistsByLocation(lat, lon) {
  var cards = document.querySelectorAll('.artist-card');
  cards.forEach(function(card) {
    var clat = card.getAttribute('data-lat');
    var clon = card.getAttribute('data-lon');
    card.style.display = (clat == lat && clon == lon) ? '' : 'none';
  });
  map.setView([lat, lon], 12);
}
function filterArtists() {
  var city = document.getElementById('city-filter').value;
  var area = document.getElementById('area-filter').value;
  var cards = document.querySelectorAll('.artist-card');
  var found = false;
  var bounds = [];
  cards.forEach(function(card) {
    var match = true;
    if (city && card.getAttribute('data-city') !== city) match = false;
    if (area && card.getAttribute('data-area') !== area) match = false;
    card.style.display = match ? '' : 'none';
    if (match && card.getAttribute('data-lat') && card.getAttribute('data-lon')) {
      bounds.push([parseFloat(card.getAttribute('data-lat')), parseFloat(card.getAttribute('data-lon'))]);
      found = true;
    }
  });
  if (found && bounds.length > 0) {
    if (bounds.length === 1) {
      map.setView(bounds[0], 12);
    } else {
      map.fitBounds(bounds, {padding: [30, 30]});
    }
  } else {
    map.setView([31.5, 34.8], 8);
  }
}
</script>

<!-- Filter UI -->
<div style="margin-bottom: 24px;">
  <label for="city-filter"><b>Filter by City:</b></label>
  <select id="city-filter" onchange="filterArtists()">
    <option value="">All Cities</option>
    
      <option value="Hod Hasharon">Hod Hasharon</option>
    
      <option value="Tel Aviv">Tel Aviv</option>
    
  </select>
  <label for="area-filter" style="margin-left:16px;"><b>Filter by Area:</b></label>
  <select id="area-filter" onchange="filterArtists()">
    <option value="">All Areas</option>
    
  </select>
  <button onclick="resetArtistFilter()" style="margin-left:16px;">Reset</button>
</div>

<div id="artist-grid" style="display: flex; flex-wrap: wrap; gap: 32px; justify-content: flex-start;">

  <div class="artist-card" data-city="Hod Hasharon" data-area="" data-lat="None" data-lon="None" style="text-align:center; width:220px; margin-bottom:32px;">
    <a href="/artists/mosheroth/">
      <img src="/assets/artists/mosheroth/1.png" alt="Moshe Roth" style="width:200px; height:200px; object-fit:cover; border-radius:8px; box-shadow:0 2px 8px #0001;" />
    </a>
    <div style="margin-top:8px; font-weight:bold; font-size:1.1em;">
      <a href="/artists/mosheroth/" style="text-decoration:none; color:inherit;">Moshe Roth</a>
    </div>
    
    <div style="font-size:0.9em; color:#666;">Sunset Over the Valley</div>
    
    
    <div style="font-size:0.85em; color:#888; margin-top:2px;">
      Hod Hasharon
    </div>
    
  </div>

  <div class="artist-card" data-city="Tel Aviv" data-area="" data-lat="None" data-lon="None" style="text-align:center; width:220px; margin-bottom:32px;">
    <a href="/artists/okundina/">
      <img src="/assets/artists/okundina/Screenshot%202025-06-22%20at%2014.35.46.png" alt="Olga Kundina" style="width:200px; height:200px; object-fit:cover; border-radius:8px; box-shadow:0 2px 8px #0001;" />
    </a>
    <div style="margin-top:8px; font-weight:bold; font-size:1.1em;">
      <a href="/artists/okundina/" style="text-decoration:none; color:inherit;">Olga Kundina</a>
    </div>
    
    <div style="font-size:0.9em; color:#666;">Spring Garden</div>
    
    
    <div style="font-size:0.85em; color:#888; margin-top:2px;">
      Tel Aviv
    </div>
    
  </div>

</div>