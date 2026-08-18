"use strict";

/* ============================================================
   PINNED CLOCK
   The prototype's "now". Everything time-based derives from it,
   so the demo is identical on every machine, on every day.
   ============================================================ */
const NOW = new Date(2026, 7, 10, 9, 0, 0); // Mon 10 Aug 2026, 09:00 local

/* ============================================================
   TENANT CONFIGURATION
   In the real system this is database rows an admin edits.
   ============================================================ */
const CFG = {
  docs:true, screen:true, pay:true,
  priorConsult:true, hasHistory:false, minAge:18,
  depMode:'percent', depVal:25,
  leadHours:24, grid:15, buffer:15, readCal:true
};

/* Working pattern for the single practitioner, Nafisa Mughal.
   0 = Sunday. Times in minutes from midnight. */
const PATTERN = {
  0:null,
  1:[540,1020],  // Mon 09:00-17:00
  2:[540,1020],  // Tue 09:00-17:00
  3:[600,840],   // Wed 10:00-14:00
  4:[540,1020],  // Thu 09:00-17:00
  5:[540,1020],  // Fri 09:00-17:00
  6:[540,780]    // Sat 09:00-13:00
};

/* Busy time imported from the practitioner's own calendar, plus
   existing bookings. Fixed, so the demo never drifts.
   [yyyy, m(0-idx), d, startMin, endMin, source] */
const BUSY = [
  [2026,7,10,660,780,'Existing booking, Laser Lift'],
  [2026,7,10,900,960,'Google Calendar, personal'],
  [2026,7,11,540,660,'Google Calendar, school run'],
  [2026,7,11,840,930,'Existing booking, Liquid Facelift'],
  [2026,7,12,600,720,'Existing booking, Sculptra'],
  [2026,7,13,690,750,'Google Calendar, lunch'],
  [2026,7,13,900,1020,'Existing booking, Polynucleotides'],
  [2026,7,14,540,720,'Google Calendar, training day'],
  [2026,7,15,600,660,'Existing booking, Skin Peel'],
  [2026,7,17,540,780,'Google Calendar, annual leave'],
  [2026,7,18,780,900,'Existing booking, RF Microneedling'],
  [2026,7,19,600,720,'Google Calendar, supplier meeting'],
  [2026,7,20,660,720,'Google Calendar, lunch'],
  [2026,7,21,900,1020,'Existing booking, Anti-Wrinkle'],
  [2026,7,22,540,600,'Existing booking, Dermaplaning'],
  [2026,7,24,600,780,'Google Calendar, conference'],
  [2026,7,25,660,780,'Existing booking, Laser Lift'],
  [2026,7,26,600,660,'Google Calendar, personal'],
  [2026,7,27,840,960,'Existing booking, Cheek Filler'],
  [2026,7,28,540,660,'Google Calendar, school run']
];

/* ============================================================
   SERVICE CATALOGUE
   Prices and durations are PureMed's live list.
   Scope: the eleven treatments carried on puremed.uk/treatments,
   plus the consultation and review services that the rules
   engine needs in order to route.
   flags: pom = prescription-only medicine, inj = injectable,
          energy = energy-based device
   ============================================================ */
const CATS = [
  ['consult','Consultations'],
  ['toxin','Anti-Wrinkle'],
  ['filler','Fillers &amp; Volume'],
  ['regen','Skin Regeneration'],
  ['device','Devices &amp; Body'],
  ['skin','Skin Health']
];

const SERVICES = [
  // Consultations and review
  {id:'consult-clinic', cat:'consult', name:'Skin Consultation, Winslow', price:25.00, mins:30, flags:[], doc:null,
   note:'Face-to-face assessment and treatment planning'},
  {id:'consult-online', cat:'consult', name:'Online Consultation', price:25.00, mins:15, flags:['remote'], doc:null,
   note:'Video consultation. Cannot satisfy the prescribing rule'},
  {id:'review', cat:'consult', name:'Review After Treatment', price:0.00, mins:15, flags:[], doc:null,
   note:'Follow-up appointment, no charge'},

  // Anti-wrinkle, the full toxin variant set
  {id:'btx-1', cat:'toxin', name:'Botulinum Toxin, One Area', price:179.63, mins:15, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-2', cat:'toxin', name:'Botulinum Toxin, Two Areas', price:205.24, mins:30, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-3', cat:'toxin', name:'Botulinum Toxin, Three Areas', price:265.58, mins:30, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-allu', cat:'toxin', name:'Alluzience, Three Areas', price:285.52, mins:30, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-brow', cat:'toxin', name:'Botulinum Toxin, Brow Lift', price:265.56, mins:30, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-lip', cat:'toxin', name:'Botulinum Toxin, Lip Flip / Smokers Lines', price:100.00, mins:15, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-gummy', cat:'toxin', name:'Botulinum Toxin, Gummy Smile', price:179.63, mins:30, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-dao', cat:'toxin', name:'Botulinum Toxin, DAO', price:179.00, mins:15, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-neck', cat:'toxin', name:'Botulinum Toxin, Neck', price:350.00, mins:15, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-necklift', cat:'toxin', name:'Botulinum Toxin, Neck Lift', price:350.00, mins:30, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-jaw', cat:'toxin', name:'Botulinum Toxin, Face Slimming / Jaw Clenching', price:349.27, mins:30, flags:['pom','inj'], doc:'DOC-BTX'},
  {id:'btx-sweat', cat:'toxin', name:'Excessive Sweating, Botulinum Toxin', price:550.00, mins:30, flags:['pom','inj'], doc:'DOC-BTX'},

  // Fillers and volume
  {id:'liquid-facelift', cat:'filler', name:'Liquid Facelift, Dermal Fillers', price:750.00, mins:75, flags:['inj'], doc:'DOC-FILLER', site:'liquid-facelift'},
  {id:'sculptra', cat:'filler', name:'Sculptra, Collagen Biostimulator', price:425.00, mins:60, flags:['inj'], doc:'DOC-FILLER', site:'sculptra'},

  // Skin regeneration
  {id:'polynucleotides', cat:'regen', name:'Polynucleotides', price:400.00, mins:30, flags:['inj'], doc:'DOC-REGEN', site:'polynucleotides'},
  {id:'skin-boosters', cat:'regen', name:'Skin Boosters', price:80.00, mins:30, flags:['inj'], doc:'DOC-REGEN', site:'skin-boosters'},
  {id:'plasma-fibroblast', cat:'regen', name:'Plasma Fibroblast', price:176.58, mins:45, flags:['energy'], doc:'DOC-DEVICE', site:'plasma-fibroblast'},

  // Devices and body
  {id:'laser-lift', cat:'device', name:'Laser Lift, Endolift', price:1900.00, mins:90, flags:['energy'], doc:'DOC-DEVICE', site:'laser-lift'},
  {id:'rf-microneedling', cat:'device', name:'Radio Frequency Microneedling', price:250.00, mins:30, flags:['energy'], doc:'DOC-DEVICE', site:'rf-microneedling'},
  {id:'body-sculpting', cat:'device', name:'Body Sculpting, HI-EMT', price:200.00, mins:45, flags:['energy'], doc:'DOC-DEVICE', site:'body-sculpting'},

  // Skin health
  {id:'skin-peels', cat:'skin', name:'Skin Peel, Bio RePeel', price:68.00, mins:30, flags:[], doc:'DOC-SKIN', site:'skin-peels'},
  {id:'enzyme-peel', cat:'skin', name:'Enzyme Peel with LED Light Therapy', price:89.00, mins:30, flags:[], doc:'DOC-SKIN'},
  {id:'dermaplaning', cat:'skin', name:'Dermaplaning', price:48.24, mins:45, flags:[], doc:'DOC-SKIN', site:'dermaplaning'}
];

/* Cards shown on the mock treatments page: the site's own eleven,
   in the site's own order. Anti-Wrinkle opens the toxin variant list. */
const SITE_CARDS = [
  {label:'Laser Lift', cat:'Skin Tightening', svc:'laser-lift'},
  {label:'Liquid Facelift', cat:'Dermal Fillers', svc:'liquid-facelift'},
  {label:'Anti-Wrinkle', cat:'Muscle-Relaxing Injections', svc:'btx-2'},
  {label:'Polynucleotides', cat:'Skin Regeneration', svc:'polynucleotides'},
  {label:'RF Microneedling', cat:'Energy-Based', svc:'rf-microneedling'},
  {label:'Skin Boosters', cat:'Deep Hydration', svc:'skin-boosters'},
  {label:'Plasma Fibroblast', cat:'Skin Tightening', svc:'plasma-fibroblast'},
  {label:'Body Sculpting', cat:'Fat Reduction', svc:'body-sculpting'},
  {label:'Skin Peels', cat:'Chemical Exfoliation', svc:'skin-peels'},
  {label:'Dermaplaning', cat:'Exfoliation', svc:'dermaplaning'},
  {label:'Sculptra', cat:'Collagen Biostimulator', svc:'sculptra'}
];

/* ============================================================
   DOCUMENT TEMPLATES
   Fidelity rule, inherited from the wealth-onboarding pack:
   wording the clinic already owns is reproduced verbatim,
   wording nobody has supplied is a LABELLED placeholder.
   Inventing plausible clinical copy is the failure mode.
   ============================================================ */
const DOCS = {
  'DOC-POLICY':{
    id:'DOC-POLICY', v:'v1.0', title:'Booking and Cancellation Policy',
    real:true, optional:false,
    body:[
      'All clients must complete medical and consent forms and provide accurate information. Treatment suitability is assessed at consultation.',
      'All payments are non-refundable, including advance bookings, packages, missed appointments, or change of mind. In rare medical cases, credit may be offered at the clinic’s discretion.',
      'We require 48 hours’ notice for cancellations or changes. Late cancellations or non-attendance will result in loss of treatment. Late arrival may lead to reduced time or cancellation.',
      'Payments made by card or online incur a non-refundable payment processing fee of 1.8% + VAT + 20p per transaction. This fee is charged by the payment provider and will not be refunded under any circumstances.',
      'Packages must be used within the stated timeframe or will be forfeited.',
      'Results vary and are not guaranteed; maintenance may be required.',
      'You must inform us of any medical changes before treatment.',
      'We are not liable for indirect damages; liability for negligence is not excluded.'
    ],
    clauses:[
      'I have read and accept the booking and cancellation policy, including that payments are non-refundable.',
      'I understand that 48 hours’ notice is required to cancel or change this appointment, and that late cancellation or non-attendance results in loss of the treatment.'
    ]
  },
  'DOC-MEDHX':{
    id:'DOC-MEDHX', v:'v0.1', title:'Medical History Declaration',
    real:false, optional:false,
    body:[
      'PLACEHOLDER. The clinic’s own medical history form has not been supplied. In the live system this document is reproduced from the clinic’s existing paperwork, version-controlled, and rendered here in full.',
      'The structure is fixed: current medications, known allergies, previous aesthetic treatments and dates, relevant medical conditions, pregnancy and breastfeeding status, anticoagulant use, and a declaration of accuracy.',
      'No clinical wording has been drafted by the studio. Substituting plausible-looking medical text would make this prototype appear more complete than it is.'
    ],
    clauses:[
      'I confirm the information I have given is accurate and complete to the best of my knowledge.',
      'I will inform the clinic of any change to my health or medication before my appointment.'
    ]
  },
  'DOC-BTX':{
    id:'DOC-BTX', v:'v0.1', title:'Informed Consent, Botulinum Toxin',
    real:false, optional:false,
    body:[
      'PLACEHOLDER. Treatment-specific informed consent for botulinum toxin. The clinic’s existing consent form is the source and has not been supplied.',
      'The live document sets out the nature of the treatment, that botulinum toxin is a prescription-only medicine, the intended effect and its duration, common and rare risks, alternatives including no treatment, aftercare requirements, and the client’s right to withdraw consent at any point before treatment.',
      'Each material risk is presented as its own acknowledgement rather than a single blanket agreement, so the record shows what was individually understood and when.'
    ],
    clauses:[
      'PLACEHOLDER. I understand the nature of the treatment, its intended effect, and that results are not guaranteed.',
      'PLACEHOLDER. I have been informed of the common and rare risks and have had the opportunity to ask questions.',
      'PLACEHOLDER. I understand this is a prescription-only medicine that will be prescribed for me following assessment.'
    ]
  },
  'DOC-FILLER':{
    id:'DOC-FILLER', v:'v0.1', title:'Informed Consent, Dermal Filler',
    real:false, optional:false,
    body:[
      'PLACEHOLDER. Treatment-specific informed consent for dermal filler and collagen biostimulator treatments. The clinic’s existing form is the source and has not been supplied.',
      'The live document covers product type and longevity, vascular occlusion risk and its management, the availability of dissolving agents where applicable, aftercare, and the review appointment.'
    ],
    clauses:[
      'PLACEHOLDER. I understand the treatment, its expected longevity, and that results are not guaranteed.',
      'PLACEHOLDER. I have been informed of the risks, including rare vascular complications, and how they are managed.'
    ]
  },
  'DOC-REGEN':{
    id:'DOC-REGEN', v:'v0.1', title:'Informed Consent, Injectable Skin Regeneration',
    real:false, optional:false,
    body:['PLACEHOLDER. Treatment-specific informed consent for polynucleotide and skin booster treatments. Clinic form not yet supplied.'],
    clauses:[
      'PLACEHOLDER. I understand the treatment, the course of sessions recommended, and that results build over time.',
      'PLACEHOLDER. I have been informed of the risks and aftercare requirements.'
    ]
  },
  'DOC-DEVICE':{
    id:'DOC-DEVICE', v:'v0.1', title:'Informed Consent, Energy-Based Treatment',
    real:false, optional:false,
    body:['PLACEHOLDER. Treatment-specific informed consent for laser, radiofrequency, plasma and electromagnetic device treatments. Clinic form not yet supplied. The live document also records the patch test where the device protocol requires one.'],
    clauses:[
      'PLACEHOLDER. I understand the treatment, the expected downtime, and that results are not guaranteed.',
      'PLACEHOLDER. I have been informed of the risks including burns, pigmentation change and scarring, and of the aftercare required.'
    ]
  },
  'DOC-SKIN':{
    id:'DOC-SKIN', v:'v0.1', title:'Consent, Skin Treatment',
    real:false, optional:false,
    body:['PLACEHOLDER. Consent for chemical peel, enzyme peel and dermaplaning treatments. Clinic form not yet supplied.'],
    clauses:['PLACEHOLDER. I understand the treatment, the expected peeling or sensitivity afterwards, and the aftercare required.']
  },
  'DOC-PHOTO':{
    id:'DOC-PHOTO', v:'v1.0', title:'Photography and Marketing Consent',
    real:false, optional:true,
    body:[
      'This consent is separate from your treatment consent and is entirely optional. Declining it will not affect your treatment, your appointment, or the care you receive.',
      'Clinical photographs are taken as part of your treatment record whether or not you agree to this. This document asks only about using images publicly, for example on the clinic website or social media.',
      'You may withdraw this consent at any time by contacting the clinic, and images will be removed from future use.',
      'PLACEHOLDER. The specific permissions, image types, channels and retention period are the clinic’s to set and have not been supplied.'
    ],
    clauses:[
      'I agree that my before and after photographs may be used publicly by the clinic.',
      'I understand this is optional, that declining does not affect my treatment, and that I can withdraw at any time.'
    ]
  }
};

/* ============================================================
   SCREENING QUESTIONS
   Outcome per answer: pass, flag (reroute), or block.
   ============================================================ */
const SCREEN_Q = [
  {id:'preg', q:'Are you pregnant, planning pregnancy, or breastfeeding?', yes:'block', rule:'RULE-011',
   msg:'Injectable and energy-based treatments are not offered during pregnancy or breastfeeding.'},
  {id:'anticoag', q:'Are you taking any blood-thinning medication (for example warfarin, apixaban, or regular aspirin)?', yes:'flag', rule:'RULE-012',
   msg:'Anticoagulant use needs assessment before an injectable treatment is booked.'},
  {id:'infection', q:'Do you have an active skin infection, cold sore, or inflammation in the treatment area?', yes:'flag', rule:'RULE-013',
   msg:'Active infection in the treatment area needs assessment before booking.'},
  {id:'conditions', q:'Do you have a neuromuscular condition, or a known allergy to any of the products used?', yes:'flag', rule:'RULE-014',
   msg:'This history needs clinical assessment before an injectable treatment is booked.'}
];

/* ============================================================
   STATE
   ============================================================ */
let S = null;
function freshState(){
  return {
    open:false, step:'service', cat:'consult', deepLinked:false,
    svcId:null, rerouted:null, blocked:null,
    screen:{}, weekStart:startOfWeek(NOW), slot:null,
    client:{first:'',last:'',dob:'',email:'',mobile:''}, errors:{},
    docIdx:0, signed:{}, sigData:null, sigMethod:null, sigName:'',
    clauses:{}, paid:false, ref:null, trace:[], committed:null
  };
}

/* ============================================================
   RULES ENGINE
   Pure function. Given a service and the config, return exactly
   what this booking requires and which rules produced it.
   ============================================================ */
function resolve(svc){
  const out = {docs:[], screening:false, deposit:{mode:'none',amount:0}, ageMin:0, fired:[], reroute:null};
  if(!svc) return out;
  const isInj = svc.flags.includes('inj');
  const isPom = svc.flags.includes('pom');
  const isEnergy = svc.flags.includes('energy');

  // RULE-001, every booking acknowledges the practice's booking policy
  out.docs.push('DOC-POLICY');
  out.fired.push({id:'RULE-001', kind:'', t:'Booking and cancellation policy acknowledgement required on every service.', in:'service = any'});

  // RULE-004, prescription-only medicines need a recent face-to-face consultation
  if(isPom && CFG.priorConsult && !CFG.hasHistory){
    out.reroute = 'consult-clinic';
    out.fired.push({id:'RULE-004', kind:'flag',
      t:'Prescription-only treatment with no consultation on record in the last 12 months. Booking rerouted to Skin Consultation.',
      in:'flags contains pom, consultation_on_record = false'});
  } else if(isPom && CFG.priorConsult && CFG.hasHistory){
    out.fired.push({id:'RULE-004', kind:'pass',
      t:'Consultation on record within 12 months. Direct booking permitted.',
      in:'flags contains pom, consultation_on_record = true'});
  }

  // RULE-006, age minimum on injectables
  if(isInj){
    out.ageMin = CFG.minAge;
    out.fired.push({id:'RULE-006', kind:'', t:'Minimum age '+CFG.minAge+' applies. Date of birth is checked.', in:'flags contains inj'});
  }

  // RULE-010, medical screening
  if(CFG.screen && (isInj || isEnergy)){
    out.screening = true;
    out.fired.push({id:'RULE-010', kind:'', t:'Medical screening required before a slot is offered.', in:'flags contains inj or energy, screening_enabled = true'});
  }

  // RULE-020 / 021, documents
  if(CFG.docs){
    if(isInj || isEnergy){
      out.docs.push('DOC-MEDHX');
      out.fired.push({id:'RULE-021', kind:'', t:'Medical history declaration required.', in:'flags contains inj or energy'});
    }
    if(svc.doc){
      out.docs.push(svc.doc);
      out.fired.push({id:'RULE-020', kind:'', t:'Treatment consent '+svc.doc+' required for this service.', in:'service = '+svc.id});
    }
    if(isInj || isEnergy){
      out.docs.push('DOC-PHOTO');
      out.fired.push({id:'RULE-022', kind:'', t:'Photography consent offered as a separate, optional document. It never blocks the booking.', in:'flags contains inj or energy'});
    }
  } else {
    out.fired.push({id:'RULE-020', kind:'', t:'Document step disabled in practice settings. No consent is captured.', in:'documents_enabled = false'});
  }

  // RULE-030 / 031, money
  if(svc.price === 0){
    out.fired.push({id:'RULE-031', kind:'', t:'Zero-price service. No payment step.', in:'price = 0.00'});
  } else if(!CFG.pay){
    out.fired.push({id:'RULE-030', kind:'', t:'Payment at booking disabled in practice settings. Client pays at the clinic.', in:'payment_enabled = false'});
  } else {
    let amt = 0, label = '';
    if(CFG.depMode === 'percent'){ amt = round2(svc.price * CFG.depVal / 100); label = CFG.depVal+'% deposit'; }
    else if(CFG.depMode === 'fixed'){ amt = Math.min(CFG.depVal, svc.price); label = 'fixed deposit'; }
    else if(CFG.depMode === 'full'){ amt = svc.price; label = 'full payment'; }
    if(CFG.depMode !== 'none' && amt > 0){
      out.deposit = {mode:CFG.depMode, amount:amt, label:label};
      out.fired.push({id:'RULE-030', kind:'', t:'Taking '+label+' of '+gbp(amt)+' at booking.', in:'price = '+gbp(svc.price)+', deposit_mode = '+CFG.depMode+', value = '+CFG.depVal});
    } else {
      out.fired.push({id:'RULE-030', kind:'', t:'No deposit configured. Client pays at the clinic.', in:'deposit_mode = none'});
    }
  }

  // RULE-040, cancellation window, from the clinic's real policy
  out.fired.push({id:'RULE-040', kind:'', t:'48 hours’ notice required to cancel or change. Payments non-refundable per clinic policy.', in:'policy = DOC-POLICY v1.0'});

  return out;
}

/* ============================================================
   AVAILABILITY ENGINE
   Pure function of pattern, busy time, duration, buffer,
   notice period and grid. No randomness anywhere.
   ============================================================ */
function computeDay(date, svc){
  const dow = date.getDay();
  const win = PATTERN[dow];
  if(!win || !svc) return [];
  const need = svc.mins + CFG.buffer;
  const earliest = new Date(NOW.getTime() + CFG.leadHours*3600e3);

  // busy intervals for this day
  const busy = (CFG.readCal ? BUSY : BUSY.filter(b => b[5].indexOf('Existing booking') === 0))
    .filter(b => b[0]===date.getFullYear() && b[1]===date.getMonth() && b[2]===date.getDate())
    .map(b => [b[3], b[4]]);

  const out = [];
  for(let t = win[0]; t + need <= win[1]; t += CFG.grid){
    const s = t, e = t + need;
    if(busy.some(b => s < b[1] && e > b[0])) continue;
    const abs = new Date(date.getFullYear(), date.getMonth(), date.getDate(), Math.floor(s/60), s%60);
    if(abs < earliest) continue;
    out.push(s);
  }
  return out;
}

/* ============================================================
   HELPERS
   ============================================================ */
function round2(n){ return Math.round(n*100)/100; }
function gbp(n){ return '£' + n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
function hhmm(m){ return String(Math.floor(m/60)).padStart(2,'0') + ':' + String(m%60).padStart(2,'0'); }
function startOfWeek(d){ const x = new Date(d.getFullYear(), d.getMonth(), d.getDate()); x.setDate(x.getDate() - ((x.getDay()+6)%7)); return x; }
function addDays(d,n){ const x = new Date(d); x.setDate(x.getDate()+n); return x; }
function fmtDate(d){ return d.toLocaleDateString('en-GB',{weekday:'long',day:'numeric',month:'long',year:'numeric'}); }
function esc(s){ return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function svcById(id){ return SERVICES.find(s => s.id === id) || null; }
function $(id){ return document.getElementById(id); }

async function sha256(str){
  try{
    const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2,'0')).join('');
  }catch(e){
    let h = 0; for(let i=0;i<str.length;i++){ h = (h*31 + str.charCodeAt(i))|0; }
    return 'fallback-' + (h>>>0).toString(16);
  }
}

/* ============================================================
   TRACE
   ============================================================ */
function trace(entry){
  const seen = S.trace.some(t => t.id === entry.id && t.t === entry.t);
  if(seen) return;
  S.trace.push(entry);
  renderTrace();
}
function traceEvent(id, t, inp){ trace({id:id, kind:'evt', t:t, in:inp||''}); }

function renderTrace(){
  const box = $('trace');
  $('trace-empty').style.display = S.trace.length ? 'none' : 'block';
  box.innerHTML = S.trace.map(t =>
    '<div class="tr '+(t.kind||'')+'">' +
      '<div class="tr-id">'+esc(t.id)+'</div>' +
      '<div class="tr-t">'+esc(t.t)+'</div>' +
      (t.in ? '<div class="tr-in">'+esc(t.in)+'</div>' : '') +
    '</div>'
  ).join('');
}

/* ============================================================
   STEP MODEL
   The visible steps depend entirely on what the rules require.
   ============================================================ */
function stepList(){
  const svc = svcById(S.svcId);
  const r = resolve(svc);
  const steps = [{k:'service', l:'Treatment'}];
  steps.push({k:'screen', l:'Screening', skip:!r.screening});
  steps.push({k:'slot', l:'Time'});
  steps.push({k:'details', l:'Details'});
  steps.push({k:'docs', l:'Documents', skip:!(CFG.docs && r.docs.length)});
  steps.push({k:'pay', l:'Payment', skip:!(r.deposit.amount > 0)});
  steps.push({k:'confirm', l:'Confirmed'});
  return steps;
}
function activeSteps(){ return stepList().filter(s => !s.skip); }
function nextStep(){
  const a = activeSteps(), i = a.findIndex(s => s.k === S.step);
  return i >= 0 && i < a.length-1 ? a[i+1].k : null;
}
function prevStep(){
  const a = activeSteps(), i = a.findIndex(s => s.k === S.step);
  return i > 0 ? a[i-1].k : null;
}

/* ============================================================
   RENDER
   ============================================================ */
function render(){
  renderSteps();
  const svc = svcById(S.svcId);
  const r = resolve(svc);
  const body = $('w-body');

  if(S.step === 'service')       body.innerHTML = viewService();
  else if(S.step === 'screen')   body.innerHTML = viewScreen(svc);
  else if(S.step === 'slot')     body.innerHTML = viewSlot(svc);
  else if(S.step === 'details')  body.innerHTML = viewDetails(svc, r);
  else if(S.step === 'docs')     { body.innerHTML = viewDocs(r); initSigPad(); }
  else if(S.step === 'pay')      body.innerHTML = viewPay(svc, r);
  else if(S.step === 'confirm')  body.innerHTML = viewConfirm(svc, r);

  if(S.deepLinked && svc && S.step !== 'service' && S.step !== 'confirm'){
    body.innerHTML = '<div class="svc-locked"><span><b>Booking:</b> '+esc(svc.name)+
      ' &nbsp;&middot;&nbsp; '+(svc.price===0?'No charge':gbp(svc.price))+
      ' &nbsp;&middot;&nbsp; '+svc.mins+' min</span>' +
      '<button type="button" id="btn-change-svc">Change</button></div>' + body.innerHTML;
  }

  renderFoot(svc, r);
  bindBody();
  if($('btn-change-svc')) $('btn-change-svc').onclick = clearDeepLink;
}

function renderSteps(){
  $('steps').innerHTML = stepList().map(s => {
    const a = activeSteps(), ai = a.findIndex(x => x.k === S.step);
    const mi = a.findIndex(x => x.k === s.k);
    let cls = 'step';
    if(s.skip) cls += ' skip';
    else if(s.k === S.step) cls += ' on';
    else if(mi > -1 && mi < ai) cls += ' done';
    return '<div class="'+cls+'">'+esc(s.l)+'</div>';
  }).join('');
}

function renderFoot(svc, r){
  const price = $('w-price'), next = $('btn-next'), back = $('btn-back');
  back.style.visibility = prevStep() ? 'visible' : 'hidden';

  if(S.step === 'confirm'){
    price.innerHTML = 'Reference <b style="font-size:13px;font-family:JetBrains Mono,monospace">'+esc(S.ref)+'</b>';
    next.textContent = 'Done';
    next.disabled = false;
    back.style.visibility = 'hidden';
    return;
  }
  if(svc){
    const dep = r.deposit.amount > 0 ? ' &nbsp;&middot;&nbsp; '+r.deposit.label+' '+gbp(r.deposit.amount) : '';
    price.innerHTML = esc(svc.name) + '<br><b>' + (svc.price === 0 ? 'No charge' : gbp(svc.price)) + '</b>' + dep;
  } else {
    price.innerHTML = '<span style="opacity:.7">Select a treatment to see the price</span>';
  }
  next.textContent = S.step === 'pay' ? 'Pay and confirm booking'
                   : S.step === 'docs' ? 'Continue'
                   : 'Continue';
  next.disabled = !canAdvance(svc, r);
}

function canAdvance(svc, r){
  if(S.blocked) return false;
  switch(S.step){
    case 'service': return !!svc;
    case 'screen':  return SCREEN_Q.every(q => S.screen[q.id] !== undefined);
    case 'slot':    return !!S.slot;
    case 'details': return true;
    case 'docs':    return r.docs.filter(d => !DOCS[d].optional).every(d => S.signed[d]);
    case 'pay':     return S.paid;
    default: return true;
  }
}

/* ---------- step: service ---------- */
function viewService(){
  const cats = CATS.map(c =>
    '<button class="cat-chip'+(S.cat===c[0]?' on':'')+'" data-cat="'+c[0]+'">'+c[1]+'</button>'
  ).join('');
  const list = SERVICES.filter(s => s.cat === S.cat).map(s =>
    '<button class="svc'+(S.svcId===s.id?' on':'')+'" data-svc="'+s.id+'">' +
      '<span><span class="svc-n">'+esc(s.name)+'</span>' +
      '<span class="svc-m">'+s.mins+' min' + (s.note ? ' &nbsp;&middot;&nbsp; '+esc(s.note) : '') + '</span></span>' +
      '<span class="svc-p">'+(s.price===0?'No charge':gbp(s.price))+
        (s.flags.includes('pom')?'<small>Prescription-only</small>':'')+'</span>' +
    '</button>'
  ).join('');

  let notice = '';
  if(S.rerouted){
    const from = svcById(S.rerouted);
    notice = '<div class="notice reroute"><h5>Consultation needed first <span class="rid">RULE-004</span></h5>' +
      esc(from.name)+' is a prescription-only medicine. It cannot be booked directly without a face-to-face consultation on record in the last 12 months. Your booking has been switched to a <b>Skin Consultation</b>, where suitability is assessed and the treatment can be planned and prescribed.</div>';
  }
  const newHere = (!S.svcId && !S.rerouted)
    ? '<div class="notice info"><h5>New here?</h5>Not sure yet, or haven\'t spoken to the clinic about pricing? Start with a Skin Consultation — Nafisa assesses what you need before anything else is booked or charged.</div>'
    : '';
  return notice + newHere +
    '<h4 class="w-title">What is your appointment for?</h4>' +
    '<p class="w-sub">The treatment you choose determines the price, the length of the appointment, which questions you are asked, and which forms you sign. Nothing else changes it.</p>' +
    '<div class="cat-row">'+cats+'</div><div class="svc-list">'+list+'</div>';
}

/* ---------- step: screening ---------- */
function viewScreen(svc){
  let out = '<h4 class="w-title">A few medical questions</h4>' +
    '<p class="w-sub">Asked because you have chosen '+esc(svc.name)+'. These are checked before you are offered a time, so you are never asked to pick a slot you cannot use.</p>';

  if(S.blocked){
    out += '<div class="notice block"><h5>We cannot book this online <span class="rid">'+esc(S.blocked.rule)+'</span></h5>' +
      esc(S.blocked.msg)+' Please call the clinic on 01296 123456 or email care@puremed.uk and Nafisa will advise you directly.</div>';
  } else {
    const flags = SCREEN_Q.filter(q => S.screen[q.id] === true && q.yes === 'flag');
    if(flags.length){
      out += '<div class="notice reroute"><h5>Assessment needed first <span class="rid">'+esc(flags[0].rule)+'</span></h5>' +
        esc(flags[0].msg)+' Continue and your booking will be made as a consultation instead, at '+gbp(25)+'.</div>';
    }
  }

  out += SCREEN_Q.map(q => {
    const v = S.screen[q.id];
    return '<div class="q"><p>'+esc(q.q)+'</p><div class="yn">' +
      '<button data-q="'+q.id+'" data-v="1" class="'+(v===true?'on warn':'')+'">Yes</button>' +
      '<button data-q="'+q.id+'" data-v="0" class="'+(v===false?'on':'')+'">No</button>' +
    '</div></div>';
  }).join('');
  return out;
}

/* ---------- step: slot ---------- */
function viewSlot(svc){
  const ws = S.weekStart;
  const cols = [];
  for(let i=0;i<7;i++){
    const d = addDays(ws,i);
    const slots = computeDay(d, svc);
    const closed = !PATTERN[d.getDay()];
    cols.push({d:d, slots:slots, closed:closed});
  }
  const heads = cols.map(c =>
    '<div class="day-h'+(c.closed?' closed':'')+'">'+c.d.toLocaleDateString('en-GB',{weekday:'short'})+'<b>'+c.d.getDate()+'</b></div>'
  ).join('');
  const body = cols.map(c => {
    if(c.closed) return '<div class="day-col"><div class="day-empty">Closed</div></div>';
    if(!c.slots.length) return '<div class="day-col"><div class="day-empty">None</div></div>';
    return '<div class="day-col">' + c.slots.slice(0,8).map(m => {
      const key = c.d.getTime()+'|'+m;
      return '<button class="slot'+(S.slot && S.slot.key===key?' on':'')+'" data-slot="'+key+'">'+hhmm(m)+'</button>';
    }).join('') + (c.slots.length>8 ? '<div class="day-empty">+'+(c.slots.length-8)+'</div>' : '') + '</div>';
  }).join('');

  const canPrev = ws > startOfWeek(NOW);
  const monthLbl = ws.toLocaleDateString('en-GB',{month:'long',year:'numeric'});

  return '<h4 class="w-title">Choose a time</h4>' +
    '<p class="w-sub">Showing '+svc.mins+' minutes for '+esc(svc.name)+', plus a '+CFG.buffer+' minute buffer, at least '+CFG.leadHours+' hours from now. Times Nafisa is unavailable have already been removed.</p>' +
    '<div class="cal-head"><h4>'+esc(monthLbl)+'</h4><div class="cal-nav">' +
      '<button data-week="-1" '+(canPrev?'':'disabled')+'>&larr; Earlier</button>' +
      '<button data-week="1">Later &rarr;</button></div></div>' +
    '<div class="week">'+heads+'</div><div class="week">'+body+'</div>' +
    '<div class="legend">' +
      '<span><i style="background:#fff;border:1px solid var(--border)"></i>Available</span>' +
      '<span><i style="background:var(--navy)"></i>Selected</span>' +
      '<span>Removed: existing bookings, imported calendar busy time, closed days, and anything inside the notice period</span>' +
    '</div>' +
    (S.slot ? '<div class="notice ok" style="margin-top:14px;margin-bottom:0"><b>'+esc(fmtDate(S.slot.date))+'</b> at <b>'+hhmm(S.slot.min)+'</b>, ending '+hhmm(S.slot.min+svc.mins)+'. Held for you for 10 minutes.</div>' : '');
}

/* ---------- step: details ---------- */
function viewDetails(svc, r){
  const c = S.client, e = S.errors;
  return '<h4 class="w-title">Your details</h4>' +
    '<p class="w-sub">Held against the booking. Your identity record and your signed forms are stored separately, so contact details can be corrected or removed without touching the clinical record.</p>' +
    '<div class="frow">' +
      fld('first','First name','text',c.first,e.first) +
      fld('last','Last name','text',c.last,e.last) +
    '</div><div class="frow">' +
      fld('email','Email','email',c.email,e.email,'Confirmation, forms and reminders go here') +
      fld('mobile','Mobile','tel',c.mobile,e.mobile) +
    '</div><div class="frow">' +
      fld('dob','Date of birth','date',c.dob,e.dob, r.ageMin ? 'Minimum age '+r.ageMin+' for this treatment (RULE-006)' : '') +
      '<div></div>' +
    '</div>';
}
function fld(k,label,type,val,err,hint){
  return '<div class="fld"><label for="f-'+k+'">'+esc(label)+'</label>' +
    '<input id="f-'+k+'" data-f="'+k+'" type="'+type+'" value="'+esc(val||'')+'" autocomplete="off">' +
    (err ? '<div class="err">'+esc(err)+'</div>' : (hint ? '<div class="hint">'+esc(hint)+'</div>' : '')) +
    '</div>';
}

/* ---------- step: documents ---------- */
function viewDocs(r){
  const ids = r.docs;
  if(S.docIdx >= ids.length) S.docIdx = 0;
  const cur = DOCS[ids[S.docIdx]];

  const tabs = ids.map((id,i) => {
    const d = DOCS[id];
    return '<button class="doc-tab'+(i===S.docIdx?' on':'')+'" data-doc="'+i+'">' +
      (S.signed[id]?'<span class="tick">&#10003;</span>':'') + esc(d.title) +
      (d.optional?'<span class="opt">Optional</span>':'') + '</button>';
  }).join('');

  const body = cur.body.map(p =>
    '<p'+(p.indexOf('PLACEHOLDER')===0?' class="ph"':'')+'>'+esc(p)+'</p>'
  ).join('');

  const clauses = cur.clauses.map((c,i) => {
    const on = (S.clauses[cur.id]||{})[i];
    return '<label class="clause'+(on?' ticked':'')+'">' +
      '<input type="checkbox" data-clause="'+i+'" '+(on?'checked':'')+'>' +
      '<span>'+esc(c)+'</span></label>';
  }).join('');

  const allTicked = cur.clauses.every((_,i) => (S.clauses[cur.id]||{})[i]);
  const signedThis = S.signed[cur.id];

  let sig = '';
  if(signedThis){
    sig = '<div class="notice ok"><h5>Signed</h5>Signed by '+esc(signedThis.name)+' at '+esc(signedThis.time)+
      ', method: '+esc(signedThis.method)+'. Document version '+esc(cur.v)+
      '.<div class="hash" style="margin-top:6px;color:#2F6B41">SHA-256 '+esc(signedThis.hash)+'</div></div>';
  } else {
    sig = '<div class="sig-zone">' +
      '<div class="sig-lbl"><span>Sign here</span>' +
        '<button data-sigclear>Clear</button></div>' +
      '<canvas id="sigpad" aria-label="Signature area"></canvas>' +
      '<div class="frow" style="margin-top:11px;margin-bottom:0">' +
        '<div class="fld"><label for="sig-name">Or type your full name</label>' +
        '<input id="sig-name" type="text" value="'+esc(S.sigName)+'" autocomplete="off" placeholder="Full name"></div>' +
        '<div class="fld"><label>&nbsp;</label>' +
        '<button class="btn-pm" id="btn-sign" '+(allTicked?'':'disabled')+' style="width:100%;justify-content:center">Sign and continue</button></div>' +
      '</div>' +
      '<p class="sig-foot">' + (allTicked
        ? 'Signing records the exact document version shown, a timestamp, and a hash of the rendered PDF.'
        : 'Tick each statement above before signing. Each one is recorded separately with its own timestamp.') + '</p>' +
    '</div>';
  }

  return '<h4 class="w-title">'+esc(cur.title)+'</h4>' +
    '<p class="w-sub">'+(cur.optional
      ? 'This one is optional. Declining it does not affect your treatment or this booking.'
      : 'Required before this appointment can be confirmed. You will receive a signed copy by email.')+'</p>' +
    '<div class="doc-tabs">'+tabs+'</div>' +
    '<div class="doc-paper"><h4>'+esc(cur.title)+'</h4>' +
      '<div class="doc-ver"><span>'+esc(cur.id)+' '+esc(cur.v)+'</span>' +
      (cur.real ? '<span class="real-badge">Clinic’s own wording</span>'
                : '<span class="ph-badge">Placeholder wording</span>') + '</div>' +
      body + '</div>' + clauses + sig;
}

/* ---------- step: payment ---------- */
function viewPay(svc, r){
  const fee = round2(r.deposit.amount * 0.018 + 0.20);
  return '<h4 class="w-title">Payment</h4>' +
    '<p class="w-sub">Your card is authorised now and the booking is only committed if the authorisation succeeds. If anything fails, the authorisation is released and no booking is made.</p>' +
    '<div class="pay-sum">' +
      '<div class="pay-row"><span>'+esc(svc.name)+'<span class="sub">'+svc.mins+' minutes with Nafisa Mughal</span></span><span>'+gbp(svc.price)+'</span></div>' +
      '<div class="pay-row"><span>'+esc(r.deposit.label.charAt(0).toUpperCase()+r.deposit.label.slice(1))+'<span class="sub">Balance of '+gbp(round2(svc.price-r.deposit.amount))+' payable at the clinic</span></span><span>'+gbp(r.deposit.amount)+'</span></div>' +
      '<div class="pay-row"><span>Card processing fee<span class="sub">1.8% + 20p, charged by the payment provider, non-refundable</span></span><span>'+gbp(fee)+'</span></div>' +
      '<div class="pay-row tot"><span>To pay now</span><span>'+gbp(round2(r.deposit.amount+fee))+'</span></div>' +
    '</div>' +
    '<div class="card-warn">Demonstration only. This prototype is not connected to a payment provider. Google Pay and the card fields below are locked previews — clicking either simulates an authorisation. Do not enter real card details anywhere in this page.</div>' +
    (S.paid ? '' :
      '<button class="gpay-btn" id="btn-gpay" type="button" aria-label="Pay with Google Pay (preview, simulated)">' +
        '<span class="gpay-g"><span style="color:#4285F4">G</span><span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span></span>' +
        '<span class="gpay-pay">Pay</span>' +
      '</button>' +
      '<div class="pay-divider"><span>Or pay by card</span></div>'
    ) +
    '<div class="stripe-field">' +
      '<input type="text" value="4242 4242 4242 4242" readonly>' +
      '<span class="card-brand" aria-hidden="true">VISA</span>' +
    '</div>' +
    '<div class="frow" style="margin-top:8px;margin-bottom:0">' +
      '<div class="stripe-field"><input type="text" value="12 / 30" readonly></div>' +
      '<div class="stripe-field"><input type="text" value="123" readonly></div>' +
    '</div>' +
    (S.paid ? '<div class="notice ok" style="margin-top:14px;margin-bottom:0"><h5>Authorised</h5>'+gbp(round2(r.deposit.amount+fee))+' authorised. Simulated. The booking commits when you continue.</div>'
            : '<button class="btn-pm" id="btn-auth" style="width:100%;justify-content:center;margin-top:14px">Authorise '+gbp(round2(r.deposit.amount+fee))+' (simulated)</button>');
}

/* ---------- step: confirm ---------- */
function viewConfirm(svc, r){
  const c = S.committed;
  const docRows = c.docs.map(d =>
    '<div class="dl"><span>'+esc(d.title)+' '+esc(d.v)+'<span class="h">SHA-256 '+esc(d.hash)+'</span></span>' +
    '<span style="color:var(--navy);font-weight:600;white-space:nowrap">PDF &darr;</span></div>'
  ).join('') || '<p style="font-size:12.5px;color:var(--mid-grey)">No documents were required by the current settings.</p>';

  return '<div class="conf-hero"><div class="conf-tick">&#10003;</div>' +
    '<h3>Your appointment is booked</h3>' +
    '<p>A confirmation, a calendar invitation and signed copies of everything you agreed to are on their way to '+esc(c.email)+'.</p></div>' +
    '<div class="conf-card"><h5>Appointment</h5>' +
      kv('Treatment', c.svcName) + kv('With', 'Nafisa Mughal') +
      kv('When', c.when) + kv('Where', '34a High Street, Winslow MK18 3HB') +
      kv('Duration', c.mins + ' minutes') + kv('Reference', c.ref) +
    '</div>' +
    '<div class="conf-card"><h5>Payment</h5>' +
      kv('Treatment price', gbp(c.price)) +
      kv(c.paidLabel, c.paid > 0 ? gbp(c.paid) : 'Nothing taken') +
      kv('Balance at the clinic', gbp(round2(c.price - c.depositOnly))) +
    '</div>' +
    '<div class="conf-card"><h5>Your signed documents</h5>' + docRows + '</div>' +
    '<div class="notice info" style="margin-bottom:0"><b>48 hours’ notice</b> is required to cancel or change this appointment. Payments are non-refundable per the clinic’s booking policy, which you acknowledged and which is attached to your confirmation email.</div>';
}
function kv(a,b){ return '<div class="kv"><span>'+esc(a)+'</span><span>'+esc(b)+'</span></div>'; }

/* ============================================================
   SIGNATURE PAD
   ============================================================ */
let sigCtx = null, drawing = false, sigHasInk = false;
function initSigPad(){
  const cv = $('sigpad');
  if(!cv) return;
  const dpr = window.devicePixelRatio || 1;
  const rect = cv.getBoundingClientRect();
  cv.width = rect.width * dpr; cv.height = rect.height * dpr;
  sigCtx = cv.getContext('2d');
  sigCtx.scale(dpr, dpr);
  sigCtx.lineWidth = 2; sigCtx.lineCap = 'round'; sigCtx.lineJoin = 'round';
  sigCtx.strokeStyle = '#1A1A2E';
  sigHasInk = false;

  const pos = ev => {
    const r = cv.getBoundingClientRect();
    return [ev.clientX - r.left, ev.clientY - r.top];
  };
  cv.addEventListener('pointerdown', ev => {
    drawing = true; cv.setPointerCapture(ev.pointerId);
    const [x,y] = pos(ev); sigCtx.beginPath(); sigCtx.moveTo(x,y);
  });
  cv.addEventListener('pointermove', ev => {
    if(!drawing) return;
    const [x,y] = pos(ev); sigCtx.lineTo(x,y); sigCtx.stroke(); sigHasInk = true;
  });
  cv.addEventListener('pointerup', () => { drawing = false; });
  cv.addEventListener('pointerleave', () => { drawing = false; });
}

/* ============================================================
   COMMIT
   ============================================================ */
async function commit(){
  const svc = svcById(S.svcId);
  const r = resolve(svc);
  S.ref = 'PM-' + String(NOW.getFullYear()).slice(2) + String(NOW.getMonth()+1).padStart(2,'0') + '-' +
          (4821 + SERVICES.findIndex(s => s.id === svc.id) * 7 + (S.slot ? S.slot.min : 0)).toString(36).toUpperCase();

  const docs = [];
  for(const id of r.docs){
    const sd = S.signed[id];
    if(sd) docs.push({id:id, title:DOCS[id].title, v:DOCS[id].v, hash:sd.hash, name:sd.name, time:sd.time, method:sd.method});
  }
  const fee = r.deposit.amount > 0 ? round2(r.deposit.amount * 0.018 + 0.20) : 0;

  S.committed = {
    ref:S.ref, svcName:svc.name, mins:svc.mins, price:svc.price,
    when: S.slot ? fmtDate(S.slot.date) + ', ' + hhmm(S.slot.min) : '',
    email:S.client.email || 'your email address',
    name:(S.client.first + ' ' + S.client.last).trim() || 'The client',
    paid: r.deposit.amount > 0 ? round2(r.deposit.amount + fee) : 0,
    depositOnly: r.deposit.amount,
    paidLabel: r.deposit.amount > 0 ? 'Paid now (' + r.deposit.label + ' plus fee)' : 'Paid now',
    docs:docs, rules:S.trace.filter(t => t.id.indexOf('RULE') === 0).map(t => t.id)
  };

  traceEvent('COMMIT', 'Booking ' + S.ref + ' committed atomically: slot locked, documents sealed, payment captured, calendar event written, booking pack sent to care@puremed.uk.', 'transaction = single');
  renderRecord();
}

/* ============================================================
   RECORD PANE
   ============================================================ */
function renderRecord(){
  const out = $('record-out');
  if(!S.committed){
    out.innerHTML = '<p class="empty">Nothing committed yet. Complete a booking to see the record.</p>';
    return;
  }
  const c = S.committed;
  const atts = c.docs.map(d =>
    '<div class="att"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>' +
    esc(d.id) + '-' + esc(c.ref) + '.pdf</div>'
  ).join('') || '<div style="font-size:11px;color:var(--mid-grey);margin-top:6px">No documents attached under the current settings.</div>';

  out.innerHTML =
    '<div class="rec"><h6>Booking record</h6>' +
      kv2('Reference', c.ref) + kv2('Client', c.name) + kv2('Service', c.svcName) +
      kv2('When', c.when) + kv2('Price at booking', gbp(c.price)) +
      kv2('Paid', c.paid > 0 ? gbp(c.paid) : 'Nothing taken') +
      kv2('Rules fired', c.rules.join(', ') || 'none') +
    '</div>' +

    '<div class="rec"><h6>Evidential documents</h6>' +
      (c.docs.length ? c.docs.map(d =>
        '<div style="margin-bottom:10px;padding-bottom:9px;border-bottom:1px solid rgba(245,239,229,.08)">' +
        '<div style="font-size:11.5px;font-weight:600;margin-bottom:4px">'+esc(d.title)+' <span style="opacity:.5">'+esc(d.v)+'</span></div>' +
        '<div style="font-size:10.5px;color:rgba(245,239,229,.5);margin-bottom:4px">Signed by '+esc(d.name)+', '+esc(d.time)+', '+esc(d.method)+'</div>' +
        '<div class="hash">'+esc(d.hash)+'</div></div>'
      ).join('') : '<p style="font-size:11.5px;color:rgba(245,239,229,.45)">None required by the current settings.</p>') +
    '</div>' +

    '<div class="rec"><h6>Sent to the practice, immediately</h6>' +
      '<div class="mail"><div class="mh">' +
        '<div><b>To</b> care@puremed.uk</div>' +
        '<div><b>Subj</b> New booking '+esc(c.ref)+', '+esc(c.svcName)+'</div>' +
      '</div>' +
      '<div>'+esc(c.name)+' has booked '+esc(c.svcName)+' for '+esc(c.when)+'. '+
      (c.paid > 0 ? gbp(c.paid)+' taken at booking. ' : 'No payment taken at booking. ') +
      'Signed documents attached. Full record and screening answers in the practice dashboard.</div>' +
      atts +
      '</div>' +
    '</div>' +

    '<div class="rec"><h6>Also written at commit</h6>' +
      kv2('Practitioner calendar', 'Event created, links back to record') +
      kv2('Client', 'Confirmation, ICS invitation, signed PDFs') +
      kv2('Audit log', S.trace.length + ' entries, append-only') +
    '</div>';
}
function kv2(a,b){ return '<div class="kv2"><span>'+esc(a)+'</span><span>'+esc(b)+'</span></div>'; }

/* ============================================================
   EVENTS
   ============================================================ */
function selectService(id, viaCard){
  const svc = svcById(id);
  if(!svc) return;
  S.svcId = id; S.cat = svc.cat; S.slot = null; S.screen = {}; S.blocked = null;
  S.signed = {}; S.clauses = {}; S.paid = false; S.docIdx = 0; S.rerouted = null;

  traceEvent('INPUT', 'Client selected: ' + svc.name + (viaCard ? ', from the treatments page' : ''), 'service_id = ' + svc.id);

  const r = resolve(svc);

  if(r.reroute){
    // Only the rule that caused the reroute is traced for the original
    // service. Its downstream requirements never applied, because the
    // booking never became that service.
    r.fired.filter(f => f.id === 'RULE-004').forEach(f => trace(f));
    S.rerouted = id;
    S.svcId = r.reroute;
    S.cat = svcById(r.reroute).cat;
    resolve(svcById(r.reroute)).fired.forEach(f => trace(f));
  } else {
    r.fired.forEach(f => trace(f));
  }
}

function bindBody(){
  const body = $('w-body');

  body.querySelectorAll('[data-cat]').forEach(b => b.onclick = () => { S.cat = b.dataset.cat; render(); });
  body.querySelectorAll('[data-svc]').forEach(b => b.onclick = () => { selectService(b.dataset.svc, false); render(); });

  body.querySelectorAll('[data-q]').forEach(b => b.onclick = () => {
    const q = SCREEN_Q.find(x => x.id === b.dataset.q);
    const val = b.dataset.v === '1';
    S.screen[q.id] = val;
    if(val && q.yes === 'block'){
      S.blocked = q;
      trace({id:q.rule, kind:'block', t:'BLOCK. ' + q.msg + ' Online booking stopped, client directed to contact the clinic.', in:q.id + ' = yes'});
    } else if(val && q.yes === 'flag'){
      if(S.blocked && S.blocked.id === q.id) S.blocked = null;
      trace({id:q.rule, kind:'flag', t:'FLAG. ' + q.msg + ' Booking will be made as a consultation.', in:q.id + ' = yes'});
    } else {
      if(S.blocked && S.blocked.id === q.id) S.blocked = null;
      trace({id:q.rule, kind:'pass', t:'PASS. No contraindication declared.', in:q.id + ' = no'});
    }
    render();
  });

  body.querySelectorAll('[data-week]').forEach(b => b.onclick = () => {
    S.weekStart = addDays(S.weekStart, 7 * Number(b.dataset.week));
    render();
  });
  body.querySelectorAll('[data-slot]').forEach(b => b.onclick = () => {
    const [t,m] = b.dataset.slot.split('|');
    S.slot = {key:b.dataset.slot, date:new Date(Number(t)), min:Number(m)};
    const svc = svcById(S.svcId);
    traceEvent('HOLD', 'Slot leased for 10 minutes: ' + fmtDate(S.slot.date) + ' ' + hhmm(S.slot.min) + ' to ' + hhmm(S.slot.min + svc.mins) + ', plus ' + CFG.buffer + ' min buffer. Nobody else can take it while the lease holds.', 'resource = nafisa, lease_ttl = 600s');
    render();
  });

  body.querySelectorAll('[data-f]').forEach(i => {
    i.oninput = () => { S.client[i.dataset.f] = i.value; };
  });

  body.querySelectorAll('[data-doc]').forEach(b => b.onclick = () => { S.docIdx = Number(b.dataset.doc); render(); });
  body.querySelectorAll('[data-clause]').forEach(cb => cb.onchange = () => {
    const r = resolve(svcById(S.svcId));
    const cur = DOCS[r.docs[S.docIdx]];
    S.clauses[cur.id] = S.clauses[cur.id] || {};
    S.clauses[cur.id][cb.dataset.clause] = cb.checked;
    if(cb.checked){
      traceEvent('CLAUSE', 'Clause ' + (Number(cb.dataset.clause)+1) + ' of ' + cur.id + ' ' + cur.v + ' acknowledged individually, with its own timestamp.', 'document = ' + cur.id + ', clause = ' + cb.dataset.clause);
    }
    render();
  });
  const clearBtn = body.querySelector('[data-sigclear]');
  if(clearBtn) clearBtn.onclick = () => {
    const cv = $('sigpad');
    if(cv && sigCtx){ sigCtx.clearRect(0,0,cv.width,cv.height); sigHasInk = false; }
  };
  const nameIn = $('sig-name');
  if(nameIn) nameIn.oninput = () => { S.sigName = nameIn.value; };

  const signBtn = $('btn-sign');
  if(signBtn) signBtn.onclick = async () => {
    const r = resolve(svcById(S.svcId));
    const cur = DOCS[r.docs[S.docIdx]];
    const typed = ($('sig-name') && $('sig-name').value.trim()) || '';
    const fallbackName = (S.client.first + ' ' + S.client.last).trim();
    if(!sigHasInk && !typed){
      alert('Draw your signature in the box, or type your full name.');
      return;
    }
    const method = sigHasInk ? 'drawn' : 'typed';
    const name = typed || fallbackName || 'Client';
    const time = new Date().toLocaleString('en-GB');
    const payload = cur.id + '|' + cur.v + '|' + name + '|' + time + '|' + method + '|' + cur.body.join(' ') + '|' + cur.clauses.join(' ');
    const hash = await sha256(payload);
    S.signed[cur.id] = {name:name, time:time, method:method, hash:hash};
    traceEvent('SIGN', cur.id + ' ' + cur.v + ' signed by ' + name + ', method ' + method + '. PDF rendered server-side and hashed. Version, timestamp, method, IP and per-clause events stored with it.', 'sha256 = ' + hash.slice(0,24) + '...');
    const nextUnsigned = r.docs.findIndex(d => !S.signed[d] && !DOCS[d].optional);
    if(nextUnsigned > -1) S.docIdx = nextUnsigned;
    render();
  };

  const authorise = (method) => {
    const r = resolve(svcById(S.svcId));
    const fee = round2(r.deposit.amount * 0.018 + 0.20);
    S.paid = true;
    traceEvent('PAYMENT', 'Payment intent authorised for ' + gbp(round2(r.deposit.amount + fee)) + ' via ' + method + ', manual capture. Simulated. If the commit that follows fails, this authorisation is voided and no booking exists.', 'idempotency_key = ' + (S.slot ? S.slot.key : 'n/a'));
    render();
  };
  const auth = $('btn-auth');
  if(auth) auth.onclick = () => authorise('card');
  const gpay = $('btn-gpay');
  if(gpay) gpay.onclick = () => authorise('Google Pay (preview)');
}

/* validation on leaving details */
function validateDetails(r){
  const e = {}, c = S.client;
  if(!c.first.trim()) e.first = 'Required';
  if(!c.last.trim()) e.last = 'Required';
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(c.email)) e.email = 'Enter a valid email address';
  if(!/^[\d\s+()-]{9,}$/.test(c.mobile)) e.mobile = 'Enter a valid mobile number';
  if(!c.dob) e.dob = 'Required';
  else if(r.ageMin){
    const dob = new Date(c.dob);
    let age = NOW.getFullYear() - dob.getFullYear();
    const m = NOW.getMonth() - dob.getMonth();
    if(m < 0 || (m === 0 && NOW.getDate() < dob.getDate())) age--;
    if(age < r.ageMin){
      e.dob = 'This treatment has a minimum age of ' + r.ageMin + '.';
      trace({id:'RULE-006', kind:'block', t:'BLOCK. Date of birth gives age ' + age + ', below the minimum of ' + r.ageMin + ' for this treatment.', in:'dob = ' + c.dob});
    } else {
      trace({id:'RULE-006', kind:'pass', t:'PASS. Age ' + age + ' meets the minimum of ' + r.ageMin + '.', in:'dob = ' + c.dob});
    }
  }
  S.errors = e;
  return Object.keys(e).length === 0;
}

/* ============================================================
   WIRING
   ============================================================ */
function openWidget(svcId){
  S.open = true;
  $('mount').hidden = false;
  $('site-view').style.display = 'none';
  traceEvent('START', 'Booking journey started from puremed.uk' + (svcId ? ', with treatment context carried from the page' : ''), 'tenant = puremed, channel = embedded widget');
  if(svcId){
    // Arriving with a treatment already named (a treatment-specific page):
    // skip the picker and open on the step after it, with the choice shown
    // as a locked context strip rather than an editable list. "Change"
    // clears the pin and drops back to the full picker.
    selectService(svcId, true);
    S.deepLinked = true;
    const a = activeSteps();
    S.step = a.length > 1 ? a[1].k : 'service';
  } else {
    // No treatment named (a generic entry point): show the full picker,
    // unpinned. freshState() already defaults cat:'consult' so Consultations
    // is the category shown first — viewService() adds a callout on top of
    // that, but nothing here pre-selects a service for the client.
    S.deepLinked = false;
    S.step = 'service';
  }
  render();
  $('mount').scrollIntoView({behavior:'smooth', block:'start'});
}
function clearDeepLink(){
  S.deepLinked = false;
  S.step = 'service';
  render();
}
function closeWidget(){
  $('mount').hidden = true;
  $('site-view').style.display = '';
  S.open = false;
}

function buildCards(){
  $('site-cards').innerHTML = SITE_CARDS.map(c => {
    const s = svcById(c.svc);
    return '<div class="pm-card" data-card="'+c.svc+'">' +
      '<div class="cat">'+esc(c.cat)+'</div>' +
      '<h4>'+esc(c.label)+'</h4>' +
      '<div class="meta"><span>'+gbp(s.price)+'</span><span>'+s.mins+' min</span></div>' +
      '<div style="margin-top:12px"><span style="font-size:12px;color:var(--navy);font-weight:600">Book &rarr;</span></div>' +
    '</div>';
  }).join('');
  document.querySelectorAll('[data-card]').forEach(el =>
    el.onclick = () => openWidget(el.dataset.card));
}

function bindShell(){
  $('cta-hero').onclick = () => openWidget(null);
  $('w-close').onclick = closeWidget;
  $('btn-reset').onclick = () => { S = freshState(); renderTrace(); renderRecord(); closeWidget(); };

  $('btn-back').onclick = () => { const p = prevStep(); if(p){ S.step = p; render(); } };
  $('btn-next').onclick = async () => {
    const svc = svcById(S.svcId), r = resolve(svc);
    if(S.step === 'confirm'){ S = freshState(); renderTrace(); renderRecord(); closeWidget(); return; }
    if(S.step === 'details' && !validateDetails(r)){ render(); return; }
    if(S.step === 'screen'){
      const flag = SCREEN_Q.find(q => S.screen[q.id] === true && q.yes === 'flag');
      if(flag && S.svcId !== 'consult-clinic'){
        traceEvent('REROUTE', 'Screening flag. Booking switched from ' + svc.name + ' to Skin Consultation so suitability can be assessed.', 'flag = ' + flag.id);
        S.svcId = 'consult-clinic'; S.slot = null; S.signed = {}; S.clauses = {}; S.paid = false;
        const r2 = resolve(svcById('consult-clinic'));
        r2.fired.forEach(f => trace(f));
      }
    }
    const n = nextStep();
    if(!n) return;
    if(n === 'confirm') await commit();
    S.step = n;
    render();
  };

  // inspector tabs
  document.querySelectorAll('.ins-tab').forEach(t => t.onclick = () => {
    document.querySelectorAll('.ins-tab').forEach(x => x.classList.remove('on'));
    document.querySelectorAll('.ins-pane').forEach(x => x.classList.remove('on'));
    t.classList.add('on');
    $('pane-' + t.dataset.pane).classList.add('on');
  });

  // admin controls
  const bind = (id, key, kind, label) => {
    const el = $(id);
    el.onchange = () => {
      CFG[key] = kind === 'bool' ? el.checked : (kind === 'num' ? Number(el.value) : el.value);
      traceEvent('CONFIG', 'Practice setting changed: ' + label + ' is now ' + (kind === 'bool' ? (el.checked ? 'on' : 'off') : el.value) + '. The journey recalculates immediately.', key + ' = ' + CFG[key]);
      if(S.svcId){
        S.signed = {}; S.clauses = {}; S.paid = false; S.docIdx = 0;
        const svc = svcById(S.svcId);
        if(key === 'priorConsult' || key === 'hasHistory'){ S.slot = null; }
        resolve(svc).fired.forEach(f => trace(f));
        const a = activeSteps();
        if(!a.some(s => s.k === S.step)) S.step = a[0].k;
      }
      if(S.open) render();
    };
  };
  bind('cfg-docs','docs','bool','require consent documents');
  bind('cfg-screen','screen','bool','require medical screening');
  bind('cfg-pay','pay','bool','take payment at booking');
  bind('cfg-priorconsult','priorConsult','bool','injectables need prior consultation');
  bind('cfg-hashistory','hasHistory','bool','client has consultation on record');
  bind('cfg-age','minAge','num','minimum age for injectables');
  bind('cfg-depmode','depMode','str','deposit mode');
  bind('cfg-depval','depVal','num','deposit value');
  bind('cfg-lead','leadHours','num','minimum notice');
  bind('cfg-grid','grid','num','slot grid');
  bind('cfg-buffer','buffer','num','post-treatment buffer');
  bind('cfg-cal','readCal','bool','read practitioner calendar');
}

/* boot */
S = freshState();
buildCards();
bindShell();
renderTrace();
renderRecord();
