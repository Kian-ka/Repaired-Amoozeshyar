from django.db import models



class User(models.Model):
    class Meta :
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        db_table = "User"

    GENDER_CHOICES = {
        0: "زن",
        1: "مرد",
    }

    BLOOD_TYPE_CHOICES = {
        "AB": "AB",
        "AB+": "AB+",
        "AB-": "AB-",
        'A': "A",
        "A+": "A+",
        "A-": "A-",
        'B': "B",
        "B+": "B+",
        "B-": "B-",
        'O': "O",
        "O+": "O+",
        "O-": "O-"
    }

    NATIONALITY_CHOICES = {
        0: "ایرانی",
        1: "اتباع",
    }

    first_Name = models.CharField(max_length=20, null=False, blank=False, verbose_name="نام")
    last_Name = models.CharField(max_length=20, null=False, blank=False, verbose_name="نام خانوادگی")
    father_Name = models.CharField(max_length=20, null=False, blank=False, verbose_name="نام پدر")
    birth_Date = models.DateField(null=False, blank=False, verbose_name="سال تولد")
    gender = models.BooleanField(choices=GENDER_CHOICES, default=1, verbose_name="جنسیت")
    national_ID = models.CharField(max_length=10, primary_key=True, null=False, blank=False, verbose_name="کد ملی")
    profile_Image = models.ImageField(upload_to="account/profiles",default="account/profiles/default_User.png", verbose_name="عکس پروفایل")
    blood_Type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, default="B+", null=False,  verbose_name="گروه خونی")
    nationality = models.BooleanField(max_length=6, choices=NATIONALITY_CHOICES, default=0, verbose_name="ملیت")
    email = models.EmailField(max_length=254, null=False, blank=True, verbose_name="آدرس الکترونیک")

    def __str__(self):
        return self.national_ID

class Tel(models.Model):
    class Meta:
        verbose_name = "شماره تماس"
        verbose_name_plural = "شماره تماس ها"
        db_table = "Tel"

    home_Number = models.CharField(max_length=15, null=False, blank=False, verbose_name="تلفن ثابت")
    phone_Number = models.CharField(max_length=11, null=False, blank=False, verbose_name="تلفن موبایل")
    work_Number = models.CharField(max_length=15, null=False, blank=True, verbose_name="تلفن محل کار")
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")

class Address(models.Model):
    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"
        db_table = "Address"

    country = models.CharField(max_length=15, null=False, blank=False, verbose_name="کشور")
    state = models.CharField(max_length=15, null=False, blank=False, verbose_name="استان")
    city = models.CharField(max_length=15, null=False, blank=False, verbose_name="شهر")
    district = models.CharField(max_length=15, null=False, blank=False, verbose_name="منطقه")
    street = models.CharField(max_length=15, null=False, blank=False, verbose_name="خیابان")
    alley = models.CharField(max_length=15, null=False, blank=False, verbose_name="کوچه")
    no = models.IntegerField(null=False, blank=False, verbose_name="پلاک")
    floor = models.IntegerField(null=False, blank=False, verbose_name="طبقه")
    post_ID = models.CharField(max_length=10, primary_key=True, verbose_name="کدپستی")
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")

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


# Create your models here.
