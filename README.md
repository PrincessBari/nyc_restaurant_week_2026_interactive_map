CREATING A MAP USING FOLIUM:

NYC Restaurant Week occurs twice a year, once in winter and again in late summer. For this year’s winter 2026 session from Jan. 20th-Feb. 12th,
I noticed that their website, https://www.nyctourism.com/restaurant-week/, lists the 653 participating restaurants across 55 pages with filtering
options, but that there’s no map available.

As someone who loves maps and making them, I decided I’d give it a go!

At first, I tried to scrape all the relevant data - including restaurant name, description, and address - by clicking into each restaurant’s individual
page on the website. However, the structure of the website proved challenging. 653 restaurants are displayed across 55 pages, with 12 hyperlinked cards
on each page (except the last page, which has 5 on it). So while I could get the restaurant name, cuisine type, and neighborhood easily from the 12 cards
on the same page, if I wanted the actual description of the restaurant and its address, you had to click into the card and get to a separate page just for
that restaurant. 

Once there, you couldn’t easily return to the previous page with the 12 restaurants just by clicking on the back arrow, and there was no forward arrow to
navigate to the next of the 12 restaurants. To leave the page, you had to scroll to the top of the page, and click “Restaurant Week,” which took you back
to the website’s first page. So if you were on the 2nd, 3rd, 4th, or any page through the 55th, once you were back on that very first page, you’d then have
to navigate back to whatever page you’d been on last to retrieve more restaurant data.

There were also timeout issues since information loads dynamically via lazy scrolling.

1) Because it was too circuitous, finally, I decided to just have Selenium scrape the restaurant name, cuisine type, and neighborhood from the 12 cards on each
of the main 55 pages - instead of clicking into anything - via the file **scrape_restaurants_cards_only.py**, which produced the csv file **nyc_restaurant_week.csv**.

2) Then, I appended each entry in the “Neighborhood” column with “, New York, NY”, so that it’d say “Brooklyn Heights, New York, NY”, “Soho, New York, NY”,
etc, via the **append_neighborhoods.py** file resulting in the csv file **nyc_restaurants_nyc.csv**.

3) Then, I used the Google Places API to append my csv file with the actual addresses of the restaurants via the file **places.py**, resulting in the file **restaurants_with_addresses.csv**.

4) Then, I used the Google Geocoding API to convert the addresses into latitude and longitude and appended my csv file with those new columns via the file geocoding_google_api.py, which produced the csv file **restaurants_geocoded.csv**.

(Also, I noticed that 3 restaurants had neighborhood info for Cuisine because on the website, that’s what data had been inserted into that html section. So I did
have to manually enter the info for those 3.)

5) Finally, I created a map using Folium via the file swipeable_filter_at_bottom.py. It features a filter option by cuisine type, a search bar for restaurant names, and hover tooltip functionality showing each restaurant’s name, cuisine type, and address. On mobile, the filter appears on the bottom half of the page and can be minimized by swiping down on the drag handle.

Please enjoy my interactive site on either desktop or mobile at
https://princessbari.github.io/nyc_restaurant_week_2026_interactive_map/.
