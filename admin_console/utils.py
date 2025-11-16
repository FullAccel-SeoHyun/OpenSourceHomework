# 등수 계산 (실제 로또 규칙: 1등~5등)
def check_rank(ticket, draw):
    # 사용자 티켓 번호 집합
    ticket_nums = {ticket.n1, ticket.n2, ticket.n3, ticket.n4, ticket.n5, ticket.n6}

    # 당첨번호 집합
    draw_nums = {draw.n1, draw.n2, draw.n3, draw.n4, draw.n5, draw.n6}

    # 일치 개수 계산
    matched = len(ticket_nums & draw_nums)

    # 보너스 번호 일치 여부
    bonus_match = draw.bonus in ticket_nums

    # 실제 로또 등수 규칙 적용
    if matched == 6:
        return 1  # 1등
    elif matched == 5 and bonus_match:
        return 2  # 2등
    elif matched == 5:
        return 3  # 3등
    elif matched == 4:
        return 4  # 4등
    elif matched == 3:
        return 5  # 5등
    else:
        return 0  # 꽝