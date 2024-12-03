from django.db import models

class Employee(models.Model):
    class Meta:
        verbose_name = "کارمند"
        verbose_name_plural = "کارمندان"
        db_table = "Employee"

    title = models.CharField(max_length=25, null=False, blank=False, verbose_name="سمت")
    agreement_image = models.ImageField(upload_to="account/contracts", null=False, blank=False, verbose_name="عکس قرارداد")
    contract_Date = models.DateField(null=False, blank=False, verbose_name="تاریخ استخدام")
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    address_ID = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="آدرس")
    tel_ID = models.ForeignKey(Tel, on_delete=models.CASCADE, verbose_name="شماره تماس")