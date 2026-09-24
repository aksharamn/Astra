import {api} from './api.js'; import {state,setState} from './state.js';
const initials = x => (x?.display_name||x?.username||'?').slice(0,1).toUpperCase();
export async function loadProfile(){try{const user=await api.me();setState({user:user.user||user});}catch{}}
export function renderProfile(){if(!state.user)return; document.querySelector('#my-name').textContent=state.user.display_name||state.user.username||'You';document.querySelector('#my-handle').textContent=state.user.astra_id_display||state.user.astra_id||('@'+(state.user.username||'user'));document.querySelector('#my-avatar').textContent=initials(state.user);}
export {initials};
