# Todo App API

Django REST Framework asosida qurilgan oddiy **Todo (vazifalar) boshqaruvi** API'si. Foydalanuvchilar ro'yxatdan o'tib, token orqali tizimga kiradi, o'z kategoriyalari va vazifalarini yaratadi.

## Imkoniyatlar

- 🔐 Token autentifikatsiyasi (register / login)
- 🗂️ Kategoriyalar — har bir foydalanuvchi uchun alohida, takrorlanmas nom
- ✅ Todo (vazifa) yaratish va ro'yxatini olish
- 🎚️ Vazifa ustuvorligi: `low`, `mid`, `high`
- 📅 Deadline (muddat) qo'yish
- 📖 Swagger / ReDoc orqali avtomatik API hujjatlari

## Texnologiyalar

| Komponent | Versiya |
|-----------|---------|
| Python | 3.x |
| Django | 6.0.4 |
| Django REST Framework | 3.17.1 |
| drf-spectacular | 0.29.0 |
| Ma'lumotlar bazasi | SQLite |

## O'rnatish

```bash
# 1. Loyihani klonlash
git clone <repo-url>
cd todo-app

# 2. Virtual muhit (agar yo'q bo'lsa)
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

# 3. Kutubxonalarni o'rnatish
pip install -r requirements.txt

# 4. Muhit o'zgaruvchilari (.env)
copy .env.example .env          # Windows
# cp .env.example .env          # Linux / macOS
# So'ng .env ichidagi SECRET_KEY va boshqa qiymatlarni to'ldiring

# 5. Migratsiyalar
python manage.py migrate

# 6. Admin foydalanuvchi (ixtiyoriy)
python manage.py createsuperuser

# 7. Serverni ishga tushirish
python manage.py runserver
```

Server `http://127.0.0.1:8000/` manzilida ishga tushadi.

## API hujjatlari

| Manzil | Tavsif |
|--------|--------|
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc |
| `/api/schema/` | OpenAPI sxema (raw) |
| `/admin/` | Django admin paneli |

## API Endpointlar

Barcha endpointlar `/api/v1/` prefiksi bilan boshlanadi.

### Autentifikatsiya

| Metod | Endpoint | Tavsif | Auth |
|-------|----------|--------|------|
| `POST` | `/api/v1/auth/register` | Ro'yxatdan o'tish | ❌ |
| `POST` | `/api/v1/auth/login/` | Tizimga kirish | ❌ |

**Register so'rovi:**
```json
{
  "first_name": "Ali",
  "last_name": "Valiyev",
  "email": "ali@example.com",
  "username": "ali",
  "password": "parol123"
}
```

Javob token qaytaradi. Token'ni keyingi so'rovlarda header'da yuboring:

```
Authorization: Token <sizning_tokeningiz>
```

### Kategoriyalar

| Metod | Endpoint | Tavsif | Auth |
|-------|----------|--------|------|
| `GET` | `/api/v1/category/list/` | Kategoriyalar ro'yxati | ✅ |
| `POST` | `/api/v1/category/create/` | Yangi kategoriya | ✅ |

**Kategoriya yaratish:**
```json
{ "name": "Ish" }
```

### Vazifalar (Todo)

| Metod | Endpoint | Tavsif | Auth |
|-------|----------|--------|------|
| `GET` | `/api/v1/todo/list/` | Vazifalar ro'yxati | ✅ |
| `POST` | `/api/v1/todo/create/` | Yangi vazifa | ✅ |

**Vazifa yaratish:**
```json
{
  "title": "Hisobotni tugatish",
  "description": "Oylik hisobotni yakunlash",
  "priority": "high",
  "deadline": "2026-06-01T12:00:00Z",
  "category_id": 1
}
```

## Ma'lumotlar modeli

**Category**
- `name` — kategoriya nomi (har bir foydalanuvchi uchun takrorlanmas)
- `user` — egasi

**Todo**
- `title`, `description`
- `is_done` — bajarilgan/bajarilmagan
- `priority` — `low` / `mid` / `high` (default: `mid`)
- `deadline` — muddat (ixtiyoriy)
- `category` — bog'langan kategoriya
- `user` — egasi

## Loyiha tuzilishi

```
todo-app/
├── api/                # Asosiy ilova (modellar, view, serializer)
│   ├── models.py       # Category, Todo modellari
│   ├── serializers.py  # DRF serializerlar
│   ├── views.py        # APIView'lar
│   └── urls.py         # API marshrutlari
├── config/             # Django sozlamalari
│   ├── settings.py
│   └── urls.py
├── .env.example        # Muhit o'zgaruvchilari namunasi
├── requirements.txt    # Python bog'liqliklari
├── manage.py
└── db.sqlite3
```

## Eslatmalar

- Sozlamalar `.env` faylidan o'qiladi (`python-dotenv`). `.env` git'ga qo'shilmaydi — har bir muhitda `.env.example` dan nusxa oling.
- `SECRET_KEY` va `DEBUG=True` faqat ishlab chiqish (development) uchun. Production'da `.env` ichida ularni o'zgartiring.
- Har bir foydalanuvchi faqat **o'zining** kategoriya va vazifalarini ko'radi.
