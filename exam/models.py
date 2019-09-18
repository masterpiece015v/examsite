from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Auth(models.Model):
    auth_key = models.CharField(max_length=40,primary_key=True)
    auth_kind = models.CharField(max_length=10)
    auth_value = models.CharField(max_length=100)
    auth_date = models.DateTimeField('date published')
    def auth_date_check(self):
         return self.auth_date >= timezone.now() - datetime.timedelta(days=1)

class Org( models.Model ):
    o_id = models.CharField(max_length=4,primary_key=True)
    o_name = models.CharField( max_length=40 )
    l_num = models.IntegerField()
    def date_check(self):
        return self.create_date + datetime.timedelta(days=1) >= timezone.now()
    def u_num_check(self,l_num):
        now_num = User.objects.filter(o_id=self.o_id).count()
        return self.l_num >= l_num + now_num

class User( models.Model ):
    u_id = models.CharField(max_length=20,primary_key=True)
    u_email = models.EmailField(max_length=100)
    u_pass = models.CharField(max_length=20)
    u_name = models.CharField(max_length=40)
    o = models.ForeignKey(Org,on_delete=models.CASCADE )
    u_admin = models.SmallIntegerField(default=0)   #管理者
    u_enable = models.SmallIntegerField(default=1)  #ユーザの有効（期限切れまたはロックに使用）
    u_hidden = models.SmallIntegerField(default=0)  #ユーザを隠す
    u_date = models.DateField()
    def pass_check(self,u_pass):
        return self.u_pass == u_pass
    def get_o_id(self):
        return self.o.o_id

class AccessLog( models.Model ):
    u = models.ForeignKey( User,on_delete=models.CASCADE )
    a_date = models.DateTimeField()
    a_ipa = models.CharField(max_length=100)
    a_page = models.CharField(max_length=100)
    a_state = models.CharField(max_length=1)        #ログイン成功、失敗

class Classify( models.Model ):
    c_id = models.CharField( max_length=6,primary_key=True )
    l_id = models.CharField( max_length=2 )
    l_name = models.CharField(max_length=40)
    m_id = models.CharField( max_length=2 )
    m_name = models.CharField( max_length=40 )
    s_id = models.CharField( max_length=2 )
    s_name = models.CharField( max_length=40 )

class Question( models.Model ):
    q_id = models.CharField( max_length=9,primary_key=True )
    q_test = models.CharField( max_length=2 )
    q_period = models.CharField( max_length=5 )
    q_num = models.CharField( max_length=2 )
    q_title = models.CharField( max_length=100 )
    q_answer = models.CharField( max_length=1 )
    c = models.ForeignKey(Classify,on_delete=models.CASCADE )
    def getclassify(self):
        classify = Classify.objects.get(pk=self.c_id)
        return classify

class LittleTest( models.Model ):
    t_key = models.CharField( max_length=16,primary_key=True)
    t_id = models.CharField( max_length=4)
    t_num = models.CharField( max_length=4 )
    q = models.ForeignKey(Question,on_delete=models.CASCADE )
    o = models.ForeignKey( Org,on_delete=models.CASCADE )
    t_date = models.DateTimeField()
    def get_q_answer(self):
        q_answer = Question.objects.get(pk=self.q_id).q_answer
        return q_answer
    def get_classify(self):
        que = Question.objects.get(pk=self.q_id)
        classify = que.getclassify()
        return classify

class ResultTest( models.Model ):
    u = models.ForeignKey( User,on_delete=models.CASCADE)
    #t_id = models.CharField( max_length=4 )
    #t_num = models.CharField( max_length=4 )
    t = models.ForeignKey( LittleTest, on_delete=models.CASCADE )
    r_answer = models.CharField( max_length=1 )
    r_date = models.DateTimeField()

class SuperUser( models.Model ):
    u_id = models.CharField( max_length=40 , primary_key=True)
    u_pass = models.CharField( max_length=40 )

class AddLicenseRequest( models.Model):
    o = models.ForeignKey(Org,on_delete=models.CASCADE)
    l_num = models.IntegerField()
    adr_date = models.DateTimeField()
    check = models.SmallIntegerField(default=0)

class AnswerImage( models.Model ):
    image = models.CharField( max_length=20 )
    o_id = models.CharField( max_length=4 )
    t_id = models.CharField( max_length=4 )
    u_id = models.CharField( max_length=20 )
