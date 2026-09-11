/* Tum sayfalarda ortak erisilebilirlik yardimcisi.
   aria-hidden="true" olan diyalog/paneller ekran okuyucudan gizleniyordu ama
   icindeki dugmelere Tab ile hala ulasilabiliyordu (axe: aria-hidden-focus).
   Bu betik bu elemanlari "inert" yapar ve aria-hidden degistikce esitler;
   boylece her sayfanin ac/kapat koduna ayri ayri dokunmak gerekmez. */
(function () {
  const ODAKLANABILIR = "button, a[href], input, select, textarea, [tabindex]";
  const esitle = eleman => { eleman.inert = eleman.getAttribute("aria-hidden") === "true"; };
  const gozlemci = new MutationObserver(kayitlar => kayitlar.forEach(kayit => esitle(kayit.target)));
  document.querySelectorAll("[aria-hidden]").forEach(eleman => {
    if (eleman.closest("svg") || !eleman.querySelector(ODAKLANABILIR)) return;
    esitle(eleman);
    gozlemci.observe(eleman, { attributes: true, attributeFilter: ["aria-hidden"] });
  });
})();
