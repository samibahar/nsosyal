const agent = window.LocalPersonalization;
const escapeJury = value => { const element = document.createElement("div"); element.textContent = value ?? ""; return element.innerHTML; };
const shortText = value => value.length > 78 ? `${value.slice(0, 75)}…` : value;
const score = value => Math.round(Number(value || 0) * 100);

function renderTrace(trace) {
  const candidates = new Map(trace.candidates.map(item => [Number(item.id), item]));
  const before = new Map(trace.before.map(item => [Number(item.id), item]));
  const after = [...trace.after].sort((a, b) => Math.abs((before.get(Number(b.id))?.position || 0) - b.position) - Math.abs((before.get(Number(a.id))?.position || 0) - a.position));
  const summary = trace.summary || {};
  document.getElementById("jury-summary").innerHTML = `<article><small>Hazır sinyal</small><b>${trace.signals.length}</b><p>örnek etkileşim</p></article><article><small>Yerel güven</small><b>%${score(summary.confidence)}</b><p>${summary.eventCount} anlamlı kayıt</p></article><article><small>Akış yoğunluğu</small><b>%${score(summary.intensity)}</b><p>${summary.repeatedNegative} yoğun içerikte uzun kalma</p></article><article><small>Görünen etki</small><b>${trace.movedCount}</b><p>gönderi yer değiştirdi</p></article>`;
  document.getElementById("jury-signal-copy").textContent = "Hazır örnek veri";
  document.getElementById("jury-signal-list").innerHTML = trace.signals.map((signal, index) => { const post = candidates.get(Number(signal.post_id)); return `<article><b>${String(index + 1).padStart(2, "0")}</b><div><span>${escapeJury(post?.konu || "Akış")} · ${Number(signal.dwell).toFixed(1)} sn</span><p>${escapeJury(shortText(post?.metin || "Örnek içerik"))}</p></div>${signal.reaction ? "<i>😟 Kullanıcı tepkisi</i>" : "<i>Uzun kalma</i>"}</article>`; }).join("");
  document.getElementById("jury-rank-list").innerHTML = after.slice(0, 6).map(item => { const post = candidates.get(Number(item.id)), old = before.get(Number(item.id))?.position || item.position, change = old - item.position, direction = change > 0 ? "up" : change < 0 ? "down" : "same", label = change ? `#${old} → #${item.position}` : "Sıra korundu"; return `<article><div class="jury-rank-number ${direction}">${label}</div><div><b>${escapeJury(post?.yazar_bilgi?.name || "Topluluk üyesi")}</b><p>${escapeJury(shortText(post?.metin || ""))}</p><span>${escapeJury(post?.konu || "")}</span></div><strong>${score(item.score)}</strong></article>`; }).join("");
  const balanced = trace.after.filter(item => item.balancing > 0).length;
  document.getElementById("jury-receipt").innerHTML = `<p><b>İlgi:</b> Hazır senaryodaki açık etkileşimler ilgili konuların yerel ağırlığını güncelledi.</p><p><b>Dengeleme:</b> ${balanced} yoğun adayın sırası, sürdürülebilir örüntü oluştuğunda içerik silinmeden nazikçe azaltıldı.</p><p><b>Kontrol:</b> Son açık tepki “Gerildim” olarak kaydedildi; bu bir teşhis değil, kullanıcının gönüllü bildirimi.</p><p><b>Gizlilik:</b> Karar izi IndexedDB’de bu cihazda tutulur. Sunucu yalnızca örnek adayları sağladı.</p>`;
  document.getElementById("jury-empty").hidden = true; document.getElementById("jury-content").hidden = false;
}

async function loadJury() {
  if (!agent) return;
  await agent.init(); const trace = await agent.getDecisionTrace();
  if (trace?.demo) renderTrace(trace); else document.getElementById("jury-empty").hidden = false;
}
loadJury().catch(() => { document.getElementById("jury-empty").hidden = false; });
