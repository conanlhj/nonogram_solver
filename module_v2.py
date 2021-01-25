import time as t
from itertools import combinations_with_replacement as cr


def partition_k(m, k):

    for div in cr(range(m+1), k-1):
        counts = [div[0]]

        for i in range(1, k-1):
            counts.append(div[i] - div[i-1])
        counts.append(m-div[-1])

        yield(counts)


# 가능한 모든 경우의 수를 찾는 함수
def find_poss_line(N, hint):
    n_hint = len(hint)
    d = N-sum(hint)-(n_hint-1)

    all_b_line = []
    poss_line = []
    # 가능한 경우 탐색
    for c in partition_k(d, n_hint+1):
        temp = []
        for j in range(n_hint+1):
            if j == 0 or j == n_hint:
                temp.append(c[j])
            else:
                temp.append(c[j]+1)
        all_b_line.append(temp)

    hint.append(0)

    for blank in all_b_line:
        temp = []
        for i in range(n_hint+1):
            for j in range(blank[i]):
                temp.append(0)
            for j in range(hint[i]):
                temp.append(1)
        poss_line.append(temp)
    del hint[len(hint)-1]

    return poss_line


# 가능한 라인들을 바탕으로 최종 라인 출력
def make_final_line(N, all_p_l):
    result = [0]*N

    for line in all_p_l:
        for i in range(N):
            if line[i] == -1:
                result[i] += 0
            else:
                result[i] += line[i]

    for i in range(N):
        result[i] /= len(all_p_l)
        if result[i] > 0 and result[i] < 1:
            result[i] = 0
        elif result[i] == 0:
            result[i] = -1
        else:
            result[i] = 1

    return result


# 한 줄을 풀고 가능한 줄들을 반환하는 함수
def solve_line(N, hint):

    if 0 in hint:
        result = []
        print('skip - 0 in hint')
        for i in range(N):
            result.append(-1)
        return [result]

    if sum(hint)+len(hint)-1-N == 0:
        print('skip - perfect line')
        result = []
        for h in hint:
            for i in range(h):
                result.append(1)
            result.append(-1)
        return [result[:-1]]

    return find_poss_line(N, hint)


# 불가능한 저장된 줄 제거
def remove_possible(N, poss_list, g_line):
    g_hint = {}
    for i in range(N):
        if g_line[i] == 1:
            g_hint[i] = 1
        elif g_line[i] == -1:
            g_hint[i] = 0
    remove_list = []
    for i in poss_list:
        for j in g_hint:
            if g_hint[j] == 0 and i[j] == 1:
                remove_list.append(i)
                break
            elif g_hint[j] == 1 and i[j] != 1:
                remove_list.append(i)
                break
    for i in remove_list:
        poss_list.remove(i)


# 보드 출력
def print_board(board):
    for i in board:
        for j in i:
            if j == 1:
                print("■", end='')
            elif j == 0:
                print("□", end='')
            elif j == -1:
                print("※", end='')
        print('')


# 네모로직 끝났는지 파악
def find_end(N, board):
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                return 1
    print("Solved")
    return 0


# 네모로직 solve
def solve_nonogram(N, hint, url):
    t_time = 0
    a_time = []
    l_time = [[], []]
    board = []
    cnt = 0
    for i in range(N):
        board.append([0]*N)
    all_poss_line = [[], []]

    start_time = t.time()
    pre_time = t.time()
    # 가로줄 1번째
    cnt += 1
    print("Attempt :", cnt)
    for i in range(N):
        print(" - Line", i)

        pre_l_time = t.time()
        all_poss_line[0].append(solve_line(N, hint[1][i]))
        l_time[1].append(t.time() - pre_l_time)
        print(t.time() - pre_l_time)

        f_line = make_final_line(N, all_poss_line[0][i])

        for j in range(N):
            board[i][j] = f_line[j]
    print_board(board)
    a_time.append(t.time()-pre_time)
    print(a_time[cnt-1])

    pre_time = t.time()
    # 세로줄 1번째
    cnt += 1
    print("Attempt :", cnt)
    for i in range(N):
        print(" - Line", i)
        g_line = []
        for j in range(N):
            g_line.append(board[j][i])

        pre_l_time = t.time()
        all_poss_line[1].append(solve_line(N, hint[0][i]))
        l_time[0].append(t.time() - pre_l_time)
        print(t.time() - pre_l_time)

        remove_possible(N, all_poss_line[1][i], g_line)
        f_line = make_final_line(N, all_poss_line[1][i])

        for j in range(N):
            board[j][i] = f_line[j]
    print_board(board)
    a_time.append(t.time()-pre_time)
    print(a_time[cnt-1])

    # 세로 가로 반복 start
    while find_end(N, board):
        pre_time = t.time()
        cnt += 1
        print("Attempt :", cnt)
        # 가로
        if cnt % 2:
            for i in range(N):
                g_line = []
                for j in range(N):
                    g_line.append(board[i][j])

                remove_possible(N, all_poss_line[0][i], g_line)
                f_line = make_final_line(N, all_poss_line[0][i])

                for j in range(N):
                    board[i][j] = f_line[j]
            print_board(board)
            a_time.append(t.time()-pre_time)
            print(a_time[cnt-1])
        # 세로
        else:
            for i in range(N):
                g_line = []
                for j in range(N):
                    g_line.append(board[j][i])

                remove_possible(N, all_poss_line[1][i], g_line)
                f_line = make_final_line(N, all_poss_line[1][i])

                for j in range(N):
                    board[j][i] = f_line[j]
            print_board(board)
            a_time.append(t.time()-pre_time)
            print(a_time[cnt-1])
        if cnt > 100:
            print('Stop solving - cnt > 100')
            break
    t_time = t.time()-start_time
    print(t_time)

    time_c = t.localtime(t.time())
    filename = str(N)+'.'
    for i in range((len(time_c)-3)):
        filename += str(time_c[i])+'.'
    f = open("./log/"+filename+".txt", 'w')
    f.write(" - url\n\n"+url+"\n\n")
    f.write(" - N\n\n"+str(N)+"\n\n")
    f.write(" - Hint\n\n"+str(hint)+"\n\n")
    if cnt > 100:
        f.write(" - Count\n\n"+str(cnt)+"  X\n\n")
    else:
        f.write(" - Count\n\n"+str(cnt)+"\n\n")
    f.write(" - Total time\n\n"+str(t_time)+"\n\n")
    f.write(" - Attempt_time\n\n")
    for i in range(len(a_time)):
        f.write("Attempt %d" % (i+1)+'\n')
        f.write(str(a_time[i])+'\n')

    f.write("\n - Line_time\n\n")
    for i in range(N):
        f.write('hint  '+str(hint[1][i])+"\n")
        f.write('n  '+str(len(hint[1][i]))+"\n")
        f.write('d  '+str(N-sum(hint[1][i])-(len(hint[1][i])-1))+"\n")
        f.write('time  '+str(l_time[1][i])+"\n\n")
    for i in range(N):
        f.write('hint  '+str(hint[0][i])+"\n")
        f.write('n  '+str(len(hint[0][i]))+"\n")
        f.write('d  '+str(N-sum(hint[0][i])-(len(hint[0][i])-1))+"\n")
        f.write('time  '+str(l_time[0][i])+"\n\n")

    f.write("\n - Board\n\n")
    for i in board:
        for j in i:
            if j == 1:
                f.write("■")
            elif j == 0:
                f.write("□")
            elif j == -1:
                f.write("※")
        f.write("\n")

    return board, cnt
