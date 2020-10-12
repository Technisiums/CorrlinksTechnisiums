from .models import Account, VPS, APIKey, Customer, SMSCustomer, CorrlinksToSMS, SMSToCorrlinks
from .serializers import AccountSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json


class GetAccounts(APIView):

    def post(self, request, format=None):
        try:
            apikey = request.data['apikey']
            objs = APIKey.objects.get(API_Key=apikey)
        except Exception as e:
            return Response(data={'error': 'API Key is not valid ' + str(e)})
        try:
            vps = request.data['vps']
            vps = VPS.objects.get(VPS_Name=vps)
        except Exception as e:
            return Response(data={'error': 'VPS is not found ' + str(e)})
        queryset = Account.objects.filter(VPS=vps.id)
        serializer = AccountSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostCorrlinksToSMS(APIView):

    def post(self, request):
        try:
            corrid = request.data['_from']
            inmate = Customer.objects.get(corrlinks_ID=corrid)
        except Exception as e:
            return Response(data={'error': 'Corrlink ID is not valid ' + str(e)})
        try:
            relative = request.data['to']
            relative = SMSCustomer.objects.get(corrlinks_Customer=inmate.id, name=relative)
        except SMSCustomer.DoesNotExist:
            smsc = SMSCustomer(corrlinks_Customer=inmate, name=relative, phone_Number=relative)
            smsc.save()
            relative = smsc
            # return Response(data={'error': 'name ID is not valid ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            body = request.data['body']
        except Exception as e:
            return Response(data={'error': 'Body is Required ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sms = CorrlinksToSMS(_from=inmate, to=relative, body=body)
            sms.save()
            resp = validate_number_and_send(relative.phone_Number, inmate.allow_International_messages, body)
            # set status according to condition
            return Response(data={'info': 'all is well'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def validate_number_and_send(phone, inter, body):
    flag = False
    if len(phone) == 10:
        phone = '+1' + phone
        flag = True
    elif phone[0:2] == '+1':
        phone = phone
        flag = True
    elif phone[0] == '1':
        phone = '+' + phone
        flag = True
    if flag:
        print('send msg inside', phone)
        return send_message(phone, body)
    elif inter:
        if phone[0] != '+':
            phone = '+' + phone
        print('send msg outside', phone)
        return send_message(phone, body)
    else:
        return "you can't send message"


def send_message(phone_number, body):
    return ''


class ListenFormBandwith(APIView):
    def post(self):
        return Response(status=status.HTTP_202_ACCEPTED)


class SMSToCorrlinksView(APIView):
    def post(self, request):
        try:
            apikey = request.data['apikey']
            objs = APIKey.objects.get(API_Key=apikey)
        except Exception as e:
            return Response(data={'error': 'API Key is not valid ' + str(e)})
        try:
            vps1 = request.data['vps']
        except Exception as e:
            return Response(data={'error': 'VPS is not found' + str(e)})
        try:
            objects = SMSToCorrlinks.objects.filter(status='new')
            data = dict()
            flag = False
            for obj in objects:
                id = str(obj.id)
                to = str(obj._from.corrlinks_Customer.corrlinks_ID)
                _from = obj._from.name
                body = obj.body
                acc = obj._from.corrlinks_Customer.corrlinks_Account.email
                vps = obj._from.corrlinks_Customer.corrlinks_Account.VPS.VPS_Name
                if vps == vps1:
                    flag = True
                    b = {'id': id, 'to': to, 'from': _from, 'body': body, 'acc': acc}
                    try:
                        data[to].append(b)
                    except:
                        data[to] = [b]
            if flag:
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class setSMStoCorrlinksStatus(APIView):
    def post(self, request):
        try:
            apikey = request.data['apikey']
            objs = APIKey.objects.get(API_Key=apikey)
        except Exception as e:
            return Response(data={'error': 'API Key is not valid ' + str(e)})
        try:
            infos = json.loads(request.data['data'])
            for info in infos:
                print(info)
                try:
                    obj = SMSToCorrlinks.objects.get(id=int(info['id']))
                    obj.status = info['status']
                    obj.save()
                except Exception as e:
                    # print(e)
                    pass
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


d = {'sis': '18789141', 'mother': '19412803'}


class addPhoneBook(APIView):
    def post(self, request):
        try:
            apikey = request.data['apikey']
            objs = APIKey.objects.get(API_Key=apikey)
        except Exception as e:
            return Response(data={'error': 'API Key is not valid ' + str(e)})
        try:
            corrid = request.data['_from']
            inmate = Customer.objects.get(corrlinks_ID=corrid)
        except Exception as e:
            return Response(data={'error': 'Corrlink ID is not valid ' + str(e)})
        try:
            body = request.data['body']
        except Exception as e:
            return Response(data={'error': 'Body is Required ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            books = json.loads(body)
            for name, phone in books.items():
                smsc = SMSCustomer(corrlinks_Customer=inmate, name=name, phone_Number=phone)
                smsc.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
