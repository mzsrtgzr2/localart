# Search

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
  artistData = [{"area": "", "artist_name": "Moshe Roth", "city": "Hod Hasharon", "lat": 32.1557, "lon": 34.8932, "slug": "mosheroth"}, {"area": "", "artist_name": "Olga Kundina", "city": "Tel Aviv", "lat": 32.0853, "lon": 34.7818, "slug": "okundina"}];
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
    document.getElementById('tag-filter').value = '';
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
  var tag = document.getElementById('tag-filter').value;
  var cards = document.querySelectorAll('.artist-card');
  var found = false;
  var bounds = [];
  cards.forEach(function(card) {
    var match = true;
    if (city && card.getAttribute('data-city') !== city) match = false;
    if (tag) {
      var tags = card.getAttribute('data-tags').split(',');
      if (tags.indexOf(tag) === -1) match = false;
    }
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
  <label for="tag-filter" style="margin-left:16px;"><b>Filter by Tag:</b></label>
  <select id="tag-filter" onchange="filterArtists()">
    <option value="">All Tags</option>
    
      <option value="abstract">abstract</option>
    
      <option value="animals">animals</option>
    
      <option value="black_and_white">black_and_white</option>
    
      <option value="classic">classic</option>
    
      <option value="colorful">colorful</option>
    
      <option value="digital">digital</option>
    
      <option value="landscape">landscape</option>
    
      <option value="minimal">minimal</option>
    
      <option value="modern">modern</option>
    
      <option value="nature">nature</option>
    
      <option value="people">people</option>
    
      <option value="portrait">portrait</option>
    
      <option value="surreal">surreal</option>
    
      <option value="traditional">traditional</option>
    
      <option value="urban">urban</option>
    
  </select>
  <button onclick="resetArtistFilter()" style="margin-left:16px;">Reset</button>
</div>

<div id="artist-grid" style="display: flex; flex-wrap: wrap; gap: 32px; justify-content: flex-start;">

  <div class="artist-card" data-city="Hod Hasharon" data-lat="32.1557" data-lon="34.8932" data-tags="nature,minimal,modern" style="text-align:center; width:220px; margin-bottom:32px; position:relative;">
    <a href="/localart/artists/mosheroth/" style="display:inline-block;">
      <span style="position:relative; display:inline-block;">
        <img src="/localart/assets/artists/mosheroth/2.png" alt="Moshe Roth" style="width:200px; height:200px; object-fit:cover; border-radius:8px; box-shadow:0 2px 8px #0001;" />
      </span>
    </a>
    <div style="margin-top:8px; font-weight:bold; font-size:1.1em;">
      <a href="/localart/artists/mosheroth/" style="text-decoration:none; color:inherit;">Moshe Roth</a>
    </div>
    
    <div style="font-size:0.9em; color:#666;">Morning Reflections</div>
    
    
    <div style="margin-top:4px;">
      
        <a href="/localart/tags/nature" style="background:#eee; color:#333; border-radius:4px; padding:2px 6px; margin-right:4px; font-size:0.85em; text-decoration:none;">nature</a>
      
        <a href="/localart/tags/minimal" style="background:#eee; color:#333; border-radius:4px; padding:2px 6px; margin-right:4px; font-size:0.85em; text-decoration:none;">minimal</a>
      
        <a href="/localart/tags/modern" style="background:#eee; color:#333; border-radius:4px; padding:2px 6px; margin-right:4px; font-size:0.85em; text-decoration:none;">modern</a>
      
    </div>
    
    <div class="img-details" tabindex="-1" style="display:none; position:absolute; left:0; top:220px; width:100%; background:#fff; border:1px solid #ccc; border-radius:8px; box-shadow:0 2px 12px #0002; z-index:10; padding:16px; text-align:left;">
      <b>Morning Reflections</b><br>
      Size: <br>
      Medium: <br>
      Date: <br>
      
      <div style="margin-top:4px;">
        
          <span style="background:#eee; color:#333; border-radius:4px; padding:2px 6px; margin-right:4px; font-size:0.85em;">nature</span>
        
          <span style="background:#eee; color:#333; border-radius:4px; padding:2px 6px; margin-right:4px; font-size:0.85em;">minimal</span>
        
          <span style="background:#eee; color:#333; border-radius:4px; padding:2px 6px; margin-right:4px; font-size:0.85em;">modern</span>
        
      </div>
      
    </div>
  </div>

  <div class="artist-card" data-city="Tel Aviv" data-lat="32.0853" data-lon="34.7818" data-tags="abstract,modern" style="text-align:center; width:220px; margin-bottom:32px; position:relative;">
    <a href="/localart/artists/okundina/" style="display:inline-block;">
      <span style="position:relative; display:inline-block;">
        <img src="/localart/assets/artists/okundina/Screenshot%202025-06-22%20at%2014.34.32.png" alt="Olga Kundina" style="width:200px; height:200px; object-fit:cover; border-radius:8px; box-shadow:0 2px 8px #0001;" />
      </span>
    </a>
    <div style="margin-top:8px; font-weight:bold; font-size:1.1em;">
      <a href="/localart/artists/okundina/" style="text-decoration:none; color:inherit;">Olga Kundina</a>
    </div>
    
    <div style="font-size:0.9em; color:#666;">Red Harmony</div>
    
    
    <div style="margin-top:4px;">
      
        <a href="/localart/tags/abstract" style="background:#eee; color:#333; border-radius:4px; padding:2px 6px; margin-right:4px; font-size:0.85em; text-decoration:none;">abstract</a>
      
        <a href="/localart/tags/modern" style="background:#eee; color:#333; border-radius:4px; padding:2px 6px; margin-right:4px; font-size:0.85em; text-decoration:none;">modern</a>
      
    </div>
    
    <div class="img-details" tabindex="-1" style="display:none; position:absolute; left:0; top:220px; width:100%; background:#fff; border:1px solid #ccc; border-radius:8px; box-shadow:0 2px 12px #0002; z-index:10; padding:16px; text-align:left;">
      <b>Red Harmony</b><br>
      Size: <br>
      Medium: <br>
      Date: <br>
      
      <div style="margin-top:4px;">
        
          <span style="background:#eee; color:#333; border-radius:4px; padding:2px 6px; margin-right:4px; font-size:0.85em;">abstract</span>
        
          <span style="background:#eee; color:#333; border-radius:4px; padding:2px 6px; margin-right:4px; font-size:0.85em;">modern</span>
        
      </div>
      
    </div>
  </div>

</div>
<script>
function showDetails(link) {
  // Hide any open details
  document.querySelectorAll('.img-details').forEach(function(d) { d.style.display = 'none'; });
  var details = link.parentElement.querySelector('.img-details');
  if (details) {
    details.style.display = 'block';
    details.focus();
    // Hide on focus out
    details.onblur = function() { details.style.display = 'none'; };
  }
}
document.addEventListener('click', function(e) {
  if (!e.target.closest('.artist-card')) {
    document.querySelectorAll('.img-details').forEach(function(d) { d.style.display = 'none'; });
  }
});
</script>