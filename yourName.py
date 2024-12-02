from django.db import models
class Tel(models.Model):
    class Meta:
        verbose_name = "شماره تماس"
        verbose_name_plural = "شماره تماس ها"
        db_table = "Tel"

    home_Number = models.CharField(max_length=15, null=False, blank=False, verbose_name="تلفن ثابت")
    phone_Number = models.CharField(max_length=11, null=False, blank=False, verbose_name="تلفن موبایل")
    work_Number = models.CharField(max_length=15, null=False, blank=True, verbose_name="تلفن محل کار")
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    
    # تو اینجا مدل خودتون رو بسازید 