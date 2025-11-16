from django.urls import path
from . import views

urlpatterns = [
    path("buy/manual/", views.buy_manual, name="buy_manual"),       # 수동
    path("buy/auto/", views.buy_auto, name="buy_auto"),             # 자동
    path("mine/", views.my_tickets, name="my_tickets"),             # 내 티켓 목록
    path("result/", views.check_result, name="check_result"),       # 당첨확인
    path("delete/<int:ticket_id>/", views.delete_ticket, name="delete_ticket"), # 내 티켓 삭제
]