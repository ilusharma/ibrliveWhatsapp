import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import *
import requests
# Create your views here.



mytoken = 'EAAEZCFOgtTMQBAMt8t2ZC31kQNPRwUnBi0TigtoNxxdlibSW698ds1QiEmH3ti02clMZB0wRHOu4w8Vo0aWZAzkCXkZCtmE0gEAOY4BP2tWdHJ4ThZBgZA3s9OiIbJCAxONyQb1spvtNaSjruFKZCPcr8ZAVNkNnIWazzf6CPzZCpuaw0tmilWge0wtVXkfdHA8UBInyKBB6nupAZDZD'


class WhatsApp(object):
    def __init__(self, phone_number_id):
        self.token = mytoken
        self.url = f"https://graph.facebook.com/v14.0/{phone_number_id}/messages"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token),
        }

    def send_message(
            self, message, recipient_id, recipient_type="individual", preview_url=True
    ):

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient_id,
            "type": "text",
            "text": {"preview_url": preview_url, "body": message},
        }
        r = requests.post(f"{self.url}", headers=self.headers, json=data)


        return r.json()
    def send_contact(self, recipient_id, components):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "contacts",
            "contacts": components,
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()


    def send_template(self, template, recipient_id, lang="en_US"):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {"name": template, "language": {"code": lang}},
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_templatev2(self, template, recipient_id, components, lang="en_US"):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {"name": template, "language": {"code": lang}, "components": components},
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_location(self, lat, long, name, address, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "location",
            "location": {
                "latitude": lat,
                "longitude": long,
                "name": name,
                "address": address,
            },
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_image(
            self,
            image,
            recipient_id,
            recipient_type="individual",
            caption=None,
            link=True,
    ):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"link": image, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"id": image, "caption": caption},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_audio(self, audio, recipient_id, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "audio",
                "audio": {"link": audio},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "audio",
                "audio": {"id": audio},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_video(self, video, recipient_id, caption=None, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "video",
                "video": {"link": video, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "video",
                "video": {"id": video, "caption": caption},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_document(self, document, recipient_id, caption=None, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "document",
                "document": {"link": document, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "document",
                "document": {"id": document, "caption": caption},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def create_button(self, button):
        return {
            "type": "list",
            "header": {"type": "text", "text": button.get("header")},
            "body": {"text": button.get("body")},
            "footer": {"text": button.get("footer")},
            "action": button.get("action"),
        }

    def send_button(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_button(button),
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_reply_button(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": button,
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def preprocess(self, data):
        return data["entry"][0]["changes"][0]["value"]

    def get_bussiness_id(self,data):
        return data["entry"][0]["id"]

    def get_mobile(self, data):
        data = self.preprocess(data)
        if "contacts" in data:
            return data["contacts"][0]["wa_id"]

    def get_name(self, data):
        contact = self.preprocess(data)
        if contact:
            return contact["contacts"][0]["profile"]["name"]

    def get_message(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["text"]["body"]

    def get_message_id(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["id"]

    def get_message_timestamp(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["timestamp"]

    def get_interactive_response(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["interactive"]["list_reply"]



    def get_message_type(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["type"]

    def get_delivery(self, data):
        data = self.preprocess(data)
        if "statuses" in data:
            return data["statuses"][0]["status"]

    def get_send_msg_id(self, data):
        data = self.preprocess(data)
        if "statuses" in data:
            return data["statuses"][0]["id"]

    def get_send_msg_timestamp(self, data):
        data = self.preprocess(data)
        if "statuses" in data:
            return data["statuses"][0]["timestamp"]

    def get_message_report(self, data):
        data = self.preprocess(data)
        if "statuses" in data:
            return "sent"
        else:
            return "recived"

    def changed_field(self, data):
        return data["entry"][0]["changes"][0]["field"]

messenger = WhatsApp(phone_number_id='108494018626228')


VERIFY_TOKEN = "30cca545-3838-48b2-80a7-9e43b1ae8ce4"



@csrf_exempt
@require_http_methods(["GET", "POST"])
def whatsapp_hook_receiver_view(request):
        if request.method == "GET":
            if request.GET["hub.verify_token"] == VERIFY_TOKEN:
                response = HttpResponse(request.GET["hub.challenge"], 200)
                response.mimetype = "text/plain"
                return response
            return "Invalid verification token"

        data = json.loads(request.body)
        print(data)
        changed_field = messenger.changed_field(data)
        if changed_field == "messages":
            new_message = messenger.get_mobile(data)
            if new_message:
                mobile = messenger.get_mobile(data)
                message_type = messenger.get_message_type(data)
                name = messenger.get_name(data)
                messenger.send_message(recipient_id=mobile,
                                       message=f"Hello {name}! Sorry currently we not accepted message here pls connect with us on our website or contact us on below number")

                messenger.send_contact(recipient_id=mobile,
                                       components=[
                                           {

                                               "emails": [
                                                   {
                                                       "email": "contact@ibrlive.com",
                                                       "type": "WORK"
                                                   },

                                               ],
                                               "name": {
                                                   "first_name": "IBRLive",
                                                   "formatted_name": "IBRLive",

                                               },
                                               "org": {
                                                   "company": "IBRLive",
                                                   "title": "CEO"
                                               },
                                               "phones": [

                                                   {
                                                       "phone": "+919813097272",
                                                       "type": "WORK",
                                                       "wa_id": "919813097272"
                                                   }
                                               ],

                                           }
                                       ]
                                       )

                if message_type == "text":
                    message = messenger.get_message(data)
                    name = messenger.get_name(data)
                    message_id = messenger.get_message_id(data)
                    message_timestamp = messenger.get_message_timestamp(data)

                    try:
                        Message.objects.create(name=name,msg=message, contact=mobile, msg_id=message_id,date=datetime.fromtimestamp(int(message_timestamp)))
                    except:
                        pass





                else:
                    pass
            else:
                delivery = messenger.get_delivery(data)
                get_msg_id  = messenger.get_send_msg_id(data)
                try:

                    timestampp = datetime.fromtimestamp(int(messenger.get_send_msg_timestamp(data)))

                except:
                    pass


                if delivery:

                    if delivery == "delivered":
                        try:
                            temp = TemplateReport.objects.get(msg_id=get_msg_id)
                            temp.delivered = True
                            temp.save()
                        except:
                            pass

                    elif delivery == "read":

                        try:
                            temp = TemplateReport.objects.get(msg_id=get_msg_id)
                            temp.seenTime = timestampp
                            temp.seen = True
                            temp.save()
                        except:
                            pass
                    elif delivery == "sent":
                        try:
                            temp = TemplateReport.objects.get(msg_id=get_msg_id)
                            temp.sent = True
                            temp.save()
                        except:
                            pass
                    else:
                        print("Message Failed")

                else:
                    print("No new message")

        return HttpResponse("OK", 200)

@login_required(login_url='/admin/login/')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/admin/login/')
def templatelist(request,pk=None):
    if pk:
        template = TemplateList.objects.get(id=pk)
        contactgroup = ContactGroup.objects.all()
        report = TemplateReport.objects.filter(template=template).order_by('-id')
        return render(request, 'template.html',{'template': template, 'contactgroup': contactgroup, 'report': report})
    else:
        templatelist = TemplateList.objects.all()
        return render(request, 'templatelist.html',{'templatelist': templatelist})

@login_required(login_url='/admin/login/')
def sendtemplate(request):
    if request.method == 'POST':
        template = TemplateList.objects.get(id=request.POST['template'])
        contactgroup = ContactGroup.objects.get(id=request.POST['contactgroup'])
        try:
            msg = request.POST['msg']
        except:
            msg = None

        if template.type == 'single':
            for contact in contactgroup.contacts.all():
                contact_number = str(+91) + contact.number
                ress = messenger.send_template(template=template.template, recipient_id=contact_number,lang=template.lang)

                try:
                    TemplateReport.objects.create(template=template, contact=contact, msg_id=ress["messages"][0]["id"])
                except:
                    pass
            return redirect('/templates/' + str(template.id))
        elif template.type == 'multi':

            for contact in contactgroup.contacts.all():
                contact_number = str(+91) + contact.number
                ress = messenger.send_templatev2(template=template.template,lang=template.lang, recipient_id=contact_number, components=[
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "image",
                                "image": {
                                    "link": "https://ibrlive.com/pix.jpg"
                                }
                            }
                        ]
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": contact_number
                            },
                            {
                                "type": "text",
                                "text": msg
                            }

                        ]

                    }])
                try:
                    TemplateReport.objects.create(template=template, contact=contact, msg_id=ress["messages"][0]["id"])
                except:
                    pass

            return redirect('/templates/' + str(template.id))
