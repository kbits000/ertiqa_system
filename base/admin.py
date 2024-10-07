from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

from .models import Workplace

from .models import Device, Processor, RAM_Size, Display_Size, Category, GPU, Software, OEM_Brand, Computer_Peripheral

from .models import Corporate_Donor, Corporate_Type, Individual_Donor, Computer_Spare_Part

from .models import Inspect_Peripheral_Request, Device_Refurbishment_Request
from .models import Spare_Part_Request, Peripheral_Request, Device_Request, Spare_Part_Peripheral_Device_Request, Anything_Request
from .models import Inspect_Peripheral_Request_Details, Device_Refurbishment_Request_Details

from .models import Windows, MacOS, Linux, IOS, Android
from .models import Computer_Peripheral_Price, Computer_Spare_Part_Price, Windows, Windows_Price
from .models import *

# Register your models here.

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class WorkPlaceInline(admin.StackedInline):
    model = Workplace
    can_delete = False
    verbose_name_plural = "work places"

class UserAdmin(BaseUserAdmin):
    inlines = [WorkPlaceInline]

admin.site.register(User, UserAdmin)

admin.site.register(Processor)
admin.site.register(RAM_Size)
admin.site.register(Display_Size)
admin.site.register(Category)
admin.site.register(GPU)
admin.site.register(Software)
admin.site.register(OEM_Brand)
admin.site.register(Computer_Peripheral)
admin.site.register(Device)

admin.site.register(Corporate_Donor)
admin.site.register(Corporate_Type)
admin.site.register(Individual_Donor)
admin.site.register(Computer_Spare_Part)

class InspectPeripheralRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'updated',]

# admin.site.register(Inspect_Device_Request)
admin.site.register(Inspect_Peripheral_Request, InspectPeripheralRequestAdmin)

admin.site.register(Device_Refurbishment_Request)

admin.site.register(Spare_Part_Request)
admin.site.register(Peripheral_Request)
admin.site.register(Device_Request)
admin.site.register(Spare_Part_Peripheral_Device_Request)
admin.site.register(Anything_Request)


admin.site.register(Inspect_Peripheral_Request_Details)
# admin.site.register(Inspect_Device_Request_Detail)
# admin.site.register(Spare_Part_Request_Detail)
# admin.site.register(Peripheral_Request_Detail)
admin.site.register(Device_Refurbishment_Request_Details)

admin.site.register(Windows)
admin.site.register(MacOS)
admin.site.register(Linux)
admin.site.register(IOS)
admin.site.register(Android)

admin.site.register(Computer_Peripheral_Price)
admin.site.register(Computer_Spare_Part_Price)
admin.site.register(Windows_Price)
admin.site.register(Software_Price)

admin.site.register(Device_Peripherals_Details)
admin.site.register(Device_Spare_Parts_Details)
admin.site.register(Device_Software_Details)
