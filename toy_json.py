from typing import Union

whitespace = (' ', '\t', '\r', '\n')


def decode(s: str) -> Union[dict, list, int, float, str, None, bool]:
    """
    基本元素：string, number, whitespace, bool, None
    组合：object, list, value
    :param s:
    :return:
    """

    def parse_object() -> dict:
        nonlocal i
        res = dict()
        i += 1
        while i < n and s[i] != '}':
            parse_whitespace()
            name = parse_string()
            parse_whitespace()
            if i < n and s[i] == ':':
                i += 1
                res[name] = parse_value()
            else:
                raise err

        if i == n:
            raise err

        i += 1
        return res

    def parse_array() -> list:
        nonlocal i
        i += 1
        parse_whitespace()
        res = []
        while i < n and s[i] != ']':
            res.append(parse_value())
            if i < n and s[i] == ',':
                i += 1
        if i == n:
            raise err

        i += 1
        return res

    def parse_number() -> Union[int, float]:
        """
        返回number值 会移动index
        :return:
        """
        nonlocal i
        neg = False
        if s[i] == '-':
            i += 1
            neg = True

        res = 0
        if i >= n or (neg and s[i] == '0'):
            raise err

        while i < n and '0' <= s[i] <= '9':
            res = res * 10 + int(s[i])
            i += 1

        if i < n and s[i] == '.':
            i += 1
            while i < n and '0' <= s[i] <= '9':
                res = (res * 10 + int(s[i])) / 10
                i += 1

        exp, exp_neg = 0, False
        if i < n and s[i] in ('e', 'E'):
            i += 1
            if i < n and s[i] == '-':
                exp_neg = True
                i += 1
            while i < n and '0' <= s[i] <= '9':
                exp = exp * 10 + int(s[i])
                i += 1
            exp = exp if not exp_neg else -exp
        if i < n and s[i] in ('e', 'E', '-'):
            raise err

        return res * 10**exp






    def parse_other() -> Union[bool, None]:
        """
        返回true false或null 会移动index
        :return:
        """
        nonlocal i
        if s[i:i+4] == 'true':
            i += 4
            return True

        if s[i:i+5] == 'false':
            i += 5
            return False

        if s[i:i+4] == 'null':
            i += 4
            return None

        raise err

    def parse_string() -> str:
        """
        返回string值 会移动index
        :return:
        """
        nonlocal i
        i += 1
        res = []
        while i < n and s[i] != '"':
            if s[i] != '\\':
                res.append(s[i])
                i += 1
            else:
                c, w = escape()
                res.append(c)
                i += w

        if i == n:
            raise err

        # s[i] == '"'
        i += 1

        return ''.join(res)

    def parse_whitespace():
        # \t \n \r " " * n
        nonlocal i
        if i >= n:
            return
        if s[i] in whitespace:
            i += 1
            return parse_whitespace()

        c, w = escape()
        if c in whitespace:
            i += w
            return parse_whitespace()

        return

    def escape() -> tuple[str, int]:
        """
        获取转义后字符
        :return: 转义后字符改字符所占字符数
        """
        if s[i] != '\\':
            return None, 0

        if i + 1 >= n:
            raise err

        if s[i + 1] == '"':
            return '"', 2
        elif s[i + 1] == '\\':
            return '"', 2
        elif s[i + 1] == '/':
            return '/', 2
        elif s[i + 1] == 'f':
            return '\f', 2
        elif s[i + 1] == 'n':
            return '\n', 2
        elif s[i + 1] == 'r':
            return '\r', 2
        elif s[i + 1] == 't':
            return '\t', 2
        elif s[i + 1] == 'u':
            if i + 5 >= n:
                raise err

            return chr(int(s[i + 2:i + 6], base=16)), 6

    def parse_value():
        # 处理tokens之间的空白
        parse_whitespace()
        if i >= n:
            raise ValueError()

        if s[i] == '"':
            value = parse_string()
        elif s[i] == '[':
            value = parse_array()
        elif s[i] == '{':
            value = parse_object()
        elif s[i] == '-' or '0' <= s[i] <= '9':
            value = parse_number()
        else:
            value = parse_other()

        parse_whitespace()
        return value

    err = ValueError("json str incorrect.")
    i, n = 0, len(s)
    return parse_value()


if __name__ == '__main__':
    s = '1'
    s = '{"a":1}'
    s = '[1, "a"]'
    s = '[{"a":1},[2,3,4.5,["eeee"]]]'
    print(decode(s))
