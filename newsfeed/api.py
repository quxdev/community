from .models import Newsitem, Vote, Comment
from . serializers import NewsitemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

PAGINATION_LIMIT = 10


class HomePageView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        output_status = False
        output_detail = "Failed"
        res_status = status.HTTP_400_BAD_REQUEST
        output_data = {}
        end = False

        qs = Newsitem.objects.all()
        if qs.exists():
            page = request.GET.get('page', 1)
            try:
                page = int(page)
            except Exception as e:
                page = 1
            qs_out = qs[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]
            if qs[PAGINATION_LIMIT * (page):PAGINATION_LIMIT * page].count() ==0:
                end = True

            output_data = NewsitemSerializer(qs_out, many=True).data
            output_status = True
            output_detail = "Success"
            res_status = status.HTTP_200_OK
        else:
            output_detail = "No data found"
        context ={
            "status": output_status,
            "detail": output_detail,
            "data": output_data,
            "end": end
        }
        return Response(context, status=res_status, content_type="application/json")


class NewsItemView(APIView):

    def get(self, request, *args, **kwargs):
        output_status = False
        output_detail = "Failed"
        res_status = status.HTTP_400_BAD_REQUEST
        output_data = {}
        id = request.GET.get('id', None)
        if id is not None and str(id).isdigit():
            try:
                item = Newsitem.objects.get(pk=int(id))
                output_data = NewsitemSerializer(item).data
                output_status = True
                output_detail = "Success"
                res_status = status.HTTP_200_OK
            except Exception as e:
                output_detail = "No data found"
        else:
            output_detail = "No id provided"
        context ={
            "status": output_status,
            "detail": output_detail,
            "data": output_data,
        }
        return Response(context, status=res_status, content_type="application/json")

    def post(self, request, *args, **kwargs):
        output_status = False
        output_detail = "Failed"
        res_status = status.HTTP_400_BAD_REQUEST
        output_data = {}
        if request.data.get('url', None) is not None:
            try:
                data_dict = {
                    "url": request.data.get('url', None),
                }
                if request.user.is_authenticated:
                    data_dict["creator"] = request.user
                Newsitem.objects.create(**data_dict)
                output_status = True
                output_detail = "Success"
            except Exception as e:
                output_detail = "No data found"
        else:
            output_detail = "No url provided"
        context ={
            "status": output_status,
            "detail": output_detail,
            "data": output_data,
        }
        return Response(context, status=res_status, content_type="application/json")

    def delete(self, request, *args, **kwargs):
        output_status = False
        output_detail = "Failed"
        res_status = status.HTTP_400_BAD_REQUEST

        id = request.GET.get('id', None)
        if id is not None and str(id).isdigit():
            try:
                item = Newsitem.objects.get(pk=int(id), creator = request.user)
                item.delete()
                output_status = True
                output_detail = "Success"
                res_status = status.HTTP_200_OK
            except Exception as e:
                output_detail = "No data found"
        else:
            output_detail = "No id provided"
        context ={
            "status": output_status,
            "detail": output_detail,
        }
        return Response(context, status=res_status, content_type="application/json")




    
    