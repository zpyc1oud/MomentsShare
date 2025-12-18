import random
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth import get_user_model
# 👇 注意这里多导入了一个 Image 模型
from moments.models import Moment, Image 
from faker import Faker

User = get_user_model()

REAL_TEXTS = [
    "今天天气真不错，出来散散心！🌞",
    "终于下班了，累死我了，需要大餐犒劳一下！🍔",
    "路边的猫咪好可爱，忍不住拍了一张。🐱",
    "周末去爬山，风景独好，推荐大家也去！⛰️",
    "打卡一家网红店，味道一般，但是拍照很好看。📸",
    "生活不仅有眼前的苟且，还有诗和远方。✨",
    "熬夜写代码，这就是程序员的浪漫吗？💻",
    "心情不好，求安慰...😔",
]

class Command(BaseCommand):
    help = '生成符合 models.py 定义的真实数据'

    def handle(self, *args, **kwargs):
        self.stdout.write('正在清理旧数据...')
        # 级联删除：删除 Moment 会自动删除关联的 Image
        Moment.objects.all().delete()
        
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('❌ 错误：没有用户数据'))
            return

        samples_dir = '/app/samples'
        images = []
        videos = []

        if os.path.exists(samples_dir):
            files = os.listdir(samples_dir)
            images = [f for f in files if f.endswith(('.jpg', '.png', '.jpeg'))]
            videos = [f for f in files if f.endswith(('.mp4', '.mov'))]
            self.stdout.write(f'✅ 素材库加载成功：{len(images)} 图 / {len(videos)} 视')
        else:
            self.stdout.write(self.style.WARNING(f'❌ 未找到 {samples_dir}，只能生成纯文字'))

        self.stdout.write('正在生成数据...')
        
        for i in range(20):
            author = random.choice(users)
            text = random.choice(REAL_TEXTS)
            m_type = random.choice(['TEXT', 'IMAGE', 'VIDEO'])

            # 降级策略
            if m_type == 'IMAGE' and not images: m_type = 'TEXT'
            if m_type == 'VIDEO' and not videos: m_type = 'TEXT'

            # 1. 先创建动态主体 (Moment)
            moment = Moment(
                author=author, 
                content=text, 
                type=m_type
            )

            try:
                # === 2. 视频处理逻辑 (字段名是 video_file) ===
                if m_type == 'VIDEO':
                    vid_name = random.choice(videos)
                    file_path = os.path.join(samples_dir, vid_name)
                    with open(file_path, 'rb') as f:
                        # save=True 会自动保存 moment 对象
                        moment.video_file.save(f'videos/{vid_name}', File(f), save=True)

                # === 3. 图片处理逻辑 (存入 Image 关联表) ===
                elif m_type == 'IMAGE':
                    # 图片动态必须先保存 moment，获得 ID 后才能创建关联的 Image
                    moment.save() 
                    
                    img_name = random.choice(images)
                    file_path = os.path.join(samples_dir, img_name)
                    
                    with open(file_path, 'rb') as f:
                        # 创建 Image 对象关联到 moment
                        new_img = Image(moment=moment, order=1)
                        # 保存文件到 image_file 字段
                        new_img.image_file.save(f'images/{img_name}', File(f), save=True)
                
                # === 4. 纯文字逻辑 ===
                else:
                    moment.save()

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠️ 第 {i+1} 条数据生成出错: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'🎉 完美生成 20 条数据！前端现在可以看到图片和视频了！'))