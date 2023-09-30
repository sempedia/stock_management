from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import Stock, StockHistory

@receiver(post_save, sender=Stock)
def create_stock_history_on_save(sender, instance, created, **kwargs):
    if created:
        # If a new Stock instance is created, create a corresponding StockHistory entry
        StockHistory.objects.create(
            category=instance.category,
            item_name=instance.item_name,
            quantity=instance.quantity,
            received_quantity=instance.received_quantity,
            received_by=instance.received_by,
            issued_quantity=instance.issued_quantity,
            issued_by=instance.issued_by,
            issued_to=instance.issued_to,
            phone_number=instance.phone_number,
            created_by=instance.created_by,
            reorder_level=instance.reorder_level,
            last_updated=instance.last_updated,
            timestamp=instance.timestamp,
        )
    else:
        # If an existing Stock instance is updated, create a corresponding StockHistory entry
        StockHistory.objects.create(
            category=instance.category,
            item_name=instance.item_name,
            quantity=instance.quantity,
            received_quantity=instance.received_quantity,
            received_by=instance.received_by,
            issued_quantity=instance.issued_quantity,
            issued_by=instance.issued_by,
            issued_to=instance.issued_to,
            phone_number=instance.phone_number,
            created_by=instance.created_by,
            reorder_level=instance.reorder_level,
            last_updated=instance.last_updated,
            timestamp=instance.timestamp,
        )

@receiver(post_delete, sender=Stock)
def create_stock_history_on_delete(sender, instance, **kwargs):
    # If a Stock instance is deleted, create a corresponding StockHistory entry
    StockHistory.objects.create(
        category=instance.category,
        item_name=instance.item_name,
        quantity=instance.quantity,
        received_quantity=instance.received_quantity,
        received_by=instance.received_by,
        issued_quantity=instance.issued_quantity,
        issued_by=instance.issued_by,
        issued_to=instance.issued_to,
        phone_number=instance.phone_number,
        created_by=instance.created_by,
        reorder_level=instance.reorder_level,
        last_updated=instance.last_updated,
        timestamp=instance.timestamp,
    )
