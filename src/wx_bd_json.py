import time

import requests


def parse_book_data(url_template: str, start_max_index: int = 0, start_rank: int = 1) -> list:
    """
    循环解析接口返回的JSON数据，提取书名和作者信息
    :param url_template: 接口URL模板（需包含{maxIndex}和{rank}占位符）
    :param start_max_index: 起始maxIndex值（默认0）
    :param start_rank: 起始rank值（默认1）
    :return: 包含书名和作者的列表
    """
    all_books = []
    current_max_index = start_max_index
    current_rank = start_rank
    has_more = 1  # 控制循环的标志

    while has_more < 10:
        # 构建当前请求的URL
        current_url = url_template.format(maxIndex=current_max_index, rank=current_rank)

        try:
            response = requests.get(current_url)
            response.raise_for_status()  # 抛出HTTP错误
            data = response.json()

            # 解析JSON数据
            books = data.get("books", [])
            if not books:
                break  # 无数据时提前终止

            # 提取书名和作者
            for book in books:
                book_info = book.get("bookInfo", {})
                title = book_info.get("title", "未知书名")
                author = book_info.get("author", "未知作者")
                all_books.append({"书名": title, "作者": author})

            # 更新下一页参数
            current_max_index += len(books)  # maxIndex通常为下一页起始索引
            current_rank = 1  # rank为下一页起始排名
            has_more += 1  # 判断是否有更多数据（1表示有）
            time.sleep(5)

            print(
                f"已获取{len(books)}条数据，当前maxIndex={current_max_index - len(books)}, rank=1,has_more={has_more}")

        except requests.exceptions.RequestException as e:
            print(f"请求出错: {e}")
            break
        except KeyError as e:
            print(f"JSON结构异常，缺少键: {e}")
            break

    return all_books


if __name__ == "__main__":
    # 接口URL模板（注意：实际使用时需确保该URL有效且支持maxIndex和rank参数）
    API_URL_TEMPLATE = "https://weread.qq.com/web/bookListInCategory/all?maxIndex={maxIndex}&rank={rank}"

    # 开始解析数据
    books_data = parse_book_data(API_URL_TEMPLATE)

    # 输出结果
    print(f"\n共解析到{len(books_data)}本书籍:")
    for idx, book in enumerate(books_data, 1):
        print(f"- {book['书名']} {book['作者']}")
