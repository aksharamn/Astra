export const state = { user:null, contacts:[], contactRequests:[], conversations:[], activeConversation:null, messages:[], socket:null, selectedPacket:null, osiEvents:[], theme:localStorage.getItem('astra-theme')||'midnight' };
export const events = new EventTarget();
export function setState(patch){ Object.assign(state,patch); events.dispatchEvent(new CustomEvent('statechange',{detail:patch})); }
export const on = (name, fn) => events.addEventListener(name, fn);
