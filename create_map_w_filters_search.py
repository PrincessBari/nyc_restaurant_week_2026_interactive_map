# NYC Restaurant Week Interactive Map with filters, search bar
# =======================================================
# Features:
# - Custom dropdown filter for cuisines
# - Search functionality
# - Hover tooltips with restaurant name, cuisine, address

import folium
from folium import IFrame
import pandas as pd
import json
from branca.element import Template, MacroElement

def create_advanced_map(csv_file='<filename>', output_file='<filename>'):
    """
    Create an advanced interactive map with custom filtering.
    """
    
    print("=" * 80)
    print("Creating Advanced Interactive Restaurant Map")
    print("=" * 80)
    
    # Read the CSV
    print(f"\nReading {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Remove rows without coordinates
    df = df.dropna(subset=['Latitude', 'Longitude'])
    print(f"✓ Loaded {len(df)} restaurants with coordinates")
    
    # Fill missing values
    df['Cuisine'] = df['Cuisine'].fillna('Unknown')
    df['Restaurant'] = df['Restaurant'].fillna('Unknown')
    df['Address'] = df['Address'].fillna('Address not available')
    
    # Get unique cuisines
    cuisines = sorted(df['Cuisine'].unique())
    print(f"✓ Found {len(cuisines)} unique cuisines")
    
    # Create the base map
    print("\nCreating map...")
    center_lat = df['Latitude'].mean()
    center_lon = df['Longitude'].mean()
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='CartoDB positron'
    )
    
    # Prepare data for JavaScript
    restaurants_data = []
    for idx, row in df.iterrows():
        restaurants_data.append({
            'name': row['Restaurant'],
            'cuisine': row['Cuisine'],
            'address': row['Address'],
            'lat': row['Latitude'],
            'lon': row['Longitude']
        })
    
    # Convert to JSON for embedding
    restaurants_json = json.dumps(restaurants_data)
    
    # Custom HTML/CSS/JavaScript for filtering
    template = """
    {% macro html(this, kwargs) %}
    
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            #filter-panel {
                position: fixed;
                top: 10px;
                left: 60px;
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                z-index: 9999;
                max-width: 350px;
                font-family: Arial, sans-serif;
            }
            
            #filter-panel h3 {
                margin: 0 0 10px 0;
                font-size: 20px;
                color: #333;
            }
            
            #filter-panel label {
                display: block;
                margin: 10px 0 5px 0;
                font-weight: bold;
                font-size: 14px;
            }
            
            #filter-panel select {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
            }
            
            #filter-panel input[type="text"] {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
            }
            
            #filter-panel button {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
            }
            
            #filter-panel button:hover {
                background-color: #1976D2;
            }
            
            .info-text {
                font-size: 12px;
                color: #666;
                margin-top: 10px;
                padding-top: 10px;
                border-top: 1px solid #eee;
            }
            
            #restaurant-count {
                font-weight: bold;
                color: #2196F3;
            }
        </style>
    </head>
    <body>
        <div id="filter-panel">
            <h3><strong>NYC Restaurant Week 2026</strong><br><span style="font-size: 16px; font-weight: normal;">Jan. 20th - Feb. 12th</span></h3>
            
            <label for="cuisine-filter">Filter by Cuisine:</label>
            <select id="cuisine-filter">
                <option value="all">All Cuisines</option>
            </select>
            
            <label for="search-input">Search Restaurant:</label>
            <input type="text" id="search-input" placeholder="Type restaurant name...">
            
            <button onclick="applyFilters()">Apply Filters</button>
            <button onclick="resetFilters()" style="background-color: #64B5F6;">Reset</button>
            
            <div class="info-text">
                Showing <span id="restaurant-count">0</span> restaurants<br>
                💡 Hover over markers for Restaurant, Cuisine, Address
            </div>
        </div>
        
        <script>
            // Restaurant data
            var restaurantsData = """ + restaurants_json + """;
            var markers = [];
            var map = null;
            
            // Wait for map to load
            window.addEventListener('load', function() {
                // Get map instance
                setTimeout(function() {
                    map = window.map_""" + m._id + """;
                    if (map) {
                        initializeMap();
                    }
                }, 500);
            });
            
            function initializeMap() {
                // Populate cuisine dropdown
                var cuisineFilter = document.getElementById('cuisine-filter');
                var cuisines = [...new Set(restaurantsData.map(r => r.cuisine))].sort();
                
                cuisines.forEach(function(cuisine) {
                    var option = document.createElement('option');
                    option.value = cuisine;
                    option.textContent = cuisine;
                    cuisineFilter.appendChild(option);
                });
                
                // Create all markers
                createMarkers(restaurantsData);
            }
            
            function createMarkers(data) {
                // Clear existing markers
                markers.forEach(function(marker) {
                    map.removeLayer(marker);
                });
                markers = [];
                
                // Create new markers
                data.forEach(function(restaurant) {
                    var tooltipContent = 
                        '<div style="font-family: Arial; font-size: 12px;">' +
                        '<strong>' + restaurant.name + '</strong><br>' +
                        '<em>Cuisine:</em> ' + restaurant.cuisine + '<br>' +
                        '<em>Address:</em> ' + restaurant.address +
                        '</div>';
                    
                    var marker = L.marker([restaurant.lat, restaurant.lon], {
                        icon: L.icon({
                            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
                            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                            iconSize: [25, 41],
                            iconAnchor: [12, 41],
                            popupAnchor: [1, -34],
                            shadowSize: [41, 41]
                        })
                    })
                    .bindTooltip(tooltipContent, {
                        permanent: false,
                        direction: 'top',
                        opacity: 0.9
                    })
                    .addTo(map);
                    
                    markers.push(marker);
                });
                
                // Update count
                document.getElementById('restaurant-count').textContent = data.length;
            }
            
            function applyFilters() {
                var cuisineFilter = document.getElementById('cuisine-filter').value;
                var searchText = document.getElementById('search-input').value.toLowerCase();
                
                var filteredData = restaurantsData.filter(function(restaurant) {
                    var cuisineMatch = (cuisineFilter === 'all' || restaurant.cuisine === cuisineFilter);
                    var searchMatch = (searchText === '' || restaurant.name.toLowerCase().includes(searchText));
                    return cuisineMatch && searchMatch;
                });
                
                createMarkers(filteredData);
                
                // Fit map to filtered markers if any exist
                if (filteredData.length > 0) {
                    var bounds = L.latLngBounds(filteredData.map(r => [r.lat, r.lon]));
                    map.fitBounds(bounds, {padding: [50, 50]});
                }
            }
            
            function resetFilters() {
                document.getElementById('cuisine-filter').value = 'all';
                document.getElementById('search-input').value = '';
                createMarkers(restaurantsData);
                
                // Reset map view
                var allBounds = L.latLngBounds(restaurantsData.map(r => [r.lat, r.lon]));
                map.fitBounds(allBounds, {padding: [50, 50]});
            }
            
            // Allow Enter key to apply filters
            document.addEventListener('DOMContentLoaded', function() {
                document.getElementById('search-input').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        applyFilters();
                    }
                });
            });
        </script>
    </body>
    </html>
    {% endmacro %}
    """
    
    # Add the custom template to the map
    macro = MacroElement()
    macro._template = Template(template)
    m.get_root().add_child(macro)
    
    # Save the map
    print(f"\nSaving map to {output_file}...")
    m.save(output_file)
    
    # Summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Restaurants mapped: {len(df)}")
    print(f"Cuisine types: {len(cuisines)}")
    
    print(f"\nTop 10 cuisines:")
    cuisine_counts = df['Cuisine'].value_counts()
    for cuisine, count in cuisine_counts.head(10).items():
        print(f"  - {cuisine}: {count} restaurants")
    
    print("\n" + "=" * 80)
    print(f"✓ Advanced map saved to: {output_file}")
    print("=" * 80)
    print("\nFeatures:")
    print("✓ Dropdown filter by cuisine type")
    print("✓ Search by restaurant name")
    print("✓ Hover to see restaurant details (name, cuisine, address)")
    print("✓ Blue color scheme")
    print("✓ Dynamic restaurant count")
    print("✓ Apply and Reset filter buttons")
    
    return output_file


if __name__ == "__main__":
    try:
        print("\nCreating advanced interactive map...\n")
        
        output_file = create_advanced_map()
        
        print("\n" + "=" * 80)
        print("✓ Map creation completed!")
        print("=" * 80)
        
    except FileNotFoundError:
        print("\n✗ Error: Could not find CSV file")
        print("Make sure 'nyc_restaurant_week.csv' is in the same directory")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
