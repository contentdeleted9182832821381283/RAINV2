import sys
import concurrent.futures
import os
import colorama
from colorama import Fore, init
import ctypes
import requests
import time
import json
import threading

colorama.init()


def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)


set_console_title("Rain V2 (Modded With Love By Fog)")


def menu():
    global onstart
    print(f"""
{Fore.GREEN} qdwqdqd
{Fore.BLUE}                r                
{Fore.BLUE}               ain               
{Fore.BLUE}               rai                         
{Fore.BLUE}             rainrai             
{Fore.BLUE}            nrainrain                   
{Fore.BLUE}         ainrainrainrain         
{Fore.BLUE}        rainrainrainrainr        
{Fore.BLUE}    inra nrainrainrainrainrai   
{Fore.BLUE}  ain   nrainrainrainrainrainra
{Fore.BLUE}nrai   inrainrainrainrainrainrain
{Fore.BLUE}rai   inrainrainrainrainrainrainr
{Fore.BLUE}rain   nrainrainrainrainrainrainr
{Fore.BLUE} rainr  nrainrainrainrainrainrai 
{Fore.BLUE}  nrain ainrainrainrainrainrain  
{Fore.BLUE}    rainrainrainrainrainrainr    
{Fore.BLUE}      rainranirainrainrainr   
{Fore.BLUE}           ainrainrain     

{Fore.BLUE}8b,dPPYba, ,adPPYYba, 88 8b,dPPYba,  
{Fore.BLUE}88P'   "Y8 ""     `Y8 88 88P'   `"8a
{Fore.BLUE}88         ,adPPPPP88 88 88       88
{Fore.BLUE}88         88,    ,88 88 88       88
{Fore.BLUE}88         `"8bbdP"Y8 88 88       88
	raintool v2 by fog <3

[0] Exit{Fore.CYAN} [1] Proxy Scraper{Fore.BLUE} [2] Unfriender{Fore.CYAN} [3] Image Unlinker{Fore.BLUE} [4] Image Deleter       
{Fore.WHITE}
""")

    # input()

    command = input(">")

    if command == "0":
        print("> Do you really want to leave ?")
        command = input("> Y/N $>")
        time.sleep(1)

    if command == "1":
        def download_proxies(url, filename):
            """Download proxies from the URL and save to a file."""
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(filename, 'w') as f:
                        f.write(response.text.strip())
                    print(f"Successfully downloaded proxies to {filename}")
                    return True
            except Exception as e:
                print(f"Error downloading proxies: {e}")
                return False

        def test_proxy(proxy):
            """Test if a proxy works with google.com."""
            try:
                proxies = {
                    'http': f'http://{proxy.strip()}',
                    'https': f'http://{proxy.strip()}'
                }

                response = requests.get(
                    'http://www.google.com',
                    proxies=proxies,
                    timeout=5  # Reduced timeout for faster checking
                )

                if response.status_code == 200:
                    print(f"[VALID] {proxy.strip()}")
                    return (proxy.strip(), True)
                return (proxy.strip(), False)
            except:
                return (proxy.strip(), False)

        def main():
            # Get thread count from user
            while True:
                try:
                    thread_count = int(input("Enter number of threads to use: "))
                    if thread_count > 0:
                        break
                    print("Please enter a positive number")
                except ValueError:
                    print("Please enter a valid number")

            # Download proxies
            proxy_url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all"
            proxy_file = "proxies.txt"

            if not download_proxies(proxy_url, proxy_file):
                print("Failed to download proxies. Exiting.")
                return

            # Read proxies from file
            try:
                with open(proxy_file, 'r') as f:
                    proxies = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"Error reading proxy file: {e}")
                return

            print(f"Testing {len(proxies)} proxies using {thread_count} threads...")

            # Test proxies in parallel
            working_proxies = []
            start_time = time.time()

            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
                future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}

                for future in concurrent.futures.as_completed(future_to_proxy):
                    proxy, is_working = future.result()
                    if is_working:
                        working_proxies.append(proxy)

            # Save working proxies to file without extra spaces
            with open('working_proxies.txt', 'w') as f:
                f.write('\n'.join(working_proxies))

            end_time = time.time()
            duration = end_time - start_time

            print(f"\nResults:")
            print(f"Total proxies tested: {len(proxies)}")
            print(f"Working proxies found: {len(working_proxies)}")
            print(f"Time taken: {duration:.2f} seconds")
            print(f"Working proxies saved to: working_proxies.txt")

        if __name__ == "__main__":
            main()

    if command == "2":
        init(autoreset=True)

        class UnfriendManager:
            def __init__(self, token, max_threads, proxy=None):
                self.token = token
                self.max_threads = max_threads
                self.headers = {
                    'Authorization': f'bearer {token}',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                }
                self.api_base = "https://api.rec.net/api"
                self.rate_limit_delay = 1.0  # Delay between requests in seconds
                self.proxy = proxy

            def get_with_retries(self, url, retries=5, delay=2):
                proxies = {
                    "http": f"http://{self.proxy['username']}:{self.proxy['password']}@{self.proxy['ip']}:{self.proxy['port']}",
                    "https": f"https://{self.proxy['username']}:{self.proxy['password']}@{self.proxy['ip']}:{self.proxy['port']}"
                } if self.proxy else None

                for attempt in range(retries):
                    response = requests.get(url, headers=self.headers, proxies=proxies)
                    if response.status_code == 200:
                        return response
                    else:
                        print(
                            f"Attempt {attempt + 1} failed with status code {response.status_code}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                raise Exception(f"{Fore.RED}Failed to get a successful response after {retries} retries.")

            def delete_with_retries(self, url, retries=5, delay=2):
                proxies = {
                    "http": f"http://{self.proxy['username']}:{self.proxy['password']}@{self.proxy['ip']}:{self.proxy['port']}",
                    "https": f"https://{self.proxy['username']}:{self.proxy['password']}@{self.proxy['ip']}:{self.proxy['port']}"
                } if self.proxy else None

                for attempt in range(retries):
                    response = requests.delete(url, headers=self.headers, proxies=proxies)
                    if response.status_code == 200:
                        return response
                    else:
                        print(
                            f"Attempt {attempt + 1} failed with status code {response.status_code}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                raise Exception(f"Failed to get a successful response after {retries} retries.")

            def get_relationships(self):
                """Fetch all relationships from the API with retries"""
                url = f"{self.api_base}/relationships/v2/get"
                response = self.get_with_retries(url)
                return response.json()

            def unfriend_user(self, relationship):
                """Unfriend a single user with proper error handling and rate limiting"""
                friend_id = relationship.get('PlayerID')
                if not friend_id:
                    print(f"{Fore.YELLOW}Invalid relationship data: {relationship}")
                    return False

                try:
                    url = f"{self.api_base}/relationships/v3/{friend_id}"

                    # Primary DELETE request with retries
                    response = self.delete_with_retries(url)

                    # Rate limiting delay
                    time.sleep(self.rate_limit_delay)

                    if response.status_code == 200:
                        print(f"{Fore.GREEN}Successfully unfriended user {friend_id}")
                        return True
                    else:
                        print(f"{Fore.RED}Failed to unfriend {friend_id}: Status {response.status_code}")
                        return False

                except requests.exceptions.RequestException as e:
                    print(f"{Fore.RED}Network error while unfriending {friend_id}: {str(e)}")
                    return False
                except Exception as e:
                    print(f"{Fore.RED}Unexpected error while unfriending {friend_id}: {str(e)}")
                    return False

            def process_all_relationships(self):
                """Process all relationships using a thread pool"""
                try:
                    print(f"{Fore.CYAN}Fetching relationships...")
                    relationships = self.get_relationships()
                    total_relationships = len(relationships)

                    if not relationships:
                        print(f"{Fore.YELLOW}No relationships found to process.")
                        return

                    print(f"{Fore.CYAN}Found {total_relationships} relationships to process")
                    successful = 0
                    failed = 0

                    with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                        # Submit all tasks and get future objects
                        future_to_relationship = {
                            executor.submit(self.unfriend_user, relationship): relationship
                            for relationship in relationships
                        }

                        # Process completed futures as they finish
                        for future in concurrent.futures.as_completed(future_to_relationship):
                            relationship = future_to_relationship[future]
                            try:
                                if future.result():
                                    successful += 1
                                else:
                                    failed += 1
                            except Exception as e:
                                print(f"{Fore.RED}Error processing relationship: {str(e)}")
                                failed += 1

                            # Print progress
                            completed = successful + failed
                            print(f"{Fore.CYAN}Progress: {completed}/{total_relationships} "
                                  f"({successful} successful, {failed} failed)")

                    print(f"\n{Fore.GREEN}Operation completed!")
                    print(f"{Fore.GREEN}Total successful: {successful}")
                    print(f"{Fore.RED}Total failed: {failed}")

                except Exception as e:
                    print(f"{Fore.RED}Fatal error in main process: {str(e)}")

        def parse_proxy(proxy_str):
            parts = proxy_str.split(':')
            return {
                'ip': parts[0],
                'port': parts[1],
                'username': parts[2],
                'password': parts[3]
            }

        def main():
            try:
                with open('auth.txt', 'r') as file:
                    token = file.read().strip()

                max_threads = int(input(f"{Fore.MAGENTA}Enter number of threads to use: "))
                proxy_str = input(
                    f"{Fore.MAGENTA}Enter proxy (IP:PORT:USERNAME:PASSWORD) or leave blank to not use proxy: ").strip()
                proxy = parse_proxy(proxy_str) if proxy_str else None

                manager = UnfriendManager(token, max_threads, proxy)
                manager.process_all_relationships()

            except ValueError:
                print(f"{Fore.RED}Please enter a valid number for threads")
            except Exception as e:
                print(f"{Fore.RED}Fatal error: {str(e)}")

            input(f"\n{Fore.CYAN}Press Enter to exit...")

        if __name__ == "__main__":
            main()

    if command == "3":

        def check_account():
            token = load_token('auth.txt')
            url = "https://accounts.rec.net/account/me"
            headers = {
                'Authorization': f'bearer {token}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'BestHTTP'
            }

            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    account_data = response.json()
                    # Store the account data in id.txt
                    with open('id.txt', 'w') as f:
                        json.dump(account_data, f, indent=4)
                    print(f"{Fore.GREEN}Account data successfully stored in id.txt")
                    return True
                else:
                    print(f"{Fore.RED}Failed to get account data. Status code: {response.status_code}")
                    return False
            except Exception as e:
                print(f"{Fore.RED}Error checking account: {e}")
                return False

        def load_token(filename):
            """Load authorization token from file."""
            with open(filename, 'r') as file:
                return file.read().strip()

        def get_image_ids(account_id):
            token = load_token('auth.txt')
            url = f"https://apim.rec.net/apis/api/images/v3/feed/player/{account_id}"

            headers = {
                'Authorization': f'bearer {token}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'BestHTTP'
            }

            params = {
                'skip': 0,
                'take': 100
            }

            try:
                response = requests.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()

                    if data and isinstance(data, list):
                        image_ids = [item['Id'] for item in data if 'Id' in item]
                        return image_ids
                    else:
                        print(f"{Fore.RED}No valid data found in response")
                        return []
                else:
                    print(f"{Fore.RED}Failed to get images. Status code: {response.status_code}")
                    return []

            except requests.exceptions.RequestException as e:
                print(f"Error making request: {e}")
                return []
            except ValueError as e:
                print(f"Error parsing JSON: {e}")
                return []

        def read_account_id(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                account_id = data.get("accountId")
                return account_id

        file_path = 'id.txt'

        def untag_image(image_id, headers, account_id):
            untag_url = f"https://api.rec.net/api/images/v1/{image_id}/player/{account_id}/untag"
            try:
                response = requests.put(untag_url, headers=headers)
                if response.status_code == 200:
                    print(f"Successfully untagged image {image_id}")
                    return True
                elif response.status_code == 429:
                    print(f"Rate limited. Retrying image {image_id} in 5 seconds.")
                    time.sleep(5)  # Wait before retrying
                    return untag_image(image_id, headers, account_id)  # Retry
                else:
                    print(f"{Fore.RED}Failed to untag image {image_id}. Status code: {response.status_code}")
                    return False
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}Error untagging image {image_id}: {e}")
                return False

        def main():
            # Ask user for the number of threads
            num_threads = int(input(f"{Fore.CYAN}How many threads would you like? "))

            # First check account and store data
            if not check_account():
                print(f"{Fore.RED}Failed to verify account. Exiting...")
                return

            # Read account ID from file
            account_id = read_account_id(file_path)
            print(f"{Fore.GREEN}Successfully read! {account_id}")

            # Get all image IDs
            image_ids = get_image_ids(account_id)

            if not image_ids:
                print(f"{Fore.RED}No images found to untag")
                return

            print(f"Found {len(image_ids)} images to untag")

            token = load_token('auth.txt')
            # Setup headers for untag requests
            headers = {
                'Authorization': f'bearer {token}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'BestHTTP'
            }

            # Process each image ID using threads
            successful_untags = 0

            def process_images(image_subset):
                nonlocal successful_untags
                for image_id in image_subset:
                    if untag_image(image_id, headers, account_id):
                        successful_untags += 1
                    time.sleep(1)  # Add a delay between requests to avoid rate limiting

            # Split image IDs into chunks for threading
            chunk_size = len(image_ids) // num_threads
            threads = []
            for i in range(num_threads):
                start_index = i * chunk_size
                end_index = (i + 1) * chunk_size if i != num_threads - 1 else len(image_ids)
                thread = threading.Thread(target=process_images, args=(image_ids[start_index:end_index],))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            print(f"\nUntagging complete. Successfully untagged {successful_untags} out of {len(image_ids)} images")

        if __name__ == "__main__":
            main()

    if command == "4":

        def check_account():
            token = load_token('auth.txt')
            url = "https://accounts.rec.net/account/me"
            headers = {
                'Authorization': f'bearer {token}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'BestHTTP'
            }

            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    account_data = response.json()
                    # Store the account data in id.txt
                    with open('id.txt', 'w') as f:
                        json.dump(account_data, f, indent=4)
                    print("Account data successfully stored in id.txt")
                    return True
                else:
                    print(f"Failed to get account data. Status code: {response.status_code}")
                    return False
            except Exception as e:
                print(f"Error checking account: {e}")
                return False

        def load_token(filename):
            """Load authorization token from file."""
            with open(filename, 'r') as file:
                return file.read().strip()

        def get_image_ids(account_id):
            token = load_token('auth.txt')
            url = f"https://apim.rec.net/apis/api/images/v4/player/{account_id}"

            headers = {
                'Authorization': f'bearer {token}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'BestHTTP'
            }

            params = {
                'skip': 0,
                'take': 10000,
                'sort': 0
            }

            try:
                response = requests.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()

                    if data and isinstance(data, list):
                        image_ids = [item['Id'] for item in data if 'Id' in item]
                        return image_ids
                    else:
                        print(f"{Fore.RED}No valid data found in response")
                        return []
                else:
                    print(f"{Fore.RED}Failed to get images. Status code: {response.status_code}")
                    return []

            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}Error making request: {e}")
                return []
            except ValueError as e:
                print(f"{Fore.RED}Error parsing JSON: {e}")
                return []

        def read_account_id(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                account_id = data.get("accountId")
                return account_id

        file_path = 'id.txt'

        def untag_image(image_id, headers, account_id):
            untag_url = f"https://api.rec.net/api/images/v1/{image_id}"
            try:
                response = requests.delete(untag_url, headers=headers)
                if response.status_code == 200:
                    print(f"{Fore.GREEN}Successfully deleted image {image_id}")
                    return True
                elif response.status_code == 429:
                    print(f"{Fore.YELLOW}Rate limited. Retrying image {image_id} in 5 seconds.")
                    time.sleep(5)  # Wait before retrying
                    return untag_image(image_id, headers, account_id)  # Retry
                else:
                    print(f"{Fore.RED}Failed to untag image {image_id}. Status code: {response.status_code}")
                    return False
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}Error deleting image {image_id}: {e}")
                return False

        def main():
            # Ask user for the number of threads
            num_threads = int(input(f"{Fore.MAGENTA}How many threads would you like? "))

            # First check account and store data
            if not check_account():
                print(f"{Fore.YELLOW}Failed to verify account. Exiting...")
                return

            # Read account ID from file
            account_id = read_account_id(file_path)
            print(f"{Fore.BLUE}Successfully read! {account_id}")

            # Get all image IDs
            image_ids = get_image_ids(account_id)

            if not image_ids:
                print(f"{Fore.RED}No images found to untag")
                return

            print(f"{Fore.YELLOW}Found {len(image_ids)} images to delete")

            token = load_token('auth.txt')
            # Setup headers for untag requests
            headers = {
                'Authorization': f'bearer {token}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'BestHTTP'
            }

            # Process each image ID using threads
            successful_untags = 0

            def process_images(image_subset):
                nonlocal successful_untags
                for image_id in image_subset:
                    if untag_image(image_id, headers, account_id):
                        successful_untags += 1
                    time.sleep(1)  # Add a delay between requests to avoid rate limiting

            # Split image IDs into chunks for threading
            chunk_size = len(image_ids) // num_threads
            threads = []
            for i in range(num_threads):
                start_index = i * chunk_size
                end_index = (i + 1) * chunk_size if i != num_threads - 1 else len(image_ids)
                thread = threading.Thread(target=process_images, args=(image_ids[start_index:end_index],))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            print(f"\nUntagging complete. Successfully deleted {successful_untags} out of {len(image_ids)} images")

        if __name__ == "__main__":
            main()

    if command == "Y":
        time.sleep(1)
        print("> Exiting.. See you next time !")
        time.sleep(1)
        sys.exit(0)

    if command == "N":
        time.sleep(1)
        print("> Nevermind.. You're Back !")
        time.sleep(1)
        onstart()

    if command == "help":
        time.sleep(1)
        print("""> Contact :

            Discord ID : @Goyardfog
	    Developed by funnymonkegif

        """)
        time.sleep(1)
        onstart()

    if command == "shutdown":
        sys.exit()


def onstart():
    cmd = 'mode 120,28'
    os.system(cmd)
    os.system(
        "cls && title yurple unfriender by yurple <3")
    menu()


onstart()


