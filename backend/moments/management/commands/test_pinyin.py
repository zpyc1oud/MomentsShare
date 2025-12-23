"""
测试拼音匹配功能的命令
用法: python manage.py test_pinyin <查询词> <文本>
"""
from django.core.management.base import BaseCommand
from moments.utils import match_pinyin, get_pinyin, get_pinyin_initials, PYPINYIN_AVAILABLE


class Command(BaseCommand):
    help = '测试拼音匹配功能'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='查询词')
        parser.add_argument('text', type=str, help='要匹配的文本')

    def handle(self, *args, **options):
        query = options['query']
        text = options['text']
        
        self.stdout.write(f"pypinyin可用: {PYPINYIN_AVAILABLE}")
        self.stdout.write(f"查询词: {query}")
        self.stdout.write(f"文本: {text}")
        self.stdout.write("")
        
        if PYPINYIN_AVAILABLE:
            text_pinyin = get_pinyin(text)
            text_initials = get_pinyin_initials(text)
            self.stdout.write(f"文本拼音: {text_pinyin}")
            self.stdout.write(f"文本首字母: {text_initials}")
            self.stdout.write("")
        
        result = match_pinyin(query, text)
        self.stdout.write(f"匹配结果: {result}")

