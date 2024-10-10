import io
import random
import string
from io import BytesIO
from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from reportlab.graphics.barcode.widgets import BarcodeStandard39
from reportlab.graphics.charts.textlabels import Label as RlLabel
from reportlab.graphics.shapes import String
from reportlab.pdfgen import canvas
from tqdm import tqdm

from pylabels import Sheet, Specification

from .models import LabelData, LabelSpecification, Subject

random.seed(10)
base_path = Path(__file__)


def get_label_specification(name: str | None) -> LabelSpecification:
    name = name or "default"
    try:
        obj = LabelSpecification.objects.get(name=name)
    except ObjectDoesNotExist:
        if name == "default":
            obj = LabelSpecification.objects.create(name=name)
        else:
            raise ObjectDoesNotExist(
                "Label specification does not exist. "
                f"Go to admin to create one or use 'default'. Got '{name}'."
            )
    return obj


def get_label_data(max_labels: int | None = None) -> QuerySet[LabelData]:
    """Generate label data"""
    max_labels = max_labels or 0
    max_labels = max_labels if 0 <= max_labels <= 48 else 12
    clinics = ["Mochudi", "Gaborone", "Kanye", "Lobatse"]
    LabelData.objects.all().delete()
    Subject.objects.all().delete()
    for i in tqdm(range(1234, 1234 + max_labels), total=max_labels):
        obj = Subject.objects.create(
            subject_identifier=f"PATIENT{i}",
            clinic=random.choice(clinics),
            gender=random.choice(["M", "F"]),
        )
        reference = "".join(random.choices(string.ascii_letters.upper() + "23456789", k=6))
        LabelData.objects.create(subject=obj, reference=reference, relative_seq=i)
    return LabelData.objects.all()


def draw_label(label, width, height, obj: LabelData):
    """Callable to draw a single label given a model instance `obj`"""
    br = BarcodeStandard39(
        humanReadable=True, checksum=False, barHeight=30, barWidth=0.7, gap=1.7
    )
    br.value = obj.reference
    br.x = width - 140
    br.y = 25
    label.add(br)
    label.add(String(15, height - 20, f"DJANGO Study - {obj.subject.clinic}", fontSize=10))
    label.add(
        String(
            width - 120,
            height - 40,
            f"{obj.subject.subject_identifier}{obj.subject.gender}",
            fontSize=12,
        )
    )
    label.add(String(15, height - 40, "Dawa kwa ajili ya utafiti", fontSize=10))
    label.add(String(15, height - 50, "wa DJANGO.", fontSize=10))
    label.add(String(15, height - 70, "Meza vidonge vinne usiku tu.", fontSize=10))
    label.add(String(15, 20, "128 tabs", fontSize=10))
    lab = RlLabel(x=width - 20, y=40, fontSize=10, angle=90)
    lab.setText(obj.relative_seq)
    label.add(lab)
    return label


def blank_buffer():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def print_sheets(
    labels: list[LabelData],
    filename: str | None = None,
    label_specification: str | None = None,
) -> BytesIO | None:
    """Generate a PDF of 6 x 2 sheets of labels"""
    label_spec = get_label_specification(name=label_specification)
    if len(labels) == 0:
        return blank_buffer()
    specs = Specification(**label_spec.kwattrs)
    sheet = Sheet(specs, draw_label, border=label_spec.border)
    sheet.add_labels(labels)
    if not filename:
        return sheet.save_to_buffer()
    sheet.save(filename)
