
# Create your views here.
import random
from django.shortcuts import render, redirect
from .models import Ticket, Draw
from django.contrib.auth.decorators import login_required
from admin_console.utils import check_rank
from django.shortcuts import get_object_or_404


@login_required
def buy_manual(request):                # 수동 구매
    rounds = Draw.objects.all().order_by("-round")

    if request.method == "POST":
        selected_round = request.POST.get("round")
        nums = request.POST.getlist("nums")  # 번호 6개 리스트

        if len(nums) != 6:
            return render(request, "tickets/buy_manual.html", {
                "rounds": rounds,
                "error": "번호는 정확히 6개 선택해야 합니다!"
            })

        nums = list(map(int, nums))
        nums.sort()

        draw = Draw.objects.get(round=selected_round)

        Ticket.objects.create(
            user=request.user,
            round=draw,
            type="manual",
            n1=nums[0], n2=nums[1], n3=nums[2],
            n4=nums[3], n5=nums[4], n6=nums[5],
        )

        return redirect("my_tickets")

    return render(request, "tickets/buy_manual.html", {"rounds": rounds})



@login_required
def buy_auto(request):                  # 자동구매
    rounds = Draw.objects.all().order_by("-round")

    selected_round = None
    generated = None

    if request.method == "POST":
        selected_round = int(request.POST.get("round"))
        nums = sorted(random.sample(range(1, 46), 6))

        draw = Draw.objects.get(round=selected_round)

        Ticket.objects.create(
            user=request.user,
            round=draw,
            type="auto",
            n1=nums[0], n2=nums[1], n3=nums[2],
            n4=nums[3], n5=nums[4], n6=nums[5],
        )

        generated = nums

    return render(request, "tickets/buy_auto.html", {
        "rounds": rounds,
        "selected_round": selected_round,
        "generated": generated,
    })


@login_required
def my_tickets(request):            # 나의 티켓 목록 확인
    tickets = Ticket.objects.filter(user=request.user).order_by("-bought_at")
    return render(request, "tickets/my_tickets.html", {"tickets": tickets})


@login_required
def check_result(request):          # 당첨 확인
    rounds = Draw.objects.all().order_by("-round")
    selected_round = request.GET.get("round")
    results = []
    draw = None
    winning_numbers = []

    if selected_round:
        draw = Draw.objects.get(round=selected_round)
        # 정렬된 당첨번호 리스트 생성
        winning_numbers = sorted([
            draw.n1, draw.n2, draw.n3, draw.n4, draw.n5, draw.n6
        ])
        my_tickets = Ticket.objects.filter(user=request.user, round=draw)

        for t in my_tickets:
            rank = check_rank(t, draw)
            results.append((t, rank))

    return render(request, "tickets/check_result.html", {
        "rounds": rounds,
        "selected_round": selected_round,
        "results": results,
        "draw": draw,
        "winning_numbers": winning_numbers,
    })


@login_required
def delete_ticket(request, ticket_id):      # 티켓 삭제하기
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        return redirect("my_tickets")   # 네 URL 패턴에 맞추기

    return redirect("my_tickets")