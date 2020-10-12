from django.urls import path, include
from .views import GetAccounts, PostCorrlinksToSMS, ListenFormBandwith, SMSToCorrlinksView, setSMStoCorrlinksStatus,addPhoneBook

urlpatterns = [
    # path('acc/', sample),
    path('getAcc/', GetAccounts.as_view()),
    path('sendSMS/', PostCorrlinksToSMS.as_view()),
    path('getPendingSMS/', SMSToCorrlinksView.as_view()),
    path('setSMSToCorrlinksStatus/', setSMStoCorrlinksStatus.as_view()),
    path('addPhoneBook/', addPhoneBook.as_view()),
    path('listenFromBandwidth/', ListenFormBandwith.as_view()),
]
