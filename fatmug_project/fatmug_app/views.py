from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from fatmug_app.models import Vendor, PurchaseOrder, HistoricalPerformance
from fatmug_app.response import Responsehandler
from fatmug_app.serializers import VendorSerializer
from fatmug_app.pagination import Pagination
from fatmug_app.vender_updation import UpdateVender
from logger_setup import logger
from django.db.models import Q
import math


response_handler = Responsehandler()

@api_view(['POST', 'GET'])
def create_and_get_vendor(request):
    """
        For 'POST' request-> create a new vendor.
        For 'GET' request-> return records of all vendors.
    """
    try:
        if request.method == 'POST':
            json_data = request.data
            name = json_data.get('name')
            contact_details = json_data.get('contact_details')
            address = json_data.get('address')
            vendor_code = json_data.get('vendor_code')

            if (name == '' and name == None) or (contact_details == '' and contact_details == None) or (address == '' and address == None) or (vendor_code == '' and vendor_code == None):
                response_dict = response_handler.msg_response(
                    f'name, contact_details, address, vendor_code fields are required.', 422)
                return Response(response_dict, status.HTTP_422_UNPROCESSABLE_ENTITY)

            vender_obj = Vendor.objects.filter(Q(vendor_code=vendor_code) | Q(contact_details=contact_details))
            if len(vender_obj) >= 1:
                response_dict = response_handler.msg_response(
                    f'Either vendor code or contact details already exists. It should be unique.', 422)
                return Response(response_dict, status.HTTP_422_UNPROCESSABLE_ENTITY)

            vendor = Vendor(
                        name=name, contact_details=contact_details, address=address,
                        vendor_code=vendor_code)
            vendor.save()

            new_vendor_obj = Vendor.objects.filter(vendor_code=vendor_code)[0]
            serializer = VendorSerializer(new_vendor_obj, many=False)
            response_dict = response_handler.success_response(
                serializer.data, 200)
            return Response(response_dict, status.HTTP_200_OK)


        elif request.method == 'GET':
            json_data = request.data
            current_page = json_data.get('page')
            filters = json_data.get('filters')
            limit = json_data.get('limit', 10)
            sort = json_data.get('sort')
            vendor_data = Vendor.objects.all()

            # fitering.
            if filters is not None and filters != {}:
                name_filter = filters.get('name')
                vendor_data = Vendor.objects.filter(
                    name__icontains=name_filter)

            # get total records after filtering.
            total_records = len(vendor_data)

            # sorting
            pagination_obj = Pagination()
            if sort is not None:
                vendor_data = pagination_obj.listing_sorting(
                    sort, vendor_data)

            # pagination.
            vendor_data, page_number = pagination_obj.listing_pagnation(
                vendor_data, limit, current_page)

            serializer_data = VendorSerializer(
                vendor_data, many=True)

            response_dict = response_handler.success_response(
                serializer_data.data, 200)
            response_dict["response_meta"] = {
                "pagination": {
                    "total": total_records,
                    "current_page": page_number,
                    "total_pages": math.ceil(total_records/limit),
                }
            }

            return Response(response_dict, status.HTTP_200_OK)

    except Exception as e:
        logger.exception(
            f"error in function create_and_get_vendor")
        exception_dict = {"message": str(e), "status": 500}
        return Response(exception_dict, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT', 'GET', 'DELETE'])
def update_and_get_single_vendor(request, vendor_id):
    try:
        """
        For 'PUT' request-> update the vendor.
        For 'GET' request-> return record of single vendors.

        Update and get single vendor.

        Args:
            request (object): request data including id of the vendor.

        Returns:
            response: response object as a dict if function will run properly.
            status: status code 200 if function will run properly else 422.


        """
        update_vendor_obj = UpdateVender()
        json_data = request.data
        if request.method == 'PUT':
            response, returned_status = update_vendor_obj.update_profile(
                json_data, vendor_id)
            response_dict = response_handler.success_response(
                response, returned_status)

            if returned_status == 200:
                return Response(response_dict, status.HTTP_200_OK)
            if returned_status == 422:
                return Response(response_dict, status.HTTP_422_UNPROCESSABLE_ENTITY)

        elif request.method == 'GET':
            response, returned_status = update_vendor_obj.get_single_vendor(vendor_id)

            response_dict = response_handler.success_response(
                response, returned_status)

            if returned_status == 200:
                return Response(response_dict, status.HTTP_200_OK)
            if returned_status == 422:
                return Response(response_dict, status.HTTP_422_UNPROCESSABLE_ENTITY)

        elif request.method == 'DELETE':
            response, returned_status = update_vendor_obj.delete_vendor(vendor_id)



    except Exception as e:
        logger.exception(
            f"error in function update_and_get_single_vendor")
        exception_dict = {"message": str(e), "status": 500}
        return Response(exception_dict, status.HTTP_500_INTERNAL_SERVER_ERROR)


