from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.

class TipoExames(models.Model):
    tipo_choices = (
        ('I','Imagem'),
        ('S','Sangue')

    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1, choices= tipo_choices)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField(null= True)
    horario_final = models.IntegerField(null= True)


    def __str__(self):
        return self.nome
    

class SolicitacaoExame(models.Model):
    choice_status = (
    ('E', 'Em Análise'),
    ('F', 'Finalizado')
    )
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exame = models.ForeignKey(TipoExames, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choice_status)
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)
    def __str__(self):
        return f'{self.usuario} | {self.exame.nome} | {self.get_status_display()}'
    
    def badge_template(self):
        if self.status == 'E':
            classe = 'bg-warning text-dark'
        else:
            classe = 'bg-success text-dark'
        
        #print(self.get_status_display())
        
        return mark_safe(f'<span class="badge {classe}"> {self.get_status_display()} </span>')
    

class PedidosExames(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateField()
    def __str__(self):
        return f'{self.id} | {self.usuario} | {self.data}'
    

