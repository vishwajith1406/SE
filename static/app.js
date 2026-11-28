"use strict";
const $=s=>document.querySelector(s);
const form=$("#analysis-form"),button=$("#analyze"),errorBox=$("#error");
function escapeHtml(value){return String(value??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
async function checkSetup(){try{const response=await fetch("/api/health");const state=await response.json();$("#setup-status").textContent=state.ready?"Embedding and generation services ready":"Add embedding and LLM keys in .env";$("#setup-status").classList.toggle("ready",state.ready)}catch{$("#setup-status").textContent="Start the FinReq local server to analyze"}}
$("#files").addEventListener("change",e=>{$("#file-names").textContent=[...e.target.files].map(f=>f.name).join(" · ")});
form.addEventListener("submit",async e=>{e.preventDefault();errorBox.hidden=true;button.disabled=true;button.innerHTML='<span class="spinner"></span> Retrieving evidence & drafting…';try{const response=await fetch("/api/analyze",{method:"POST",body:new FormData(form)});const data=await response.json();if(!response.ok)throw new Error(data.detail||"Analysis could not be completed.");$("#model").textContent=data.recommended_sdlc;$("#rationale").textContent=data.rationale;
    // The server builds this HTML from escaped source strings and model output.
    $("#srs-preview").innerHTML=data.srs_html;$("#download").href=data.srs_url;form.hidden=true;$("#intro").hidden=true;$("#result").hidden=false;window.scrollTo({top:0,behavior:"smooth"});
    }catch(err){errorBox.textContent=err.message;errorBox.hidden=false;button.disabled=false;button.innerHTML='Analyze project <span>→</span>'}});
$("#new-project").addEventListener("click",()=>{form.reset();$("#file-names").textContent="";$("#result").hidden=true;form.hidden=false;$("#intro").hidden=false;errorBox.hidden=true;button.disabled=false;button.innerHTML='Analyze project <span>→</span>';window.scrollTo({top:0,behavior:"smooth"})});
checkSetup();
