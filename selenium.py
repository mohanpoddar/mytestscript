
===========
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Enable performance logging
capabilities = DesiredCapabilities.CHROME.copy()
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

# Initialize WebDriver with desired capabilities
service = Service("/path/to/chromedriver")  # Replace with your chromedriver path
driver = webdriver.Chrome(service=service, desired_capabilities=capabilities)

==============

def log_filter(log_) -> bool:
    return (
        # is an actual response
        log_["method"] == "Network.responseReceived"
        # and json
        and "json" in log_["params"]["response"]["mimeType"]
    )

def filter_products(self) -> list:
    products = []
    for log in filter(log_filter, self.logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        try:
            if "search" in resp_url:
                # Fetch the response headers
                d1 = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                headers = log["params"]["response"]["headers"]
                print(f"Response Headers for {resp_url}: {headers}")
                
                # (Optional) Process response body if still needed
                data = json.loads(d1["body"])
                for i in data["layout"]:
                    if len(i["data"]["resolver"]["data"]["items"]) != 0:
                        for j in i["data"]["resolver"]["data"]["items"]:
                            products.append(j["productResponse"])
        except Exception as e:
            print("Caught Exception: ", e)

    return products

logs_raw = self.driver.get_log("performance")
self.logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
self.products = self.filter_products()
