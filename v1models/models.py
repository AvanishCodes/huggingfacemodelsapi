from django.db import models

# Create your models here.

class Text2Speech(models.Model):
    uuid_str = models.CharField(max_length=100)
    text = models.TextField()
    audio_file_path = models.FileField(upload_to='data/tts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Text2Speech'
        verbose_name_plural = 'Text2Speeches'
        db_table = 'text2speech'
        ordering = ['-created_at']


class Speech2Text(models.Model):
    uuid_str = models.CharField(max_length=100)
    audio_file_path = models.FileField(upload_to='data/stt')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Speech2Text'
        verbose_name_plural = 'Speech2Texts'
        db_table = 'speech2text'
        ordering = ['-created_at']

class ImageGeneration(models.Model):
    uuid_str = models.CharField(max_length=100)
    text = models.TextField()
    image_file_path = models.FileField(upload_to='data/imagegeneration')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'ImageGeneration'
        verbose_name_plural = 'ImageGenerations'
        db_table = 'imagegeneration'
        ordering = ['-created_at']

class TextCompletion(models.Model):
    uuid_str = models.CharField(max_length=100)
    text = models.TextField()
    completions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'TextCompletion'
        verbose_name_plural = 'TextCompletions'
        db_table = 'textcompletion'
        ordering = ['-created_at']