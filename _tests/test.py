def solution(triangle):
    answer = triangle[0][0]

    if len(triangle) > 1:
        right = []
        left = []
        for k in range(1,len(triangle)) :
            right.append(triangle[k][1:])
            left.append(triangle[k][:-2])
        if solution(left) > solution(right): 
            answer += solution(left)
        elif solution(left) < solution(right): 
            answer += solution(right)
    print(answer)
    return answer

d = [[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]
print(d[0][0])

solution(d)