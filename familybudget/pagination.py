from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 10

class WidePagination(PageNumberPagination):
    page_size = 100
    page_query_param = 'page'
    max_page_size = 1000

