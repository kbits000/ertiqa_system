from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

from datetime import date

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone

class User(AbstractUser):
    pass

# Create your models here.

class Workplace(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE,)
    WORKPLACE_CHOICES = [('operation_lab', 'Operation Lab'), ('warehouse', 'Warehouse'), ('else', 'Else'),]
    workplace = models.CharField(max_length=30, default='else', choices=WORKPLACE_CHOICES, null=False, blank=False,)

    def __str__(self):
        return f'{self.user.username}, working in {self.workplace}'

# TODO make unique fields unique regardless of capital and small letters
# TODO add help_text to almost every field
# TODO consider changes primary keys of some models
class Processor(models.Model):
    # TODO do I have to make name field unique??
    name = models.CharField(verbose_name="Processor's Company and Name/Model", max_length=30, unique=True, null=False,
                            blank=False, help_text="E.g., Intell Core i7 or Intell Core i5",)

    def __str__(self):
        return self.name


class RAM_Size(models.Model):
    size = models.IntegerField(verbose_name="RAM's Size(GB)", default=4, unique=True, blank=False, null=False,
                               db_column='ram_size',)

    class Meta:
        verbose_name = 'RAM Size'

    def __str__(self):
        return str(self.size) + 'GB RAM'


class Display_Size(models.Model):
    # TODO restrict value of size to positive numbers
    size = models.FloatField(default='4.70', unique=True, null=False, blank=False, help_text="Display sizes are in inches",)

    class Meta:
        verbose_name = "Display's Size"

    def __str__(self):
        return str(self.size) + ' inch'


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False, )

    class Meta:
        verbose_name = "Devices' Category"
        verbose_name_plural = "Devices' Categories"

    def __str__(self):
        return self.name


class GPU(models.Model):
    name = models.CharField(max_length=30, verbose_name="GPU's Company and Model/Name", unique=True, null=False, blank=False, help_text="E.g., Nvidia GeForce 720M",)

    class Meta:
        verbose_name = 'GPU'
        verbose_name_plural = "GPU's"

    def __str__(self):
        return self.name


class Android(models.Model):
    device = models.OneToOneField('Device', on_delete=models.SET_NULL, null=True, blank=True,)

    class Meta:
        verbose_name = 'Operating System - Android'
        verbose_name_plural = 'Operating Systems - Android'

    def __str__(self):
        return f'Android ID: {self.id}, {self.name}'

class IOS(models.Model):
    device = models.OneToOneField('Device', on_delete=models.SET_NULL, null=True, blank=True,)

    class Meta:
        verbose_name = 'Operating System - iOS'
        verbose_name_plural = 'Operating Systems - iOS'

    def __str__(self):
        return f'iOS ID: {self.id}, {self.name}'

class Linux(models.Model):
    device = models.OneToOneField('Device', on_delete=models.SET_NULL, null=True, blank=True,)

    class Meta:
        verbose_name = 'Operating System - Linux'
        verbose_name_plural = "Operating Systems - Linux"

    def __str__(self):
        return f'Linux ID: {self.id}, {self.name}'

class MacOS(models.Model):
    device = models.OneToOneField('Device', on_delete=models.SET_NULL, null=True, blank=True,)

    class Meta:
        verbose_name = 'Operating System - macOS'
        verbose_name_plural = "Operating System - macOS"

    def __str__(self):
        return f'macOS ID: {self.id}, {self.name}'


class Windows_Price(models.Model):
    # TODO ask warehouse employee or technicians if let them decide if price should be added manually or automatically
    price = models.DecimalField(max_digits=5, decimal_places=3, unique=True, null=False, blank=False,)
    do_use = models.BooleanField(default=True, db_comment="A flag representing whethere to use this price object or not for calculating costs of spends", verbose_name='Do you want to use this price for future Windows products?', help_text='check this option if you want to use this price for calculating future Windows Costs',)
    added = models.DateTimeField(auto_now_add=True,)

    class Meta:
        verbose_name = 'Windows Price'
        verbose_name_plural = 'Windows Prices'
        constraints = [
            models.UniqueConstraint(name='Only one Price should be True', fields=['do_use'], condition=Q(do_use=True)),]

    def __str__(self):
        return f'Windows, Price: {self.price}, Used? {self.do_use}'


# TODO add mar_coa_name
class Windows(models.Model):
    device = models.OneToOneField('Device', on_delete=models.PROTECT, null=True, blank=True,)
    report_name = models.TextField(null=False, blank=False, help_text='E.g., MAR-Citizenship',)
    mar_name = models.TextField(null=False, blank=False, verbose_name='MAR Name', help_text='E.g., ACTIVE-IT s.c.',)
    # TODO name OR product OR product_name
    name = models.TextField(null=False, blank=False, db_comment='This is also called Product Installed', help_text='E.g., Windows 10 PRO Citizenship',)
    installation_date = models.DateField(default=date.today, null=False, blank=False,)
    product_key_id = models.TextField(unique=True, null=False, blank=False, db_comment='This is also called MAR COA SN', help_text='I.e., MAR COA SN',)
    price = models.ForeignKey('Windows_Price', on_delete=models.PROTECT,)
    remark = models.TextField(default=None, null=True, blank=True,)
    
    added = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    
    class Meta:
        verbose_name = 'Operating System - Windows'
        verbose_name_plural = "Operating Systems - Windows"

    def __str__(self):
        return f'{self.name}, Key ID: {self.product_key_id}, Installation Date: {self.installation_date}'


# TODO make Windows, macOS... flags
class Software(models.Model):
    name = models.TextField(verbose_name="Software's Name", null=False, blank=False,)
    # PROBLEM HERE
    OPERATING_SYSTEM_CHOICES = [('windows', 'Windows'), ('macos', 'macOS'), ('linux', 'Linux'), ('ios', 'iOS'), ('android', 'Android'),]
    operating_system = models.CharField(max_length=20, choices=OPERATING_SYSTEM_CHOICES, default='windows', null=False, blank=False,)
    remark = models.TextField(default=None, null=True, blank=True, verbose_name='Remark/Description',)

    def __str__(self):
        return f'{self.name} (for {self.operating_system})'


class Software_Price(models.Model):
    software = models.ForeignKey('Software', on_delete=models.PROTECT,)
    price = models.DecimalField(max_digits=8, decimal_places=3, null=False, blank=False, default=0.0, db_comment='The price of spare part',)
    do_use = models.BooleanField(default=True, db_comment="A flag representing whethere to use this price object or not for calculating costs of spends", verbose_name='Do you want to use this price for the sepecified item ?', help_text='If checked, this price will be used for calculating future costs for the specified software.',)
    added = models.DateTimeField(auto_now_add=True,)
    
    constraints = [models.UniqueConstraint(name='Duplicate. There is already a price of this software in the same date', fields=['price', 'software', 'date', 'do_use'], violation_error_message='There is already a software with the same details as all of this one.' ),
                    models.UniqueConstraint(name='Cannot use more than two prices for a single software at the same time', fields=['software', 'do_use'], condition=Q(do_use=True), violation_error_message='Cannot use more than two prices for a single software at the same time. Please make do_use field of old prices False to add new to be used prices.' ),]
    
    class Meta:
        verbose_name = 'Software(s) Price'
        verbose_name_plural = "Softwares Prices"

    def __str__(self):
        return f'{self.software.name}, {self.added}, {self.price} SAR, Do Use: {self.do_use}'


class OEM_Brand(models.Model):
    name = models.CharField(max_length=30, verbose_name="Devices' OEM Brand", unique=True, null=False, blank=False,
                            db_column='oem_brand', )

    class Meta:
        verbose_name = 'OEM Brand'
        verbose_name_plural = "OEM Brands"

    def __str__(self):
        return self.name


# Specilization of Computer Peripheral
class Computer_Peripheral_Price(models.Model):
    peripheral = models.ForeignKey('Computer_Peripheral', on_delete=models.PROTECT,)
    price = models.DecimalField(max_digits=8, decimal_places=3, null=False, blank=False, default=0.0, db_comment='The price of spare part/peripheral',)
    # date = models.DateField(null=False, blank=False, default=date.today,)
    # TODO fix verbose name of do_use
    do_use = models.BooleanField(default=True, db_comment="A flag representing whethere to use this price object or not for calculating costs of spends", verbose_name='Do you want to use this price for the sepecified item ?', help_text='If checked, this price will be used for calculating future costs for the specified peripheral.',)
    added = models.DateTimeField(auto_now_add=True,)

    class Meta:
        verbose_name = "Computer Peripheral Price Object"
        verbose_name_plural = "Computer Peripherals' Prices"
        constraints = [models.UniqueConstraint(name='Duplicate. There is already a price of this peripheral', fields=['price', 'peripheral', 'do_use'], violation_error_message='There is already a peripheral with the same details as all of this one.' ),
                       models.UniqueConstraint(name='Cannot use more than two prices for a single peripheral at the same time', fields=['peripheral', 'do_use'], condition=Q(do_use=True), violation_error_message='Cannot use more than two prices for a single peripheral at the same time. Please make do_use field of old prices False to add new to be used prices.' ),]
    
    def __str__(self):
        return f'{self.peripheral.name} SN: {self.peripheral.serial_number}, {self.price}, Do Use: {self.do_use}'


class Computer_Spare_Part_Price(models.Model):
    spare_part = models.ForeignKey('Computer_Spare_Part', on_delete=models.PROTECT,)
    price = models.DecimalField(max_digits=8, decimal_places=3, null=False, blank=False, default=0.0, db_comment='The price of spare part',)
    # date = models.DateField(null=False, blank=False, default=date.today,)
    # TODO fix verbose name of do_use
    do_use = models.BooleanField(default=True, db_comment="A flag representing whethere to use this price object or not for calculating costs of spends", verbose_name='Do you want to use this price for the sepecified item ?',)
    added = models.DateTimeField(auto_now_add=True,)

    class Meta:
        verbose_name = "Computer Spare Part Price Object"
        verbose_name_plural = "Computer Spare Parts' Prices"
        constraints = [models.UniqueConstraint(name='Duplicate. There is already a price of this spare part', fields=['price', 'spare_part', 'do_use'], violation_error_message='There is already a spare part with the same details as all of this one.' ),
                       models.UniqueConstraint(name='Cannot use more than two prices for a single spare part at the same time', fields=['spare_part', 'do_use'], condition=Q(do_use=True), violation_error_message='Cannot use more than two prices for a single spare part at the same time. Please make do_use field of old prices False to add new to be used prices.' ), ]
    
    def __str__(self):
        return f'{self.spare_part.name} SN: {self.spare_part.serial_number}, {self.price}, Do Use: {self.do_use}'




class Computer_Spare_Part(models.Model):
    name = models.TextField(null=False, blank=False, help_text='E.g., CPU, HDD, SSD, RAM, ROM or RTC',)
    serial_number = models.TextField(unique=True, null=False, blank=False,)
    remark = models.TextField(default=None, null=True, blank=True, verbose_name='Remark/Description',)
    added = models.DateTimeField(auto_now_add=True,)

    class Meta:
        verbose_name = 'Computer Spare Part'
        verbose_name_plural = "Computer Spare Parts"

    def __str__(self):
        return f'{self.name}, SN: {self.serial_number}'


class Computer_Peripheral(models.Model):
    name = models.TextField(null=False, blank=False, help_text='E.g., mouse, keyboard, speaker, printer, headpone or USB flash memory', )
    serial_number = models.TextField(unique=True, null=False, blank=False,)
    remark = models.TextField(default=None, null=True, blank=True, verbose_name='Remark/Description',)
    added = models.DateTimeField(auto_now_add=True,)

    class Meta:
        verbose_name = 'Computer Peripheral'
        verbose_name_plural = "Computer Peripherals"

    def __str__(self):
        return f'{self.name}, SN: {self.serial_number}'


class Device_Spare_Parts_Details(models.Model):
    device = models.ForeignKey('Device', on_delete=models.PROTECT,)
    spare_part = models.ForeignKey('Computer_Spare_Part', on_delete=models.PROTECT,)
    quantity = models.BigIntegerField(default=1, null=False, blank=False,)
    is_bought = models.BooleanField(null=True, blank=True,)
    price = models.ForeignKey('Computer_Spare_Part_Price', on_delete=models.PROTECT, null=True, blank=True,)

    class Meta:
        verbose_name = "Device - Spare Part(s) with Device"
        verbose_name_plural = "Device - Spare Part(s) with Devices"
        # constraints = [models.CheckConstraint(  name='It is either not bought with no price or bought with a price', check=((Q(is_bought=True) & Q(price__isnull=True)) | ( Q(is_bought=False) & Q(price__isnull=False)))  ), ]


class Device_Peripherals_Details(models.Model):
    device = models.ForeignKey('Device', on_delete=models.PROTECT,)
    peripheral = models.ForeignKey('Computer_Peripheral', on_delete=models.PROTECT,)
    quantity = models.BigIntegerField(default=1, null=False, blank=False,)
    # TODO ask if by default it is False
    is_bought = models.BooleanField(null=True, blank=True,)
    price = models.ForeignKey('Computer_Peripheral_Price', on_delete=models.PROTECT, null=True, blank=True,)

    class Meta:
        verbose_name = "Device - Peripheral(s) with Device"
        verbose_name_plural = "Device - Peripheral(s) with Devices"
    
    def __str__(self):
        if self.is_bought == True:
            return f'ID: {self.id}, Device ID: {self.device.id}, Device Barcode: {self.device.barcode}, Peripheral Name: {self.peripheral.name}, Quantity: {self.quantity}, bought'
        else:
            return f'ID: {self.id}, Device ID: {self.device.id}, Device Barcode: {self.device.barcode}, Peripheral Name: {self.peripheral.name}, Quantity: {self.quantity}'


class Device_Software_Details(models.Model):
    device = models.ForeignKey('Device', on_delete=models.PROTECT,)
    software = models.ForeignKey('Software', on_delete=models.PROTECT,)
    is_bought = models.BooleanField(null=True, blank=True,)
    price = models.ForeignKey('Software_Price', on_delete=models.PROTECT, null=True, blank=True,)
    
    class Meta:
        verbose_name = "Device - Software(s) installed in Device"
        verbose_name_plural = "Device - Software(s) installed in Devices"


# TODO ask technicians what to do in case of deleting a table
class Device(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True,)
    barcode = models.TextField(unique=True, null=False, blank=False, db_comment='Bar Code works like an id', help_text='Bar Code is like an id',)
    serial_number = models.TextField(unique=True, null=True,blank=True,)

    # TODO Is it better to use integer choices than words?
    # TODO DO I have to add a new STATUS choice called 'In Process'?
    STATUS_CHOICES = [('not_inspected', 'Not Inspected'), ('scrapped', 'Scrapped'), ('refurbished', 'Refurbished/Ready'), ]
    # TODO add db_comment='Status of device is what the condition of the device. That is, whethere it has been processed by technicians or not' in status field
    # TODO add help_text attribute in status field
    status = models.CharField(verbose_name='Status of Device', max_length=30, choices=STATUS_CHOICES, default='not_inspected',
                              null=False, blank=False, )

    refurbished = models.OneToOneField('Refurbished_Device', default=None, on_delete=models.PROTECT, null=True,)
    scrapped = models.OneToOneField('Scrapped_Device', default=None, on_delete=models.PROTECT, null=True,)

    category = models.ForeignKey('Category', verbose_name='Category of Device', on_delete=models.PROTECT, null=False,
                                 blank=False, )

    processor = models.ForeignKey('Processor', on_delete=models.PROTECT, null=True, blank=True,)

    OPERATING_SYSTEM_CHOICES = [('windows', 'Windows'), ('macos', 'macOS'), ('linux', 'Linux'), ('ios', 'iOS'), ('android', 'Android'),]
    operating_system = models.CharField(max_length=20, choices=OPERATING_SYSTEM_CHOICES, default='windows', null=False, blank=False,)


    oem_brand = models.ForeignKey('OEM_Brand', verbose_name="Device's OEM Brand", on_delete=models.PROTECT, null=False, blank=False,)

    ram_size = models.ForeignKey('RAM_Size', default=None, verbose_name='GB RAM size in the device (optional)',
                                 on_delete=models.SET_NULL, null=True, blank=True, )

    display_size = models.ForeignKey('Display_Size', default=None, verbose_name='Display Size in Inches (optional)',
                                     on_delete=models.SET_NULL, null=True, blank=True,)

    gpu = models.ForeignKey('GPU', default=None, verbose_name="Device's GPU (optional)", on_delete=models.SET_NULL,
                            null=True, blank=True, )

    # TODO check if it is better to add on_delete field
    softwares = models.ManyToManyField('Software', through='Device_Software_Details',default='', verbose_name='Installed Software(s) (optional)',
                                       null=True, blank=True, )

    peripherals = models.ManyToManyField('Computer_Peripheral', default=None, through='Device_Peripherals_Details', verbose_name='peripherals with the device', null=True, blank=True,)
    spare_parts = models.ManyToManyField('Computer_Spare_Part', default=None, through='Device_Spare_Parts_Details', verbose_name='New spare parts added to this device', null=True, blank=True,)
    # TODO write a constraint that makes either corporate_donor or individual_donor an empty but not both. Also, make sure that it is not allowed for both of them to be empty
    corporate_donor = models.ForeignKey('Corporate_Donor', default=None, on_delete=models.PROTECT, null=True,)
    individual_donor = models.ForeignKey('Individual_Donor', default=None, on_delete=models.PROTECT, null=True,)
    individual_donor_flag = models.BooleanField(default=False, null=True, blank=True, verbose_name='Device(s) has been donated by individual person',)

    total_spendings = models.OneToOneField('Total_Spendings', on_delete=models.PROTECT, default=None, null=True, blank=True,)

    added = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    remark = models.TextField(default=None, null=True, blank=True,)

    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(name='A category should be selected', check=Q(category__isnull=False)),
    #         models.CheckConstraint(name='A processor should be selected', check=Q(processor__isnull=False)),
    #         models.CheckConstraint(name='A device cannot be donated by both corporate and individual donors',
    #                                check=Q(corporate_donor__isnull=False) & Q(individual_donor__isnull=True) | Q(
    #                                    individual_donor__exact=False) & Q(corporate_donor__isnull=True)),
    #         models.CheckConstraint(name='A description for scrapping this device should be provided', check=~Q(status__exact='scrapped_device') & Q(description__exact='')),
    #         # models.CheckConstraint(name='Only One Operating System Can Be Chosen', check=)
    #         # models.CheckConstraint(name='macOS Operating System Cannot have Windows Product Key',
    #         #                        check=Q(operating_system__iexact='macos') & Q(windows_product_key__isnull=True),),
    #         # models.CheckConstraint(name='No Need For Processor Selection If Operating System is iOS or Android', check=Q(Q(operating_system__exact='ios') & Q(processor__isnull=False))
    #         #                        | Q(Q(operating_system__exact='android') & Q(processor__isnull=False)) ),
    #         # models.CheckConstraint(name='Check Operating System and Windows Product Key fields', check= Q(Q(operating_system__exact='windows') & Q(windows_product_key__isnull=False))
    #         #                        | Q(Q(operating_system__exact='macos') & Q(windows_product_key__isnull=True))
    #         #                        | Q(Q(operating_system__exact='linux') & Q(windows_product_key__isnull=True))
    #         #                        | Q(Q(operating_system__exact='ios') & Q(windows_product_key__isnull=True))
    #         #                        | Q(Q(operating_system__exact='android') & Q(windows_product_key__isnull=True))
    #         #                        | Q(Q(operating_system__exact='ios') & Q(processor__isnull=False))
    #         #                        | Q(Q(operating_system__exact='android') & Q(processor__isnull=False)))
    #     ]

    def __str__(self):
        return f'ID:{self.id}, Barcode: {str(self.barcode)}, {self.category}, {self.operating_system}, {self.status}'


class Corporate_Donor(models.Model):
    name = models.CharField(max_length=40, unique=True, null=False, blank=False, db_comment='Corporate_Donor_name',)
    type = models.ForeignKey('Corporate_Type', default=None, on_delete=models.SET_NULL, null=True, blank=True,)

    class Meta:
        verbose_name = "Corporate Donor"
        verbose_name_plural = "Corporate Donors"

    def __str__(self):
        if self.type is None:
            return f'ID:{self.id}, {self.name}'
        else:
            return f'ID:{self.id}, {self.name}, {self.type}'


class Corporate_Type(models.Model):
    type = models.CharField(max_length=30, unique=True, null=False, blank=False,)

    class Meta:
        verbose_name = "Corporate's Type"
        verbose_name_plural = "Corporates' Types"

    def __str__(self):
        return self.type


class Individual_Donor(models.Model):

    class Meta:
        verbose_name = "Individual Donor"
        verbose_name_plural = "Individual Donors"


class Device_Refurbishment_Request_Details(models.Model):
    request = models.ForeignKey('Device_Refurbishment_Request', on_delete=models.PROTECT,)
    category = models.ForeignKey('Category', on_delete=models.PROTECT,)
    quantity = models.BigIntegerField(default=1, null=False, blank=False,)

    # OPERATING_SYSTEM_CHOICES = [('windows', 'Windows'), ('macos', 'macOS'), ('linux', 'Linux'), ('ios', 'iOS'), ('android', 'Android'),]
    # TODO It should be OEM-Brand
    # DB_COMMENT_OPERATING_SYSTEM = 'Operating System names should be unified. For example, if many categories have Windows operating system, then  field for them should be the same. That is, "windows"'
    # operating_system = models.CharField(max_length=30, null=False, blank=False, default='windows', db_comment=DB_COMMENT_OPERATING_SYSTEM, help_text=DB_COMMENT_OPERATING_SYSTEM,)
    
    OEM_BRAND_CHOICES = [('apple', 'Apple'), ('others', 'Others'),]
    oem_brand = models.CharField(max_length=20, default='others', choices=OEM_BRAND_CHOICES, null=False, blank=False,)

    # TODO draw these in conseptual design/diagram
    # TODO make  cooperate_donor models.PROTECT
    corporate_donor = models.ForeignKey('Corporate_Donor', default=None, on_delete=models.SET_NULL, null=True, blank=True,)
    # check if it is better to change individual_donor from Foreign Key to CharField
    individual_donor_flag = models.BooleanField(default=False, null=True, blank=True, verbose_name='Device(s) has been donated by individual person',)

    class Meta:
        verbose_name = "Request Details - Refurbishment of Device"
        verbose_name_plural = "Requests Details - Refurbishment of Devices"

    def __str__(self):
        return f'Category: {self.category}, Request: {self.request}, Quantity: {self.quantity}'


class Device_Refurbishment_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    user_response = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_response_device_refurbishment_request',)
    # TODO ask technicians about the list of request statuses
    STATUS_CHOICES = [('pending','Pending'), ('completed', 'Completed'), ('canceled', 'Canceled'), ('rejected', 'Rejected'), ('accepted', 'Accepted'),]
    status = models.CharField(verbose_name='Status of Report', max_length=20, choices=STATUS_CHOICES, default='Pending', null=False, blank=False,)
    receive_date = models.DateTimeField(null=True, blank=True,)
    # request_from
    created = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    remark = models.TextField(null=True, blank=True, default=None,)
    remark_response = models.TextField(null=True, blank=True, default=None,)
    categories = models.ManyToManyField('Category', through='Device_Refurbishment_Request_Details',)

    class Meta:
        verbose_name = "Request - Refurbishment of Device"
        verbose_name_plural = "Requests - Refurbishment of Devices"

    # def __str__(self):
    #     if self.updated is not None:
    #         return f'Request ID: {self.id}, Created In: {self.created}, Updated In: {self.updated}'
    #     else:
    #         return f'Request ID: {self.id}, Created In: {self.created}, No Updates'


class Inspect_Peripheral_Request_Details(models.Model):
    # TODO add null=False & blank=False
    peripheral = models.ForeignKey('Computer_Peripheral', on_delete=models.PROTECT,)
    request = models.ForeignKey('Inspect_Peripheral_Request', on_delete=models.PROTECT,)
    number = models.BigIntegerField(default=1, null=False, blank=False,)

    class Meta:
        verbose_name = 'Request Details - Peripheral Inspection'
        verbose_name_plural = 'Requests Details - Peripheral(s) Inspections'

    def __str__(self):
        return f'Peripheral: {self.peripheral}, Request: {self.request}, Number: {self.number}'

class Inspect_Peripheral_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    user_response = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_response_peripheral_inspection_request',)
    # TODO ask technicians about the list of request statuses
    STATUS_CHOICES = [('pending','Pending'), ('completed', 'Completed'), ('canceled', 'Canceled'), ('rejected', 'Rejected'), ('accepted', 'Accepted'),]
    status = models.CharField(verbose_name='Status of Report', max_length=20, choices=STATUS_CHOICES, default='Pending', null=False, blank=False,)
    receive_date = models.DateTimeField(null=True, blank=True,)
    # request_from
    created = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    remark = models.TextField(null=True, blank=True, default=None,)
    remark_response = models.TextField(null=True, blank=True, default=None,)
    # TODO it should be screen, keyboards, mouses
    peripherals = models.ManyToManyField('Computer_Peripheral', verbose_name='Peripheral(s) to be inspected by technician(s)',)

    class Meta:
        verbose_name = 'Requests - Peripheral Inspection'
        verbose_name_plural = 'Requests - Peripheral(s) Inspections'

    def is_updated(self):
        if self.updated.year == self.created.year and self.updated.month == self.created.month and self.updated.day == self.created.day and self.updated.minute == self.created.minute and self.updated.second == self.created.second:
            return False
        else:
            return True
    
    def __str__(self):
        return f'Request ID: {self.id}'

# TODO make numbers a must
# class Requested_Spare_Parts_And_Numbers(models.Model):
#


class Spare_Part_Request(models.Model):
    request = models.ForeignKey('Spare_Part_Peripheral_Device_Request', on_delete=models.SET_NULL, null=True,)
    spare_part = models.ForeignKey('Computer_Spare_Part', on_delete=models.SET_NULL, null=True,)
    quantity = models.BigIntegerField(default=1, null=False, blank=False,)

    class Meta:
        verbose_name = 'Request - Spare Parts'
        verbose_name_plural = 'Requests - Spare Part(s)'

    def __str__(self):
        return f'Spare Part Request ID: {self.id}'


class Peripheral_Request(models.Model):
    request = models.ForeignKey('Spare_Part_Peripheral_Device_Request', on_delete=models.SET_NULL, null=True,)
    peripheral = models.ForeignKey('Computer_Peripheral', on_delete=models.SET_NULL, null=True,)
    quantity = models.BigIntegerField(default=1, null=False, blank=False,)

    class Meta:
        verbose_name = 'Request - Peripheral'
        verbose_name_plural = 'Requests - Peripheral(s)'

    def __str__(self):
        return f'Peripheral Request ID: {self.id}'


class Device_Request(models.Model):
    request = models.ForeignKey('Spare_Part_Peripheral_Device_Request', on_delete=models.SET_NULL, null=True,)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True,)
    OEM_BRAND_CHOICES = [('apple', 'Apple'), ('others', 'Others'),]
    oem_brand = models.CharField(max_length=20, default='others', choices=OEM_BRAND_CHOICES, null=False, blank=False,)
    quantity = models.BigIntegerField(default=1, null=False, blank=False,)

    class Meta:
        verbose_name = 'Request - Device'
        verbose_name_plural = 'Requests - Device(s)'

    def __str__(self):
        return f'Device Request ID: {self.id}'

class Anything_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    user_response = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_response_anything_request',)
    # TODO ask technicians about the list of request statuses
    STATUS_CHOICES = [('pending','Pending'), ('completed', 'Completed'), ('canceled', 'Canceled'), ('rejected', 'Rejected'), ('accepted', 'Accepted'),]
    status = models.CharField(verbose_name='Status of Report', max_length=20, choices=STATUS_CHOICES, default='Pending', null=False, blank=False,)
    # request_from
    created = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    remark = models.TextField(null=True, blank=True, default=None,)
    remark_response = models.TextField(null=True, blank=True, default=None,)

    class Meta:
        verbose_name = "Random Request"
        verbose_name_plural = "Random Requests"
    
    def is_updated(self):
        if self.updated.year == self.created.year and self.updated.month == self.created.month and self.updated.day == self.created.day and self.updated.minute == self.created.minute and self.updated.second == self.created.second:
            return False
        else:
            return True

    def __str__(self):
        if self.updated is not None:
            return f'Request ID: {self.id}'

class Spare_Part_Peripheral_Device_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    user_response = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_response_sp_p_d_request',)
    # TODO ask technicians about the list of request statuses
    # TODO change fields of STATUS_CHOICES
    STATUS_CHOICES = [('pending','Pending'), ('completed', 'Completed'), ('canceled', 'Canceled'), ('rejected', 'Rejected'), ('accepted', 'Accepted'),]
    status = models.CharField(verbose_name='Status of Report', max_length=20, choices=STATUS_CHOICES, default='Pending', null=False, blank=False,)
    receive_date = models.DateTimeField(null=True, blank=True,)
    # request_from
    created = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    remark = models.TextField(null=True, blank=True, default=None,)
    remark_response = models.TextField(null=True, blank=True, default=None,)
    spare_part_flag = models.BooleanField(default=False, verbose_name='Spare Part(s) has been requested', db_comment='Indicates whether spare part(s) has been requested or not', help_text='Has Spare Part(s) Been Requested?',)
    peripheral_flag = models.BooleanField(default=False, verbose_name='Peripheral(s) has been requested', db_comment='Indicates whether peripheral(s) has been requested or not', help_text='Has Peripheral(s) Been Requested?',)
    device_flag = models.BooleanField(default=False, verbose_name='Device(s) has been requested', db_comment='Indicates whether device(s) has been requested or not', help_text='Has device(s) Been Requested?',)


    class Meta:
        verbose_name = "Request - Spare Part/Peripheral/Device"
        verbose_name_plural = "Requests - Spare Part(s)/Peripheral(s)/Device(s)"

    def is_updated(self):
        if self.updated.year == self.created.year and self.updated.month == self.created.month and self.updated.day == self.created.day and self.updated.minute == self.created.minute and self.updated.second == self.created.second:
            return False
        else:
            return True

    def __str__(self):
        return f'Request ID: {self.id}, Created In: {self.created.strftime("%a, %d %b, %Y")}, Updated In: {self.updated.strftime("%a, %d %b, %Y")}'


class Total_Spendings(models.Model):
    total_spendings = models.DecimalField(max_digits=9, decimal_places=4, default=0,)
    peripherals_total_spendings = models.DecimalField(max_digits=9, decimal_places=4, default=0,)
    spare_parts_total_spendings = models.DecimalField(max_digits=9, decimal_places=4, default=0,)
    software_total_spendings = models.DecimalField(max_digits=9, decimal_places=4, default=0,)
    windows_spending = models.DecimalField(max_digits=9, decimal_places=4, default=0,)

    added = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = 'Total Spendings'
        verbose_name_plural = 'Total Spendings'

    def __str__(self):
        return f'Total Spendings: {self.total_spendings}'


class Refurbished_Device(models.Model):

    class Meta:
        verbose_name = 'Refurbished Device'
        verbose_name_plural = 'Refurbished Devices'


class Scrapped_Device(models.Model):

    class Meta:
        verbose_name = 'Scrapped Device'
        verbose_name_plural = 'Scrapped Devices'