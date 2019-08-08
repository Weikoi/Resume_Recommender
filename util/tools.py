def pretty_dict(obj, indent=' '):
    def _pretty(obj, indent):
        for i, tup in enumerate(obj.items()):
            k, v = tup
            # 如果是字符串则拼上""
            if isinstance(k, str):
                k = '"%s"' % k
            if isinstance(v, str):
                v = '"%s"' % v
            # 如果是字典则递归
            if isinstance(v, dict):
                v = ''.join(_pretty(v, indent + ' ' * len(str(k) + ': {')))  # 计算下一层的indent
            # case,根据(k,v)对在哪个位置确定拼接什么
            if i == 0:  # 开头,拼左花括号
                if len(obj) == 1:
                    yield ('{%s: %s}' % (k, v))
                else:
                    yield ('{%s: %s,\n' % (k, v))
            elif i == len(obj) - 1:  # 结尾,拼右花括号
                yield ('%s%s: %s}' % (indent, k, v))
            else:  # 中间
                yield ('%s%s: %s,\n' % (indent, k, v))

    print(''.join(_pretty(obj, indent)))
