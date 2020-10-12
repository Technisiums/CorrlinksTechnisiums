from django.db import models


# Create your models here.
class APIKey(models.Model):
    API_Key = models.CharField(max_length=15, blank=False)

    def __str__(self):
        return self.API_Key


class VPS(models.Model):
    VPS_Name = models.CharField(max_length=5, blank=False)
    notes = models.TextField(max_length=1000, blank=True)

    class Meta:
        verbose_name = "VPS"
        verbose_name_plural = "VPS"

    def get_active_count(self):
        objs = Account.objects.filter(VPS=self.id).filter(status='act')
        return len(objs)

    def get_disabled_count(self):
        objs = Account.objects.filter(VPS=self.id).filter(status='dis')
        return len(objs)

    def __str__(self):
        return self.VPS_Name


class Account(models.Model):
    Dis = 'dis'
    Act = 'act'
    choi = [(Dis, 'Disabled'), (Act, 'Active')]
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(blank=False, max_length=200)
    status = models.CharField(max_length=3, choices=choi, default=Act)
    VPS = models.ForeignKey(VPS, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.email + ' -- ' + self.get_status_display()


class Customer(models.Model):
    Blo = 'blo'
    Act = 'act'
    Unk = 'ukn'
    Tw = 'twi'
    choi = [(Act, 'Active'), (Blo, 'Blocked'), (Unk, 'Unknown')]
    status = models.CharField(max_length=3, choices=choi, default=Act)
    balance = models.FloatField(blank=True, default=0.00)
    due_Date = models.DateField(blank=False)
    allow_International_messages = models.BooleanField(default=False)
    # (only valid USA address +1, 1, 10 digit)
    # if it is international, the inmate might sent + country code or country code(without plus)
    notes = models.TextField(max_length=1000, blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    phone_Number = models.CharField(max_length=15, blank=True)
    corrlinks_ID = models.CharField(max_length=15, unique=True, blank=False)
    corrlinks_Account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' -- ' + self.corrlinks_ID

    def get_image_count_customer(self):
        smscustomers = SMSCustomer.objects.filter(corrlinks_Customer=self.id)
        # print(smscustomers)
        all_messages = SMSToCorrlinks.objects.filter(_from__in=smscustomers)
        count = 0
        for msg in all_messages:
            count += int(msg.get_image_count())
        # print(count)
        return str(count)


class SMSCustomer(models.Model):
    corrlinks_Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    phone_Number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return str(self.corrlinks_Customer) + ' -- ' + self.name + ' -- ' + self.phone_Number


class CorrlinksToSMS(models.Model):
    New = 'new'
    Sent = 'snt'
    Disabled = 'dis'
    Error = 'err'
    choi = [(New, 'New'), (Sent, 'Sent'), (Disabled, 'Disabled'), (Error, 'Error')]
    createdAt = models.DateTimeField(auto_now_add=True)
    _from = models.ForeignKey(Customer, on_delete=models.CASCADE)
    to = models.ForeignKey(SMSCustomer, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=choi, default=New)
    body = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return str(self._from) + '-->' + str(self.to)

    class Meta:
        verbose_name = "Corrlinks To SMS"
        verbose_name_plural = "Corrlinks To SMS"


class SMSToCorrlinks(models.Model):
    New = 'new'
    Sent = 'snt'
    Disabled = 'dis'
    Error = 'err'
    choi = [(New, 'New'), (Sent, 'Sent'), (Disabled, 'Disabled'), (Error, 'Error')]
    createdAt = models.DateTimeField(auto_now_add=True)
    _from = models.ForeignKey(SMSCustomer, on_delete=models.CASCADE)
    # to = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=choi, default=New)
    body = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return str(self._from)

    def get_image_count(self):
        objects = Image.objects.filter(message=self.id)
        return str(len(objects))

    class Meta:
        verbose_name = "SMS To Corrlinks"
        verbose_name_plural = "SMS To Corrlinks"


class Image(models.Model):
    message = models.ForeignKey(SMSToCorrlinks, on_delete=models.CASCADE)
    bandwidth_Message_ID = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=False)
    corrCustomer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, blank=True, null=True)

    def save(self):
        self.corrCustomer = self.message._from.corrlinks_Customer
        super(Image, self).save()

    def __str__(self):
        return str(self.message)
