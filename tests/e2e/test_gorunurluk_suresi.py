"""Görünür süre yalnız bir karta yazılır; eşik, örtülme ve çift sayım regresyonları."""
from test_akis import akisi_ac


def test_tek_kart_esik_uzun_kart_ve_pencere(masaustu):
    akisi_ac(masaustu)
    result = masaustu.evaluate("""() => {
      const saved=sendInteraction, oldHidden=Object.getOwnPropertyDescriptor(document,'hidden');
      const records=[];sendInteraction=(id,dwell)=>records.push({id,dwell});
      dwellStop();records.length=0;dwellCards.clear();
      const head=document.querySelector('.topbar').getBoundingClientRect();
      const top=Math.max(0,head.bottom), height=innerHeight-top;
      const cards=[];
      function card(id,y,h){const c=document.createElement('article');c.dataset.id=id;
        c.getBoundingClientRect=()=>({top:y,bottom:y+h,height:h,width:400,left:300,right:700});
        document.body.append(c);dwellCards.add(c);cards.push(c);return c;}
      try{
        const full=card(9001,top+10,200),partial=card(9002,innerHeight-40,200);
        dwellUpdate();const selected=[...visibleSince.keys()];
        visibleSince.set(9001,performance.now()-2000);
        const first=dwellFor(9001),second=dwellFor(9001),offscreen=dwellFor(9002);
        document.getElementById('explanation-sheet').classList.add('open');dwellUpdate();
        const covered=visibleSince.size;
        document.getElementById('explanation-sheet').classList.remove('open');
        full.remove();partial.remove();
        card(9003,top-100,height+300);dwellUpdate();const tall=[...visibleSince.keys()];
        Object.defineProperty(document,'hidden',{configurable:true,value:true});dwellUpdate();
        return {selected,first,second,offscreen,covered,tall,hidden:visibleSince.size};
      }finally{
        cards.forEach(c=>c.remove());dwellCards.clear();visibleSince.clear();sendInteraction=saved;
        if(oldHidden)Object.defineProperty(document,'hidden',oldHidden);else delete document.hidden;
      }
    }""")
    assert result['selected'] == [9001]
    assert 1.9 < result['first'] < 2.2
    assert result['second'] < .1
    assert 0 < result['offscreen'] < .1  # süresi tutulmayan karta tıklama/yorum da kaydedilir
    assert result['covered'] == 0
    assert result['tall'] == [9003]
    assert result['hidden'] == 0
