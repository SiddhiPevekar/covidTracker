from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

OPTIONS= (
    ('ICU','ICU beds'),
    ('Ventilator','Ventilator beds'),
    ('ICU+Ventilator','ICU+Ventilator beds'),
)
OXYGEN= (
    ('cylinder','Oxygen Cylinder'),
    ('refill','Oxygen Cylinder Refill'),
)

class Supplier(models.Model):
    s_id=models.AutoField(primary_key=True)
    s_agency_name=models.CharField(max_length=100, null=True, blank=True)
    s_emailid=models.EmailField(('email address'),  null=True, blank=True)
    s_pass1=models.CharField(max_length=40, null=True, blank=True)
    s_pass2=models.CharField(max_length=40, null=True, blank=True)
    s_govcode=models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.s_agency_name

class ICU(models.Model):
    s_icu_id=models.AutoField(primary_key=True)
    supplier=models.ForeignKey(Supplier, on_delete=CASCADE, null= True)
    i_state=models.CharField(max_length=70, null=True, blank=True)
    i_district=models.CharField(max_length=70, null=True, blank=True)
    icu_beds=models.IntegerField(null=True, blank=True)

class Ventilator(models.Model):
    s_ventilator_id=models.AutoField(primary_key=True)
    supplier=models.ForeignKey(Supplier, on_delete=CASCADE, null= True)
    v_state=models.CharField(max_length=70, null=True, blank=True)
    v_district=models.CharField(max_length=70, null=True, blank=True)
    ventilator_beds=models.IntegerField(null=True, blank=True)

class IcuVentilator(models.Model):
    s_icu_ventilator_id=models.AutoField(primary_key=True)
    supplier=models.ForeignKey(Supplier, on_delete=CASCADE, null= True)
    iv_state=models.CharField(max_length=70, null=True, blank=True)
    iv_district=models.CharField(max_length=70, null=True, blank=True)
    icu_ventilator_beds=models.IntegerField(null=True, blank=True)

class Oxygen(models.Model):
    s_oxygen_id=models.AutoField(primary_key=True)
    supplier=models.ForeignKey(Supplier, on_delete=CASCADE, null= True)
    o_state=models.CharField(max_length=70, null=True, blank=True)
    o_district=models.CharField(max_length=70, null=True, blank=True)
    oxygen=models.CharField(max_length=5, null=True, blank=True)

class Patient(models.Model):
    p_id=models.AutoField(primary_key=True)
    p_username=models.CharField(max_length=100, null=True, blank=True)
    p_firstname=models.CharField(max_length=100, null=True, blank=True)
    p_lastname=models.CharField(max_length=100, null=True, blank=True)
    p_emailid=models.EmailField(('email address'),null=True, blank=True)
    p_pass1=models.CharField(max_length=40,null=True, blank=True)
    p_pass2=models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.p_username


class Booking(models.Model):
    booking_id=models.AutoField(primary_key=True)
    bed=models.CharField(max_length=40,choices=OPTIONS, null=True)
    oxygen=models.CharField(max_length=40,choices=OXYGEN, null=True)
    patient=models.ForeignKey(Patient, on_delete=CASCADE, null= True)
    supplier=models.ForeignKey(Supplier, on_delete=CASCADE, null= True)

    def __str__(self):
        return self.bed

# class Supplier(models.Model):
#     s_id=models.AutoField(primary_key=True)
#     s_agency_name=models.CharField(max_length=100)
#     s_emailid=models.EmailField(('email address'), unique=True)
#     s_password=models.CharField(max_length=40, default='name4587')
#     s_state=models.CharField(max_length=70)
#     s_district=models.CharField(max_length=70)
#     icu_beds=models.IntegerField()
#     ventilator_beds=models.IntegerField()
#     icu_ventilator_beds=models.IntegerField()
#     oxygen=models.CharField(max_length=5)


#     # def __str__(self):
#     #     return self.s_agency_name

#     empAuth_objects = models.Manager()

# ModelAdmin to show in form of table 

#Creating class
# Class ModelAdminClassName(admin.ModelAdmin):
# list_display=('fn1','fn2',...)

#registering class
#admin.site.register(ModelClassName, ModelAdminClassName)