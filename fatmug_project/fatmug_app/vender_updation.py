from fatmug_app.models import Vendor
from fatmug_app.serializers import VendorSerializer


class UpdateVender():
    def update_profile(self, json_data, vendor_id):
        """
        Update vendor's fields in table.

        Args:
            json_data (dict): json_data as a dict of profile data to be updated.
            id(int) : id as an int of profile to be updated.

        Returns:
            groups: return data and status if function will run properly.

        """
        updated_name = json_data.get('name')
        updated_address = json_data.get('address')
        updated_contact_details = json_data.get('contact_details')
        on_time_delivery_rate = json_data.get('on_time_delivery_rate')
        quality_rating_avg = json_data.get('quality_rating_avg')
        average_response_time = json_data.get('average_response_time')
        fulfillment_rate = json_data.get('fulfillment_rate')


        # check if record exists with requested vendor id(code).
        table_vendor_id_record = list(
            Vendor.objects.filter(vendor_code=vendor_id).values())
        if len(table_vendor_id_record) < 1:
            return 'There is no record with this vendor id', 422

        # restrict to add duplicate group name.
        exclude_obj = Vendor.objects.exclude(vendor_code=vendor_id)
        duplicate_records = list(exclude_obj.filter(
            contact_details=updated_contact_details).values())
        if len(duplicate_records) > 0:
            return 'You cannot update with duplicate contact details', 422

        # update profile_name of correct vendor_id.
        table_vendor_row_obj = Vendor.objects.get(vendor_code=vendor_id)
        if updated_name:
            table_vendor_row_obj.name = updated_name
        if updated_address:
            table_vendor_row_obj.address = updated_address
        if updated_contact_details:
            table_vendor_row_obj.contact_details = updated_contact_details
        if on_time_delivery_rate:
            table_vendor_row_obj.on_time_delivery_rate = on_time_delivery_rate
        if quality_rating_avg:
            table_vendor_row_obj.quality_rating_avg = quality_rating_avg
        if average_response_time:
            table_vendor_row_obj.average_response_time = average_response_time
        if fulfillment_rate:
            table_vendor_row_obj.fulfillment_rate = fulfillment_rate

        table_vendor_row_obj.save()

        serializer = VendorSerializer(
            table_vendor_row_obj, many=False)
        return serializer.data, 200

    def get_single_vendor(self, vendor_id):
        """
        Get single vendor's fields in table.

        Args:
            id : id(vendor_code) of a vendor to get its data.

        Returns:
            groups: return data and status if function will run properly.

        """

        # check if vendor id exists or not.
        table_vendor_id_record = list(
            Vendor.objects.filter(vendor_code=vendor_id).values())
        if len(table_vendor_id_record) < 1:
            return 'There is no record with this vendor id', 422

        table_vendor_row_obj = Vendor.objects.get(vendor_code=vendor_id)
        serializer = VendorSerializer(
            table_vendor_row_obj, many=False)
        return serializer.data, 200

    def delete_vendor(self, vendor_id):
        """
        Delete vendor's fields in table and its connected data in other tables.

        Args:
            id : id(vendor_code) of a vendor to get its data.

        Returns:
            groups: return data and status if function will run properly.

        """
        table_vendor_id_record = list(
            Vendor.objects.filter(vendor_code=vendor_id).values())

        if len(table_vendor_id_record) < 1:
            return 'There is no record with this vendor id', 422

        Vendor.objects.filter(vendor_code=vendor_id).delete()
        return "vendor deleted successfully", 200