/* Heritage Editorial — Shared JS */

// Scroll reveal
function observeReveals(){
  var els=document.querySelectorAll('.reveal:not(.revealed)');
  var obs=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){e.target.classList.add('revealed');obs.unobserve(e.target)}
    });
  },{threshold:.08,rootMargin:'0px 0px -30px 0px'});
  var vh=window.innerHeight;
  els.forEach(function(el){
    var rect=el.getBoundingClientRect();
    if(rect.top<vh&&rect.bottom>0){el.classList.add('revealed');return;}
    obs.observe(el);
  });
}

// Header scroll shadow
var lastScroll=0;
window.addEventListener('scroll',function(){
  var header=document.querySelector('.site-header');
  if(!header)return;
  var y=window.scrollY;
  header.classList.toggle('scrolled',y>30);
  lastScroll=y;
},{passive:true});

// Parallax — desktop only. On mobile the browser chrome (address bar)
// shows/hides while scrolling, which resizes the viewport mid-scroll and
// makes the transform jump; the translate can also reveal gaps inside the
// overflow:hidden wrapper. We also honor prefers-reduced-motion.
var mqDesktop=window.matchMedia('(min-width:769px)');
var mqReduce=window.matchMedia('(prefers-reduced-motion: reduce)');
function parallaxEnabled(){return mqDesktop.matches&&!mqReduce.matches;}
function resetParallax(){
  document.querySelectorAll('.parallax-img').forEach(function(img){img.style.transform='';});
}
window.addEventListener('scroll',function(){
  if(!parallaxEnabled())return;
  document.querySelectorAll('.parallax-img').forEach(function(img){
    var rect=img.getBoundingClientRect();
    var viewH=window.innerHeight;
    if(rect.top<viewH&&rect.bottom>0){
      var pct=(rect.top+rect.height/2-viewH/2)/(viewH+rect.height);
      img.style.transform='translateY('+pct*-40+'px)';
    }
  });
},{passive:true});
// When crossing the breakpoint (resize / rotate), clear any stale transform
// so the image sits naturally on mobile.
if(mqDesktop.addEventListener){mqDesktop.addEventListener('change',resetParallax);}
else if(mqDesktop.addListener){mqDesktop.addListener(resetParallax);}

// Mobile menu
document.addEventListener('DOMContentLoaded',function(){
  var toggle=document.getElementById('menuToggle');
  var menu=document.getElementById('mobileMenu');
  if(toggle&&menu){
    toggle.addEventListener('click',function(){
      toggle.classList.toggle('active');
      menu.classList.toggle('open');
    });
    menu.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click',function(){
        toggle.classList.remove('active');
        menu.classList.remove('open');
      });
    });
  }
  // Chip toggles
  document.querySelectorAll('.chip').forEach(function(c){
    c.addEventListener('click',function(){c.classList.toggle('active')});
  });
  // Filter toggles
  document.querySelectorAll('.testimonials-filter span').forEach(function(s){
    s.addEventListener('click',function(){
      document.querySelectorAll('.testimonials-filter span').forEach(function(x){x.classList.remove('active')});
      s.classList.add('active');
    });
  });
  // Blog filter toggles
  document.querySelectorAll('.blog-filters span').forEach(function(s){
    s.addEventListener('click',function(){
      document.querySelectorAll('.blog-filters span').forEach(function(x){x.classList.remove('active')});
      s.classList.add('active');
    });
  });
  // Form submission → Supabase webhook
  var WEBHOOK_URL='https://ayskxkjorhoaknkqtyvm.supabase.co/functions/v1/webhook-receive';
  var WEBHOOK_KEY='e3302b5d21fc46979aacd6da8576642f';
  document.querySelectorAll('form[data-form-type]').forEach(function(form){
    // Spam defenses. Stamp when the form became interactive (time trap),
    // and inject a hidden honeypot field that real users never see.
    form._renderedAt=Date.now();
    var hp=document.createElement('input');
    hp.type='text';
    hp.name='company_website';
    hp.className='hp-field';
    hp.tabIndex=-1;
    hp.setAttribute('autocomplete','off');
    hp.setAttribute('aria-hidden','true');
    form.appendChild(hp);
    // Render a generic success state and remove the form (used both for a
    // real submit and to silently dead-end bots so they think they won).
    function showSuccess(name){
      var msg=document.createElement('div');
      msg.className='form-success';
      msg.innerHTML='<div class="form-success-check">✓</div>'
        +'<h3>Thank you'+(name?', '+name.split(' ')[0]:'')+'.</h3>'
        +'<p>'+({valuation:'I’ll review your property details and be in touch shortly.',
                 showing:'Your showing request is in. I’ll confirm a time by text, usually within a couple of hours.'
                }[form.dataset.formType]||'Your message has been received. I’ll be in touch shortly.')+'</p>';
      form.parentNode.replaceChild(msg,form);
    }
    form.addEventListener('submit',function(e){
      e.preventDefault();
      // Bot caught: honeypot filled, or submitted implausibly fast.
      // Fake success silently — don't tip the bot off, don't hit the webhook.
      if(hp.value.trim()||Date.now()-(form._renderedAt||0)<3000){
        showSuccess('');
        return;
      }
      var btn=form.querySelector('button[type="submit"]');
      var origText=btn.textContent;
      btn.textContent='SENDING...';
      btn.disabled=true;
      var formType=form.dataset.formType;
      var fields={};
      form.querySelectorAll('input[name],textarea[name]').forEach(function(el){
        if(el.classList.contains('hp-field'))return;
        if(el.value.trim())fields[el.name]=el.value.trim();
      });
      var chips=form.querySelectorAll('.chip.active');
      var interests=[];
      chips.forEach(function(c){interests.push(c.textContent)});
      var notesParts=[];
      if(formType==='valuation'){
        if(fields.property_address)notesParts.push('Address: '+fields.property_address);
        if(fields.acreage)notesParts.push('Acreage: '+fields.acreage);
        if(fields.property_type)notesParts.push('Type: '+fields.property_type);
      }
      // Showing requests come off a specific listing page — lead the note with
      // the property so the alert is actionable without opening anything.
      if(formType==='showing'){
        if(fields.listing_address)notesParts.push('SHOWING REQUEST: '+fields.listing_address);
        if(fields.listing_mls)notesParts.push('MLS# '+fields.listing_mls);
      }
      if(interests.length)notesParts.push((formType==='showing'?'Availability: ':'Interests: ')+interests.join(', '));
      if(fields.message)notesParts.push(fields.message);
      var contactVal=fields.contact||'';
      var emailVal=fields.email||'';
      var phoneVal=fields.phone||'';
      if(contactVal&&!emailVal&&!phoneVal){
        if(contactVal.indexOf('@')>-1)emailVal=contactVal;
        else phoneVal=contactVal;
      }
      var isPrivacy = formType==='privacy-request';
      if(isPrivacy){
        // A do-not-sell request is a compliance obligation, not a lead.
        notesParts.unshift('⚠ CCPA / DO-NOT-SELL REQUEST — DO NOT MARKET TO THIS PERSON');
      }
      var payload={
        assigned_to:'Larissa Mayfield',
        lead_type: isPrivacy ? 'privacy_request' : (formType==='valuation' ? 'seller' : 'buyer'),
        tags: isPrivacy ? ['privacy-request','do-not-sell','do-not-market'] : ['website',formType],
        name:fields.name||'Unknown',
        email:emailVal||null,
        phone:phoneVal||null,
        source:window.location.hostname+window.location.pathname+' ('+formType+')',
        notes:notesParts.join(' | ')||null,
        seller_listing_address: fields.listing_address||null,
        seller_listing_mls: fields.listing_mls||null,
        consent_email: true
      };
      fetch(WEBHOOK_URL,{method:'POST',headers:{'Content-Type':'application/json','X-Webhook-Key':WEBHOOK_KEY},body:JSON.stringify(payload)})
        .then(function(r){
          if(!r.ok)throw new Error(r.status);
          showSuccess(fields.name);
        })
        .catch(function(){
          btn.textContent='ERROR — TRY AGAIN';
          btn.disabled=false;
          setTimeout(function(){btn.textContent=origText},3000);
        });
    });
  });
  // Reveal init
  observeReveals();
});

/* ============================================================================
   LISTING PAGES
   Lightbox gallery, payment estimator, sticky action bar, video facade.
   All of it no-ops on pages that don't have the markup, so this stays one
   shared bundle rather than a second request on every listing.
   ========================================================================== */
document.addEventListener('DOMContentLoaded', function(){

  /* --- Sticky action bar ---------------------------------------------------
     Shows once the hero is off screen. IntersectionObserver rather than a
     scroll handler so it costs nothing while you're reading. */
  var bar = document.getElementById('listingStickyBar');
  var hero = document.querySelector('.listing-hero');
  if(bar && hero && 'IntersectionObserver' in window){
    new IntersectionObserver(function(entries){
      bar.classList.toggle('visible', !entries[0].isIntersecting);
    }, {threshold:0, rootMargin:'-120px 0px 0px 0px'}).observe(hero);
  }

  /* --- Lightbox ------------------------------------------------------------ */
  var photoTag = document.getElementById('galleryPhotos');
  var lb = document.getElementById('lightbox');
  if(photoTag && lb){
    var photos = [];
    try { photos = JSON.parse(photoTag.textContent) || []; } catch(e){ photos = []; }
    var lbImg = document.getElementById('lbImg');
    var lbCap = document.getElementById('lbCap');
    var lbCount = document.getElementById('lbCount');
    var idx = 0, lastFocus = null;

    function show(i){
      if(!photos.length) return;
      idx = (i + photos.length) % photos.length;
      var p = photos[idx];
      lbImg.src = p.src;
      // The alt already describes the photo; the caption is the human note.
      lbImg.alt = p.alt || '';
      lbCap.textContent = p.cap || '';
      lbCap.style.display = p.cap ? '' : 'none';
      lbCount.textContent = (idx + 1) + ' / ' + photos.length;
      // Warm the neighbours so arrowing through feels instant.
      [idx + 1, idx - 1].forEach(function(n){
        var q = photos[(n + photos.length) % photos.length];
        if(q){ var im = new Image(); im.src = q.src; }
      });
    }
    function open(i){
      lastFocus = document.activeElement;
      lb.hidden = false;
      document.body.classList.add('lb-open');
      show(i);
      lb.querySelector('.lb-close').focus();
    }
    function close(){
      lb.hidden = true;
      document.body.classList.remove('lb-open');
      lbImg.src = '';
      if(lastFocus && lastFocus.focus) lastFocus.focus();
    }

    document.querySelectorAll('[data-lightbox-open]').forEach(function(el){
      el.addEventListener('click', function(){ open(parseInt(el.dataset.lightboxOpen, 10) || 0); });
    });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function(){ show(idx - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function(){ show(idx + 1); });
    // Click the backdrop (not the photo) to dismiss.
    lb.addEventListener('click', function(e){ if(e.target === lb) close(); });
    document.addEventListener('keydown', function(e){
      if(lb.hidden) return;
      if(e.key === 'Escape') close();
      else if(e.key === 'ArrowRight') show(idx + 1);
      else if(e.key === 'ArrowLeft') show(idx - 1);
    });
    // Horizontal swipe on touch. 45px threshold, and we ignore gestures that
    // are mostly vertical so pinch-zoom panning doesn't change the photo.
    var tx = 0, ty = 0;
    lb.addEventListener('touchstart', function(e){
      tx = e.changedTouches[0].clientX; ty = e.changedTouches[0].clientY;
    }, {passive:true});
    lb.addEventListener('touchend', function(e){
      var dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
      if(Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) show(idx + (dx < 0 ? 1 : -1));
    }, {passive:true});
  }

  /* --- Gallery expand ------------------------------------------------------
     The extra tiles are already in the DOM (so they're in the page source for
     crawlers and work with the lightbox immediately) — this just unhides them. */
  document.querySelectorAll('[data-gallery-more]').forEach(function(btn){
    btn.addEventListener('click', function(){
      var grid = btn.closest('.listing-gallery').querySelector('.ggrid');
      var hidden = grid.querySelectorAll('.gtile.is-hidden');
      if(!hidden.length) return;
      var first = hidden[0];
      hidden.forEach(function(t){ t.classList.remove('is-hidden'); });
      btn.parentNode.remove();
      // Land the viewport on the first newly revealed row rather than leaving
      // the reader stranded where the button used to be.
      if(first.scrollIntoView) first.scrollIntoView({behavior:'smooth', block:'center'});
    });
  });

  /* --- Payment estimator ---------------------------------------------------
     Standard amortisation. Deliberately not persisted or transmitted — it is a
     back-of-envelope tool, and the disclaimer on the page says so. */
  var calc = document.getElementById('payment');
  if(calc){
    var $ = function(id){ return document.getElementById(id); };
    var el = {price:$('calcPrice'), down:$('calcDown'), rate:$('calcRate'), term:$('calcTerm'),
              tax:$('calcTax'), ins:$('calcIns')};
    var out = {downPct:$('calcDownPct'), downAmt:$('calcDownAmt'), ratePct:$('calcRatePct'),
               total:$('calcTotal'), pi:$('calcPI'), taxM:$('calcTaxM'), insM:$('calcInsM'),
               loan:$('calcLoan')};
    var money = function(n){
      return isFinite(n) ? '$' + Math.round(n).toLocaleString('en-US') : '—';
    };
    var num = function(input){
      return parseFloat(String(input.value).replace(/[^0-9.]/g, '')) || 0;
    };

    function run(){
      var price = num(el.price);
      var downPct = parseFloat(el.down.value);
      var rate = parseFloat(el.rate.value);
      var years = parseInt(el.term.value, 10);
      var downAmt = price * downPct / 100;
      var loan = Math.max(price - downAmt, 0);
      var r = rate / 100 / 12;
      var n = years * 12;
      // r === 0 would divide by zero; the no-interest case is just loan/months.
      var pi = r > 0 ? loan * r / (1 - Math.pow(1 + r, -n)) : (n ? loan / n : 0);
      var taxM = num(el.tax) / 12;
      var insM = num(el.ins) / 12;

      out.downPct.textContent = downPct;
      out.ratePct.textContent = rate.toFixed(3).replace(/0+$/, '').replace(/\.$/, '');
      out.downAmt.textContent = money(downAmt) + ' down';
      out.loan.textContent = money(loan);
      out.pi.textContent = money(pi);
      out.taxM.textContent = money(taxM);
      out.insM.textContent = money(insM);
      out.total.textContent = money(pi + taxM + insM);
    }
    Object.keys(el).forEach(function(k){
      el[k].addEventListener('input', run);
      el[k].addEventListener('change', run);
    });
    // Format the free-text money fields on blur so they read like money.
    [el.price, el.tax, el.ins].forEach(function(i){
      i.addEventListener('blur', function(){ i.value = num(i).toLocaleString('en-US'); run(); });
      i.value = num(i).toLocaleString('en-US');
    });
    run();
  }

  /* --- Video facade --------------------------------------------------------
     The YouTube player is ~1MB of script most visitors never press play on.
     Swap in the real iframe only on click. */
  document.querySelectorAll('.media-facade').forEach(function(f){
    function load(){
      var id = f.dataset.yt;
      var frame = document.createElement('iframe');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      frame.title = f.getAttribute('aria-label') || 'Property video tour';
      frame.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      var wrap = document.createElement('div');
      wrap.className = 'media-frame';
      wrap.appendChild(frame);
      f.parentNode.replaceChild(wrap, f);
    }
    f.addEventListener('click', load);
    f.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); load(); }
    });
  });

  /* --- Print flyer --------------------------------------------------------- */
  document.querySelectorAll('[data-print]').forEach(function(b){
    b.addEventListener('click', function(){ window.print(); });
  });
});
