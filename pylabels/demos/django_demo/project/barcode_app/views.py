from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.views import View
from django.views.generic import TemplateView

from .barcode import get_label_data, print_sheets


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"


class PrintBarcodeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs) -> FileResponse:
        label_data = get_label_data(
            max_labels=int(request.GET.get("max_labels")),
        )
        buffer = print_sheets(
            [obj for obj in label_data],
            label_specification=request.GET.get("label_specification"),
        )
        return FileResponse(buffer, as_attachment=True, filename="barcode.pdf")
