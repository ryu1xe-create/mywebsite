import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from manga_app.models import CustomUser, Manga, Chapter, Anime, Episode, Review

# 1. Админ болон хэрэглэгчид үүсгэх
admin_user, _ = CustomUser.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@animanga.com', 'is_staff': True, 'is_superuser': True}
)
admin_user.set_password('admin123')
admin_user.save()

demo_user, _ = CustomUser.objects.get_or_create(
    username='otaku_boy',
    defaults={'email': 'otaku@animanga.com', 'bio': 'Аниме, манга сонирхогч'}
)
demo_user.set_password('user123')
demo_user.save()

print("✅ Хэрэглэгчид үүссэн (Admin: admin/admin123, User: otaku_boy/user123)")

# 2. Алдартай мангануудын мэдээлэл
mangas_data = [
    {
        'title': 'One Piece',
        'author': 'Eiichiro Oda',
        'summary': 'Манганы хаан болох хүсэлтэй Монки Д. Луффи болон түүний Далайн дээрэмчдийн багийн адал явдал.',
    },
    {
        'title': 'Naruto',
        'author': 'Masashi Kishimoto',
        'summary': 'Тосгоныхоо хамгийн шилдэг Хокагэ болохыг мөрөөддөг залуу нинжа Нарутогийн түүх.',
    },
    {
        'title': 'Attack on Titan',
        'author': 'Hajime Isayama',
        'summary': 'Үлэмж биетэн титануудаас хүн төрөлхтнийг хамгаалах залуус болон Эрен Йегерийн тэмцэл.',
    },
    {
        'title': 'Jujutsu Kaisen',
        'author': 'Gege Akutami',
        'summary': 'Хараалтай хурууг залгиснаар хараалын ертөнцөд хөл тавих Итадори Южигийн түүх.',
    },
    {
        'title': 'Demon Slayer',
        'author': 'Koyoharu Gotouge',
        'summary': 'Гэр бүлийг нь хөнөөсөн чөтгөрүүдээс дүүгээ аврахын тулд тэмцэх Танжирогийн аялал.',
    },
    {
        'title': 'Berserk',
        'author': 'Kentaro Miura',
        'summary': 'Хар баатар Гатсын харанхуй, харгис ертөнц дэх өшөө авалт ба тэмцэл.',
    }
]

for item in mangas_data:
    manga, created = Manga.objects.get_or_create(
        title=item['title'],
        defaults={
            'author': item['author'],
            'summary': item['summary'],
            'created_by': admin_user
        }
    )
    if created:
        # Chapter үүсгэх
        Chapter.objects.create(
            manga=manga,
            chapter_number=1,
            title='Эхлэл',
            content_images_folder='chapters/ch1'
        )
        # Сэтгэгдэл болон үнэлгээ үүсгэх
        Review.objects.create(
            manga=manga,
            user=demo_user,
            score=5,
            comment=f"{manga.title} үнэхээр агуу манга! Заавал уншаарай."
        )
        print(f"✅ Амжилттай нэмэгдлээ: {manga.title}")

print("\n🎉 Бүх дата амжилттай оруулж дууслаа!")