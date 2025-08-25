import yaml
from datetime import date


def get_books_by_date(yaml_path: str = "/Users/linear/myown/code/coze_to_xhs/src/books.yaml") -> list:
    """根据当前日期从 YAML 配置中获取对应的书籍列表"""
    # 读取 YAML 文件
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 获取当前日期
    today = date.today()

    # 遍历配置中的日期范围，查找匹配的书籍列表
    for period in config.get("reading_plan", []):
        start = date.fromisoformat(period["start_date"])
        end = date.fromisoformat(period["end_date"])

        if start <= today <= end:
            return period["books"]

    # 如果没有找到匹配的日期范围，返回空列表
    return []


# 使用示例
if __name__ == "__main__":
    books = get_books_by_date()

    if books:
        print(f"今日 ({date.today()}) 阅读计划：")
        for book in books:
            print(f"- {book} ")
    else:
        print("今日没有阅读计划")
