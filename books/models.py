from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    #asgrega fecha automaticamente
    created_at = models.DateTimeField(auto_now_add=True)
    #actualiza fecha cada que hago cambios
    updated_at = models.DateTimeField(auto_now=True)
    
    #mostrar ttulo en panel de control
    def __str__(self):
        #Erntonces especificamos que muestra el titulo
        return self.title