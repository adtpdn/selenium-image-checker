import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

urls_to_check = [
    'https://adengroup.com',
    'https://www.adengroup.com',
    'https://adenenergies.com',
    'https://www.adenenergies.com',
    'https://nx-park.com',
    'https://www.nx-park.com'
    # Add more URLs as needed
]

def check_images_on_page(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    images = driver.find_elements(By.CSS_SELECTOR, 'img')
    missing_images = []

    for img in images:
        src = img.get_attribute('src')
        natural_width = img.get_attribute('naturalWidth')

        if natural_width == '0':
            missing_images.append({
                'name': src.split('/')[-1],
                'url': src
            })

    return missing_images

def run_test(browser_name):
    driver = None
    results = {}
    
    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    elif browser_name == 'firefox':
        options = FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

    try:
        for url in urls_to_check:
            print(f"Checking {url} with {browser_name}")
            missing_images = check_images_on_page(driver, url)

            results[url] = {
                'status': 'OK' if not missing_images else 'Missing Images',
                'missing_images': missing_images
            }

            if missing_images:
                print(f"Missing images on {url}:")
                for img in missing_images:
                    print(f"- {img['name']} ({img['url']})")
            else:
                print(f"No missing images found on {url}")
            print('---')
    finally:
        if driver:
            driver.quit()
    
    return results

def main():
    chrome_results = run_test('chrome')
    firefox_results = run_test('firefox')

    combined_results = {
        'timestamp': datetime.now().isoformat(),
        'chrome': chrome_results,
        'firefox': firefox_results
    }

    with open('results.json', 'w') as f:
        json.dump(combined_results, f, indent=2)

if __name__ == '__main__':
    main()