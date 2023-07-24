# Third Party Library
from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPaginaion(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = 5
