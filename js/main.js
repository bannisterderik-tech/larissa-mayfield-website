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

// Parallax
window.addEventListener('scroll',function(){
  document.querySelectorAll('.parallax-img').forEach(function(img){
    var rect=img.getBoundingClientRect();
    var viewH=window.innerHeight;
    if(rect.top<viewH&&rect.bottom>0){
      var pct=(rect.top+rect.height/2-viewH/2)/(viewH+rect.height);
      img.style.transform='translateY('+pct*-40+'px)';
    }
  });
},{passive:true});

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
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var btn=form.querySelector('button[type="submit"]');
      var origText=btn.textContent;
      btn.textContent='SENDING...';
      btn.disabled=true;
      var formType=form.dataset.formType;
      var fields={};
      form.querySelectorAll('input[name],textarea[name]').forEach(function(el){
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
      if(interests.length)notesParts.push('Interests: '+interests.join(', '));
      if(fields.message)notesParts.push(fields.message);
      var contactVal=fields.contact||'';
      var emailVal=fields.email||'';
      var phoneVal=fields.phone||'';
      if(contactVal&&!emailVal&&!phoneVal){
        if(contactVal.indexOf('@')>-1)emailVal=contactVal;
        else phoneVal=contactVal;
      }
      var payload={
        assigned_to:'Larissa Mayfield',
        name:fields.name||'Unknown',
        email:emailVal||null,
        phone:phoneVal||null,
        source:'larissamayfield.com'+window.location.pathname+' ('+formType+')',
        notes:notesParts.join(' | ')||null
      };
      fetch(WEBHOOK_URL,{method:'POST',headers:{'Content-Type':'application/json','X-Webhook-Key':WEBHOOK_KEY},body:JSON.stringify(payload)})
        .then(function(r){
          if(!r.ok)throw new Error(r.status);
          var msg=document.createElement('div');
          msg.className='form-success';
          msg.innerHTML='<div class="form-success-check">✓</div>'
            +'<h3>Thank you'+(fields.name?', '+fields.name.split(' ')[0]:'')+'.</h3>'
            +'<p>'+(formType==='valuation'?'I’ll review your property details and be in touch shortly.':'Your message has been received. I’ll be in touch shortly.')+'</p>';
          form.parentNode.replaceChild(msg,form);
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
