from django.db import models

class CMS(models.Model):
    pagina = models.CharField(verbose_name="Pagina", max_length=40, null=False)
    contenido = models.TextField(verbose_name="Contenido")

    def __unicode__(self):
        return self.pagina

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Paginas'
