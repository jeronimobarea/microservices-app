# Schemas
from src.schemas import Pagination


# Methods
def get_paginator(page, per_page, item_list, query):
    total_pages = int(len(item_list) / per_page)

    if (total_pages - page) > 0:
        has_next = True
    else:
        has_next = False

    if page == 0:
        has_prev = False
    else:
        has_prev = True

    pagination = Pagination(
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        has_next=has_next,
        has_prev=has_prev,
        results=query
    )
    return pagination
