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
  // Reveal init
  observeReveals();
});
