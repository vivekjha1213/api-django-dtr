from django.core.paginator import Paginator
from django.http import JsonResponse

from Hospitals.models import Hospital
from doctors.models import Doctor
from patients.models import Patient

MAX_PAGES = 100  # Maximum number of pages
DEFAULT_PER_PAGE = 10  # Default number of items per page

# Define custom per-page values for specific models
CUSTOM_PER_PAGE = {
    'Hospital': 20,
    'Doctor': 15,
    'Patient': 25,
}

class PaginationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def paginate_queryset(self, queryset, page_number, per_page):
        paginator = Paginator(queryset, per_page)
        page = paginator.get_page(page_number)
        return page

    def __call__(self, request):
        if request.path.startswith('/api/'):
            page_number = request.GET.get('page', 1)
            
            paginated_data = {}

            for model in [Hospital, Doctor, Patient]:
                queryset = model.objects.all()
                model_name = model.__name__

                # Use a custom per-page value if available, or the default
                per_page = CUSTOM_PER_PAGE.get(model_name, DEFAULT_PER_PAGE)

                page = self.paginate_queryset(queryset, page_number, per_page)

                paginated_data[model_name.lower()] = {
                    'results': list(page),
                    'pagination': {
                        'page_number': page.number,
                        'total_pages': min(MAX_PAGES, page.paginator.num_pages),
                        'total_items': page.paginator.count,
                    }
                }

            response = self.get_response(request)
            return response

        return self.get_response(request)
