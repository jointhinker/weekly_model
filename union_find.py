#coding:utf-8
import copy
class UnionFind():
    class_dict = {}
    class_sz = {}
    count = 0

    def __init__(self, test_data):
        """初始化每个节点，根节点是本身，class_dict存储 {节点:当前所在树的根节点}
            初始化每个节点的size，用来判断该如何合并树，策略是小树合并到大树中"""
        for item_list in test_data:
            for item_value in item_list:
                if item_value not in self.class_dict:
                    self.class_dict[item_value] = item_value
                    self.class_sz[item_value] = 1

    def find(self,node):
        """找到node节点的根节点"""
        while (self.class_dict[node] != node):
            if self.class_dict[node] == node:
                break
            else:
                node = self.class_dict[node]
        return node

    def is_connected(self,p, q):
        """找到两个node的根节点，相同则不用合并，不相同则合并"""
        if self.find(p) == self.find(q):
            return True
        else:
            return False

    def union_fun(self,tuple_data):
        self.count = len(self.class_dict)
        for item_tuple in tuple_data:
            p, q = item_tuple[0], item_tuple[1]
            # 比较p和q的sz，决定如何合并树（将一个树的根节点指向另一个树的根节点），策略是：小树挂到大树上
            # 如果不连接，赋值
            if not self.is_connected(p, q):
                # print(p+" and "+q + " is not connected")
                if self.class_sz[self.find(p)] > self.class_sz[self.find(q)]:
                    self.class_dict[q] = self.find(p)
                    self.class_sz[self.find(p)] += self.class_sz[self.find(q)]
                else:
                    self.class_dict[p] =self.find(q)
                    self.class_sz[self.find(q)] += self.class_sz[self.find(p)]
                # count存放有几个树
                self.count -= 1

    def get_union_list(self):
        """实现思路，基于根节点去分类，class_dict存放每个node，对应所在树根节点。
            """
        root_dict = {}
        # 先找出根节点，存储
        for value, root in self.class_dict.items():
            if value == root:
                root_dict[root] = set([])

        # 然后遍历每个node的根节点，添加元素
        for value, root in self.class_dict.items():
            root_dict[self.find(value)].add(value)
        return root_dict

def create_test_data():
    #test_data = [["a","b","d"],["e","h"],["c","b","d"],["g"],["d","e"]]
    test_data = [("4", "3"),("3", "8"), ("6", "5"),("9", "4"),("2", "1"),("8", "9"),("5", "0"),("7", "2"),("6", "1"),("1", "0"), ("6", "7")]
    return test_data

def trans_tuple(test_data):
    """[[1,2,3],[],[]]->[(1,2),(2,3),()]"""
    result_data = set([])
    for item in test_data:
        for index in range(0,len(item)-1):
            result_data.add((item[index],item[index+1]))
    return result_data

if __name__ == "__main__":
    test_data = create_test_data()
    tuple_data = trans_tuple(test_data)
    union_class = UnionFind(tuple_data)
    union_class.union_fun(tuple_data)
    print(union_class.get_union_list())














