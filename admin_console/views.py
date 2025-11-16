import random
from django.shortcuts import render, redirect, get_object_or_404
from tickets.models import Draw, Ticket
from django.db.models import Count
from .utils import check_rank

# Create your views here.

# 관리자 대시보드
def dashboard(request):
    return render(request, 'admin_console/dashboard.html')

# 로또 생성 
def draw_create(request):
    if request.method == "POST":
        round_num = request.POST.get("round")
        date = request.POST.get("date")

        # 동일 회차 중복 생성 방지
        if Draw.objects.filter(round=round_num).exists():
            return render(request, "admin_console/draw_create.html", {
                "error": "이미 존재하는 회차입니다!",
                "round": round_num,
                "date": date,
            })

        # 자동 추첨 번호 생성
        numbers = random.sample(range(1, 46), 7)
        n1, n2, n3, n4, n5, n6 = numbers[:6]
        bonus = numbers[6]

        Draw.objects.create(
            round=round_num,
            date=date,
            n1=n1, n2=n2, n3=n3, n4=n4, n5=n5, n6=n6,
            bonus=bonus
        )

        return redirect("admin_dashboard")

    return render(request, "admin_console/draw_create.html")

# 판매기록
def sales_view(request):
    sales = Ticket.objects.values('round__round').annotate(total=Count('id')).order_by('round__round')

    return render(request, "admin_console/sales.html", {'sales': sales})

# 당첨 조회
def winners_view(request):
    selected_round = request.GET.get("round")
    rounds = Draw.objects.all().order_by("round")

    winners = []

    if selected_round:
        draw = Draw.objects.get(round=selected_round)
        tickets = Ticket.objects.filter(round=draw)

        for t in tickets:
            rank = check_rank(t, draw)
            if rank > 0:
                winners.append((t, rank))

    return render(request, "admin_console/winners.html", {
        "rounds": rounds,
        "winners": winners,
        "selected_round": selected_round,
    })

# 추첨 목록 확인
def draw_list(request):
    draws = Draw.objects.all().order_by("-round")

    # 각 draw 객체에 정렬된 당첨번호 리스트 추가
    for d in draws:
        d.sorted_numbers = sorted([d.n1, d.n2, d.n3, d.n4, d.n5, d.n6])

    return render(request, "admin_console/draw_list.html", {
        "draws": draws
    })

# 추첨 삭제
def delete_draw(request, draw_id):
    draw = get_object_or_404(Draw, id=draw_id)
    if request.method == "POST":
        draw.delete()
    return redirect("draw_list")