from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    ordering = '-id'
    page_size_query_param = 'page_size'
    page_size = 25
    max_page_size = 25
