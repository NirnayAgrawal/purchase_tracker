from django.db import models

class ItemUpload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Item(models.Model):
    name = models.CharField(max_length=255)
    supplier = models.CharField(max_length=255)
    upload = models.ForeignKey(ItemUpload, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.name} ({self.supplier})"

class Purchase(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity} on {self.date}"
