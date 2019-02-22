import math
import scipy.stats
match = {(1, 2): 0.023114355231143552,  
         (1, 3): 0.0012165450121654502, 
         (2, 2): 0.006082725060827251, 
         (3, 1): 0.0006082725060827251, 
         (1, 1): 0.9422141119221411, 
         (2, 1): 0.0267639902676399}
c = 1.467
s2 = 6.315

def prob_delta(delta):
    return scipy.stats.norm(0,1).cdf(delta) 

def length(sentence):
    punt_list = ',.!?:;~，。！？：；～”“《》'
    sentence = sentence
    return sum(1 for char in sentence if char not in punt_list)

def distance(partition1,partition2,match_prob):
    l1 = sum(map(length,partition1))
    l2 = sum(map(length,partition2))
    try:
        delta = (l2-l1*c)/math.sqrt(l1*s2)
    except ZeroDivisionError:
        return float('inf')
    prob_delta_given_match = 2*(1 - prob_delta(abs(delta)))    
    try:
        return - math.log(prob_delta_given_match) - math.log(match_prob)
    except ValueError:
        return float('inf')

def align(para1,para2):
    """
    输入两个句子序列，生成句对
    句对是倒序的，从段落结尾开始向开头对齐
    """
    align_trace = {} 
    for i in range(len(para1) + 1):
        for j in range(len(para2) + 1):     
            if i == j == 0:
                align_trace[0, 0] = (0, 0, 0) 
            else:
                align_trace[i,j] = (float('inf'),0,0)
                for (di, dj), match_prob in match.items():
                    if i-di>=0 and j-dj>=0:
                        align_trace[i,j] = min(align_trace[i,j],(align_trace[i-di, j-dj][0] + distance(para1[i-di:i],para2[j-dj:j],match_prob), di, dj))
                
    i, j = len(para1), len(para2)
    while True:
        (c, di, dj) = align_trace[i, j]
        if di == dj == 0:
            break
        yield ''.join(para1[i-di:i]), ''.join(para2[j-dj:j])
        i -= di
        j -= dj  
