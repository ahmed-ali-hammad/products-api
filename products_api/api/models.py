from api.utils import NoLeadingZerosCharField
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Session(TimeStampedModel):
    """Table to stor the session information"""

    session_id = models.BigIntegerField(_("Session ID"), null=True, blank=True)
    session_start_time = models.DateTimeField(
        _("Session Start Time"), null=True, blank=True
    )
    session_end_time = models.DateTimeField(
        _("Session End Time"), null=True, blank=True
    )
    supplier_id = models.CharField(
        _("Supplier id"), max_length=225, null=True, blank=True
    )
    user_id = models.CharField(_("User id"), max_length=225, null=True, blank=True)

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")

    def __str__(self):
        return str(self.session_id)


class Lot(TimeStampedModel):
    session = models.ForeignKey(
        "Session", related_name="lot", on_delete=models.CASCADE, null=True, blank=True
    )
    item = models.ForeignKey(
        "Item", related_name="lot", on_delete=models.CASCADE, null=True, blank=True
    )
    lot_number = models.CharField(
        _("Lot Number"), max_length=225, null=True, blank=True
    )
    amount = models.IntegerField(_("Amount"), null=True, blank=True)
    bbd = models.DateTimeField(_("Best Before Date"), null=True, blank=True)
    comment = models.CharField(_("Comment"), max_length=225, null=True, blank=True)
    country_of_disassembly = models.CharField(
        _("Country of Disassembly"), max_length=100, null=True, blank=True
    )
    country_of_rearing = models.CharField(
        _("Country of Rearing"), max_length=100, null=True, blank=True
    )
    country_of_slaughter = models.CharField(
        _("Country of Slaughter"), max_length=100, null=True, blank=True
    )
    cutting_plant_registration = models.CharField(
        _("Cutting Plant Registration"), max_length=225, null=True, blank=True
    )
    slaughterhouse_registration = models.CharField(
        _("Slaughter House Registration"), max_length=225, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Lot")
        verbose_name_plural = _("Lots")


class Item(TimeStampedModel):
    db_id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name="Database ID"
    )
    id = models.CharField(
        _("Item ID"),
        help_text="This is not the database id",
        max_length=225,
        null=True,
        blank=True,
    )
    code = NoLeadingZerosCharField(
        _("Code"), max_length=225, db_index=True, null=True, blank=True
    )
    type = models.CharField(_("Type"), max_length=225, null=True, blank=True)
    brand = models.CharField(_("Brand"), max_length=225, null=True, blank=True)
    description = models.CharField(
        _("Description"), max_length=225, null=True, blank=True
    )
    status = models.CharField(_("Status"), max_length=225, null=True, blank=True)
    categ_id = models.IntegerField(_("Categ ID"), null=True, blank=True)
    category_id = models.CharField(
        _("Category ID"), max_length=225, null=True, blank=True
    )
    amount_multiplier = models.IntegerField(
        _("Amount Multiplier"), null=True, blank=True
    )
    edeka_article_number = models.CharField(
        _("Edeka Article Number"), max_length=225, null=True, blank=True
    )
    gross_weight = models.JSONField(_("Gross Weight"), null=True, blank=True)
    net_weight = models.JSONField(null=True, blank=True)
    unit_name = models.CharField(_("Unit Name"), max_length=50, null=True, blank=True)
    notes = models.CharField(_("Notes"), max_length=225, null=True, blank=True)
    packaging = models.CharField(_("Packaging"), max_length=100, null=True, blank=True)
    requires_best_before_date = models.BooleanField(
        _("Requires Best Before Date"), null=True, blank=True
    )
    requires_meat_info = models.BooleanField(
        _("Requires Meat Info"), null=True, blank=True
    )
    trade_item_unit_descriptor = models.CharField(
        _("Trade Item Unit Descriptor"), max_length=225, null=True, blank=True
    )
    trade_item_unit_descriptor_name = models.CharField(
        _("Trade Item Unit Descriptor Name"), max_length=225, null=True, blank=True
    )
    validation_status = models.CharField(
        _("Validation Status"), max_length=100, null=True, blank=True
    )
    regulated_name = models.CharField(
        _("Regulated Name"), max_length=100, null=True, blank=True
    )
    vat = models.JSONField(_("Vat"), null=True, blank=True)
    vat_rate = models.CharField(_("Vat Rate"), max_length=100, null=True, blank=True)
    category = models.CharField(_("Category"), max_length=225, null=True, blank=True)
    hierarchies = models.JSONField(_("Hierarchies"), null=True, blank=True)

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        unique_together = ["code", "type"]

    def __str__(self):
        return self.code


class RelatedProduct(TimeStampedModel):
    item = models.ForeignKey(
        "Item", related_name="related_products", on_delete=models.CASCADE
    )
    gtin = models.CharField(_("Gtin"), max_length=225, null=True, blank=True)
    trade_item_unit_descriptor = models.CharField(
        _("Trade Item Unit Descriptor"), max_length=225, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Related Product")
        verbose_name_plural = _("Related Products")

    def __str__(self):
        return self.trade_item_unit_descriptor
