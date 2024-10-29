from rest_framework.serializers import ModelSerializer
from base.models import User, Device

class User_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ['barcode', 'serial_number', 'status', 'oem_brand', 'individual_donor_flag', 'category']