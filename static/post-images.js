// Curated local Pexels images for the deterministic demo feed.
// Images provide visual context only; ranking and sentiment stay text/interaction based.
const PEXELS_POST_IMAGES = {
  spor: ["01-soccer", "02-running"],
  gundem: ["03-city", "15-market", "16-architecture"],
  teknoloji: ["04-laptop", "05-circuit", "18-robot"],
  bilim: ["06-space", "07-lab"],
  saglik: ["02-running", "14-coffee"],
  ekonomi: ["15-market", "03-city", "16-architecture"],
  sanat: ["08-museum", "09-paint", "19-concert"],
  egitim: ["10-library", "07-lab"],
  oyun: ["17-gaming", "18-robot"],
  seyahat: ["11-mountains", "12-forest", "13-sea", "20-train"],
  varsayilan: ["03-city", "11-mountains", "16-architecture"]
};

function postImage(post) {
  const id = Number(post && post.id) || 1;
  const images = PEXELS_POST_IMAGES[post && post.konu] || PEXELS_POST_IMAGES.varsayilan;
  return `/assets/explore/${images[(Math.abs(id) - 1) % images.length]}.jpg`;
}
