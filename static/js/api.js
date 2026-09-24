const base = (window.ASTRA_CONFIG?.apiBase || '').replace(/\/$/, '');
async function request(path, options = {}) {
  const response = await fetch(`${base}${path}`, { credentials: 'include', headers: {'Content-Type':'application/json', ...(options.headers||{})}, ...options });
  const text = await response.text(); let body = {}; try { body = text ? JSON.parse(text) : {}; } catch { body = {message:text}; }
  if (!response.ok) throw new Error(body.error || body.message || `Request failed (${response.status})`);
  return body;
}
export const api = {
  health: () => request('/api/health'),
  login: data => request('/api/auth/login',{method:'POST',body:JSON.stringify(data)}),
  register: data => request('/api/auth/register',{method:'POST',body:JSON.stringify(data)}),
  recover: data => request('/api/auth/recover',{method:'POST',body:JSON.stringify(data)}),
  me: () => request('/api/me'),
  contacts: () => request('/api/contacts'),
  requestContact: data => request('/api/contacts/requests',{method:'POST',body:JSON.stringify(data)}),
  contactRequests: () => request('/api/contacts/requests'),
  acceptContact: id => request(`/api/contacts/requests/${encodeURIComponent(id)}/accept`,{method:'POST'}),
  declineContact: id => request(`/api/contacts/requests/${encodeURIComponent(id)}/decline`,{method:'POST'}),
  conversations: () => request('/api/conversations'),
  messages: id => request(`/api/messages/${encodeURIComponent(id)}`),
  send: (id,data) => request(`/api/messages/${encodeURIComponent(id)}`,{method:'POST',body:JSON.stringify(data)}),
  profileByAstraId: id => request(`/api/profile/by-astra-id/${encodeURIComponent(id)}`),
  tamper: data => request('/api/messages/tamper',{method:'POST',body:JSON.stringify(data)}),
  logout: () => request('/api/auth/logout',{method:'POST'})
};
