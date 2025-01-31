import numpy as np
import itertools
import random
from scipy.spatial import distance

def find_nearest_neighbor_path(points, start_idx):
    """ 最も近い順に点を結ぶ経路を決定 """
    remaining = set(range(len(points)))
    remaining.remove(start_idx)
    path = [start_idx]
    current_idx = start_idx
    
    while remaining:
        nearest_idx = min(remaining, key=lambda idx: distance.euclidean(points[current_idx], points[idx]))
        path.append(nearest_idx)
        remaining.remove(nearest_idx)
        current_idx = nearest_idx
    
    return path


def check_intersections(points, path):
    """ 経路が交差しているかを判定 """
    edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
    
    def lines_intersect(p1, p2, p3, p4):
        """ 2つの線分 (p1, p2) と (p3, p4) が交差するか判定 """
        def ccw(a, b, c):
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
        
        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)
    
    for (i, (a1, a2)) in enumerate(edges):
        for (b1, b2) in edges[i+2:]:  # 連続する辺同士は交差しないのでスキップ
            if lines_intersect(points[a1], points[a2], points[b1], points[b2]):
                return True
    
    return False


def generate_two_column():
    """ 2列横隊の8点を生成 """
    width = 1  # 横方向の間隔（AD, EH）
    height = 2  # 縦方向の間隔（AE, DH）
    
    upper_row = [(i * width, height / 2) for i in range(4)]  # 上段 A, B, C, D
    lower_row = [(i * width, -height / 2) for i in range(4)] # 下段 E, F, G, H
    
    return np.array(upper_row + lower_row)

def simulate_two_column(n_trials):
    """ 2列横隊の交差確率を求める """
    points = generate_two_column()
    intersection_count = 0
    
    for _ in range(n_trials):
        remaining_indices = list(range(8))
        removed = random.sample(remaining_indices, 2)  # 2点をランダムに削除
        remaining_indices = [idx for idx in remaining_indices if idx not in removed]
        
        start_idx = random.choice(remaining_indices)  # 残った点からランダムに開始
        path = find_nearest_neighbor_path(points[remaining_indices], remaining_indices.index(start_idx))
        path = [remaining_indices[i] for i in path]
        
        if check_intersections(points, path):
            intersection_count += 1
    
    return intersection_count / n_trials

# シミュレーション実行
probability = simulate_two_column(1000000)
print(f"交差する確率: {probability:.10f}")