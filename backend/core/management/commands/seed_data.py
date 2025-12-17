import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
# 引入你的业务模型 (根据Wiki中的表名推测，如果报错需核对代码中的类名)
from moments.models import Moment  # 假设动态模型叫 Moment
from interactions.models import Comment # 假设评论模型叫 Comment

User = get_user_model()

class Command(BaseCommand):
    help = '生成测试数据 (Users, Moments, Comments)'

    def handle(self, *args, **kwargs):
        self.stdout.write('正在初始化造数引擎...')
        fake = Faker('zh_CN')  # 使用中文生成器

        # ==========================================
        # 1. 生成用户 (Users)
        # ==========================================
        self.stdout.write('Step 1: 正在生成 50 个虚拟用户...')
        existing_phones = set(User.objects.values_list('phone', flat=True))
        
        users = []
        for _ in range(50):
            # 生成唯一的手机号
            while True:
                phone = fake.phone_number()
                if phone not in existing_phones:
                    existing_phones.add(phone)
                    break
            
            user = User(
                phone=phone,
                username=fake.user_name() + str(random.randint(1000, 9999)),
                nickname=fake.name(),
                password='pbkdf2_sha256$...' # 这里的密码无法直接登录，仅占位。如需登录请用 createsuperuser 的账号
            )
            # 设置统一密码 123456
            user.set_password('123456')
            users.append(user)
        
        # 批量插入数据库 (比一个个save快100倍)
        User.objects.bulk_create(users, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'成功生成 {len(users)} 个用户!'))

        # ==========================================
        # 2. 生成动态 (Moments)
        # ==========================================
        self.stdout.write('Step 2: 正在生成 200 条动态...')
        all_users = list(User.objects.all())
        moments = []
        
        # 模拟一些真实的文案
        sample_texts = [
            "今天天气真不错！", "打卡网红店，味道一般。", "刚下班，好累啊。", 
            "分享一首好听的歌。", "周末去哪里玩比较好？", "新买的相机到了！",
            "为了梦想，继续前行！", "好久不见的老朋友。", "这就是生活。", "早安，打工人！"
        ]

        for _ in range(200):
            author = random.choice(all_users)
            content = fake.text(max_nb_chars=100) + " " + random.choice(sample_texts)
            
            # 随机决定是图文还是视频 (80%图文, 20%视频)
            moment_type = 'IMAGE' if random.random() < 0.8 else 'VIDEO'
            
            moment = Moment(
                author=author,
                content=content,
                type=moment_type,
                # 这里暂时不放真实图片文件，只留空，或者你可以指向一个静态默认图
            )
            moments.append(moment)
            
        Moment.objects.bulk_create(moments)
        self.stdout.write(self.style.SUCCESS(f'成功生成 {len(moments)} 条动态!'))

        # ==========================================
        # 3. 生成评论 (Comments)
        # ==========================================
        self.stdout.write('Step 3: 正在生成 500 条评论...')
        all_moments = list(Moment.objects.all())
        comments = []

        for _ in range(500):
            author = random.choice(all_users)
            moment = random.choice(all_moments)
            
            comment = Comment(
                author=author,
                moment=moment,
                content=fake.sentence()
            )
            comments.append(comment)
            
        Comment.objects.bulk_create(comments)
        self.stdout.write(self.style.SUCCESS(f'成功生成 {len(comments)} 条评论!'))
        
        self.stdout.write(self.style.SUCCESS('----------------------------------'))
        self.stdout.write(self.style.SUCCESS('所有数据生成完毕！Mission Complete!'))