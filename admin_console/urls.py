from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),                  # 메인대시보드
    path('draw/create/', views.draw_create, name='draw_create'),        # 로또 만들기
    path('sales/', views.sales_view, name='sales_view'),                # 판매기록
    path('winners/', views.winners_view, name='winners_view'),          # 당첨자 조회
    path("draws/", views.draw_list, name="draw_list"),                  # 추첨 목록 확인
    path("draws/delete/<int:draw_id>/", views.delete_draw, name="delete_draw"), # 추첨 삭제
]
