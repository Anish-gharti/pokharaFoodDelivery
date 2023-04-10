from django.db import models
from accounts.models import User, UserProfile
from  accounts.utils import send_notification
# Create your models here:

from datetime import time

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            orig = Vendor.objects.get(pk=self.pk)
            print(orig.is_approved)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }

                if self.is_approved == True:
                    # send notifcation email    
                    mail_subject = "Congratulations! your accounrt has been activated."
                    send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject = "We are sorry. You are not eligible for publishing your food on our marketplace."
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)                
    

DAYS = [
   
       (1, ("MONDAY")),
          (2, ("TUESDAY")),
             (3, ("WEDNESDAY")),
                (4, ("THRUSDAY")),
                   (5, ("FRIDAY")),
                      (6, ("SATURDAY")),
                       (7, ("SUNDAY")),
]

HOURLY_TIME_FOR_ONEDAY = [(time(h,m).strftime('%I:%M %p'), time(h,m).strftime('%I:%M %p')) for h in range(0,24) for m in (0,30)]

class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField( choices=HOURLY_TIME_FOR_ONEDAY , max_length=10, blank=True)
    to_hour = models.CharField(choices=HOURLY_TIME_FOR_ONEDAY , max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', 'from_hour')
        unique_together = ('vendor', 'day', 'from_hour','to_hour')

    def __str__(self):
        return self.get_day_display()