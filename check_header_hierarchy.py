import requests
from bs4 import BeautifulSoup

def check_header_hierarchy(url):
    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code!= 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize a stack to track the header hierarchy
    header_stack = []

    # Function to check if the current header is valid in the hierarchy
    def is_valid_header(header):
        if not header_stack:
            return True
        last_header = header_stack[-1]
        if header.name == 'h1':
            return True
        elif header.name == 'h2' and last_header in ['h1', 'h2']:
            return True
        elif header.name == 'h3' and last_header in ['h1', 'h2', 'h3']:
            return True
        return False

    # Iterate through all headers (H1, H2, H3)
    for header in soup.find_all(['h1', 'h2', 'h3']):
        if not is_valid_header(header):
            print(f"Invalid header hierarchy: {header.name} at {header.text.strip()}")
        else:
            # Push the current header onto the stack
            header_stack.append(header.name)
            # If the stack has more than one element and the current header is of a higher level than the previous one, pop elements until it's valid
            while len(header_stack) > 1 and int(header.name[1]) < int(header_stack[-2][1]):
                header_stack.pop()

    print("Header hierarchy check completed.")

# Example usage
url = "https://example.com"
check_header_hierarchy(url)
