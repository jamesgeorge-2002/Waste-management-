from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from locations.models import LocalBody, Ward

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)
    local_body_type = forms.ChoiceField(choices=User.LOCAL_BODY_TYPE_CHOICES, required=True)
    local_body = forms.ModelChoiceField(queryset=LocalBody.objects.all(), required=True)
    ward = forms.ModelChoiceField(queryset=Ward.objects.none(), required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'user_type', 'local_body_type', 'local_body', 'ward', 'address', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'local_body' in self.data:
            try:
                local_body_id = int(self.data.get('local_body'))
                self.fields['ward'].queryset = Ward.objects.filter(local_body_id=local_body_id)
            except (ValueError, TypeError):
                pass


class WorkerRegistrationForm(UserCreationForm):
    worker_id = forms.CharField(max_length=50, required=True)
    local_body = forms.ModelChoiceField(queryset=LocalBody.objects.all(), required=True)
    assigned_wards = forms.ModelMultipleChoiceField(queryset=Ward.objects.none(), required=False)
    phone = forms.CharField(max_length=20, required=False)
    id_proof = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'worker_id', 'local_body', 'assigned_wards', 'phone', 'id_proof')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Assigned wards can be populated via JS after choosing local body in the template
