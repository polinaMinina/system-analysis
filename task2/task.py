from typing import Dict, List, Tuple
import csv
import io

def parse_csv(input_string: str) -> List[Tuple[int, int]]:
    edges = []
    f = io.StringIO(input_string)
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        if len(row) == 2:
            edges.append((int(row[0]), int(row[1])))
    return edges

def build_graph(edges: List[Tuple[int, int]]) -> Dict[int, List[int]]:
    graph = {}
    for edge in edges:
        if edge[0] not in graph:
            graph[edge[0]] = []
        graph[edge[0]].append(edge[1])
    return graph

def dfs_depth(graph: Dict[int, List[int]], node: int, depth: int, depths: Dict[int, int]) -> None:
    depths[node] = depth
    if node in graph:
        for child in graph[node]:
            dfs_depth(graph, child, depth + 1, depths)

def dfs_subtree_size(graph: Dict[int, List[int]], node: int, subtree_sizes: Dict[int, int]) -> int:
    if node not in graph:
        subtree_sizes[node] = 1
        return 1
    size = 1
    for child in graph[node]:
        size += dfs_subtree_size(graph, child, subtree_sizes)
    subtree_sizes[node] = size
    return size

def calculate_levels_depths(depths: Dict[int, int]) -> Dict[int, List[int]]:
    levels = {}
    for node, depth in depths.items():
        if depth not in levels:
            levels[depth] = []
        levels[depth].append(node)
    return levels

def task(csv_string: str) -> str:
    edges = parse_csv(csv_string)
    
    graph = build_graph(edges)
    reverse_graph = {child: parent for parent, children in graph.items() for child in children}

    children_counts = {node: len(children) for node, children in graph.items()}
    depths = {}
    subtree_sizes = {}
    same_level = {}

    for node in graph:
        if node not in depths:
            dfs_depth(graph, node, 0, depths)
        if node not in subtree_sizes:
            dfs_subtree_size(graph, node, subtree_sizes)
    
    levels = calculate_levels_depths(depths)
    
    for level, nodes in levels.items():
        for node in nodes:
            same_level[node] = len(nodes) - 1
    
    all_nodes = set(graph.keys()) | {child for children in graph.values() for child in children}
    
    output = io.StringIO()
    writer = csv.writer(output, delimiter='\t')
    
    for node in sorted(all_nodes):
        r1 = children_counts.get(node, 0)
        r2 = 1 if node in reverse_graph else 0
        r3 = subtree_sizes.get(node, 1) - r1 - 1
        r4 = depths.get(node, 0) - 1 if node in reverse_graph else 0
        r5 = same_level.get(node, 0)
        writer.writerow([r1, r2, r3, r4, r5])
    
    return output.getvalue().strip()


def csv_string_to_file(csv_string: str, file_path: str) -> None:
    data = csv_string.replace('\t', ';')
    
    with open(file_path, 'w', newline='') as csvfile:
        csvfile.write(data)

csv_string = "1;2\n1;3\n3;4\n3;5"
csv_result = task(csv_string) 

csv_file_path_csvlib = "./task3.csv"
csv_string_to_file(csv_result, csv_file_path_csvlib)
