from rest_framework import serializers
from fatmug_app.models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

# class PropertyCalendarSerializer(serializers.ModelSerializer):
#     listing_details = serializers.SerializerMethodField()

#     def get_listing_details(self, obj):
#         listing_obj = Propertylisting.objects.filter(id=obj.listing_id)
#         return ListingFieldSerializer(listing_obj, many=True).data[0]

#     class Meta:
#         model = Propertycalendar
#         fields = ('id', 'listing_id', 'date', 'calendar_id',
#                   'minimum_stay', 'maximum_stay', 'avb_units', 'is_available', 'is_processed',
#                   'customized_price', 'override_price', 'status', 'min_price', 'max_price', 'seasonal_per', 'occupancy_per',
#                   'calendar_price', 'created_at', 'updated_at', 'listing_details')

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'

