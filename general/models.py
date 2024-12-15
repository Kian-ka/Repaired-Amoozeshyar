from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class Person(models.Model):
    """مدل پایه برای اطلاعات پرسنلی"""
    GENDER_CHOICES = [
        ('M', 'مرد'),
        ('F', 'زن'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('S', 'مجرد'),
        ('M', 'متاهل'),
    ]

    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    national_code = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='کد ملی باید ۱۰ رقم باشد'
            )
        ],
        verbose_name="کد ملی"
    )
    password = models.CharField(
        max_length=128, 
        verbose_name="رمز عبور",
        null=True,  # Allow NULL in database
        blank=True  # Allow blank in forms
    )
    birth_date = models.DateField(verbose_name="تاریخ تولد")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="جنسیت")
    marital_status = models.CharField(
        max_length=1,
        choices=MARITAL_STATUS_CHOICES,
        verbose_name="وضعیت تاهل"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        abstract = True
        verbose_name = "شخص"
        verbose_name_plural = "اشخاص"

    def clean(self):
        try:
            # اعتبارسنجی کد ملی (یک نمونه ساده)
            if len(self.national_code) != 10:
                raise ValidationError(_('کد ملی باید ۱۰ رقم باشد'))
            
            # اعتبارسنجی سن
            from datetime import date
            age = (date.today() - self.birth_date).days / 365
            if age < 15:
                raise ValidationError(_('سن باید بیشتر از ۱۵ سال باشد'))

            # Add password validation
            if len(self.password) < 6:
                raise ValidationError(_('رمز عبور باید حداقل ۶ کاراکتر باشد'))
                
        except Exception as e:
            raise ValidationError(f'خطا در اعتبارسنجی اطلاعات شخصی: {str(e)}')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Faculty(models.Model):
    """
    دانشکده‌های دانشگاه را نگهداری می‌کند.
    
    این مدل برای ذخیره اطلاعات دانشکده‌های مختلف دانشگاه استفاده می‌شود.
    
    نمونه داده:
        - نام: "دانشکده مهندسی کامپیوتر", کد: "CE"
        - نام: "دانشکده برق", کد: "EE"
        - نام: "دانشکده مکانیک", کد: "ME"
    """
    name = models.CharField(max_length=100, verbose_name="نام دانشکده")
    code = models.CharField(max_length=10, unique=True, verbose_name="کد دانشکده")
    
    class Meta:
        verbose_name = "دانشکده"
        verbose_name_plural = "دانشکده‌ها"
    
    def __str__(self):
        return self.name

class Professor(Person):
    """استاد"""
    faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT, verbose_name="دانشکده")
    personnel_code = models.CharField(max_length=10, unique=True, verbose_name="کد پرسنلی")
    academic_rank = models.CharField(
        max_length=50,
        choices=[
            ('assistant', 'استادیار'),
            ('associate', 'دانشیار'),
            ('full', 'استاد تمام'),
        ],
        verbose_name="مرتبه علمی"
    )
    hire_date = models.DateField(verbose_name="تاریخ استخدام")

    class Meta:
        verbose_name = "استاد"
        verbose_name_plural = "اساتید"

    def clean(self):
        try:
            super().clean()
            # اعتبارسنجی‌های خاص استاد
            from datetime import date
            if self.hire_date > date.today():
                raise ValidationError(_('تاریخ استخدام نمی‌تواند در آینده باشد'))
        except Exception as e:
            raise ValidationError(f'خطا در اعتبارسنجی اطلاعات استاد: {str(e)}')

class Student(Person):
    """دانشجو"""
    faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT, verbose_name="دانشکده")
    student_number = models.CharField(max_length=10, unique=True, verbose_name="شماره دانشجویی")
    entry_year = models.IntegerField(verbose_name="سال ورود")
    DEGREE_CHOICES = [
        ('associate', 'کاردانی'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکتری'),
    ]
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, verbose_name="مقطع تحصیلی")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت تحصیلی")

    class Meta:
        verbose_name = "دانشجو"
        verbose_name_plural = "دانشجویان"

    def clean(self):
        try:
            super().clean()
            # اعتبارسنجی‌های خاص دانشجو
            from datetime import date
            current_year = date.today().year
            if self.entry_year > current_year:
                raise ValidationError(_('سال ورود نمی‌تواند در آینده باشد'))
        except Exception as e:
            raise ValidationError(f'خطا در اعتبارسنجی اطلاعات دانشجو: {str(e)}')

class Course(models.Model):
    """
    اطلاعات دروس ارائه شده در دانشگاه را نگهداری می‌کند.
    
    این مدل شامل مشخصات دروس و پیش‌نیازهای آنها است.
    
    نمونه داده:
        - نام: "برنامه‌نویسی پیشرفته", کد: "40244", واحد: 3
          دانشکده: "مهندسی کامپیوتر", پیش‌نیاز: "مبانی برنامه‌نویسی"
        - نام: "پایگاه داده", کد: "40242", واحد: 3
          دانشکده: "مهندسی کامپیوتر", پیش‌نیاز: "ساختمان داده"
    """
    name = models.CharField(max_length=100, verbose_name="نام درس")
    code = models.CharField(max_length=10, unique=True, verbose_name="کد درس")
    units = models.PositiveSmallIntegerField(verbose_name="تعداد واحد")
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, verbose_name="دانشکده")
    prerequisites = models.ManyToManyField('self', blank=True, verbose_name="پیش‌نیازها")
    
    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "دروس"
    
    def __str__(self):
        return self.name

class Semester(models.Model):
    """
    اطلاعات ترم‌های تحصیلی را نگهداری می‌کند.
    
    این مدل برای مدیریت ترم‌های تحصیلی و وضعیت فعال بودن آنها استفاده می‌شود.
    
    نمونه داده:
        - سال: 1402, نیمسال: "1" (نیمسال اول), فعال: True
        - سال: 1402, نیمسال: "2" (نیمسال دوم), فعال: False
        - سال: 1402, نیمسال: "3" (ترم تابستان), فعال: False
    """
    SEMESTER_CHOICES = [
        ('1', 'نیمسال اول'),
        ('2', 'نیمسال دوم'),
        ('3', 'ترم تابستان'),
    ]
    
    year = models.IntegerField(verbose_name="سال تحصیلی")
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES, verbose_name="نیمسال")
    is_active = models.BooleanField(default=False, verbose_name="ترم فعال")
    
    class Meta:
        verbose_name = "ترم تحصیلی"
        verbose_name_plural = "ترم‌های تحصیلی"
        unique_together = ['year', 'semester']
    
    def __str__(self):
        return f"{self.get_semester_display()} {self.year}"

class ClassSchedule(models.Model):
    """
    برنامه زمانی کلاس‌های درسی را نگهداری می‌کند.
    
    این مدل شامل اطلاعات زمان‌بندی، استاد، درس و ظرفیت کلاس‌ها است.
    
    نمونه داده:
        - درس: "برنامه‌نویسی پیشرفته", استاد: "دکتر محمدی"
          ترم: "نیمسال اول 1402", ظرفیت: 30
          روز: "2" (دوشنبه), زمان: 10:30 - 12:00
        - درس: "پایگاه داده", استاد: "دکتر احمدی"
          ترم: "نیمسال اول 1402", ظرفیت: 40
          روز: "1" (یکشنبه), زمان: 9:00 - 10:30
    """
    DAYS_OF_WEEK = [
        ('0', 'شنبه'),
        ('1', 'یکشنبه'),
        ('2', 'دوشنبه'),
        ('3', 'سه‌شنبه'),
        ('4', 'چهارشنبه'),
        ('5', 'پنج‌شنبه'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name="درس")
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT, verbose_name="استاد")
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT, verbose_name="ترم")
    students = models.ManyToManyField(Student, through='Enrollment', verbose_name="دانشجویان")
    capacity = models.PositiveIntegerField(verbose_name="ظرفیت")
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK, verbose_name="روز")
    start_time = models.TimeField(verbose_name="زمان شروع")
    end_time = models.TimeField(verbose_name="زمان پایان")
    
    class Meta:
        verbose_name = "کلاس درسی"
        verbose_name_plural = "کلاس‌های درسی"
    
    def clean(self):
        try:
            if self.start_time >= self.end_time:
                raise ValidationError(_('زمان شروع باید قبل از زمان پایان باشد'))
        except Exception as e:
            raise ValidationError(f'خطا در بررسی زمان کلاس: {str(e)}')
    
    def __str__(self):
        return f"{self.course.name} - {self.professor}"

class Enrollment(models.Model):
    """
    اطلاعات ثبت‌نام دانشجویان در کلاس‌ها را نگهداری می‌کند.
    
    این مدل برای مدیریت ثبت‌نام دانشجویان در کلاس‌ها و ثبت نمرات استفاده می‌شود.
    
    نمونه داده:
        - دانشجو: "رضا کریمی", کلاس: "برنامه‌نویسی پیشرفته - دکتر محمدی"
          نمره: 18.5, تاریخ ثبت‌نام: "2024-02-01 10:30:00"
        - دانشجو: "زهرا حسینی", کلاس: "پایگاه داده - دکتر احمدی"
          نمره: 17.75, تاریخ ثبت‌نام: "2024-02-01 11:15:00"
    """
    student = models.ForeignKey(Student, on_delete=models.PROTECT, verbose_name="دانشجو")
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.PROTECT, verbose_name="کلاس")
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="نمره")
    enrollment_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت‌نام")
    
    class Meta:
        verbose_name = "ثبت‌نام"
        verbose_name_plural = "ثبت‌نام‌ها"
        unique_together = ['student', 'class_schedule']
    
    def clean(self):
        try:
            if self.grade is not None and (self.grade < 0 or self.grade > 20):
                raise ValidationError(_('نمره باید بین 0 تا 20 باشد'))
        except Exception as e:
            raise ValidationError(f'خطا در بررسی نمره: {str(e)}')
    
    def __str__(self):
        return f"{self.student} - {self.class_schedule.course}"

# class ContactInfo(models.Model):
#     """مدل پایه برای اطلاعات تماس"""
#     person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name="شخص")
#     is_primary = models.BooleanField(default=False, verbose_name="اطلاعات اصلی")
#     is_active = models.BooleanField(default=True, verbose_name="فعال")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

#     class Meta:
#         abstract = True

#     def clean(self):
#         try:
#             if self.is_primary:
#                 # بررسی اینکه فقط یک مورد اصلی وجود داشته باشد
#                 primary_exists = self.__class__.objects.filter(
#                     person=self.person,
#                     is_primary=True
#                 ).exclude(pk=self.pk).exists()
                
#                 if primary_exists:
#                     raise ValidationError(_('فقط یک مورد می‌تواند اصلی باشد'))
#         except Exception as e:
#             raise ValidationError(f'خطا در اعتبارسنجی اطلاعات تماس: {str(e)}')

# class PhoneNumber(ContactInfo):
#     """شماره تلفن"""
#     PHONE_TYPE_CHOICES = [
#         ('mobile', 'موبایل'),
#         ('home', 'منزل'),
#         ('work', 'محل کار'),
#         ('other', 'سایر'),
#     ]
    
#     phone_type = models.CharField(
#         max_length=10,
#         choices=PHONE_TYPE_CHOICES,
#         verbose_name="نوع تلفن"
#     )
#     number = models.CharField(
#         max_length=11,
#         validators=[
#             RegexValidator(
#                 regex=r'^(0|\+98)?(9\d{9}|[1-8]\d{7})$',
#                 message='شماره تلفن معتبر نیست'
#             )
#         ],
#         verbose_name="شماره تلفن"
#     )

#     class Meta:
#         verbose_name = "شماره تلفن"
#         verbose_name_plural = "شماره تلفن‌ها"
#         unique_together = ['person', 'number']

#     def __str__(self):
#         return f"{self.get_phone_type_display()}: {self.number}"

# class EmailAddress(ContactInfo):
#     """آدرس ایمیل"""
#     EMAIL_TYPE_CHOICES = [
#         ('personal', 'شخصی'),
#         ('work', 'کاری'),
#         ('academic', 'دانشگاهی'),
#         ('other', 'سایر'),
#     ]
    
#     email_type = models.CharField(
#         max_length=10,
#         choices=EMAIL_TYPE_CHOICES,
#         verbose_name="نوع ایمیل"
#     )
#     email = models.EmailField(verbose_name="آدرس ایمیل")

#     class Meta:
#         verbose_name = "آدرس ایمیل"
#         verbose_name_plural = "آدرس‌های ایمیل"
#         unique_together = ['person', 'email']

#     def __str__(self):
#         return f"{self.get_email_type_display()}: {self.email}"

# class Address(ContactInfo):
#     """آدرس"""
#     ADDRESS_TYPE_CHOICES = [
#         ('home', 'منزل'),
#         ('work', 'محل کار'),
#         ('other', 'سایر'),
#     ]
    
#     address_type = models.CharField(
#         max_length=10,
#         choices=ADDRESS_TYPE_CHOICES,
#         verbose_name="نوع آدرس"
#     )
#     province = models.CharField(max_length=50, verbose_name="استان")
#     city = models.CharField(max_length=50, verbose_name="شهر")
#     postal_code = models.CharField(
#         max_length=10,
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{10}$',
#                 message='کد پستی باید ۱۰ رقم باشد'
#             )
#         ],
#         verbose_name="کد پستی"
#     )
#     street_address = models.TextField(verbose_name="آدرس")
    
#     class Meta:
#         verbose_name = "آدرس"
#         verbose_name_plural = "آدرس‌ها"
#         unique_together = ['person', 'postal_code']

#     def clean(self):
#         try:
#             super().clean()
#             # اعتبارسنجی کد پستی
#             if not self.postal_code.isdigit() or len(self.postal_code) != 10:
#                 raise ValidationError(_('کد پستی باید ۱۰ رقم باشد'))
#         except Exception as e:
#             raise ValidationError(f'خطا در اعتبارسنجی آدرس: {str(e)}')

#     def __str__(self):
#         return f"{self.get_address_type_display()}: {self.city}, {self.street_address}"
