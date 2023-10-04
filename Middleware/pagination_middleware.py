from django.core.paginator import Paginator, EmptyPage


from Hospitals.models import Hospital
from doctors.models import Doctor
from patients.models import Patient

class PaginationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def paginate_queryset(self, queryset, page_number, per_page):
        paginator = Paginator(queryset, per_page)
        try:
            page = paginator.page(page_number)
            return page
        except EmptyPage:
            return None

    def __call__(self, request):
        # Detect if the request is for an API view (you may customize this check)
        if request.path.startswith('/api/'):
            # Get the page number from the request
            page_number = request.GET.get('page', 1)  # Default to page 1 if not specified
            per_page = 10  # Set the default page size


            models_to_paginate = [Hospital, Doctor, Patient]  

            paginated_data = {}

            for model in models_to_paginate:
                queryset = model.objects.all()
                paginator = Paginator(queryset, per_page)  # Move paginator definition inside the loop

                page = self.paginate_queryset(queryset, page_number, per_page)

                if page is not None:
                    paginated_data[model.__name__.lower()] = {
                        'results': page.object_list,
                        'pagination': {
                            'page_number': page.number,
                            'total_pages': paginator.num_pages,
                            'total_items': paginator.count,
                        }
                    }

            # Modify the response data to include paginated data
            response = self.get_response(request)
            response.data['pagination'] = paginated_data
            return response

        # If the request is not for an API view, proceed with the original response
        return self.get_response(request)
