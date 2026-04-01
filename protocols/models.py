from django.db import models
from django.conf import settings

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Indication(models.Model):
    region = models.ForeignKey(Region, related_name='indications', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('region', 'name')

    def __str__(self):
        return f"{self.region.name} - {self.name}"

class SavedProtocol(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='protocols', on_delete=models.SET_NULL, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    indication = models.CharField(max_length=255, null=True, blank=True)
    clinical_details = models.TextField(blank=True, null=True)
    urgency = models.CharField(max_length=50, null=True, blank=True)
    age_group = models.CharField(max_length=50, null=True, blank=True)
    motion_risk = models.CharField(max_length=50, null=True, blank=True)
    claustrophobia = models.BooleanField(default=False)
    renal_status = models.CharField(max_length=100, null=True, blank=True)
    has_implant = models.BooleanField(default=False)
    field_strength = models.CharField(max_length=50, null=True, blank=True)
    vendor = models.CharField(max_length=100, null=True, blank=True)
    selected_coils = models.JSONField(default=list) # Store as list of strings
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.region} - {self.indication} ({self.created_at.date()})"

class ProtocolRequest(models.Model):
    # Mapping to the columns in the high-level requirements/image
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='protocol_requests', on_delete=models.SET_NULL, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    indication = models.CharField(max_length=255, null=True, blank=True)
    clinical_details = models.TextField(blank=True, null=True)
    urgency = models.CharField(max_length=50, null=True, blank=True)
    age_group = models.CharField(max_length=50, null=True, blank=True)
    motion_risk = models.CharField(max_length=50, null=True, blank=True)
    claustrophobia = models.BooleanField(default=False)
    renal_status = models.CharField(max_length=100, null=True, blank=True)
    has_implant = models.BooleanField(default=False)
    field_strength = models.CharField(max_length=50, null=True, blank=True)
    vendor = models.CharField(max_length=100, null=True, blank=True)
    selected_coils = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id} - {self.indication if self.indication else 'No Indication'}"
