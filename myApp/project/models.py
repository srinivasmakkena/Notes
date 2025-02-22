from django.db import models

class Section(models.Model):
    title = models.CharField(max_length=255, default='Default Section')

    def __str__(self):
        return self.title

class Page(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='pages')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Assign to default section if no section is provided
        if not self.section:
            default_section, created = Section.objects.get_or_create(title='')
            self.section = default_section
        super().save(*args, **kwargs)