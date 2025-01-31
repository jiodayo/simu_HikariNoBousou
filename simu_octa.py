import numpy as np
import itertools
import random
from scipy.spatial import distance
from itertools import combinations


def generate_large_octagon(radius=1000):
    """ 正八角形の頂点を生成 """
    theta = np.linspace(0, 2 * np.pi, 9)[:-1]  # 0~2πの間を8分割
    return np.array([(radius * np.cos(t), radius * np.sin(t)) for t in theta])


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
    
    # 全ての辺の組み合わせに対して交差判定を実行
    for (a1, a2), (b1, b2) in combinations(edges, 2):
        if lines_intersect(points[a1], points[a2], points[b1], points[b2]):
            return True
    
    return False


def simulate(n_trials):
    """ 交差するケースの確率をシミュレーションで求める """
    octagon = generate_large_octagon(radius=100)
    intersection_count = 0
    
    for _ in range(n_trials):
        remaining_indices = list(range(8))
        removed = random.sample(remaining_indices, 2)
        remaining_indices = [idx for idx in remaining_indices if idx not in removed]
        
        # 除外された点以外のすべての点からスタート地点を選ぶ
        start_idx = random.choice(remaining_indices)
        
        # 経路を決定
        path = find_nearest_neighbor_path(octagon[remaining_indices], remaining_indices.index(start_idx))
        path = [remaining_indices[i] for i in path]  # インデックスを元の番号に戻す
        
        # 交差判定
        if check_intersections(octagon, path):
            intersection_count += 1
            
    print(intersection_count)


    return intersection_count / n_trials



# シミュレーション実行
probability= simulate(100000)
print(f"交差する確率: {probability:.1f}")
