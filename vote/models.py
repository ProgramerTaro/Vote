from django.db import models
from django.utils import timezone
import datetime

class voteType(models.Model):
    typeId = models.AutoField('投票形式ID', primary_key=True)
    typeName = models.CharField('投票形式名', max_length=32)

    def __str__(self):
        return self.typeName

class Room(models.Model):
    roomId = models.AutoField('部屋番号', primary_key=True)
    typeId = models.ForeignKey(voteType, on_delete=models.CASCADE)
    roomName = models.CharField('部屋名', max_length=200)
    creatorId = models.ForeignKey('auth.User')
    password = models.CharField('合言葉', max_length=32)
    roomInfo = models.TextField('部屋説明文')
    roomBirth = models.DateField('部屋作成日', default=timezone.now)
    roomLimit = models.DateField('投票期限')

    #投票期限が過ぎているかを判断
    def judge_limit(self):
        #期限を過ぎていればFalse, 過ぎていなければTrueを返す
        return self.roomLimit >= datetime.date.today()

    def __str__(self):
        return self.roomName

class voter(models.Model):
    voterId = models.ForeignKey('auth.User')
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.voterId) +' -> '+ str(self.roomId)

class elect(models.Model):
    EchoiceId = models.AutoField('選択肢ID', primary_key=True)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    EchoiceName = models.CharField('選択肢名', max_length=200, null=False, blank=False)
    voteNum = models.IntegerField('獲得票数', default=0)

    #票を増やす
    def addVote(self):
        self.voteNum += 1

    def __str__(self):
        return self.EchoiceName

class gradeFive(models.Model):
    GchoiceId = models.AutoField('選択肢ID', primary_key=True)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    GchoiceName = models.CharField('選択肢名', max_length=200)
    one = models.IntegerField('評点1の票数', default=0)
    two = models.IntegerField('評点2の票数', default=0)
    three = models.IntegerField('評点3の票数', default=0)
    four = models.IntegerField('評点4の票数', default=0)
    five = models.IntegerField('評点5の票数', default=0)

    #投票された評点の平均値を求める
    def get_average(self):
        sum = self.one + self.two + self.three + self.four + self.five
        if sum == 0 :
            return sum
        else:
            return (self.one + self.two*2 + self.three*3 + self.four*4 + self.five*5) / sum

    def __str__(self):
        return self.GchoiceName
