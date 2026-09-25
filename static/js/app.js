import {api} from './api.js';
import {state,setState,on} from './state.js';
import {initAuth,logout} from './auth.js';
import {loadProfile,renderProfile} from './profiles.js';
import {loadContacts,renderContacts,sendRequest} from './contacts.js';
import {loadConversations,openConversation,initMessaging,renderMessages,renderConversations} from './messaging.js';
import {connectSocket} from './websocket.js';
import {packetView,tamperDemo,runTamper} from './encryption.js';
import {osiView} from './osi.js';
import {initThemes,exportTheme,applyTheme} from './themes.js';
import {initPresentation} from './presentation.js';

const $=s=>document.querySelector(s);
const show=(s,v)=>$(s).classList.toggle('hidden',!v);

function showToast(message){
  const toast=$('#toast-region');
  toast.textContent=message;
  clearTimeout(showToast.timer);
  showToast.timer=setTimeout(()=>{toast.textContent='';},3500);
}

function initLandingExperience(){
  const landing=document.querySelector('.landing-page');
  if(!landing)return;

  const nav=document.querySelector('#landing-nav');
  const navToggle=document.querySelector('#landing-nav-toggle');
  navToggle?.addEventListener('click',()=>{
    const open=nav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded',String(open));
  });
  nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{
    nav.classList.remove('is-open');
    navToggle?.setAttribute('aria-expanded','false');
  }));

  const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems=[...landing.querySelectorAll('[data-reveal]')];
  if(reduceMotion||!('IntersectionObserver' in window)){
    revealItems.forEach(item=>item.classList.add('reveal-in'));
  }else{
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.classList.add('reveal-in');
        observer.unobserve(entry.target);
      }
    }),{threshold:.12,rootMargin:'0px 0px -7%'});
    revealItems.forEach(item=>observer.observe(item));
  }

  const parallaxItems=[...landing.querySelectorAll('[data-parallax]')];
  if(!reduceMotion&&parallaxItems.length){
    let frame=0;
    const updateParallax=()=>{
      frame=0;
      const scrollY=window.scrollY;
      parallaxItems.forEach(item=>{
        const speed=Number(item.dataset.parallax)||0;
        const bounds=item.getBoundingClientRect();
        if(bounds.bottom>0&&bounds.top<window.innerHeight){
          item.style.setProperty('--parallax-y',`${(scrollY-window.innerHeight*.25)*speed}px`);
        }
      });
    };
    window.addEventListener('scroll',()=>{
      if(!frame)frame=requestAnimationFrame(updateParallax);
    },{passive:true});
    updateParallax();
  }
}

async function boot(){
  show('#auth-screen',false);
  show('#app-shell',true);
  await loadProfile();
  renderProfile();
  await Promise.all([loadContacts(),loadConversations()]);
  renderContacts(openConversation);
  renderConversations(openConversation);
  initThemes();
  initPresentation();
  document.querySelector('#mobile-menu').onclick=()=>document.querySelector('.sidebar').classList.toggle('open');
  document.querySelector('#import-theme').onchange=async e=>{
    const file=e.target.files[0];
    if(!file)return;
    try{const theme=JSON.parse(await file.text());applyTheme('custom',theme);}catch{showToast('Invalid theme file.');}
  };
  document.querySelectorAll('.tab').forEach(b=>b.onclick=()=>{
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    show('#chat-list',b.dataset.tab==='chats');
    show('#contact-list',b.dataset.tab==='contacts');
  });
  document.querySelector('#logout-button').onclick=()=>{logout();show('#app-shell',false);show('#auth-screen',true);window.scrollTo({top:0,behavior:'smooth'});};
  document.querySelector('#add-contact').onclick=()=>$('#contact-dialog').showModal();
  document.querySelector('#contact-dialog .dialog-close').onclick=()=>$('#contact-dialog').close();
  document.querySelector('#contact-form').onsubmit=async e=>{
    e.preventDefault();
    try{await sendRequest(new FormData(e.target).get('query'));$('#contact-feedback').textContent='Request sent.';e.target.reset();}
    catch(err){$('#contact-feedback').textContent=err.message;}
  };
  document.querySelector('#settings-button').onclick=()=>$('#settings-dialog').showModal();
  document.querySelector('#export-theme').onclick=exportTheme;
  document.querySelector('#inspect-button').onclick=()=>openInspector('packet');
  document.querySelector('#secure-toggle').onclick=()=>openInspector('packet');
  document.querySelector('#close-inspector').onclick=()=>show('#inspector-panel',false);
  document.querySelectorAll('[data-inspect-tab]').forEach(b=>b.onclick=()=>openInspector(b.dataset.inspectTab));
  connectSocket().then(s=>{setState({socket:s});initMessaging(s);});
}

function openInspector(tab){
  show('#inspector-panel',true);
  document.querySelectorAll('[data-inspect-tab]').forEach(b=>b.classList.toggle('active',b.dataset.inspectTab===tab));
  const content=$('#inspector-content');
  if(tab==='packet')content.innerHTML=packetView();
  if(tab==='tamper'){content.innerHTML=tamperDemo();runTamper();}
  if(tab==='osi')content.innerHTML=osiView();
}

initLandingExperience();
initAuth(boot);
on('statechange',e=>{
  if(e.detail.contacts)renderContacts(openConversation);
  if(e.detail.conversations)renderConversations(openConversation);
  if(e.detail.messages)renderMessages();
});
