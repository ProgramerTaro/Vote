from django import forms
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import voteType, Room, voter, elect, gradeFive

TYPE_CHOICES = (
    ('1', '選出形式'),
    # ('2', '評点形式 ※未実装'),
)

#日付入力フォーム
class DateInput(forms.DateInput):
    input_type = 'date'

#会員登録フォーム
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username']
        self.fields['password1']
        self.fields['password2']

#投票部屋作成フォーム
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('roomName', 'password', 'roomInfo', 'roomLimit', 'typeId')
        #ラベルが反映されない
        labes = {
            'typeId': _('投票形式'),
        }
        widgets = {
            'roomLimit': DateInput(),
        }
    typeId = forms.Select(choices=TYPE_CHOICES)

#投票選択肢作成(選出形式)フォーム
class ElectForm(forms.ModelForm):
    class Meta:
        model = elect
        fields = ('EchoiceName',)

#後期追記ここから
#投票選択肢作成(選出形式)フォーム
class GradeForm(forms.ModelForm):
    class Meta:
        model = gradeFive
        fields = ('GchoiceName',)
#後期追記ここまで

#投票対象数フォーム
class ChoiceNumForm(forms.Form):
    choiceNum = forms.IntegerField(label='投票対象数')

#投票部屋入室フォーム
class EnterForm(forms.Form):
    room_password = forms.CharField(max_length=200, label='合言葉')

#後期追記ここから
#投票部屋検索フォーム
class SearchForm(forms.Form):
    room_name = forms.CharField(max_length=200, label='部屋名')
#後期追記ここまで
