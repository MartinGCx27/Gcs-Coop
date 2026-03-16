from django.db import models
# Import User model
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

# Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
# Price model
class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
	
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

# Transaction details model
class transaction_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='User')
    runway_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora pago')
    runway_period = models.CharField(max_length=254, verbose_name='Periodo pago')
    runway_motive = models.CharField(max_length=254, verbose_name='Motivo pago')
    runway_method = models.CharField(max_length=254, verbose_name='Metodo pago')
    runway_status = models.CharField(max_length=254, verbose_name='Estatus pago')
    reference = models.CharField(max_length=254, null=True, blank=True, verbose_name='Referencia')

    class Meta:
        verbose_name = 'Detalle de transaccion'
        verbose_name_plural = 'Detalle de transacciones'

    def __str__(self):
        return "Transaccion de %s" % (self.user.get_full_name())

