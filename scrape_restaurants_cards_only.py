# NYC Restaurant Week web scraping 
# ================================
# Extracts restaurant name, cuisine, and neighborhood directly from the listing cards. There are 55
# pages with 12 restaurants on each page (and less than 12 on the last page)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def scrape_restaurant_week():
 
    # Scrape restaurant data directly from listing cards.
    
    base_url = "https://www.nyctourism.com/restaurant-week/"
    all_restaurants = []
    
    # Set up Chrome options
    chrome_options = Options()
    # Uncomment the next line to run in headless mode (no browser window)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    print("=" * 80)
    print("NYC Restaurant Week Scraper - Simple Card Reading")
    print("=" * 80)
    print("\nInitializing browser...")
    
    # Initialize the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    
    try:
        page_count = 0
        max_pages = 55
        
        # Start at the main page
        driver.get(base_url)
        time.sleep(3)
        
        while page_count < max_pages:
            page_count += 1
            print(f"\n{'='*80}")
            print(f"Page {page_count}/{max_pages}")
            print(f"{'='*80}")
            
            # Handle lazy loading by scrolling through the page
            print("Loading all cards...")
            
            # Scroll down incrementally
            for scroll_step in range(5):
                driver.execute_script(f"window.scrollTo(0, {(scroll_step + 1) * 500});")
                time.sleep(0.3)
            
            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Scroll back to top
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Wait for restaurant cards to load
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h3.CardHeading_headline__qu1q3"))
                )
            except:
                print("  ⚠ Timeout waiting for restaurant cards to load")
                break
            
            # Find all restaurant names
            restaurant_names = driver.find_elements(By.CSS_SELECTOR, "h3.CardHeading_headline__qu1q3")
            
            # Find all tag containers (for cuisine and neighborhood)
            tag_containers = driver.find_elements(By.CSS_SELECTOR, "div.PromotionCardGrid_taglines__qTyHJ")
            
            num_restaurants = len(restaurant_names)
            print(f"Found {num_restaurants} restaurants on this page")
            
            if num_restaurants == 0:
                print("  ⚠ No restaurants found on this page")
                break
            
            # Process each restaurant
            for i in range(num_restaurants):
                try:
                    # Get restaurant name
                    restaurant_name = restaurant_names[i].text.strip()
                    
                    # Get cuisine and neighborhood from the corresponding tag container
                    cuisine = ""
                    neighborhood = ""
                    
                    if i < len(tag_containers):
                        tags = tag_containers[i].find_elements(By.CSS_SELECTOR, "div.Tag_tag__cc4nK")
                        
                        # First tag is typically cuisine, second is neighborhood
                        if len(tags) >= 1:
                            cuisine = tags[0].text.strip()
                        if len(tags) >= 2:
                            neighborhood = tags[1].text.strip()
                    
                    # Add to results
                    all_restaurants.append({
                        'Restaurant': restaurant_name,
                        'Cuisine': cuisine,
                        'Neighborhood': neighborhood
                    })
                    
                    print(f"  {i+1}. {restaurant_name} | {cuisine} | {neighborhood}")
                    
                except Exception as e:
                    print(f"  ✗ Error processing restaurant {i+1}: {str(e)[:50]}")
                    continue
            
            print(f"\n  📊 Total restaurants collected: {len(all_restaurants)}")
            
            # Move to next page
            try:
                # Scroll to pagination area
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                # Find next button
                next_button = driver.find_element(By.CSS_SELECTOR, "li.next a")
                
                # Check if disabled
                parent_li = next_button.find_element(By.XPATH, "..")
                parent_classes = parent_li.get_attribute("class") or ""
                
                if "disabled" in parent_classes:
                    print("\n  ℹ Next button is disabled - reached the end")
                    break
                
                # Click next
                print(f"\n  → Moving to page {page_count + 1}...")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                time.sleep(0.5)
                
                # Try regular click first
                try:
                    next_button.click()
                except:
                    # If regular click fails, use JavaScript
                    driver.execute_script("arguments[0].click();", next_button)
                
                time.sleep(3)  # Wait for new page to load
                
            except Exception as e:
                print(f"\n  ℹ Could not find next button - reached the end")
                break
        
    finally:
        # Close the browser
        print("\n" + "=" * 80)
        print("Closing browser...")
        driver.quit()
    
    # Write to CSV
    output_file = 'nyc_restaurant_week.csv'
    
    print("\n" + "=" * 80)
    print("Writing results to CSV...")
    print("=" * 80)
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Restaurant', 'Cuisine', 'Neighborhood']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for restaurant in all_restaurants:
                writer.writerow(restaurant)
        
        print(f"✓ Successfully saved {len(all_restaurants)} restaurants to: {output_file}")
        
        # Print summary statistics
        print("\n" + "=" * 80)
        print("Summary")
        print("=" * 80)
        print(f"Pages scraped: {page_count}")
        print(f"Total restaurants: {len(all_restaurants)}")
        
        # Count unique cuisines and neighborhoods
        cuisines = set(r['Cuisine'] for r in all_restaurants if r['Cuisine'])
        neighborhoods = set(r['Neighborhood'] for r in all_restaurants if r['Neighborhood'])
        
        print(f"Unique cuisines: {len(cuisines)}")
        print(f"Unique neighborhoods: {len(neighborhoods)}")
        
        # Count complete entries
        complete = sum(1 for r in all_restaurants if r['Restaurant'] and r['Cuisine'] and r['Neighborhood'])
        print(f"Complete entries: {complete}/{len(all_restaurants)}")
        
        # Show first few restaurants as preview
        if all_restaurants:
            print("\nPreview (first 10 restaurants):")
            print("-" * 80)
            for i, rest in enumerate(all_restaurants[:10], 1):
                print(f"{i}. {rest['Restaurant']}")
                print(f"   Cuisine: {rest['Cuisine']}")
                print(f"   Neighborhood: {rest['Neighborhood']}")
        
        return output_file
        
    except Exception as e:
        print(f"✗ Error writing CSV: {str(e)}")
        return None


if __name__ == "__main__":
    try:
        print("\nStarting simple scraper...")
        print("This will open a Chrome browser window.")
        print("It will just read the cards without clicking into them.\n")
        
        output_file = scrape_restaurant_week()
        
        if output_file:
            print("\n" + "=" * 80)
            print("✓ Scraping completed successfully!")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("✗ Scraping failed")
            print("=" * 80)
            
    except KeyboardInterrupt:
        print("\n\n✗ Scraping interrupted by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
