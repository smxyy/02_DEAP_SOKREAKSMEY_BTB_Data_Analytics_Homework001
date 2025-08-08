import time

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestispiderSpider(scrapy.Spider):
    name = "testispider"
    allowed_domains = ["web-scraping.dev"]
    start_urls = ["http://web-scraping.dev/login?cookies="]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url = url,
                callback = self.process_login,
                wait_time = 10,
                wait_until = EC.element_to_be_clickable((By.CLASS_NAME, "modal-dialog"))
            )

    def process_login(self, response):
        driver = response.meta["driver"]
        try:
            button_ok = driver.find_element(By.ID, "cookie-ok")
            if button_ok :
                button_ok.click()
        except Exception:
            pass

        username_field = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        username_field.clear()
        username_field.send_keys("user123")

        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        password_field.clear()
        password_field.send_keys("password")

        button_submit = driver.find_element(By.XPATH, "//button[@type='submit']")
        if button_submit :
            button_submit.click()

        time.sleep(3)

        cookies = driver.get_cookies()
        if any(c["name"].lower() == "auth" for c in cookies):
            driver.get("https://web-scraping.dev/testimonials")
            time.sleep(2)

            # --- Auto-scroll logic ---
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            html = driver.page_source

            # Return response to Scrapy for parsing
            response_object = scrapy.http.HtmlResponse(
                url = driver.current_url,
                body = html,
                encoding = "utf-8",
                request = response.request
            )
            yield from self.parse_testimonials(response_object)

    def parse_testimonials(self, response):
        testimonials = response.xpath('//div[@class="testimonial"]')
        if not testimonials:
            self.logger.warning("No testimonials found!")

        for testimonial in testimonials:
            yield {
                'testimony': testimonial.xpath('.//p[@class="text"]/text()').get(),
                'ratings': len(testimonial.xpath('.//span[contains(@class,"rating")]/svg'))
            }