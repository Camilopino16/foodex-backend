from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    nombre_rol = models.CharField(max_length=30, unique=True)
    def __str__(self): return self.nombre_rol

class User(AbstractUser):
    rol = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
    semestre = models.IntegerField(null=True, blank=True)
    carrera = models.CharField(max_length=50, null=True, blank=True)

class Receta(models.Model):
    nombre_receta = models.CharField(max_length=100)
    tipo = models.CharField(max_length=28, blank=True)
    autor = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, related_name='recetas')
    porciones_base = models.PositiveIntegerField(default=1)
    tiempo_preparacion_min = models.PositiveIntegerField(default=0)
    detalle_montaje = models.CharField(max_length=255, blank=True)
    url_bosquejo_base = models.CharField(max_length=255, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

class PasoProcedimiento(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='pasos')
    orden_procedimiento = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=255)
    class Meta:
        ordering = ['orden_procedimiento']
        unique_together = ('receta','orden_procedimiento')

class Ingrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='ingredientes')
    nombre_ing = models.CharField(max_length=58)
    tipo_ing = models.CharField(max_length=58, blank=True)
    cantidad_base = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=32)

class Canasta(models.Model):
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, related_name='stock_items')
    cantidad_disponible = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidad = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural = "Canasta"
