from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        # Only return results and current page info, no page.paginator.count
        return Response({
            "page": self.page.number,
            "page_size": self.get_page_size(self.request),
            "results": data,
        })
