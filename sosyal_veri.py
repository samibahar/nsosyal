"""Demo için küçük ama kalıcı sosyal veri katmanı.

SQLite seçildi: harici servis gerektirmez, yarışma demosunda tekrar üretilebilirdir
ve FastAPI uygulaması tek makinede çalışırken yeterlidir. Bu katman duygu/ranking
modelinden bağımsızdır; yalnızca sosyal uygulama durumunu saklar.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DEMO_KULLANICILAR = {
    "denizcetin": {"ad": "Deniz Çetin", "handle": "@denizcetin", "bas_harf": "DÇ", "bio": "Teknoloji, bilim ve açık kaynak notları.", "renk": "#527da7"},
    "eceyilmaz": {"ad": "Ece Yılmaz", "handle": "@eceyilmaz", "bas_harf": "EY", "bio": "Kültür rotaları, sergiler ve küçük keşifler.", "renk": "#ad657a"},
    "ardaatlas": {"ad": "Arda Atlas", "handle": "@ardaatlas", "bas_harf": "AA", "bio": "Spor, oyun ve her gün biraz hareket.", "renk": "#4d8659"},
    "selinkaya": {"ad": "Selin Kaya", "handle": "@selinkaya", "bas_harf": "SK", "bio": "Kampüs hayatı ve iyi yaşam üzerine.", "renk": "#5b8c7b"},
    "mertdemir": {"ad": "Mert Demir", "handle": "@mertdemir", "bas_harf": "MD", "bio": "Şehir, ekonomi ve gündelik notlar.", "renk": "#9b7049"},
    "emiryusuf": {"ad": "Emir Yusuf", "handle": "@emiryusuf", "bas_harf": "EU", "bio": "NSosyal'de yeni fikirleri takip ediyor.", "renk": "#1f2720"},
}

KONU_YAZARLARI = {
    "teknoloji": "denizcetin", "bilim": "denizcetin", "sanat": "eceyilmaz", "seyahat": "eceyilmaz",
    "spor": "ardaatlas", "oyun": "ardaatlas", "saglik": "selinkaya", "egitim": "selinkaya",
    "gundem": "mertdemir", "ekonomi": "mertdemir",
}

HIKAYELER = [
    ("emiryusuf", "/assets/explore/12-forest.jpg", "Bugün akışta küçük bir mola."),
    ("denizcetin", "/assets/explore/04-laptop.jpg", "Bugün masada küçük bir düzen kurdum."),
    ("eceyilmaz", "/assets/explore/13-sea.jpg", "Sabahın en sessiz saati."),
    ("ardaatlas", "/assets/explore/01-soccer.jpg", "Kısa bir maç arası."),
    ("selinkaya", "/assets/explore/10-library.jpg", "Çalışma molası."),
    ("mertdemir", "/assets/explore/15-market.jpg", "Mahalleden küçük notlar."),
]


class SosyalDepo:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path

    def _baglan(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def hazirla(self, kaynak_gonderiler: list[dict]):
        with self._baglan() as con:
            con.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY, name TEXT NOT NULL, handle TEXT NOT NULL,
                    initials TEXT NOT NULL, bio TEXT NOT NULL, color TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY, topic TEXT NOT NULL, text TEXT NOT NULL,
                    author_id TEXT NOT NULL REFERENCES users(id), created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS follows (
                    follower_id TEXT NOT NULL REFERENCES users(id), following_id TEXT NOT NULL REFERENCES users(id),
                    created_at TEXT NOT NULL, PRIMARY KEY(follower_id, following_id)
                );
                CREATE TABLE IF NOT EXISTS reactions (
                    user_id TEXT NOT NULL REFERENCES users(id), post_id INTEGER NOT NULL REFERENCES posts(id),
                    kind TEXT NOT NULL, created_at TEXT NOT NULL, PRIMARY KEY(user_id, post_id, kind)
                );
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INTEGER NOT NULL REFERENCES posts(id),
                    user_id TEXT NOT NULL REFERENCES users(id), text TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL REFERENCES users(id), actor_id TEXT REFERENCES users(id),
                    post_id INTEGER REFERENCES posts(id), kind TEXT NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS stories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL REFERENCES users(id), media_path TEXT NOT NULL,
                    caption TEXT NOT NULL, position INTEGER NOT NULL
                );
            """)
            for user_id, user in DEMO_KULLANICILAR.items():
                con.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)", (user_id, user["ad"], user["handle"], user["bas_harf"], user["bio"], user["renk"]))
            if con.execute("SELECT COUNT(*) FROM posts").fetchone()[0] == 0:
                now = _simdi()
                con.executemany(
                    "INSERT INTO posts(id, topic, text, author_id, created_at) VALUES (?, ?, ?, ?, ?)",
                    [(post["id"], post["konu"], post["metin"], post.get("yazar") or KONU_YAZARLARI.get(post["konu"], "emiryusuf"), now) for post in kaynak_gonderiler],
                )
            if con.execute("SELECT COUNT(*) FROM stories").fetchone()[0] == 0:
                con.executemany("INSERT INTO stories(user_id, media_path, caption, position) VALUES (?, ?, ?, ?)", [(user, media, caption, position) for position, (user, media, caption) in enumerate(HIKAYELER)])
            elif not con.execute("SELECT 1 FROM stories WHERE user_id = 'emiryusuf'").fetchone():
                con.execute("INSERT INTO stories(user_id, media_path, caption, position) VALUES (?, ?, ?, ?)", HIKAYELER[0] + (0,))

    def gonderileri_yukle(self) -> list[dict]:
        with self._baglan() as con:
            rows = con.execute("SELECT id, topic, text, author_id FROM posts ORDER BY id").fetchall()
        return [{"id": row["id"], "konu": row["topic"], "metin": row["text"], "yazar": row["author_id"]} for row in rows]

    def kullanici(self, user_id: str):
        with self._baglan() as con:
            row = con.execute("SELECT id, name, handle, initials, bio, color FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

    def kullanici_ozeti(self, user_id: str, izleyen: str = "emiryusuf"):
        with self._baglan() as con:
            user = con.execute("SELECT id, name, handle, initials, bio, color FROM users WHERE id = ?", (user_id,)).fetchone()
            if not user:
                return None
            posts = con.execute("SELECT COUNT(*) FROM posts WHERE author_id = ?", (user_id,)).fetchone()[0]
            followers = con.execute("SELECT COUNT(*) FROM follows WHERE following_id = ?", (user_id,)).fetchone()[0]
            following = con.execute("SELECT COUNT(*) FROM follows WHERE follower_id = ?", (user_id,)).fetchone()[0]
            follows = bool(con.execute("SELECT 1 FROM follows WHERE follower_id = ? AND following_id = ?", (izleyen, user_id)).fetchone())
        return {**dict(user), "post_count": posts, "followers": followers, "following": following, "following_by_viewer": follows}

    def post_ozellikleri(self, post_id: int, izleyen: str = "emiryusuf"):
        with self._baglan() as con:
            reaction_count = con.execute("SELECT COUNT(*) FROM reactions WHERE post_id = ?", (post_id,)).fetchone()[0]
            comment_count = con.execute("SELECT COUNT(*) FROM comments WHERE post_id = ?", (post_id,)).fetchone()[0]
            reacted = bool(con.execute("SELECT 1 FROM reactions WHERE post_id = ? AND user_id = ? AND kind = 'rocket'", (post_id, izleyen)).fetchone())
        return {"roket_sayisi": reaction_count, "yorum_sayisi": comment_count, "kullanici_roketledi": reacted}

    def gonderi_olustur(self, post_id: int, text: str, topic: str, author_id: str = "emiryusuf"):
        with self._baglan() as con:
            con.execute("INSERT INTO posts(id, topic, text, author_id, created_at) VALUES (?, ?, ?, ?, ?)", (post_id, topic, text, author_id, _simdi()))
        return {"id": post_id, "metin": text, "konu": topic, "yazar": author_id}

    def takip_degistir(self, follower_id: str, following_id: str):
        if follower_id == following_id:
            return False
        with self._baglan() as con:
            exists = con.execute("SELECT 1 FROM follows WHERE follower_id = ? AND following_id = ?", (follower_id, following_id)).fetchone()
            if exists:
                con.execute("DELETE FROM follows WHERE follower_id = ? AND following_id = ?", (follower_id, following_id))
                return False
            con.execute("INSERT INTO follows VALUES (?, ?, ?)", (follower_id, following_id, _simdi()))
            con.execute("INSERT INTO activities(user_id, actor_id, post_id, kind, message, created_at) VALUES (?, ?, NULL, 'follow', ?, ?)", (following_id, follower_id, "Seni takip etmeye başladı.", _simdi()))
            return True

    def roket_degistir(self, user_id: str, post_id: int):
        with self._baglan() as con:
            exists = con.execute("SELECT 1 FROM reactions WHERE user_id = ? AND post_id = ? AND kind = 'rocket'", (user_id, post_id)).fetchone()
            if exists:
                con.execute("DELETE FROM reactions WHERE user_id = ? AND post_id = ? AND kind = 'rocket'", (user_id, post_id))
                return False
            con.execute("INSERT INTO reactions VALUES (?, ?, 'rocket', ?)", (user_id, post_id, _simdi()))
            author = con.execute("SELECT author_id FROM posts WHERE id = ?", (post_id,)).fetchone()
            if author and author[0] != user_id:
                con.execute("INSERT INTO activities(user_id, actor_id, post_id, kind, message, created_at) VALUES (?, ?, ?, 'rocket', ?, ?)", (author[0], user_id, post_id, "Gönderini roketledi.", _simdi()))
            return True

    def yorum_ekle(self, user_id: str, post_id: int, text: str):
        with self._baglan() as con:
            cur = con.execute("INSERT INTO comments(post_id, user_id, text, created_at) VALUES (?, ?, ?, ?)", (post_id, user_id, text, _simdi()))
            author = con.execute("SELECT author_id FROM posts WHERE id = ?", (post_id,)).fetchone()
            if author and author[0] != user_id:
                con.execute("INSERT INTO activities(user_id, actor_id, post_id, kind, message, created_at) VALUES (?, ?, ?, 'comment', ?, ?)", (author[0], user_id, post_id, "Gönderine yorum yaptı.", _simdi()))
            return cur.lastrowid

    def yorumlar(self, post_id: int):
        with self._baglan() as con:
            rows = con.execute("""SELECT comments.id, comments.text, comments.created_at, users.id AS user_id, users.name, users.handle, users.initials, users.color
                                FROM comments JOIN users ON users.id = comments.user_id WHERE post_id = ? ORDER BY comments.id DESC""", (post_id,)).fetchall()
        return [dict(row) for row in rows]

    def etkinlikler(self, user_id: str):
        with self._baglan() as con:
            rows = con.execute("""SELECT activities.id, activities.kind, activities.message, activities.created_at, activities.post_id,
                                users.name AS actor_name, users.initials AS actor_initials, users.color AS actor_color
                                FROM activities LEFT JOIN users ON users.id = activities.actor_id
                                WHERE activities.user_id = ? ORDER BY activities.id DESC LIMIT 30""", (user_id,)).fetchall()
        return [dict(row) for row in rows]

    def hikayeler(self):
        with self._baglan() as con:
            rows = con.execute("""SELECT stories.id, stories.user_id, stories.media_path, stories.caption, stories.position,
                                users.name, users.handle, users.initials, users.color
                                FROM stories JOIN users ON users.id = stories.user_id ORDER BY stories.position""").fetchall()
        return [dict(row) for row in rows]


def _simdi() -> str:
    return datetime.now(timezone.utc).isoformat()
