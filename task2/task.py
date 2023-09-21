import csv

# Считываем дерево из файла
def read_tree(filename):
    tree = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            parent, child = map(int, row)
            if parent not in tree:
                tree[parent] = []
            tree[parent].append(child)
    return tree

# Получаем непосредственных детей (подчиненных) узла
def get_children(node, tree):
    return tree.get(node, [])

# Проверяем, является ли node1 родителем для node2
def is_direct_manager(node1, node2, tree):
    return node2 in get_children(node1, tree)

# Проверяем, является ли node1 дочерним узлом для node2
def is_direct_subordinate(node1, node2, tree):
    return is_direct_manager(node2, node1, tree)

# Проверяем, управляет ли node1 node2 опосредованно
def is_indirect_manager(node1, node2, tree):
    for child in get_children(node1, tree):
        if child != node2 and (child == node2 or is_indirect_manager(child, node2, tree)):
            return True
    return False

# Проверяем, является ли node1 опосредованным подчиненным для node2
def is_indirect_subordinate(node1, node2, tree):
    return is_indirect_manager(node2, node1, tree)

# Проверяем, являются ли node1 и node2 соподчиненными узлами
def is_peer(node1, node2, tree):
    for key in tree:
        if is_direct_subordinate(node1, key, tree) and is_direct_subordinate(node2, key, tree) and node1 != node2:
            return True
    return False

def get_all_descendants(node, tree):
    descendants = set()
    children = get_children(node, tree)
    descendants.update(children)
    for child in children:
        descendants.update(get_all_descendants(child, tree))
    return descendants

def get_parent(node, tree):
    for key, children in tree.items():
        if node in children:
            return key
    return None

def get_all_ancestors(node, tree):
    ancestors = set()
    parent = get_parent(node, tree)
    while parent is not None:
        ancestors.add(parent)
        parent = get_parent(parent, tree)
    return ancestors

def determine_relations(tree):
    relations_list = []
    all_nodes = sorted(list(set(tree.keys()).union(*tree.values())))

    for node in all_nodes:
        node_relations = [
            [],  # непосредственное управление
            [],  # непосредственное подчинение
            [],  # опосредованное управление
            [],  # опосредованное подчинение
            []   # соподчиненность
        ]

        for other_node in all_nodes:
            if other_node == node:
                continue
            if is_direct_manager(node, other_node, tree):
                node_relations[0].append(other_node)
            elif is_direct_subordinate(node, other_node, tree):
                node_relations[1].append(other_node)
            elif other_node in get_all_descendants(node, tree) and not is_direct_manager(node, other_node, tree):
                node_relations[2].append(other_node)
            elif other_node in get_all_ancestors(node, tree) and not is_direct_subordinate(node, other_node, tree):
                node_relations[3].append(other_node)
            elif is_peer(node, other_node, tree):
                node_relations[4].append(other_node)

        relations_list.append(node_relations)

    return relations_list

def task_2_1():
    filename = "tree_list.csv"
    tree = read_tree(filename)
    all_relations = determine_relations(tree)

    for node_relations in all_relations:
        print(node_relations)


def gather_relations_by_type(all_relations):
    # Получаем все уникальные узлы
    all_nodes = sorted(list(set(node for relations in all_relations for node_list in relations for node in node_list)))

    relations_by_type = [set() for _ in range(5)]

    for idx, node_relations in enumerate(all_relations):
        node = all_nodes[idx]
        for rel_idx, nodes in enumerate(node_relations):
            if nodes:
                relations_by_type[rel_idx].add(node)

    # Преобразуем множества в списки
    for idx, rel_set in enumerate(relations_by_type):
        relations_by_type[idx] = sorted(list(rel_set))

    return relations_by_type

def task_2_2():
    filename = "tree_list.csv"
    tree = read_tree(filename)
    all_relations = determine_relations(tree)
    
    relations_by_type = gather_relations_by_type(all_relations)

    res = []
    for rel_list in relations_by_type:
        res.append(rel_list)

    return res

