"""
MomentsShare 完整测试数据生成脚本

功能：
1. 创建测试用户（包含已知账号密码）
2. 建立好友关系（发起申请、接受申请）
3. 发布动态（从网络下载真实图片/视频）
4. 创建评论、点赞、评分等互动数据
5. 支持首次启动自动执行

使用方式：
    python manage.py seed_data          # 正常执行
    python manage.py seed_data --force  # 强制重新生成（清除旧数据）
"""

import os
import random
import tempfile
import urllib.request
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from users.models import User
from moments.models import Moment, Image, Tag
from friends.models import Friendship
from interactions.models import Comment, Like, Rating, Message


# ========== 测试用户配置 ==========
TEST_USERS = [
    # 管理员账号
    {
        "phone": "13500000000",
        "username": "admin",
        "nickname": "管理员",
        "password": "admin123",
        "avatar_seed": "admin",
        "is_staff": True,
        "is_superuser": True
    },
    # 普通用户账号
    {
        "phone": "13800000001",
        "username": "alice",
        "nickname": "爱丽丝",
        "password": "Test123456",
        "avatar_seed": "alice"
    },
    {
        "phone": "13800000002",
        "username": "bob",
        "nickname": "鲍勃",
        "password": "Test123456",
        "avatar_seed": "bob"
    },
    {
        "phone": "13800000003",
        "username": "charlie",
        "nickname": "查理",
        "password": "Test123456",
        "avatar_seed": "charlie"
    },
    {
        "phone": "13800000004",
        "username": "diana",
        "nickname": "戴安娜",
        "password": "Test123456",
        "avatar_seed": "diana"
    },
    {
        "phone": "13800000005",
        "username": "evan",
        "nickname": "伊万",
        "password": "Test123456",
        "avatar_seed": "evan"
    },
    {
        "phone": "13800000006",
        "username": "fiona",
        "nickname": "菲奥娜",
        "password": "Test123456",
        "avatar_seed": "fiona"
    },
    {
        "phone": "13800000007",
        "username": "george",
        "nickname": "乔治",
        "password": "Test123456",
        "avatar_seed": "george"
    },
    {
        "phone": "13800000008",
        "username": "helen",
        "nickname": "海伦",
        "password": "Test123456",
        "avatar_seed": "helen"
    },
]

# ========== 动态内容配置 ==========
MOMENT_CONTENTS = [
    {"content": "今天天气真不错，出来散散心！🌞", "tags": ["日常", "心情"]},
    {"content": "终于下班了，累死我了，需要大餐犒劳一下！🍔", "tags": ["美食", "日常"]},
    {"content": "路边的猫咪好可爱，忍不住拍了一张。🐱", "tags": ["宠物", "萌宠"]},
    {"content": "周末去爬山，风景独好，推荐大家也去！⛰️", "tags": ["旅行", "风景"]},
    {"content": "打卡一家网红店，味道一般，但是拍照很好看。📸", "tags": ["美食", "打卡"]},
    {"content": "生活不仅有眼前的苟且，还有诗和远方。✨", "tags": ["心情", "文艺"]},
    {"content": "熬夜写代码，这就是程序员的浪漫吗？💻", "tags": ["程序员", "工作"]},
    {"content": "心情不好，求安慰...😔", "tags": ["心情"]},
    {"content": "新买的咖啡机到了，自己在家做拿铁☕", "tags": ["咖啡", "生活"]},
    {"content": "今天学会了一道新菜，成就感满满！👨‍🍳", "tags": ["美食", "学习"]},
    {"content": "公司团建去了海边，玩得很开心🏖️", "tags": ["旅行", "团建"]},
    {"content": "读完了一本好书，强烈推荐《三体》📚", "tags": ["读书", "推荐"]},
    {"content": "健身房打卡第30天，坚持就是胜利💪", "tags": ["健身", "运动"]},
    {"content": "和老朋友见面，聊了一下午，很开心😊", "tags": ["朋友", "日常"]},
    {"content": "新入手的相机，拍照效果太棒了📷", "tags": ["摄影", "数码"]},
    {"content": "看了场电影，剧情很感人🎬", "tags": ["电影", "娱乐"]},
    {"content": "周末在家做甜点，草莓蛋糕成功了🍓", "tags": ["美食", "烘焙"]},
    {"content": "加班到深夜，明天继续努力💼", "tags": ["工作", "加班"]},
    {"content": "收到了朋友送的礼物，好感动🎁", "tags": ["友情", "感动"]},
    {"content": "夕阳无限好，只是近黄昏🌅", "tags": ["风景", "文艺"]},
]

# ========== 评论内容配置 ==========
COMMENTS = [
    "哇，太棒了！👍",
    "羡慕啊～",
    "同款！我也想要",
    "好美的图片！",
    "加油！",
    "哈哈哈笑死我了",
    "真的吗？太厉害了",
    "下次带上我",
    "这家店在哪里？",
    "看起来很好吃的样子",
    "支持你！",
    "辛苦了～",
    "真羡慕你的生活",
    "我也想去",
    "666",
    "太有才了",
    "学习了",
    "很有共鸣",
    "棒棒的！",
    "期待你的下一条动态",
]

REPLY_COMMENTS = [
    "谢谢支持！❤️",
    "哈哈是的～",
    "下次一起！",
    "改天约",
    "你也可以的！",
    "过奖了～",
    "确实不错",
    "我也觉得",
]

# ========== 私信内容配置 ==========
MESSAGE_CONTENTS = [
    "在吗？",
    "你好呀～",
    "最近怎么样？",
    "周末有空吗？",
    "看到你发的动态了，太棒了！",
    "好久不见，最近忙什么呢？",
    "今天天气真好",
    "晚上一起吃饭？",
    "谢谢你的点赞！",
    "有空出来玩吗？",
    "刚看到一个好玩的地方，改天带你去",
    "哈哈哈，太搞笑了",
    "收到，没问题！",
    "好的好的",
    "明白了～",
]

MESSAGE_REPLIES = [
    "在呢，怎么了？",
    "你好！",
    "还行，有点忙",
    "可以呀，有什么安排？",
    "谢谢～",
    "是呀，好久没见了",
    "确实！",
    "好呀，去哪吃？",
    "不客气！",
    "好啊，去哪里？",
    "太期待了！",
    "哈哈哈",
    "好的～",
    "OK！",
    "了解～",
]

# ========== 图片资源配置 ==========
# 使用 picsum.photos 和 unsplash source 获取真实图片
IMAGE_URLS = [
    "https://picsum.photos/800/600?random=1",
    "https://picsum.photos/800/600?random=2",
    "https://picsum.photos/800/600?random=3",
    "https://picsum.photos/800/600?random=4",
    "https://picsum.photos/800/600?random=5",
    "https://picsum.photos/800/600?random=6",
    "https://picsum.photos/800/600?random=7",
    "https://picsum.photos/800/600?random=8",
    "https://picsum.photos/800/600?random=9",
    "https://picsum.photos/800/600?random=10",
    "https://picsum.photos/600/800?random=11",
    "https://picsum.photos/600/800?random=12",
    "https://picsum.photos/800/800?random=13",
    "https://picsum.photos/800/800?random=14",
    "https://picsum.photos/1200/800?random=15",
]

# 头像使用 DiceBear API
def get_avatar_url(seed):
    return f"https://api.dicebear.com/7.x/avataaars/png?seed={seed}&size=200"

# 示例视频 URL（使用小尺寸示例视频）
VIDEO_URLS = [
    "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4",
    "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_2mb.mp4",
]


class Command(BaseCommand):
    help = '生成完整的测试数据，包括用户、好友关系、动态、评论、点赞等'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制重新生成数据（清除旧数据）',
        )
        parser.add_argument(
            '--skip-media',
            action='store_true',
            help='跳过下载媒体文件（加速测试）',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        skip_media = options.get('skip_media', False)
        
        # 检查是否已有测试数据
        if not force and self._check_seed_data_exists():
            self.stdout.write(self.style.WARNING('⚠️ 测试数据已存在，跳过生成。使用 --force 强制重新生成。'))
            return
        
        self.stdout.write(self.style.NOTICE('🚀 开始生成测试数据...'))
        
        try:
            with transaction.atomic():
                if force:
                    self._clean_data()
                
                users = self._create_users(skip_media)
                self._create_friendships(users)
                moments = self._create_moments(users, skip_media)
                self._create_interactions(users, moments)
                self._create_messages(users)
                self._mark_seed_complete()
                
            self.stdout.write(self.style.SUCCESS('🎉 测试数据生成完成！'))
            self._print_summary(users)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ 生成数据失败: {str(e)}'))
            import traceback
            traceback.print_exc()

    def _check_seed_data_exists(self):
        """检查是否已存在测试数据"""
        seed_marker = Path(settings.BASE_DIR) / '.seed_complete'
        if seed_marker.exists():
            return True
        # 也检查是否存在测试用户
        return User.objects.filter(phone__startswith='1380000000').exists()

    def _mark_seed_complete(self):
        """标记种子数据已完成"""
        seed_marker = Path(settings.BASE_DIR) / '.seed_complete'
        seed_marker.touch()

    def _clean_data(self):
        """清理旧数据"""
        self.stdout.write('  🧹 清理旧数据...')
        # 按依赖顺序删除
        Message.objects.all().delete()
        Like.objects.all().delete()
        Rating.objects.all().delete()
        Comment.objects.all().delete()
        Image.objects.all().delete()
        Moment.objects.all().delete()
        Friendship.objects.all().delete()
        # 只删除测试用户
        User.objects.filter(phone__startswith='1380000000').delete()
        Tag.objects.all().delete()
        # 删除标记文件
        seed_marker = Path(settings.BASE_DIR) / '.seed_complete'
        if seed_marker.exists():
            seed_marker.unlink()
        self.stdout.write('  ✅ 旧数据清理完成')

    def _download_image(self, url, timeout=10):
        """从URL下载图片"""
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'    ⚠️ 下载图片失败 {url}: {str(e)}'))
            return None

    def _download_video(self, url, timeout=30):
        """从URL下载视频"""
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'    ⚠️ 下载视频失败: {str(e)}'))
            return None

    def _create_users(self, skip_media=False):
        """创建测试用户"""
        self.stdout.write('  👥 创建测试用户...')
        users = []
        
        for user_data in TEST_USERS:
            # 提取额外的字段
            is_staff = user_data.pop('is_staff', False)
            is_superuser = user_data.pop('is_superuser', False)
            avatar_seed = user_data.pop('avatar_seed', None)
            
            user, created = User.objects.get_or_create(
                phone=user_data['phone'],
                defaults={
                    'username': user_data['username'],
                    'nickname': user_data['nickname'],
                    'is_staff': is_staff,
                    'is_superuser': is_superuser
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                
                # 下载并设置头像
                if not skip_media and avatar_seed:
                    avatar_url = f"https://api.dicebear.com/7.x/avataaars/png?seed={avatar_seed}"
                    avatar_content = self._download_image(avatar_url)
                    if avatar_content:
                        user.avatar.save(f"{user.username}_avatar.png", ContentFile(avatar_content))
                
                self.stdout.write(self.style.SUCCESS(f'    ✅ 创建用户: {user.nickname} ({user.phone})'))
            else:
                # 即使已存在，也更新权限字段
                if is_staff != user.is_staff or is_superuser != user.is_superuser:
                    user.is_staff = is_staff
                    user.is_superuser = is_superuser
                    user.save()
                self.stdout.write(f'    ℹ️ 用户已存在: {user.nickname}')
            
            users.append(user)
        
        self.stdout.write(f'  ✅ 用户创建完成，共 {len(users)} 个')
        return users

    def _create_friendships(self, users):
        """创建好友关系"""
        self.stdout.write('  🤝 创建好友关系...')
        
        # 定义好友关系图：每个用户和哪些用户成为好友
        # 用户索引: 0=alice, 1=bob, 2=charlie, 3=diana, 4=evan, 5=fiona, 6=george, 7=helen
        friend_pairs = [
            (0, 1),  # alice - bob
            (0, 2),  # alice - charlie
            (0, 3),  # alice - diana
            (1, 2),  # bob - charlie
            (1, 4),  # bob - evan
            (2, 3),  # charlie - diana
            (2, 5),  # charlie - fiona
            (3, 6),  # diana - george
            (4, 5),  # evan - fiona
            (4, 7),  # evan - helen
            (5, 6),  # fiona - george
            (6, 7),  # george - helen
        ]
        
        # 待处理的好友请求（用于测试待处理功能）
        pending_pairs = [
            (7, 0),  # helen 向 alice 发送请求（待处理）
            (6, 1),  # george 向 bob 发送请求（待处理）
        ]
        
        # 创建已接受的好友关系
        for from_idx, to_idx in friend_pairs:
            from_user = users[from_idx]
            to_user = users[to_idx]
            
            friendship, created = Friendship.objects.get_or_create(
                from_user=from_user,
                to_user=to_user,
                defaults={'status': Friendship.Status.ACCEPTED}
            )
            if created:
                self.stdout.write(f"    ✅ 好友关系: {from_user.nickname} ↔ {to_user.nickname}")
        
        # 创建待处理的好友请求
        for from_idx, to_idx in pending_pairs:
            from_user = users[from_idx]
            to_user = users[to_idx]
            
            friendship, created = Friendship.objects.get_or_create(
                from_user=from_user,
                to_user=to_user,
                defaults={'status': Friendship.Status.PENDING}
            )
            if created:
                self.stdout.write(f"    ⏳ 待处理请求: {from_user.nickname} → {to_user.nickname}")
        
        self.stdout.write(f'  ✅ 好友关系创建完成')

    def _create_moments(self, users, skip_media=False):
        """创建动态"""
        self.stdout.write('  📝 创建动态...')
        moments = []
        image_index = 0
        video_index = 0
        
        # 每个用户创建2-4条动态
        for user in users:
            num_moments = random.randint(2, 4)
            
            for _ in range(num_moments):
                content_data = random.choice(MOMENT_CONTENTS)
                moment_type = random.choices(
                    ['IMAGE', 'VIDEO'],
                    weights=[85, 15],  # 85%图片，15%视频
                    k=1
                )[0]
                
                # 创建动态
                moment = Moment.objects.create(
                    author=user,
                    content=content_data['content'],
                    type=moment_type,
                    video_status=Moment.VideoStatus.READY
                )
                
                # 添加标签
                for tag_name in content_data['tags']:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    moment.tags.add(tag)
                
                # 处理媒体文件
                if moment_type == 'IMAGE':
                    num_images = random.randint(1, 4)
                    for img_order in range(1, num_images + 1):
                        if not skip_media:
                            url = IMAGE_URLS[image_index % len(IMAGE_URLS)]
                            image_index += 1
                            image_data = self._download_image(url)
                            
                            if image_data:
                                img = Image(moment=moment, order=img_order)
                                img.image_file.save(
                                    f"moment_{moment.id}_img_{img_order}.jpg",
                                    ContentFile(image_data),
                                    save=True
                                )
                        else:
                            # 跳过媒体时创建空图片记录
                            Image.objects.create(moment=moment, order=img_order)
                
                elif moment_type == 'VIDEO':
                    if not skip_media and VIDEO_URLS:
                        url = VIDEO_URLS[video_index % len(VIDEO_URLS)]
                        video_index += 1
                        video_data = self._download_video(url)
                        
                        if video_data:
                            moment.video_file.save(
                                f"moment_{moment.id}_video.mp4",
                                ContentFile(video_data),
                                save=True
                            )
                    moment.video_status = Moment.VideoStatus.READY
                    moment.save()
                
                moments.append(moment)
                self.stdout.write(f"    ✅ 动态: {user.nickname} - {moment_type} - {content_data['content'][:20]}...")
        
        self.stdout.write(f'  ✅ 动态创建完成，共 {len(moments)} 条')
        return moments

    def _create_interactions(self, users, moments):
        """创建互动数据（评论、点赞、评分）"""
        self.stdout.write('  💬 创建互动数据...')
        
        comment_count = 0
        like_count = 0
        rating_count = 0
        
        for moment in moments:
            # 随机选择一些用户进行互动
            interacting_users = random.sample(users, k=random.randint(2, min(6, len(users))))
            
            for user in interacting_users:
                # 跳过作者自己的部分互动
                if user == moment.author and random.random() > 0.3:
                    continue
                
                # 点赞（60%概率）
                if random.random() < 0.6:
                    Like.objects.get_or_create(moment=moment, user=user)
                    like_count += 1
                
                # 评分（40%概率）
                if random.random() < 0.4:
                    Rating.objects.update_or_create(
                        moment=moment,
                        user=user,
                        defaults={'score': random.randint(3, 5)}
                    )
                    rating_count += 1
                
                # 评论（50%概率）
                if random.random() < 0.5:
                    comment = Comment.objects.create(
                        moment=moment,
                        author=user,
                        content=random.choice(COMMENTS)
                    )
                    comment_count += 1
                    
                    # 作者回复评论（30%概率）
                    if random.random() < 0.3 and user != moment.author:
                        Comment.objects.create(
                            moment=moment,
                            author=moment.author,
                            content=random.choice(REPLY_COMMENTS),
                            parent=comment
                        )
                        comment_count += 1
        
        self.stdout.write(f'  ✅ 互动数据创建完成: {comment_count} 评论, {like_count} 点赞, {rating_count} 评分')

    def _create_messages(self, users):
        """创建私信数据"""
        self.stdout.write('  💬 创建私信数据...')
        
        message_count = 0
        
        # 好友对之间创建私信
        friend_pairs = [
            (0, 1),  # alice - bob
            (0, 2),  # alice - charlie
            (1, 4),  # bob - evan
            (2, 5),  # charlie - fiona
            (4, 7),  # evan - helen
        ]
        
        for from_idx, to_idx in friend_pairs:
            user1 = users[from_idx]
            user2 = users[to_idx]
            
            # 创建2-4轮对话
            num_rounds = random.randint(2, 4)
            for _ in range(num_rounds):
                # user1 发消息给 user2
                Message.objects.create(
                    sender=user1,
                    receiver=user2,
                    content=random.choice(MESSAGE_CONTENTS),
                    is_read=True
                )
                message_count += 1
                
                # user2 回复 user1
                Message.objects.create(
                    sender=user2,
                    receiver=user1,
                    content=random.choice(MESSAGE_REPLIES),
                    is_read=random.choice([True, False])
                )
                message_count += 1
        
        # 给 alice 添加一些未读消息用于测试
        alice = users[0]
        bob = users[1]
        Message.objects.create(
            sender=bob,
            receiver=alice,
            content="在吗？有事找你",
            is_read=False
        )
        message_count += 1
        
        self.stdout.write(f'  ✅ 私信数据创建完成: {message_count} 条消息')

    def _print_summary(self, users):
        """打印测试账号汇总"""
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('📋 测试账号汇总'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write('  手机号            用户名      昵称        密码')
        self.stdout.write('  ' + '-' * 54)
        
        for user_data in TEST_USERS:
            self.stdout.write(
                f"  {user_data['phone']}    {user_data['username']:<10}  "
                f"{user_data['nickname']:<10}  {user_data['password']}"
            )
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('💡 推荐测试账号: alice (13800000001) / Test123456'))
        self.stdout.write(self.style.SUCCESS('   该账号有多个好友和动态，适合测试大部分功能'))
        self.stdout.write('')