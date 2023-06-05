from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def prepare_pagination(query, page=None, items_per_page=5):
    paginator = Paginator(query, items_per_page)
    total_items = paginator.count
    try:
        paginated_items = paginator.page(page)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
    return paginated_items, total_items
