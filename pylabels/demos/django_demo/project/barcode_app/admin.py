import uuid

from django.contrib import admin, messages

from .models import LabelData, LabelSpecification, Subject


def copy_label_specification(modeladmin, request, queryset):
    if queryset.count() > 1 or queryset.count() == 0:
        messages.add_message(
            request, messages.ERROR, "Select one and only one existing label specification"
        )
    else:
        obj = queryset.first()
        obj.pk = None
        obj.name = uuid.uuid4()
        obj.save()


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("subject_identifier", "gender", "clinic")
    list_filter = ("clinic",)
    search_fields = ("subject_identifier", "reference")


@admin.register(LabelData)
class LabelDataAdmin(admin.ModelAdmin):
    list_display = ("__str__", "subject", "created")
    list_filter = ("created",)
    search_fields = ("subject__subject_identifier", "reference")


@admin.register(LabelSpecification)
class LabelSpecificationAdmin(admin.ModelAdmin):

    actions = [copy_label_specification]

    list_display = (
        "name",
        "page_description",
        "layout_description",
        "label_description",
        "border",
    )

    readonly_fields = (
        "page_description",
        "layout_description",
        "label_description",
    )
