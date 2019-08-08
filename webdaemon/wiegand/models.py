from django.db import models

# Create your models here.


class Reader(models.Model):

    READER_MODEL = (
            ('T', 'Tag reader'),
            ('P', 'PinPad'),
            ('K', 'KeyPad'),
            ('N', 'NFC antenna'),
        )

    READER_STATE = (
            ('A', 'On'),
            ('P', 'Off'),
            ('L', 'Lock'),
            ('B', 'Busy'),
        )

    reader_text = models.CharField(max_length=100)
    last_use_date = models.DateTimeField('last use',blank=True,null=True)
    model_text = models.CharField(max_length=1, choices=READER_MODEL)
    state_text = models.CharField(max_length=1, choices=READER_STATE)
    error_counter_int = models.IntegerField(default=0)
    def __str__(self):
        return self.reader_text

class Group(models.Model):
    group_text = models.CharField(max_length=100)
    info_text = models.CharField(max_length=200)
    def __str__(self):
        return self.group_text

class User(models.Model):
    user_text = models.CharField(max_length=100)
    last_use_date = models.DateTimeField('last use',blank=True,null=True)
    state_text = models.CharField(max_length=20)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    def __str__(self):
        return self.user_text

class Pin(models.Model):

    PIN_STATE = (
            ('A', 'On'),
            ('P', 'Off'),
            ('L', 'Lock'),
        )

    pin_text = models.CharField(max_length=100)
    value_text = models.CharField(max_length=100)
    last_use_date = models.DateTimeField('last use',blank=True,null=True)
    expire_date = models.DateTimeField('expiration date',blank=True,null=True)
    state_text = models.CharField(max_length=1, choices=PIN_STATE)
    valid = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.pin_text

class Tag(models.Model):

    TAG_STATE = (
            ('A', 'On'),
            ('P', 'Off'),
            ('L', 'Lock'),
        )

    uid_text = models.CharField(max_length=100)
    tag_text = models.CharField(max_length=100)
    last_use_date = models.DateTimeField('last use',blank=True,null=True)
    expire_date = models.DateTimeField('expiration date',blank=True,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    state_text = models.CharField(max_length=1, choices=TAG_STATE)
    valid = models.BooleanField(default=False)
    def __str__(self):
        return self.tag_text

class Action(models.Model):

    ACTION_TYPE = (
            ('H', 'HomeAssistant'),
            ('M', 'MQTT'),
            ('A', 'API'),
        )

    name_text = models.CharField(max_length=100)

    type_status = models.CharField(max_length=1, choices=ACTION_TYPE)
    payload = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)

    def __str__(self):
        return self.name_text

class Status(models.Model):

    STATUS_TYPE = (
            ('M', 'MQTT'),
            ('S', 'HomeAssistant Service'),
            ('N', 'HomeAssistant Notify'),
        )

    name_text = models.CharField(max_length=100)

    type_status = models.CharField(max_length=1, choices=STATUS_TYPE)
    last_udate_date = models.DateTimeField('last update',blank=True,null=True)
    value_text = models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return self.name_text

class Condition(models.Model):

    CONDITION_TYPE = (
            ('T', 'Tag used'),
            ('P', 'PIN used'),
            ('S', 'Status'),
            ('N', 'Not Status'),            
        )

    CONDITION_CHAIN = (
            ('I', 'IF'),
            ('A', 'AND'),
            ('O', 'OR'),
        )

    name_text = models.CharField(max_length=100)
    iftype = models.CharField(max_length=1, choices=CONDITION_TYPE)
    ifchain = models.CharField(max_length=1, choices=CONDITION_CHAIN)
    associated_tag = models.ForeignKey(Tag, on_delete=models.CASCADE,blank=True,null=True)
    associated_pin = models.ForeignKey(Pin, on_delete=models.CASCADE,blank=True,null=True)
    associated_status = models.ForeignKey(Status, on_delete=models.CASCADE,blank=True,null=True)
    status_trigger_value = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name_text

class Trigger(models.Model):

    name_text = models.CharField(max_length=100)

    actions = models.ManyToManyField(Action)
    conditions = models.ManyToManyField(Condition)
    last_use_date = models.DateTimeField('last use',blank=True,null=True)
    enabled = models.BooleanField(default=True)
    def __str__(self):
        return self.name_text