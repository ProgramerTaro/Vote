from django.shortcuts import render, redirect
from .forms import RegisterForm, RoomForm, ElectForm, ChoiceNumForm, EnterForm
from .models import Room, elect, voter
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.http import HttpResponse

#ホームビュー
def index(request):
    return render(request, 'vote/index.html', {})

#会員登録ビュー
def register(request):
    #フォームからの入力であるかチェック
    if request.method == "POST":
        #フォームの値を取得
        form = RegisterForm(request.POST)
        #フォームの内容を検証
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'vote/register.html', {'form': form})

#投票部屋入室ビュー
def room_list(request):
    form = EnterForm()
    rooms = Room.objects.all()
    context = {'rooms': rooms, 'form': form}
    return render(request, 'vote/room_list.html', context)

#入室処理(合言葉確認)ビュー
def room_enter(request):
    #フォームからの入力であるかチェック
    if request.method == "POST":
        #フォームの値を取得
        form = EnterForm(request.POST)
        #フォームの内容を検証
        if form.is_valid():
            #部屋番号を取得
            roomId = int(request.POST['roomId'])
            #部屋番号に対応した部屋を取得
            room = Room.objects.get(roomId=roomId)
            #合言葉を照合
            if room.password == form.cleaned_data['room_password']:
                #投票形式に応じたテンプレートへリダイレクト
                if str(room.typeId) == '選出形式':
                    #投票対象を取得
                    choiceElect = elect.objects.filter(roomId=roomId)
                    #投票期限が過ぎているかを真偽値で取得
                    result = room.judge_limit()
                    context = {'room': room, 'choiceElect': choiceElect, 'result': result}
                    return render(request, 'vote/room_elect.html', context)
                return HttpResponse(roomId)
            else:
                return redirect('/room_list/')
        else:
            return redirect('/room_list/')
    else:
        return redirect('/')

#投票部屋作成ビュー
@login_required
def room_create(request):
    #フォームからの入力であるかチェック
    if request.method == "POST":
        request.session['room'] = request.POST
        #フォームの値を取得
        form = RoomForm(request.POST)
        #フォームの内容を検証
        if form.is_valid():
            room = form.save(commit=False)
            room.creatorId = request.user
            if(str(room.typeId) == '選出形式'):
                return redirect('/room_create_elect/')
            return redirect('/')
    else:
        form = RoomForm()
    return render(request, 'vote/room_create.html', {'form': form})

#投票対象作成(選出形式)ビュー
def room_create_elect(request):
    ElectFormSet = formset_factory(ElectForm, extra=5, max_num=100)
    #フォームからの入力であるかチェック
    if request.method == "POST":
        #投票対象フォームの値を取得
        form = ChoiceNumForm(request.POST)
        #項目数フォームの値を取得
        formset = ElectFormSet(request.POST)
        #投票対象フォームの内容を検証
        if form.is_valid():
            num = form.cleaned_data['choiceNum']
            ElectFormSet = formset_factory(ElectForm, extra=num, max_num=100)
            form = ChoiceNumForm()
            formset = ElectFormSet()
            context = {'formset': formset, 'form':form}
        else:
            #項目数フォームの内容を検証
            if formset.is_valid():
                roomform = RoomForm(request.session.pop("room", None))
                room = roomform.save(commit=False)
                room.creatorId = request.user
                room.save()
                for form in formset:
                    if form.is_valid():
                        elect = form.save(commit=False)
                        elect.roomId = Room.objects.get(pk = room.roomId)
                        elect.save()
                return redirect('/')
    else:
        form = ChoiceNumForm()
        formset = ElectFormSet()
        context = {'formset': formset, 'form':form}
    return render(request, 'vote/room_create_elect.html', context)

#投票処理ビュー
def vote_elect(request):
    #票、投票部屋、投票者を取得
    choiceId = int(request.POST['choice'])
    room = Room.objects.get(roomId=int(request.POST['roomId']))
    user = User.objects.get(id=request.user.id)
    #投票済みのユーザーであるかを判断
    if voter.objects.filter(voterId=user.id, roomId=room.roomId):
        context = {'result': '既に投票済みです。'}
        return render(request, 'vote/vote_result.html', context)
    else:
        #voterテーブルにデータを追加
        votealready = voter(voterId=user, roomId=room)
        votealready.save()

    #投票された選択肢を取得
    choice = elect.objects.get(EchoiceId=choiceId)
    #票を増やす
    choice.addVote()
    choice.save()
    context = {'result': '投票が完了しました。'}
    return render(request, 'vote/vote_result.html', context)
