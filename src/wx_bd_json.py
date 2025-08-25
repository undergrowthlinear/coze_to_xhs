import datetime
import time
from typing import List, Dict, Any

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

    while has_more < 30:
        # 构建当前请求的URL
        current_url = url_template.format(maxIndex=current_max_index, rank=current_rank)

        print(current_url)

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://weread.qq.com/web/category/1000005",  # 添加来源页（可选，部分服务器需要）
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
            }

            response = requests.get(current_url, headers=headers)
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


def generate_reading_plans(books: List[str], start_date: datetime.date, days_per_batch: int = 1) -> List[
    Dict[str, Any]]:
    plans = []
    for i in range(0, len(books), 20):
        batch_books = books[i:i + 20]
        end_date = start_date + datetime.timedelta(days=days_per_batch - 1)

        plan = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "books": batch_books
        }
        plans.append(plan)

        # 更新下一批的开始日期
        start_date = end_date + datetime.timedelta(days=1)

    return plans


if __name__ == "__main__":
    # 接口URL模板（注意：实际使用时需确保该URL有效且支持maxIndex和rank参数）
    # top 200 总榜
    # API_URL_TEMPLATE = "https://weread.qq.com/web/bookListInCategory/all?maxIndex={maxIndex}&rank={rank}"
    # 神作
    # API_URL_TEMPLATE = "https://weread.qq.com/web/bookListInCategory/newrating_publish?maxIndex={maxIndex}&rank={rank}"
    # 小说
    # API_URL_TEMPLATE = "https://weread.qq.com/web/bookListInCategory/general_novel_rising?maxIndex={maxIndex}&rank={rank}"
    # 个人成长 人在职场
    #API_URL_TEMPLATE = "https://weread.qq.com/web/bookListInCategory/1000005?maxIndex={maxIndex}"
    # 个人成长 认知思维
    #API_URL_TEMPLATE = "https://weread.qq.com/web/bookListInCategory/1000006?maxIndex={maxIndex}"
    # 生活百科 情感
    # API_URL_TEMPLATE = "https://weread.qq.com/web/bookListInCategory/1600005?maxIndex={maxIndex}"
    # 生活百科 旅游
    API_URL_TEMPLATE = "https://weread.qq.com/web/bookListInCategory/1600002?maxIndex={maxIndex}"

    # 开始解析数据
    books_data = parse_book_data(API_URL_TEMPLATE)

    # 输出结果
    #   - start_date: "2025-05-31"
    #     end_date: "2025-05-31"
    #     books:
    #       - “她”的力量 露西·库克
    print(f"\n共解析到{len(books_data)}本书籍:")
    start = datetime.date(2025, 8, 9)

    # 生成阅读计划
    reading_plans = generate_reading_plans(books_data, start)

    # 输出YAML格式（仅示例，实际使用需导入yaml库）
    for plan in reading_plans:
        print(f"- start_date: \"{plan['start_date']}\"")
        print(f"  end_date: \"{plan['end_date']}\"")
        print("  books:")
        for book in plan['books']:
            print(f"    - {book['书名']} {book['作者']}")
        print()
