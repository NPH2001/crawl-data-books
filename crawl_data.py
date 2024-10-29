import requests
from bs4 import BeautifulSoup
import csv

# URL của trang Vinabook
url = 'https://www.vinabook.com/collections/sach-kinh-te'

# Gửi yêu cầu GET đến trang web
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Danh sách lưu thông tin sách
books = []

# Tìm các thẻ chứa thông tin sách
for item in soup.find_all('div', class_='product-item'):
    title = item.find('h3', class_='pro-name').text.strip() if item.find('h3', class_='pro-name') else 'N/A'
    author = item.find('p', class_='author').text.strip() if item.find('p', class_='author') else 'N/A'
    price = item.find('del', class_='compare-price').text.strip() if item.find('del', class_='compare-price') else 'N/A'
    summary = item.find('div', class_='summary').text.strip() if item.find('div', class_='summary') else 'N/A'
    image_url = "https:" + item.find('img')['src'] if item.find('img') else 'N/A'
    
    # Lưu thông tin vào danh sách
    books.append({
        'Title': title,
        'Author': author,
        'Price': price,
        'Summary': summary,
        'Image URL': image_url
    })

# Ghi dữ liệu vào file CSV
with open('vinabook_books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Price', 'Summary', 'Image URL'])
    writer.writeheader()
    writer.writerows(books)

print("Dữ liệu đã được ghi vào file vinabook_books.csv")
