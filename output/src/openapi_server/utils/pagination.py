from typing import List, Any, Dict

def paginate(items: List[Any], page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """
    简单内存分页工具。
    :param items: 待分页的列表
    :param page: 当前页码（从1开始）
    :param page_size: 每页数量
    :return: 分页结果 dict，包括总数、总页数、当前页、每页数量、数据列表
    """
    total = len(items)
    total_pages = (total + page_size - 1) // page_size
    start = (page - 1) * page_size
    end = start + page_size
    data = items[start:end]
    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "data": data
    } 