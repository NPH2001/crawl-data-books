import requests
from bs4 import BeautifulSoup
import csv
import time

# Đọc danh sách URL từ file txt
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip()]


# Thêm User-Agent để tránh bị chặn
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
}

# Danh sách lưu thông tin sách
books = []

# Lặp qua từng URL trong danh sách
for url in urls:
    # Gửi yêu cầu GET đến trang web
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')


    # Tìm các thẻ chứa thông tin sách và lấy link chi tiết
    for item in soup.find_all('div', class_='product-item'):
        book_info = {}

        # Lấy tiêu đề và link chi tiết của sách
        title_tag = item.find('h3', class_='pro-name')
        if title_tag:
            title = title_tag.text.strip()
            detail_url = "https://www.vinabook.com" + title_tag.find('a')['href']
            
            # Gửi yêu cầu đến trang chi tiết của sách
            detail_response = requests.get(detail_url, headers=headers)
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

            for row in detail_soup.find_all('tr'):
                header = row.find('th').text.strip() if row.find('th') else None
                value = row.find('td').text.strip() if row.find('td') else None
                
                if header and value:
                    book_info[header] = value
                
            # Lấy thông tin chi tiết từ trang sách
            price = detail_soup.select_one('span.pro-price').text.strip() if detail_soup.select_one('span.pro-price') else 'N/A'
            description = detail_soup.select_one('div.product-description').text.strip() if detail_soup.select_one('div.product-description') else 'N/A'
            image_url = detail_soup.find('img', {'class': 'product-image-feature'})['src'] if detail_soup.find('img', {'class': 'product-image-feature'}) else 'N/A'
            
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            elif image_url.startswith("/"):
                image_url = "https://www.vinabook.com" + image_url
            
            # Lưu thông tin vào danh sách
            books.append({
                'Title': title,
                'Author': book_info.get("Tác giả"),
                'Price': price,
                'Language': book_info.get("Ngôn Ngữ"),
                'Weight': book_info.get("Trọng lượng"),
                'Publisher': book_info.get("NXB"),
                'Publish Year': book_info.get("Năm XB"),
                'Description': description,
                'Image URL': image_url,
                'Detail URL': detail_url
            })

            # Tránh gửi yêu cầu quá nhanh
            time.sleep(1)

# Ghi dữ liệu vào file CSV
with open('vinabook_books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Price', 'Language', 'Publish Year', 'Publisher', 'Weight', 'Description', 'Image URL', 'Detail URL'])
    writer.writeheader()
    writer.writerows(books)

print("Dữ liệu đã được ghi vào file vinabook_books.csv")
