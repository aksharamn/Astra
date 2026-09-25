import {setState,state} from './state.js';
import {renderMessages} from './messaging.js';
import {api} from './api.js';

export async function connectSocket(){
  try{
    if(typeof window.io !== 'function'){
      throw new Error('Socket.IO client is not loaded.');
    }

    const socket=window.io({
      withCredentials:true,
      reconnection:true,
      reconnectionAttempts:Infinity,
      reconnectionDelay:1000,
      reconnectionDelayMax:5000,
      timeout:10000
    });

    socket.on('connect',async()=>{
      console.log('ASTRA Socket.IO connected:',socket.id);
      setState({socket});

      try{
        if(state.activeConversation){
          const id=state.activeConversation.id||state.activeConversation.conversation_id;
          const d=await api.messages(id);
          setState({messages:d.messages||d||[]});
          renderMessages();
        }
      }catch(err){
        console.warn('ASTRA message sync failed:',err);
      }
    });

    socket.on('connect_error',err=>{
      console.warn('ASTRA Socket.IO connection error:',err.message);
      setState({socket:null});
    });

    socket.on('disconnect',reason=>{
      console.warn('ASTRA Socket.IO disconnected:',reason);
      setState({socket:null});
    });

    socket.on('message:new',m=>{
      setState({selectedPacket:m});

      if(
        state.activeConversation &&
        (
          m.recipient_id===state.activeConversation.id ||
          m.sender_id===state.activeConversation.id
        ) &&
        !state.messages.some(existing=>existing.id===m.id)
      ){
        setState({messages:[...state.messages,m]});
        renderMessages();
      }
    });

    socket.on('message:sent',m=>{
      setState({selectedPacket:m});

      if(
        state.activeConversation?.id===m.recipient_id &&
        !state.messages.some(existing=>existing.id===m.id)
      ){
        setState({messages:[...state.messages,m]});
        renderMessages();
      }
    });

    socket.on('message:error',data=>{
      const message=data?.error||'Message could not be delivered.';
      const toast=document.querySelector('#toast-region');

      if(toast){
        toast.textContent=message;
        clearTimeout(window.__astraToastTimer);
        window.__astraToastTimer=setTimeout(()=>{
          toast.textContent='';
        },3500);
      }
    });

    socket.on('osi:event',e=>{
      setState({
        osiEvents:[...state.osiEvents,e]
      });

      document.dispatchEvent(
        new CustomEvent('osi:event',{detail:e})
      );
    });

    socket.on('packet',p=>{
      setState({selectedPacket:p});

      document.dispatchEvent(
        new CustomEvent('packet:event',{detail:p})
      );
    });

    return socket;
  }catch(err){
    console.warn('ASTRA Socket.IO unavailable:',err);
    return null;
  }
}
