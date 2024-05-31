from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Option(models.Model):
    title = models.CharField(_("Title"),max_length=255)
    isCorrect = models.BooleanField(_("IsCorrect"),default=False)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(_("Name"),max_length=255)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Categories"

class ConductingTime(models.Model):
    start = models.DateTimeField(_("Starting Time"),null=True,blank=True)
    end = models.DateTimeField(_("Ending Time"),null=True,blank=True)

    def __str__(self):
        return f"{self.start} - {self.end}"
    
    class Meta:
        verbose_name_plural = "ConductingTimes"

class Quiz(models.Model):
    question = models.CharField(_("Name"),max_length= 255)
    options = models.ManyToManyField(Option,_("Options"))
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    
    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.question