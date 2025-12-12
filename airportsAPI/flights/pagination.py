from rest_framework.pagination import PageNumberPagination, CursorPagination

class AdminFlightPagination(PageNumberPagination):
    page_size = 10
    page_size_query_description = 'page_size'
    max_page_size = 500

class UserFlightPagination(CursorPagination):
    page_size = 10
    ordering = "-departure_time"
    