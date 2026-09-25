import {api} from './api.js'; import {state,setState} from './state.js'; import {initials} from './profiles.js';
export async function loadContacts(){try{const [data,incoming]=await Promise.all([api.contacts(),api.contactRequests()]);setState({contacts:data.contacts||data||[],contactRequests:incoming.requests||[]});}catch{}}
const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
export function renderContacts(onOpen){const el=document.querySelector('#contact-list');el.innerHTML='';if(!state.contactRequests?.length&&!state.contacts?.length){el.innerHTML='<div class="empty-state compact"><p>No contacts yet.<br>Use + to send a request.</p></div>';}(state.contactRequests||[]).forEach(r=>{const sender=r.sender||{};const row=document.createElement('div');row.className='person-row';row.innerHTML=`<span class="avatar">${esc(initials(sender))}</span><span><strong>${esc(sender.display_name||sender.username||'Unknown')}</strong><small>Contact request · ${esc(sender.astra_id_display||sender.astra_id||'')}</small></span><button class="btn subtle accept-request">Accept</button>`;row.querySelector('.accept-request').onclick=async e=>{e.stopPropagation();try{await api.acceptContact(r.id);await loadContacts();renderContacts(onOpen);}catch(err){document.querySelector('#toast-region').textContent=err.message;}};el.append(row);});(state.contacts||[]).forEach(c=>{const row=document.createElement('button');row.className='person-row';row.innerHTML=`<span class="avatar">${esc(initials(c))}</span><span><strong>${esc(c.display_name||c.username||'Contact')}</strong><small>${esc(c.astra_id_display||c.astra_id||'')}</small></span><span class="contact-state">${esc(c.status||'available')}</span>`;row.onclick=()=>onOpen(c);el.append(row);});}
export async function sendRequest(query){
 const input=String(query).trim().toUpperCase();

 if(!/^ASTRA-[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}$/.test(input)){
  throw new Error('Enter a valid ASTRA ID (ASTRA-XXXX-XXXX-XXXX).');
 }

 const normalized=input.replace('ASTRA-','').replaceAll('-','');
 const profile=await api.profileByAstraId(normalized);

 if(!window.confirm(`Send a connection request to ${profile.display_name || profile.username}?`)) return null;

 return api.requestContact({astra_id:normalized});
}
