from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit

# Create your models here.


class Posting(models.Model):
    content = models.TextField(default='')
    icon = models.CharField(max_length=20, default='')

    # Save as origin
    # image = models.ImageField(blank=True, upload_to='postings/%Y%M%d')

    # Save resized version
    image = ProcessedImageField(
        blank=True,
        upload_to='postings/resize/%Y%m%d',
        processors=[ResizeToFit(width=960, upscale=False)],
        format='JPEG'
    )

    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=320, upscale=False)],
        format='JPEG',
        options={'quality': 60}
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}: {self.content[:20]}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        string = f'\n=== Saved Posting with id: {self.id} ==='
        print(f'\n {string}')
        print(f'    content: {self.content}')
        if self.image:
            print(f'    image: {self.image.width}px {self.image.height}px: {self.image.size}')
        for i in range(len(string)-1):
            print('=', end="")
        print()


class Comment(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.posting.content[:10]}: {self.content[:20]}'



