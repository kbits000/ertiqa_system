from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import views
from .forms import DeviceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Anything_Request, Category, Corporate_Donor, Device_Refurbishment_Request, Device_Refurbishment_Request_Details
from .models import Computer_Peripheral, Computer_Spare_Part, OEM_Brand, Spare_Part_Request, Peripheral_Request, Device_Request
from .models import Inspect_Peripheral_Request, Inspect_Peripheral_Request_Details, Processor
from .models import Spare_Part_Peripheral_Device_Request, Computer_Peripheral_Price, Computer_Spare_Part_Price, RAM_Size, Display_Size
from .models import GPU, Device, Windows, Windows_Price
from .models import *
import datetime
from django.contrib import messages
from decimal import Decimal, getcontext

# Create your views here.

from http import HTTPStatus
from django.http import HttpResponse

class HttpResponseNoContent(HttpResponse):
    status_code = HTTPStatus.NO_CONTENT


def main(request):
    context = {}
    return render(request, 'base/main.html', context)

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def home_manager(request):
    if request.user.is_superuser:

        all_usernames = User.objects.all()

        username_numOfDevices = []
        for username in all_usernames:
            username_devices = {}
            num_of_devices_inspected = Device.objects.filter(user=username).count()
            username_devices['username'] = username.username
            username_devices['num_of_devices'] = num_of_devices_inspected
            username_numOfDevices.append(username_devices)

        username_numOfScrappedAndRefurbished = []
        for username in all_usernames:
            username_scrapped_refurbished = {}
            username_scrapped_refurbished['username'] = username
            num_of_scrapped_devices = Device.objects.filter(user=username, status='scrapped').count()
            username_scrapped_refurbished['scrapped'] = num_of_scrapped_devices
            num_of_refurbished_devices = Device.objects.filter(user=username, status='refurbished').count()
            username_scrapped_refurbished['refurbished'] = num_of_refurbished_devices
            username_numOfScrappedAndRefurbished.append(username_scrapped_refurbished)
        
        # Device.objects.filter(added__month=8, status='refurbished').count() 
        # Device.objects.filter(added__month=8, status='refurbished').count() 
        
        context = {
            'username_numOfDevices': username_numOfDevices,
            'username_numOfScrappedAndRefurbished': username_numOfScrappedAndRefurbished,
        }
        return render(request, 'base/manager/home_manager.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def manager_chart_1(request, year, month):
    if request.user.is_superuser:

        all_usernames = User.objects.all()
        username_numOfScrappedAndRefurbished = []
        for username in all_usernames:
            username_scrapped_refurbished = {}
            username_scrapped_refurbished['username'] = username
            num_of_scrapped_devices = Device.objects.filter(user=username, status='scrapped').count()
            username_scrapped_refurbished['scrapped'] = num_of_scrapped_devices
            num_of_refurbished_devices = Device.objects.filter(user=username, status='refurbished').count()
            username_scrapped_refurbished['refurbished'] = num_of_refurbished_devices
            username_numOfScrappedAndRefurbished.append(username_scrapped_refurbished)
        print(username_numOfScrappedAndRefurbished)
        context = {
            'username_numOfScrappedAndRefurbished': username_numOfScrappedAndRefurbished
        }
        return render(request, 'base\manager\charts_pages\chart_1.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def manager_chart_2(request):

    if request.user.is_superuser:
        all_usernames = User.objects.all()
        username_numOfScrappedAndRefurbished = []
        
        if request.GET.get('year') == 'all':
            for username in all_usernames:
                username_scrapped_refurbished = {}
                username_scrapped_refurbished['username'] = username
                num_of_scrapped_devices = Device.objects.filter(user=username, status='scrapped').count()
                username_scrapped_refurbished['scrapped'] = num_of_scrapped_devices
                num_of_refurbished_devices = Device.objects.filter(user=username, status='refurbished').count()
                username_scrapped_refurbished['refurbished'] = num_of_refurbished_devices
                username_numOfScrappedAndRefurbished.append(username_scrapped_refurbished)
        else:
            year = request.GET['year']
            year = int(year)
            for username in all_usernames:
                username_scrapped_refurbished = {}
                username_scrapped_refurbished['username'] = username
                num_of_scrapped_devices = Device.objects.filter(added__year=year, user=username, status='scrapped').count()
                username_scrapped_refurbished['scrapped'] = num_of_scrapped_devices
                num_of_refurbished_devices = Device.objects.filter(added__year=year, user=username, status='refurbished').count()
                username_scrapped_refurbished['refurbished'] = num_of_refurbished_devices
                username_numOfScrappedAndRefurbished.append(username_scrapped_refurbished)


        context = {
            'username_numOfScrappedAndRefurbished': username_numOfScrappedAndRefurbished
        }
        return render(request, 'base\manager\charts_pages\chart_2.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def manager_change_prices(request):
    if request.user.is_superuser:
        return render(request, 'base/manager/manager_change_prices.html')
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def manager_change_windows_price(request):
    if request.user.is_superuser:
        
        windows_price = Windows_Price.objects.filter(do_use=True)
        if windows_price:
            windows_price = Windows_Price.objects.filter(do_use=True)[0].price
        else:
            windows_price = None
        
        context = {
            'windows_price': windows_price,
        }

        if request.method == 'POST':
            new_windows_price = request.POST.get('new-windows-price', None)
            if new_windows_price is None:
                messages.error(request, 'new-windows-price parameter has not been sent.')
                return redirect('manager-change-windows-price')
            
            if new_windows_price.strip() == '':
                messages.error(request, 'New Windows price field cannot be empty nor has only spaces.')
                return redirect('manager-change-windows-price')
            getcontext().prec = 4
            new_windows_price = Decimal(new_windows_price)
            old_windows_price_like_new = Windows_Price.objects.filter(price=new_windows_price)
            if old_windows_price_like_new:
                # Price like the new one exists
                old_windows_price_like_new = old_windows_price_like_new[0]
                windows_price_with_do_use_true = Windows_Price.objects.filter(do_use=True)
                if windows_price_with_do_use_true:
                    windows_price_with_do_use_true = Windows_Price.objects.filter(do_use=True)[0]
                    windows_price_with_do_use_true.do_use = False
                    windows_price_with_do_use_true.save()
                    old_windows_price_like_new.do_use = True
                    old_windows_price_like_new.save()
                else:
                    old_windows_price_like_new.do_use = True
                    old_windows_price_like_new.save()

            else:
                # A price like the new one does nots exists
                windows_price_with_do_use_true = Windows_Price.objects.filter(do_use=True)
                print(windows_price_with_do_use_true)
                if windows_price_with_do_use_true:
                    windows_price_with_do_use_true = Windows_Price.objects.filter(do_use=True)[0]
                    windows_price_with_do_use_true.do_use = False
                    windows_price_with_do_use_true.save()
                    new_windows_price_object = Windows_Price(price=new_windows_price, do_use=True)
                    new_windows_price_object.save()
                else:
                    new_windows_price_object = Windows_Price(price=new_windows_price, do_use=True)
                    new_windows_price_object.save()
            messages.success(request, f'Windows price has been changed to {new_windows_price}')
            return redirect('manager-change-windows-price')


        return render(request, 'base/manager/change_prices_windows.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


# LIST
@login_required(login_url='login')
def manager_change_peripherals_prices_list(request):
    if request.user.is_superuser:
        peripherals_list = Computer_Peripheral.objects.all()

        peripherals_with_their_current_prices = []
        for peripheral in peripherals_list:
            peripheral_with_current_price = {}
            peripheral_with_current_price['peripheral'] = peripheral
            peripheral_price = Computer_Peripheral_Price.objects.filter(peripheral=peripheral, do_use=True)
            if peripheral_price:
                peripheral_price = peripheral_price[0]
                peripheral_with_current_price['price'] = peripheral_price.price
            else:
                peripheral_with_current_price['price'] = None
            peripherals_with_their_current_prices.append(peripheral_with_current_price)

        context = {
            'peripherals_list': peripherals_list,
            'peripherals_with_their_current_prices': peripherals_with_their_current_prices,
        }
        return render(request, 'base/manager/manager_change_peripherals_prices_list.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def manager_change_price_of_peripheral(request, peripheral_id):
    if request.user.is_superuser:
        peripheral_object = Computer_Peripheral.objects.filter(id=peripheral_id)[0]
        peripheral_price_object = Computer_Peripheral_Price.objects.filter(peripheral=peripheral_object, do_use=True)
        
        if peripheral_price_object:
            peripheral_price_object = peripheral_price_object[0].price
        else:
            peripheral_price_object = None
        
        context = {
            'peripheral': peripheral_object,
            'peripheral_current_price': peripheral_price_object,
        }

        if request.method == "POST":
            new_peripheral_price = request.POST.get('new-peripheral-price', None)
            if new_peripheral_price is None:
                messages.error(request, 'new_peripheral_price parameter has not been sent.')
                return redirect('manager-change-price-of-peripheral')
            if new_peripheral_price.strip() == '':
                messages.error(request, 'New price of peripheral should not be empty neither has only spaces.')
                return redirect('manager-change-price-of-peripheral')
            
            getcontext().prec = 4
            new_peripheral_price = Decimal(new_peripheral_price)
            old_peripheral_price_like_new = Computer_Peripheral_Price.objects.filter(price=new_peripheral_price)
            if old_peripheral_price_like_new:
                # Price like the new one exists
                old_peripheral_price_like_new = old_peripheral_price_like_new[0]
                peripheral_price_with_do_use_true = Computer_Peripheral_Price.objects.filter(do_use=True)
                if peripheral_price_with_do_use_true:
                    peripheral_price_with_do_use_true = Computer_Peripheral_Price.objects.filter(do_use=True)[0]
                    peripheral_price_with_do_use_true.do_use = False
                    peripheral_price_with_do_use_true.save()
                    old_peripheral_price_like_new.do_use = True
                    old_peripheral_price_like_new.save()
                else:
                    old_peripheral_price_like_new.do_use = True
                    old_peripheral_price_like_new.save()
            else:
                # A price like the new one does nots exists
                peripheral_price_with_do_use_true = Computer_Peripheral_Price.objects.filter(do_use=True)
                if peripheral_price_with_do_use_true:
                    peripheral_price_with_do_use_true = Computer_Peripheral_Price.objects.filter(do_use=True)[0]
                    peripheral_price_with_do_use_true.do_use = False
                    peripheral_price_with_do_use_true.save()
                    new_peripheral_price_object = Computer_Peripheral_Price(peripheral=peripheral_object, price=new_peripheral_price, do_use=True)
                    # fedgfegeg
                    new_peripheral_price_object.save()
                else:
                    new_peripheral_price_object = Computer_Peripheral_Price(peripheral=peripheral_object, price=new_peripheral_price, do_use=True)
                    new_peripheral_price_object.save()
            
            messages.success(request, f'Peripheral Price has been changed to {new_peripheral_price}')
            return redirect('manager-change-peripherals-prices')

        return render(request, 'base/manager/change_price_of_peripheral.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')



@login_required(login_url='login')
def manager_change_spart_parts_prices_list(request):
    if request.user.is_superuser:
        spare_parts_list = Computer_Spare_Part.objects.all()

        spare_parts_with_their_current_prices = []
        for spare_part in spare_parts_list:

            spare_parts_with_current_price = {}
            spare_parts_with_current_price['spare_part'] = spare_part
            spare_parts_price = Computer_Spare_Part_Price.objects.filter(spare_part=spare_part, do_use=True)
            if spare_parts_price:
                spare_parts_price = spare_parts_price[0]
                spare_parts_with_current_price['price'] = spare_parts_price.price
            else:
                spare_parts_with_current_price['price'] = None
            spare_parts_with_their_current_prices.append(spare_parts_with_current_price)

        context = {
            'spare_parts_with_their_current_prices': spare_parts_with_their_current_prices,
        }

        return render(request, 'base/manager/manager_change_spare_parts_prices_list.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')



# SPARE PART PRICE CHANGING PAGE
@login_required(login_url='login')
def manager_change_price_of_spare_part(request, spare_part_id):
    if request.user.is_superuser:
        spare_part_object = Computer_Spare_Part.objects.filter(id=spare_part_id)[0]
        spare_part_price_object = Computer_Spare_Part_Price.objects.filter(spare_part=spare_part_object, do_use=True)
        
        if spare_part_price_object:
            spare_part_price_object = spare_part_price_object[0].price
        else:
            spare_part_price_object = None
        
        if request.method == "POST":
            new_spare_part_price = request.POST.get('new-spare-part-price', None)

            if new_spare_part_price is None:
                messages.error(request, 'new_spare_part_price parameter has not been sent.')
                return redirect('manager-change-price-of-spare-part')
            if new_spare_part_price.strip() == '':
                messages.error(request, 'New price of spare part should not be empty neither has only spaces.')
                return redirect('manager-change-price-of-spare-part')
            
            getcontext().prec = 4
            new_spare_part_price = Decimal(new_spare_part_price)
            old_spare_part_price_like_new = Computer_Spare_Part_Price.objects.filter(price=new_spare_part_price)
            if old_spare_part_price_like_new:
                # Price like the new one exists
                old_spare_part_price_like_new = old_spare_part_price_like_new[0]
                spare_part_price_with_do_use_true = Computer_Spare_Part_Price.objects.filter(do_use=True)
                if spare_part_price_with_do_use_true:
                    spare_part_price_with_do_use_true = Computer_Spare_Part_Price.objects.filter(do_use=True)[0]
                    spare_part_price_with_do_use_true.do_use = False
                    spare_part_price_with_do_use_true.save()
                    old_spare_part_price_like_new.do_use = True
                    old_spare_part_price_like_new.save()
                else:
                    old_spare_part_price_like_new.do_use = True
                    old_spare_part_price_like_new.save()
            else:
                # A price like the new one does nots exists
                spare_part_price_with_do_use_true = Computer_Spare_Part_Price.objects.filter(do_use=True)
                if spare_part_price_with_do_use_true:
                    spare_part_price_with_do_use_true = Computer_Spare_Part_Price.objects.filter(do_use=True)[0]
                    spare_part_price_with_do_use_true.do_use = False
                    spare_part_price_with_do_use_true.save()
                    new_spare_part_price_object = Computer_Spare_Part_Price(spare_part=spare_part_object, price=new_spare_part_price, do_use=True)
                    # fedgfegeg
                    new_spare_part_price_object.save()
                else:
                    new_spare_part_price_object = Computer_Spare_Part_Price(spare_part=spare_part_object, price=new_spare_part_price, do_use=True)
                    new_spare_part_price_object.save()
            
            messages.success(request, f'{spare_part_object.name} Price has been changed to {new_spare_part_price}')
            return redirect('manager-change-spare-parts-prices-list')

        context = {
            'spare_part': spare_part_object,
            'spare_part_current_price': spare_part_price_object,
        }
        return render(request, 'base/manager/manager_change_price_of_spare_part.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def manager_all_added_devices_list(request):
    if request.user.is_superuser:

        devices_added_by_user = Device.objects.select_related('total_spendings', 'user').all()

        # Get total spending on each device
        devices_added_by_user_brief_details = []
        for single_device in devices_added_by_user:
            device_total_spendings_dictionary = {}
            device_total_spendings_dictionary['device'] = single_device
            
            total_spendings_on_device = None
            if single_device.total_spendings is not None:
                total_spendings_on_device = single_device.total_spendings.total_spendings

            device_total_spendings_dictionary['total_spendings'] = total_spendings_on_device
            devices_added_by_user_brief_details.append(device_total_spendings_dictionary)

        
        context = {
            'devices': devices_added_by_user,
            'devices_added_by_user_brief_details': devices_added_by_user_brief_details,
        }


        return render(request, 'base/manager/manager_all_added_devices_list.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def manager_general_statistics(request):
    if request.user.is_superuser:
        # total_spendings = 0
        # spendings_objects = Total_Spendings.objects.all().order_by('added')
        # date_of_first_spendings = spendings_objects[0].added

        # for spendings in spendings_objects:
        #     total_spendings += spendings.total_spendings
        
        # num_of_inspected_devices = Device.objects.all().count()
        # num_of_refurbished_devices = Refurbished_Device.objects.all().count()
        # num_of_scrapped_devices = Scrapped_Device.objects.all().count()

        # average_spendings_per_device = total_spendings / num_of_inspected_devices
        
        
        # context= {
        #     'total_spendings': total_spendings,
        #     'date_of_first_spendings': date_of_first_spendings,
        #     'num_of_inspected_devices': num_of_inspected_devices,
        #     'num_of_refurbished_devices': num_of_refurbished_devices,
        #     'num_of_scrapped_devices': num_of_scrapped_devices,
        #     'average_spendings_per_device': average_spendings_per_device,
        # }
        context={}
        return render(request, 'base/manager/manager_general_statistics.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')

@login_required(login_url='login')
def manager_statistics_main_page(request):
    if request.user.is_superuser:
        context={}
        return render(request, 'base/manager/manager_statistics.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')

@login_required(login_url='login')
def manager_statistics_graphs(request):
    if request.user.is_superuser:
        context={}
        return render(request, 'base/manager/manager_statistics_graphs.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')

@login_required(login_url='login')
def addDevice(request):
    form = DeviceForm()
    if request.method == "POST":
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'base/junk/device_form.html')
    context = {'form': form}
    return render(request, 'base/junk/device_form.html', context)


def loginPage(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('manager')
        elif request.user.workplace.workplace == 'warehouse':
            return redirect('warehouse')
        elif request.user.workplace.workplace == 'operation_lab':
            return redirect('operation-lab')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('manager')
            elif user.workplace.workplace == 'warehouse':
                return redirect('warehouse')
            elif user.workplace.workplace == 'operation_lab':
                return redirect('operation-lab')
        else:
            messages.error(request, 'User name or password do not exist')
    context = {}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('main')

@login_required(login_url='login')
def warehouse(request):
    if request.user.workplace.workplace == 'warehouse':
        return render(request, 'base/warehouse/home_warehouse.html')
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def request_devices_refurbishments(request):
    if request.user.workplace.workplace == 'warehouse':
        categories = Category.objects.all()
        cooperate_donors = Corporate_Donor.objects.all()
        context = {
            'categories' : categories,
            'cooperate_donors': cooperate_donors,
        }

        if request.method == "POST":
            number_of_rows_of_devices_categories = 0
            for key in request.POST:
                if key.startswith("device-category-added-name-"):
                    number_of_rows_of_devices_categories += 1
            print(f'number_of_rows_of_devices_categories: {number_of_rows_of_devices_categories}')
            
            number_of_rows_of_oem_brands = 0
            for key in request.POST:
                if key.startswith("oem-brand-added-name-"):
                    number_of_rows_of_oem_brands += 1
            print(f'number_of_rows_of_oem_brands: {number_of_rows_of_oem_brands}')


            number_of_rows_of_donor_names = 0
            for key in request.POST:
                if key.startswith("donor-added-name-"):
                    number_of_rows_of_donor_names += 1
            print(f'number_of_rows_of_donor_names: {number_of_rows_of_donor_names}')

            
            number_of_rows_of_quantities = 0
            for key in request.POST:
                if key.startswith("quantity-added-"):
                    number_of_rows_of_quantities += 1
            print(f'number_of_rows_of_quantities: {number_of_rows_of_quantities}')
            
            request_main = Device_Refurbishment_Request(user=request.user, remark=request.POST['remark'])
            request_main.save()

            if number_of_rows_of_devices_categories==number_of_rows_of_oem_brands==number_of_rows_of_donor_names==number_of_rows_of_quantities:
                for singleRequest in range(1, number_of_rows_of_devices_categories+1):
                    device_category = request.POST[f'device-category-added-name-{singleRequest}']
                    category_object = Category.objects.filter(name__exact=device_category)[0]
                    oem_brand_name = request.POST[f'oem-brand-added-name-{singleRequest}']
                    oem_brand_name= oem_brand_name.casefold()
                    donor_name = request.POST[f'donor-added-name-{singleRequest}']
                    requested_quantity = request.POST[f'quantity-added-{singleRequest}']
                    if donor_name == 'Individual Person':
                        refurbishment_request_details = Device_Refurbishment_Request_Details(request=request_main, category=category_object, oem_brand=oem_brand_name, quantity=requested_quantity, corporate_donor=None, individual_donor_flag=True)
                        refurbishment_request_details.save()
                    else:
                        cooperate_donor_object = Corporate_Donor.objects.filter(name__exact=donor_name)[0]
                        refurbishment_request_details = Device_Refurbishment_Request_Details(request=request_main, category=category_object, oem_brand=oem_brand_name, quantity=requested_quantity, corporate_donor=cooperate_donor_object, individual_donor_flag=False)
                        refurbishment_request_details.save()
                        
                return redirect('request-device-refurbishment')


        return render(request, 'base/warehouse/warehouse_request_device_refurbishment.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')

# warehouse-device-refurbishment-request-details
@login_required(login_url='login')
def warehouse_device_refurbishment_request_details(request, request_id):
    if request.user.workplace.workplace == 'warehouse':
            # request_details = Device
            request_main = Device_Refurbishment_Request.objects.get(id=request_id)
            request_details = Device_Refurbishment_Request_Details.objects.filter(request_id=request_main.id)
            context = {
                'request_main': request_main,
                'request_details': request_details,
            }
            return render(request, 'base/warehouse/my_requests_device_refurbishment_request_details.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def request_peripheral_inspection(request):
    if request.user.workplace.workplace == 'warehouse':
        perihperals = Computer_Peripheral.objects.all()
        context = {
            'peripherals': perihperals
        }
        if request.method == "POST":
            numberOfRequestedPeripherals = 0
            for key in request.POST:
                if key.startswith("peripheralList"):
                    numberOfRequestedPeripherals = key[14:]
            
            peripheral_inspection_request = Inspect_Peripheral_Request(user=request.user,remark=request.POST['remark'])
            peripheral_inspection_request.save()
            getcontext().prec = 4
            for peripheralInspectionRequestNumber in range(int(numberOfRequestedPeripherals)):
                peripheral_name = request.POST[f'peripheralList{peripheralInspectionRequestNumber + 1}']
                peripheral_name_price_obj = peripheral_name.split(';')
                peripheral_object = Computer_Peripheral.objects.filter(name__exact=f'{peripheral_name_price_obj[0]}', price__exact=Decimal(peripheral_name_price_obj[1]))[0]
                
                quantity = request.POST[f'quantity{peripheralInspectionRequestNumber+1}']
                # print(f'Quantity IS: {quantity}')

                peripheral_inspection_request_details = Inspect_Peripheral_Request_Details(request=peripheral_inspection_request, peripheral=peripheral_object, number=quantity)
                peripheral_inspection_request_details.save()
            
            return redirect ('request-peripheral-inspection')
        
        # print('GET REQUEST')
        return render(request, 'base/warehouse/warehouse_request_peripheral_inspection.html', context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def request_anything(request):
    if request.user.workplace.workplace == 'warehouse':
        if request.method == 'POST':
            request = Anything_Request(user=request.user, remark=request.POST['remark'])
            request.save()
            return redirect('warehouse-request-anything')
        
        return render(request, 'base/warehouse/warehouse_request_anything.html')
    elif request.user.workplace.workplace == 'operation_lab':
        if request.method == 'POST':
            request = Anything_Request(user=request.user, remark=request.POST['remark'])
            request.save()
            return redirect('operation-lab-request-anything')

        return render(request, 'base/operation_lab/operation_lab_request_anything.html')
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def warehouse_my_requests_main(request):
    if request.user.workplace.workplace == 'warehouse':
        return render(request, 'base/warehouse/warehouse_my_requests_main.html')
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def warehouse_my_requests_device_refurbishment_requests(request):
    if request.user.workplace.workplace == 'warehouse':
        user_requests = Device_Refurbishment_Request.objects.filter(user__exact=request.user)
        
        context = {
            'user_requests': user_requests,
        }
        return render(request, 'base/warehouse/my_requests_device_refurbishment_requests_list.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def warehouse_peripherals_inspection_requests(request):
    if request.user.workplace.workplace == 'warehouse':
        user_requests = Inspect_Peripheral_Request.objects.filter(user__exact=request.user)
        
        context = {
            'user_requests': user_requests,
        }
        return render(request, 'base/warehouse/my_requests_peripheral_inspection_requests_list.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')

@login_required(login_url='login')
def warehouse_peripherals_inspection_request_details(request, request_id):
    if request.user.workplace.workplace == 'warehouse':
        request_main = Inspect_Peripheral_Request.objects.filter(id=request_id)[0]
        request_details = Inspect_Peripheral_Request_Details.objects.filter(request__id=request_main.id)
        context = {
            'request_main': request_main,
            'request_details': request_details,
        }
        return render(request, 'base/warehouse/my_requests_peripheral_inspection_request_details.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def warehouse_anything_requests_list(request):
    if request.user.workplace.workplace == 'warehouse':
        user_requests = Anything_Request.objects.filter(user__exact=request.user)
        
        context = {
            'user_requests': user_requests,
        }
        return render(request, 'base/warehouse/warehouse_my_requests_anything_requests_list.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def warehouse_anything_request_details(request, request_id):
    if request.user.workplace.workplace == 'warehouse':
        if request.method == "POST":
            request_details = Anything_Request.objects.get(id=request_id)
            request_details.status = "Canceled"
            request_details.save()
            return redirect('warehouse-anything-request-details')
    
        request_details = Anything_Request.objects.get(id=request_id)

        context = {
            "request_details": request_details,
        }
        return render(request, 'base/warehouse/warehouse_my_requests_anything_request_details.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def operation_lab(request):
    if request.user.workplace.workplace == 'operation_lab':
        devices_a = Device.objects.filter(user=request.user)
        number_of_devices_in_sunday = 0
        number_of_devices_in_monday = 0
        number_of_devices_in_tuesday = 0
        number_of_devices_in_wednesday = 0
        number_of_devices_in_thursday = 0

        for device in devices_a:
            day_name = device.added.strftime('%A')
            if day_name == 'Sunday':
                number_of_devices_in_sunday += 1
            elif day_name == 'Monday':
                number_of_devices_in_monday += 1
            elif day_name == 'Tuesday':
                number_of_devices_in_tuesday += 1
            elif day_name == 'Wednesday':
                number_of_devices_in_wednesday += 1
            elif day_name == 'Thursday':
                number_of_devices_in_thursday += 1

        refurbished_devices_per_day = [number_of_devices_in_sunday, number_of_devices_in_monday, number_of_devices_in_tuesday, number_of_devices_in_wednesday, number_of_devices_in_thursday]
        context = {
            'myDataset': refurbished_devices_per_day,
        }
        
        logged_in_username = request.user.username;
        return render(request, 'base/operation_lab/home_operation_lab.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')



@login_required(login_url='login')
def  operation_lab_add_device(request):
    if request.user.workplace.workplace == 'operation_lab':
        corporate_donors = Corporate_Donor.objects.all()
        categories = Category.objects.all()
        oem_brands = OEM_Brand.objects.all()
        processors = Processor.objects.all()
        computer_spare_parts = Computer_Spare_Part.objects.all()
        computer_peripherals = Computer_Peripheral.objects.all()
        ram_sizes = RAM_Size.objects.all()
        display_sizes = Display_Size.objects.all()
        gpus = GPU.objects.all()
        software = Software.objects.all()
        
        windows_price_object = Windows_Price.objects.filter(do_use=True)
        if windows_price_object:
            windows_price_object = Windows_Price.objects.filter(do_use=True)[0]
        else:
            pass


        computer_peripherals_with_price_if_exists = []

        for onePeripheral in computer_peripherals:
            single_peripheral = {}
            single_peripheral['name'] = onePeripheral
            price_of_peripheral = Computer_Peripheral_Price.objects.filter(do_use=True, peripheral=onePeripheral)
            if price_of_peripheral.exists():
                single_peripheral['price'] = price_of_peripheral[0]
            computer_peripherals_with_price_if_exists.append(single_peripheral)
        
        computer_spare_parts_with_price_if_exists = []

        for oneSparePart in computer_spare_parts:
            single_spare_parts = {}
            single_spare_parts['name'] = oneSparePart
            price_of_spare_part = Computer_Spare_Part_Price.objects.filter(do_use=True, spare_part=oneSparePart)
            if price_of_spare_part.exists():
                single_spare_parts['price'] = price_of_spare_part[0]
            computer_spare_parts_with_price_if_exists.append(single_spare_parts)


        software_with_prices_if_exists = []
        for one_software in software:
            single_software = {}
            single_software['name'] = one_software.name
            price_of_software = Software_Price.objects.filter(do_use=True, software=one_software)
            if price_of_software.exists():
                single_software['price'] = price_of_software[0]
            software_with_prices_if_exists.append(single_software)

        context = {
            'corporate_donors': corporate_donors,
            'categories': categories,
            'oem_brands': oem_brands,
            'processors': processors,
            'computer_peripherals': computer_peripherals_with_price_if_exists,
            'computer_spare_parts': computer_spare_parts_with_price_if_exists,
            'ram_sizes': ram_sizes,
            'display_sizes': display_sizes,
            'gpus': gpus,
            'software': software_with_prices_if_exists,
            'windows_price': windows_price_object,
        }


        if request.method == 'POST':
            barcode = request.POST.get('barcode', None)
            
            if barcode is None:
                messages.error(request, "Problem in barcode entry. Barcode parameter has not been sent")
                return redirect('operation-lab-add-device')
            else:
                if barcode.strip() == '':
                    messages.error(request, "Problem in barcode entry. Barcode should not be empty neither has only space.")
                    return redirect('operation-lab-add-device')

            barcode = barcode.strip()

            device_with_same_barcode = Device.objects.filter(barcode__exact=barcode)
            if device_with_same_barcode:
                messages.error(request, f'Duplicate barcode. A device with {barcode} already exists.')
                return redirect('operation-lab-add-device')

            serial_number = request.POST.get('serial-number', None) # THIS IS OPTIONAL
            if serial_number is None:
                # Form should submit a serial_number wethere the user wrote anything in the field or not
                messages.error(request, "Problem in serial number entry. Serial Number parameter has not been sent")
                return redirect('operation-lab-add-device')
            elif serial_number.strip() == '':
                serial_number = None
            else:
                serial_number = serial_number.strip()


            if serial_number is not None:
                device_with_same_serial_number = Device.objects.filter(serial_number__exact=serial_number)
                if device_with_same_serial_number:
                    messages.error(request, f'Duplicate serial number. A device with {serial_number} already exists.')
                    return redirect('operation-lab-add-device')

            category = request.POST.get('category', None)
            if category is None:
                messages.error(request, "Problem in category entry. Category parameter has not been sent.")
                return redirect('operation-lab-add-device')
            elif category.strip() == '':
                    messages.error(request, "Problem in category entry. Category field should not be empty.")
                    return redirect('operation-lab-add-device')


            category_object = Category.objects.filter(name__exact=category)
            if category_object:
                category_object = Category.objects.filter(name__exact=category)[0]
            else:
                messages.error(request, "Problem in category. Category does not exist in database.")
                return redirect('operation-lab-add-device')
            # print(f'category_object: {category_object}')


            oem_brand = request.POST.get('oem-brand', None)
            if oem_brand is None:
                messages.error(request, "Problem in OEM brand. OEM Brand parameter has not been sent.")
                return redirect('operation-lab-add-device')
            elif oem_brand.strip() == '':
                messages.error(request, "Problem in OEM brand. OEM Brand field should not be empty.")
                return redirect('operation-lab-add-device')

            # print(f'oem_brand: {oem_brand}')
            oem_brand_object = OEM_Brand.objects.filter(name__exact=oem_brand)
            if oem_brand_object:
                oem_brand_object = OEM_Brand.objects.filter(name__exact=oem_brand)[0]
            else:
                messages.error(request, "Problem in OEM brand. OEM Brand does not exist in database.")
                return redirect('operation-lab-add-device')
            # print(f'oem_brand_object: {oem_brand_object}')


            operating_system = request.POST.get('operating-system', None)
            if operating_system is None:
                messages.error(request, "Problem in operating system. Operating system parameter has not been sent.")
                return redirect('operation-lab-add-device')
            elif operating_system.strip() == '':
                messages.error(request, "Problem in operating system. Operating system field should not be empty.")
                return redirect('operation-lab-add-device')

            operating_system_choice = None
            if operating_system == 'Windows':
                operating_system_choice = 'windows'
            elif operating_system == 'macOS':
                operating_system_choice = 'macos'
            elif operating_system == 'Linux':
                operating_system_choice = 'linux'
            elif operating_system == 'iOS':
                operating_system_choice = 'ios'
            elif operating_system == 'Android':
                operating_system_choice = 'android'


            processor = request.POST.get('processor', None)
            processor_object = None
            if processor is None:
                messages.error(request, "Problem in processor. Processor parameter has not been sent.")
                return redirect('operation-lab-add-device')
            elif processor.strip() == '':
                pass
            else:
                processor_object = Processor.objects.filter(name__exact=processor)
                if processor_object:
                    processor_object = Processor.objects.filter(name__exact=processor)[0]
                else:
                    messages.error(request, "Problem in processor. Processor does not exist in database.")
                    return redirect('operation-lab-add-device')


            status = request.POST['status']
            status_choice = None
            status_object = None
            if status == 'Ready':
                status_object = Refurbished_Device()
                status_object.save()
                status_choice = 'refurbished'
            elif status == 'Scrap':
                status_object = Scrapped_Device()
                status_object.save()
                status_choice = 'scrapped'
            else:
                messages.error(request, "Problem in status. Status entry is not valid.")
                return redirect('operation-lab-add-device')
            

            # OPTIONAL
            ram_size = request.POST.get('ram-size', None)
            ram_size_object = None
            if ram_size is None:
                messages.error(request, "Problem in RAM size. RAM size parameter has not been sent.")
                return redirect('operation-lab-add-device')
            elif ram_size.strip() != '':
                ram_size_object = RAM_Size.objects.filter(size=int(ram_size))
                if ram_size_object:
                    pass
                else:
                    messages.error(request, "Problem in RAM size. RAM size entry does not exist in database.")
                    return redirect('operation-lab-add-device')
            
            
            display_size = request.POST.get('display-size', None)
            display_size_object = None
            if display_size is None:
                messages.error(request, "Problem in display size. Display size parameter has not been sent.")
                return redirect('operation-lab-add-device')
            elif display_size.strip() != '':
                getcontext().prec = 4
                display_size_object = Display_Size.objects.filter(size=Decimal(display_size))
                if display_size_object:
                    pass
                else:
                    messages.error(request, "Problem in display size. Display size entry does not exist in database.")
                    return redirect('operation-lab-add-device')
            
            
            gpu = request.POST.get('gpu', None)
            gpu_object = None
            if gpu is None:
                messages.error(request, "Problem in GPU. GPU parameter has not been sent.")
                return redirect('operation-lab-add-device')
            elif gpu != '':
                gpu_object = GPU.objects.filter(name__exact=gpu)
                if gpu_object:
                    pass
                else:
                    messages.error(request, "Problem in GPU. GPU entry does not exist in database.")
                    return redirect('operation-lab-add-device')


            remark = request.POST.get('remark', None)
            if remark is None:
                messages.error(request, "Problem in remark. remark parameter has not been sent.")
                return redirect('operation-lab-add-device')
            elif remark.strip() == '':
                remark = None


            donor_name = request.POST.get('donor', None)
            if donor_name is None:
                messages.error(request, "Problem in Donor. Donor parameter has not been sent.")
                return redirect('operation-lab-add-device')
            elif donor_name.strip() == '':
                messages.error(request, "Problem in Donor. Donor entry should not be empty nor has only spaces.")
                return redirect('operation-lab-add-device')
            
            
            device_object = None
            if donor_name == 'Individual Person':
                individual_donor_object = Individual_Donor()
                individual_donor_object.save()
                if status_choice == 'refurbished':
                    refurbished_device_object = Refurbished_Device()
                    refurbished_device_object.save()
                    device_object = Device(user=request.user, barcode=barcode, serial_number=serial_number, category=category_object, oem_brand=oem_brand_object, processor=processor_object,  status=status_choice, refurbished=refurbished_device_object, scrapped=None, corporate_donor=None, individual_donor_flag=True, individual_donor=individual_donor_object, ram_size=ram_size_object, display_size=display_size_object, gpu=gpu_object, remark=remark, total_spendings=None)
                    device_object.save()
                elif status_choice == 'scrapped':
                    scrapped_device_object = Scrapped_Device()
                    scrapped_device_object.save()
                    device_object = Device(user=request.user, barcode=barcode, serial_number=serial_number, category=category_object, oem_brand=oem_brand_object, processor=processor_object,  status=status_choice, refurbished=None, scrapped=scrapped_device_object, corporate_donor=None, individual_donor_flag=True, individual_donor=individual_donor_object, ram_size=ram_size_object, display_size=display_size_object, gpu=gpu_object, remark=remark, total_spendings=None)
                    device_object.save()
            else:
                corporate_donor_object = corporate_donors.filter(name__exact=donor_name)
                if corporate_donor_object:
                    corporate_donor_object = corporate_donors.filter(name__exact=donor_name)[0]
                    if status_choice == 'refurbished':
                        refurbished_device_object = Refurbished_Device()
                        refurbished_device_object.save()
                        device_object = Device(user=request.user, barcode=barcode, serial_number=serial_number, category=category_object, oem_brand=oem_brand_object, processor=processor_object, status=status_choice, refurbished=refurbished_device_object, scrapped=None, corporate_donor=corporate_donor_object, individual_donor_flag=False, individual_donor=None, ram_size=ram_size_object, display_size=display_size_object, gpu=gpu_object, remark=remark, total_spendings=None)
                        device_object.save() # CHECK FOR DUPLICATION
                    elif status_choice == 'scrapped':
                        scrapped_device_object = Scrapped_Device()
                        scrapped_device_object.save()
                        device_object = Device(user=request.user, barcode=barcode, serial_number=serial_number, category=category_object, oem_brand=oem_brand_object, processor=processor_object, status=status_choice, refurbished=None, scrapped=scrapped_device_object, corporate_donor=corporate_donor_object, individual_donor_flag=False, individual_donor=None, ram_size=ram_size_object, display_size=display_size_object, gpu=gpu_object, remark=remark, total_spendings=None)
                        device_object.save()
                else:
                    messages.error(request, f"Problem in corporate donor ({donor_name}). Corporate donor ({donor_name}) entry is either not valid or it does not exist in database.")
                    return redirect('operation-lab-add-device') 
            
            getcontext().prec = 4
            total_spendings_all = Decimal('0')

            windows_spending = Decimal('0')
            if operating_system_choice == 'windows':
                # Windows Details
                report_name = request.POST.get('report-name', None)
                if report_name is None:
                    messages.error(request, "Problem in Windows report name. Windows report name parameter has not been sent.")
                    return redirect('operation-lab-add-device') 
                elif report_name.strip() == '':
                    messages.error(request, "Problem in Windows report name.")
                    return redirect('operation-lab-add-device') 
                # print(f'report_name: {report_name}')
                
                mar_name = request.POST.get('mar-name', None)
                if mar_name is None:
                    messages.error(request, "Problem in Windows MAR name. Windows MAR name parameter has not been sent.")
                    return redirect('operation-lab-add-device') 
                elif mar_name.strip() == '':
                    messages.error(request, "Problem in Windows MAR name. Windows MAR name entry should not be empty not has onlt spaces.")
                    return redirect('operation-lab-add-device') 
                # print(f'mar_name: {mar_name}')
                
                product_installed = request.POST.get('product-installed', None)
                if product_installed is None:
                    messages.error(request, "Problem in Windows product installed. Windows product installed parameter has not been sent.")
                    return redirect('operation-lab-add-device') 
                elif product_installed.strip() == '':
                    messages.error(request, "Problem in Windows product installed. Windows product installed entry should not be empty not has onlt spaces.")
                    return redirect('operation-lab-add-device') 
                # print(f'product_installed: {product_installed}')
                
                mar_coa_sn = request.POST.get('mar-coa-sn', None)
                if mar_coa_sn is None:
                    messages.error(request, "Problem in Windows MAR COA SN. Windows MAR COA SN parameter has not been sent.")
                    return redirect('operation-lab-add-device') 
                elif mar_coa_sn.strip() == '' or mar_coa_sn is None:
                    messages.error(request, "Problem in Windows MAR COA SN. Windows MAR COA SN entry should not be empty not has onlt spaces.")
                    return redirect('operation-lab-add-device') 
                print(f'mar_coa_sn: {mar_coa_sn}')
                
                installation_date = request.POST.get('installation-date', None)
                if installation_date is None:
                    messages.error(request, "Problem in Windows installation date. Windows installation date parameter has not been sent.")
                    return redirect('operation-lab-add-device') 
                elif installation_date.strip() == '':
                    messages.error(request, "Problem in Windows installation date. Windows installation date entry should not be empty not has onlt spaces.")
                    return redirect('operation-lab-add-device') 
                
                remark_windows = request.POST.get('remark-windows', None)
                if remark_windows is None:
                    messages.error(request, "Problem in Windows remark. Windows remark parameter has not been sent.")
                    return redirect('operation-lab-add-device') 
                # if remark_windows == '' or remark_windows is None:
                #     remark_windows = None
                
                # if windows_price_object.price is None:
                #     messages.error('No price has been set to Windows!')
                #     return redirect('operation-lab-add-device')

                windows_spending += Decimal(f'{windows_price_object.price}')
                total_spendings_all += Decimal(f'{windows_price_object.price}')
                # Create Windows Object
                windows_object = Windows(device=device_object, report_name=report_name, mar_name=mar_name, name=product_installed, installation_date=installation_date, price=windows_price_object, product_key_id=mar_coa_sn, remark=remark_windows)
                windows_object.save()



            
            total_peripherals_spendings = Decimal('0')
            # Peripherals
            # check for one only
            if request.POST.get('part-added-name-1', None) is None:
                pass
            else:
                number_of_rows_of_peripherals_added = 0
                for key in request.POST:
                    if key.startswith("part-added-name-"):
                        number_of_rows_of_peripherals_added += 1
                for row_order in range(1, number_of_rows_of_peripherals_added+1):
                    peripheral_name = request.POST[f'part-added-name-{row_order}']
                    peripheral_serial_number = request.POST[f'part-added-serial-number-{row_order}']
                    peripheral_object = Computer_Peripheral.objects.filter(serial_number__exact=peripheral_serial_number)[0]
                    peripheral_quantity = request.POST[f'part-added-quantity-{row_order}']
                    peripheral_quantity = int(peripheral_quantity)
                    peripheral_cost = request.POST[f'part-added-price-{row_order}']

                    if peripheral_cost == '0.000 SAR':
                        device_pheripheral_details = Device_Peripherals_Details(device=device_object, peripheral=peripheral_object, quantity=peripheral_quantity, is_bought=False, price=None)
                        device_pheripheral_details.save()
                    else:
                        price_object = Computer_Peripheral_Price.objects.filter(peripheral=peripheral_object, do_use=True)[0]
                        total_spendings_all += Decimal(f'{peripheral_quantity}') * Decimal(f'{price_object.price}')
                        total_peripherals_spendings += Decimal(f'{peripheral_quantity}') * Decimal(f'{price_object.price}')
                        device_pheripheral_details = Device_Peripherals_Details(device=device_object, peripheral=peripheral_object, quantity=peripheral_quantity, is_bought=True, price=price_object)
                        device_pheripheral_details.save()


            total_spare_parts_spendings = Decimal('0')
            # Spare Parts
            if request.POST.get('spare-part-added-name-1', None) is None:
                pass
            else:
                number_of_rows_of_spare_parts_table = 0
                for key in request.POST:
                    if key.startswith("spare-part-added-name-"):
                        number_of_rows_of_spare_parts_table += 1
                
                for row_order in range(1, number_of_rows_of_spare_parts_table+1):
                    spare_part_name = request.POST[f'spare-part-added-name-{row_order}']
                    spare_part_serial_number = request.POST[f'spare-part-added-serial-number-{row_order}']
                    spare_part_object = Computer_Spare_Part.objects.filter(serial_number__exact=spare_part_serial_number)[0]
                    spare_part_quantity = request.POST[f'spare-part-added-quantity-{row_order}']
                    spare_part_quantity = int(spare_part_quantity)
                    spare_part_cost = request.POST[f'spare-part-added-price-{row_order}']

                    if spare_part_cost == '0.000 SAR':
                        device_spare_part_details = Device_Spare_Parts_Details(device=device_object, spare_part=spare_part_object, quantity=spare_part_quantity, is_bought=False, price=None)
                        device_spare_part_details.save()
                    else:
                        spare_part_price_object = Computer_Spare_Part_Price.objects.filter(spare_part=spare_part_object, do_use=True)[0]
                        total_spendings_all += Decimal(f'{spare_part_quantity}') * Decimal(f'{spare_part_price_object.price}')
                        total_spare_parts_spendings += Decimal(f'{spare_part_quantity}') * Decimal(f'{spare_part_price_object.price}')
                        # print(f'total_spare_parts_spendings: {total_spare_parts_spendings}')
                        # print(type(total_spare_parts_spendings))
                        device_spare_part_details = Device_Spare_Parts_Details(device=device_object, spare_part=spare_part_object, quantity=spare_part_quantity, is_bought=True, price=spare_part_price_object)
                        device_spare_part_details.save()
            
            total_software_spendings = Decimal('0')
            # Software
            if request.POST.get('software-added-name-1', None) is None:
                pass
            else:
                number_of_rows_of_software_table = 0
                for key in request.POST:
                    if key.startswith("software-added-name-"):
                        number_of_rows_of_software_table += 1
                
                for row_order in range(1, number_of_rows_of_software_table+1):
                    software_name = request.POST[f'software-added-name-{row_order}']
                    software_object = Software.objects.filter(name__exact=software_name)[0]
                    software_cost = request.POST[f'software-added-price-{row_order}']

                    if software_cost == '0.000 SAR':
                        device_software_details = Device_Software_Details(device=device_object, software=software_object, is_bought=False, price=None)
                        device_software_details.save()
                    else:
                        software_price_object = Software_Price.objects.filter(software=software_object, do_use=True)[0]
                        total_spendings_all += Decimal(f'{software_price_object.price}')
                        total_software_spendings += Decimal(f'{software_price_object.price}')
                        device_software_details = Device_Software_Details(device=device_object, software=software_object, is_bought=True, price=software_price_object)
                        device_software_details.save()

            
            total_spendings_all = Decimal(total_spendings_all)
            total_peripherals_spendings = Decimal(total_peripherals_spendings)
            total_spare_parts_spendings = Decimal(total_spare_parts_spendings)
            total_software_spendings = Decimal(total_software_spendings)
            windows_spending_copy = Decimal(windows_spending)

            print(f'total_spendings_allaaa: {total_spendings_all}', end='')
            print(f'total_peripherals_spendings: {total_peripherals_spendings}', end='')
            print(f'total_spare_parts_spendings: {total_spare_parts_spendings}', end='')
            print(f'total_software_spendings: {total_software_spendings}', end='')
            print(f'windows_spending_copy: {windows_spending_copy}', end='')

            total_spendings_object = Total_Spendings(total_spendings=total_spendings_all, peripherals_total_spendings=total_peripherals_spendings, spare_parts_total_spendings=total_spare_parts_spendings, software_total_spendings=total_software_spendings, windows_spending=windows_spending_copy)
            
            total_spendings_object.save()
            device_object.total_spendings = total_spendings_object
            device_object.save()

            messages.success(request, f'Device with barcode {barcode} has been successfully added')
            return redirect('operation-lab-add-device')
        
        return render(request, 'base/operation_lab/operation_lab_add_device.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def operation_lab_request_spare_part_peripheral_device(request):
    if request.user.workplace.workplace == 'operation_lab':
        spare_parts = Computer_Spare_Part.objects.all()
        peripherals = Computer_Peripheral.objects.all()
        device_categories = Category.objects.all()

        context = {
            'spare_parts' : spare_parts,
            'peripherals' : peripherals,
            'device_categories' : device_categories,
        }
        if request.method == 'POST':

            number_of_rows_of_spare_parts_table = 0
            for key in request.POST:
                if key.startswith("spare-part-added-name-"):
                    number_of_rows_of_spare_parts_table += 1

            number_of_rows_of_peripherals_table = 0
            for key in request.POST:
                if key.startswith("peripheral-added-name-"):
                    number_of_rows_of_peripherals_table += 1
            
            number_of_rows_of_devices_table = 0
            for key in request.POST:
                if key.startswith("device-category-added-name-"):
                    number_of_rows_of_devices_table += 1
            

            request_main = Spare_Part_Peripheral_Device_Request(user=request.user, remark=request.POST['remark'])
            request_main.save()

            # Create Spare Parts Requets objects
            if number_of_rows_of_spare_parts_table != 0:
                request_main.spare_part_flag = True
                request_main.save()

                for spare_part_number in range(1, number_of_rows_of_spare_parts_table+1):
                    spare_part_serial_number = request.POST[f'spare-part-added-serial-number-{spare_part_number}']
                    spare_part_object = Computer_Spare_Part.objects.filter(serial_number__exact=spare_part_serial_number)[0]
                    spare_part_request = Spare_Part_Request(request=request_main, spare_part=spare_part_object, quantity=request.POST[f'spare-part-added-quantity-{spare_part_number}'])
                    spare_part_request.save()
            
            if number_of_rows_of_peripherals_table != 0:
                request_main.peripheral_flag = True
                request_main.save()

                for peripheral_number in range(1, number_of_rows_of_peripherals_table+1):
                    peripheral_serial_number = request.POST[f'peripheral-added-serial-number-{peripheral_number}']
                    peripheral_object = Computer_Peripheral.objects.filter(serial_number__exact=peripheral_serial_number)[0]
                    peripheral_request = Peripheral_Request(request=request_main, peripheral=peripheral_object, quantity=request.POST[f'peripheral-added-quantity-{peripheral_number}'])
                    peripheral_request.save()
            
            if number_of_rows_of_devices_table != 0:
                request_main.device_flag = True
                request_main.save()

                for device_number in range(1,number_of_rows_of_devices_table+1):
                    device_category = request.POST[f'device-category-added-name-{device_number}']
                    category_object = Category.objects.filter(name__exact=device_category)[0]
                    oem_brand = request.POST[f'device-category-added-oem-brand-{device_number}'].casefold()
                    device_request = Device_Request(request=request_main, category=category_object, oem_brand=oem_brand, quantity=request.POST[f'device-category-added-quantity-{device_number}'])
                    device_request.save()


            return redirect('request-spare-parts-peripherals-devices')

        return render(request, 'base/operation_lab/operation_lab_request_spare_parts_peripherals_devices.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def operation_lab_my_requests_main(request):
    if request.user.workplace.workplace == 'operation_lab':
        return render(request, 'base/operation_lab/my_requests_main.html')
    else:
        return HttpResponseBadRequest('Not Allowed')



@login_required(login_url='login')
def operation_lab_my_requets_spare_parts_peripherals_devices_request(request):
    if request.user.workplace.workplace == 'operation_lab':

        user_requests = Spare_Part_Peripheral_Device_Request.objects.filter(user__exact=request.user)
        
        context = {
            'user_requests': user_requests,
        }

        return render(request, 'base/operation_lab/my_requests_main_spare_parts_peripherals_devices_requests.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


# HTTP request object name has been changes due to conflict with a field name
@login_required(login_url='login')
def operation_lab_sp_p_d_request_details(request, request_id):
    if request.user.workplace.workplace == 'operation_lab':
        if request.method == "POST":
            request_details = Spare_Part_Peripheral_Device_Request.objects.get(id=request_id)
            request_details.status = "Canceled"
            request_details.save()

            return redirect('operation-lab-sp-p-d-request-details', request_id)

        request_details = Spare_Part_Peripheral_Device_Request.objects.get(id=request_id)

        spare_parts_requests = None
        if request_details.spare_part_flag:
            spare_parts_requests = Spare_Part_Request.objects.select_related('spare_part').filter(request__id=request_details.id)

        peripherals_requests = None
        if request_details.peripheral_flag:
            peripherals_requests = Peripheral_Request.objects.select_related('peripheral').filter(request__id=request_details.id)
        
        devices_requests = None
        if request_details.device_flag:
            devices_requests = Device_Request.objects.select_related('category').filter(request__id=request_details.id)

        context = {
            "request_details": request_details,
            "spare_parts_requests": spare_parts_requests,
            "peripherals_requests": peripherals_requests,
            "devices_requests": devices_requests,
        }

        return render(request,'base/operation_lab/spare_parts_peripherals_devices_request_details.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def operation_lab_anything_requests(request):
    if request.user.workplace.workplace == 'operation_lab':

        user_requests = Anything_Request.objects.filter(user__exact=request.user)

        context = {
            'user_requests': user_requests,
        }
        return render(request, 'base/operation_lab/my_requests_main_anything_requests.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def operation_lab_anything_requests_details(request, request_id):
    if request.user.workplace.workplace == 'operation_lab':
        if request.method == "POST":
            request_details = Anything_Request.objects.get(id=request_id)
            request_details.status = "Canceled"
            request_details.save()

            return redirect('opeation-lab-anything-request-details')
    
        request_details = Anything_Request.objects.get(id=request_id)

        context = {
            "request_details": request_details,
        }
        return render(request, 'base/operation_lab/anything_requests_details.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def operation_lab_devices_added_by_user_list(request):
    if request.user.workplace.workplace == 'operation_lab':
        devices_added_by_user = Device.objects.select_related('total_spendings').filter(user=request.user)

        # Get total spending on each device
        devices_added_by_user_brief_details = []
        for single_device in devices_added_by_user:
            device_total_spendings_dictionary = {}
            device_total_spendings_dictionary['device'] = single_device
            
            total_spendings_on_device = None
            if single_device.total_spendings is not None:
                total_spendings_on_device = single_device.total_spendings.total_spendings

            device_total_spendings_dictionary['total_spendings'] = total_spendings_on_device
            devices_added_by_user_brief_details.append(device_total_spendings_dictionary)
        
        context = {
            'devices': devices_added_by_user,
            'devices_added_by_user_brief_details': devices_added_by_user_brief_details,
        }
        return render(request, 'base/operation_lab/operation_lab_devices_added_by_user_list.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')


@login_required(login_url='login')
def operation_lab_device_added_by_user_details(request, device_id):
    if request.user.workplace.workplace == 'operation_lab':
        device_object = Device.objects.filter(user=request.user, id=device_id)[0]
        installed_windows_details_object = Windows.objects.filter(device=device_object)
        windows_price = None
        if installed_windows_details_object:
            installed_windows_details_object = installed_windows_details_object[0]
            windows_price = installed_windows_details_object.price.price
        else:
            installed_windows_details_object = None

        peripherals_with_device = Device_Peripherals_Details.objects.select_related('peripheral', 'price').filter(device=device_object)
        
        peripherals_total_spendings_on_device = 0
        device_with_peripheral_total_spending = []
        for peripheral_related_details in peripherals_with_device:
            peripheral_and_total_spending = {}
            peripheral_and_total_spending['peripheral_details_obj'] = peripheral_related_details
            if peripheral_related_details.is_bought:
                peripheral_and_total_spending['total_spending'] = peripheral_related_details.price.price * peripheral_related_details.quantity
                peripherals_total_spendings_on_device += peripheral_related_details.price.price * peripheral_related_details.quantity

            else:
                peripheral_and_total_spending['total_spending'] = 0
            device_with_peripheral_total_spending.append(peripheral_and_total_spending)
        

        # Spare Parts
        spare_parts_with_device = Device_Spare_Parts_Details.objects.select_related('spare_part', 'price').filter(device=device_object)
        spare_parts_total_spendings_on_device = 0
        spare_parts_with_total_spending = []
        for spare_part_related_details in spare_parts_with_device:
            spare_part_spending = {}
            spare_part_spending['spare_part_details_obj'] = spare_part_related_details
            if spare_part_related_details.is_bought:
                spare_part_spending['total_spending'] = spare_part_related_details.price.price * spare_part_related_details.quantity
                spare_parts_total_spendings_on_device += spare_part_related_details.price.price * spare_part_related_details.quantity
            else:
                spare_part_spending['total_spending'] = 0
            spare_parts_with_total_spending.append(spare_part_spending)
        

        # Software
        software_installed_in_device = Device_Software_Details.objects.select_related('software', 'price').filter(device=device_object)
        software_total_spendings_on_device = 0
        software_with_total_spending = []
        for single_software in software_installed_in_device:
            software_and_spending = {}
            software_and_spending['software_details_obj'] = single_software
            if single_software.is_bought:
                software_and_spending['spending'] = single_software.price.price
                software_total_spendings_on_device += single_software.price.price
            else:
                software_and_spending['spending'] = 0
            software_with_total_spending.append(software_and_spending)
        

        total_spendings_on_device = peripherals_total_spendings_on_device + spare_parts_total_spendings_on_device + software_total_spendings_on_device


        if windows_price:
            peripherals_total_spendings_on_device += windows_price

        context = {
            'device_details': device_object,
            'installed_windows_details': installed_windows_details_object,
            'peripheral_with_device': peripherals_with_device,
            'windows_price': windows_price,
            'device_with_peripheral_total_spending': device_with_peripheral_total_spending,
            'peripherals_total_spendings_on_device': peripherals_total_spendings_on_device,
            'spare_parts_with_total_spending': spare_parts_with_total_spending,
            'software_with_total_spending': software_with_total_spending,
            'total_spendings_on_device': total_spendings_on_device,
        }

        return render(request, 'base/operation_lab/device_added_by_user_details.html', context=context)
    else:
        return HttpResponseBadRequest('Not Allowed')