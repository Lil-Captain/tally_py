
class StringUtil:
    @classmethod
    def snake_to_camel(cls, snake_str):
        components = snake_str.split('_')
        # 第一个单词保持小写，后续单词首字母大写
        return components[0] + ''.join(x.title() for x in components[1:])