from django.db import models
from django.conf import settings


class Draw(models.Model):
    round = models.PositiveIntegerField(unique=True)   # 회차
    date = models.DateField()
    n1 = models.PositiveIntegerField()
    n2 = models.PositiveIntegerField()
    n3 = models.PositiveIntegerField()
    n4 = models.PositiveIntegerField()
    n5 = models.PositiveIntegerField()
    n6 = models.PositiveIntegerField()
    bonus = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.round}회차 ({self.date})"
    


class Ticket(models.Model):
    TYPE_CHOICES = (
        ("manual", "수동"),
        ("auto", "자동"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 구매자
    round = models.ForeignKey(Draw, on_delete=models.CASCADE)                     # 회차 
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)                  # 수동 / 자동

    n1 = models.PositiveIntegerField()                                            # 티켓 번호
    n2 = models.PositiveIntegerField()
    n3 = models.PositiveIntegerField()
    n4 = models.PositiveIntegerField()
    n5 = models.PositiveIntegerField()
    n6 = models.PositiveIntegerField()

    bought_at = models.DateTimeField(auto_now_add=True)                           # 구매시각

    def __str__(self):
        return f"{self.user} - {self.round}회차 ({self.type})"