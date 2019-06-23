#coding:utf-8


class Node():
    """
    定义树结构
    """

    def __init__(self, char):
        self.children = {}
        self.char = char
        self.string = ""
        self.fail = None


def create_tree(data_list):
    """
    生成前缀树
    """
    root = Node("")
    for item_str in data_list:
        tmp = root
        for item_char in item_str:
            if item_char not in tmp.children:
                tmp.children[item_char] = Node(item_char)
            tmp = tmp.children[item_char]

        tmp.string = item_str
    return root


def walk_tree(root):
    """
    基于队列遍历树结果，广度优先输出节点值
    """
    queue = []
    queue.append(root)
    while (len(queue) != 0):
        tmp = queue.pop()
        for item, item_node in tmp.children.items():
            print(item, item_node.string)
            queue.insert(-1, item_node)


def make_fail(root):
    """
    创建fail指针对于每个节点:加入父节点的fail指针可以通过节点上的字符转移，那fail指针指向转移后的节点。如果不能通过转移，则继续查找该fail节点指向的fail指针。（实质是寻找个公共子串，是该节点的最大后缀，并且为根节点的最大前缀）
    """
    # 建立队列，广度遍历树节点，树的第一层fail指向根节点。因为依赖父节点的fail，所以遍历child
    # 赋初值
    queue = []
    queue.insert(-1, root)
    root.fail = root

    while (len(queue) != 0):
        temp = queue.pop()
        # 遍历child
        for item_str, item_node in temp.children.items():
            queue.insert(-1, item_node)
            # 看是否第一层节点
            if temp == root:
                item_node.fail = root

            else:
                # 从父节点的fail开始迭代
                iter_fail = temp.fail
                while 1:
                    # 如果可以从fail下成功转移，赋值fail
                    if (item_str in iter_fail.children):
                        item_node.fail = iter_fail.children[item_str]
                        break
                    # 如果不能成功转移，则迭代遍历。假如fail指向根节点，上面的也没有break证明已经失配，则赋初值
                    else:
                        if iter_fail == root:
                            item_node.fail = root
                            break
                        else:
                            iter_fail = iter_fail.fail
    return root


# 开始匹配某个字符串，需要find函数
def find(root, input_str):
    """
    匹配输入字符串，实质就是自动机转移的过程，当字符串不在child中，转移到fail节点上，每遍历一个状态判断一下是否有string（匹配的字符串），有则保存。
    停止匹配当前字符（i+=1）的条件是匹配节点成功或者匹配失败（不在根节点的孩子节点中）
    """
    re_string = []
    tmp = root
    i = 0
    while (i < len(input_str)):
        #for i in range(0, len(input_str)):
        if input_str[i] in tmp.children:
            tmp = tmp.children[input_str[i]]
            i += 1
        elif tmp == root:
            i += 1
        else:
            tmp = tmp.fail

        if tmp.string:
            print(i - len(tmp.string), i)
            re_string.append(tmp.string)

    print(re_string)
    return re_string


if __name__ == "__main__":
    data_list = ["abc", "she", "sh", "hi"]
    root = create_tree(data_list)
    root = make_fail(root)
    find(root, "sabcshehi")
    #walk_tree(root)
    #print(root.children)
    #for i in root.children:
    #    print(root.children.get(i).children)
