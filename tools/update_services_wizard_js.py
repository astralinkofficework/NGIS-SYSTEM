with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = '''// Open / Close New Request Modal
function openNewRequestModal() {
  const modal = document.getElementById('mobileNewRequestModal');
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.style.overflow = 'hidden';
  }
}

function closeNewRequestModal() {
  const modal = document.getElementById('mobileNewRequestModal');
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    document.body.style.overflow = '';
  }
}'''

new_block = '''/* ═══════════════════════════════════════════════════════════════════
   GUIDED 4-STEP SERVICE REQUEST WIZARD CONTROLLER
   ═══════════════════════════════════════════════════════════════════ */
var srvWizardStep = 1;
var srvSelectedKey = 'enrollment_cert';
var srvSelectedTitle = 'Certificate of Enrollment';
var srvSelectedUrgency = 'standard';
var srvAttachedFile = null;
var srvIsDirty = false;

function openNewRequestModal() {
  const modal = document.getElementById('mobileNewRequestModal');
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
    srvWizardStep = 1;
    srvIsDirty = false;
    updateServiceWizardUI();
  }
}

function closeNewRequestModal(force) {
  if (!force && srvIsDirty) {
    const leave = window.confirm("You have an unsaved request in progress. Discard your input and close?");
    if (!leave) return;
  }
  const modal = document.getElementById('mobileNewRequestModal');
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    document.body.classList.remove('modal-open');
    document.body.style.overflow = '';
    srvWizardStep = 1;
    srvIsDirty = false;
    srvAttachedFile = null;
    const filePrev = document.getElementById('srvFilePreview');
    if (filePrev) filePrev.classList.add('hidden');
  }
}

function selectServiceOption(key, title) {
  srvSelectedKey = key;
  srvSelectedTitle = title;
  srvIsDirty = true;

  document.querySelectorAll('.service-opt-btn').forEach(btn => {
    btn.classList.remove('border-2', 'border-forest-700', 'bg-forest-50/50');
    btn.classList.add('border', 'border-surface-border', 'bg-white');
    const iconWrap = btn.querySelector('div:first-child');
    if (iconWrap) {
      iconWrap.classList.remove('bg-forest-100', 'text-forest-800');
      iconWrap.classList.add('bg-surface-subtle', 'text-ink-main');
    }
  });

  if (event && event.currentTarget) {
    const activeBtn = event.currentTarget;
    activeBtn.classList.remove('border', 'border-surface-border', 'bg-white');
    activeBtn.classList.add('border-2', 'border-forest-700', 'bg-forest-50/50');
    const iconWrap = activeBtn.querySelector('div:first-child');
    if (iconWrap) {
      iconWrap.classList.remove('bg-surface-subtle', 'text-ink-main');
      iconWrap.classList.add('bg-forest-100', 'text-forest-800');
    }
  }
}

function setServiceUrgency(urgency) {
  srvSelectedUrgency = urgency;
  srvIsDirty = true;
  const stdBtn = document.getElementById('srvUrgencyStandard');
  const urgBtn = document.getElementById('srvUrgencyUrgent');

  if (urgency === 'standard') {
    if (stdBtn) {
      stdBtn.className = 'p-2.5 rounded-xl border-2 border-forest-700 bg-forest-50/50 text-center text-xs font-normal text-forest-800 cursor-pointer';
    }
    if (urgBtn) {
      urgBtn.className = 'p-2.5 rounded-xl border border-surface-border bg-white text-center text-xs font-normal text-ink-muted cursor-pointer hover:border-forest-400';
    }
  } else {
    if (urgBtn) {
      urgBtn.className = 'p-2.5 rounded-xl border-2 border-forest-700 bg-forest-50/50 text-center text-xs font-normal text-forest-800 cursor-pointer';
    }
    if (stdBtn) {
      stdBtn.className = 'p-2.5 rounded-xl border border-surface-border bg-white text-center text-xs font-normal text-ink-muted cursor-pointer hover:border-forest-400';
    }
  }
}

function handleServiceFile(file) {
  if (!file) return;
  srvAttachedFile = file;
  srvIsDirty = true;
  const prevBox = document.getElementById('srvFilePreview');
  const nameEl = document.getElementById('srvFileName');
  const sizeEl = document.getElementById('srvFileSize');

  if (nameEl) nameEl.textContent = file.name;
  if (sizeEl) {
    const size = file.size >= 1024 * 1024 ? (file.size / (1024 * 1024)).toFixed(1) + ' MB' : Math.max(1, Math.round(file.size / 1024)) + ' KB';
    sizeEl.textContent = size + ' • Ready to attach';
  }
  if (prevBox) prevBox.classList.remove('hidden');
}

function removeServiceFile() {
  srvAttachedFile = null;
  const input = document.getElementById('srvFileInput');
  if (input) input.value = '';
  const prevBox = document.getElementById('srvFilePreview');
  if (prevBox) prevBox.classList.add('hidden');
}

function toggleServiceSubmitBtn() {
  const check = document.getElementById('srvConfirmCheck');
  const submitBtn = document.getElementById('srvSubmitBtn');
  if (submitBtn) {
    submitBtn.disabled = !check || !check.checked;
  }
}

function serviceWizardNav(delta) {
  if (delta > 0) {
    if (srvWizardStep === 1) {
      if (!srvSelectedKey) {
        if (window.toast) window.toast('Please choose a service to request.', 'warning');
        return;
      }
    } else if (srvWizardStep === 2) {
      const purpose = document.getElementById('srvPurpose');
      if (!purpose || !purpose.value) {
        if (window.toast) window.toast('Please select a purpose for your request.', 'warning');
        return;
      }
      srvIsDirty = true;
    }
  }

  srvWizardStep = Math.max(1, Math.min(4, srvWizardStep + delta));
  updateServiceWizardUI();
}

function updateServiceWizardUI() {
  const badge = document.getElementById('serviceWizardStepBadge');
  const title = document.getElementById('serviceWizardStepTitle');
  const prevBtn = document.getElementById('srvPrevBtn');
  const nextBtn = document.getElementById('srvNextBtn');
  const submitBtn = document.getElementById('srvSubmitBtn');

  // Step containers
  for (let s = 1; s <= 4; s++) {
    const stepEl = document.getElementById('serviceStep' + s);
    if (stepEl) {
      if (s === srvWizardStep) stepEl.classList.remove('hidden');
      else stepEl.classList.add('hidden');
    }
  }

  const titles = {
    1: 'Step 1 of 4: Select Service',
    2: 'Step 2 of 4: Request Information',
    3: 'Step 3 of 4: Supporting Documents',
    4: 'Step 4 of 4: Review & Submit'
  };

  const headers = {
    1: 'Select Service Request',
    2: 'Provide Request Details',
    3: 'Upload Supporting Documents',
    4: 'Review & Confirm Request'
  };

  if (badge) badge.textContent = titles[srvWizardStep] || '';
  if (title) title.textContent = headers[srvWizardStep] || '';

  if (prevBtn) {
    if (srvWizardStep > 1) prevBtn.classList.remove('hidden');
    else prevBtn.classList.add('hidden');
  }

  if (nextBtn) {
    if (srvWizardStep < 4) nextBtn.classList.remove('hidden');
    else nextBtn.classList.add('hidden');
  }

  if (submitBtn) {
    if (srvWizardStep === 4) {
      submitBtn.classList.remove('hidden');
      toggleServiceSubmitBtn();
    } else {
      submitBtn.classList.add('hidden');
    }
  }

  // Populate Step 4 Review Info
  if (srvWizardStep === 4) {
    const revService = document.getElementById('reviewService');
    const revPurpose = document.getElementById('reviewPurpose');
    const revUrgency = document.getElementById('reviewUrgency');
    const revDelivery = document.getElementById('reviewDelivery');
    const revFile = document.getElementById('reviewFile');

    const purposeVal = document.getElementById('srvPurpose')?.value || 'General Administrative';
    const deliveryVal = document.getElementById('srvDelivery')?.value || 'Digital PDF (Email)';

    if (revService) revService.textContent = srvSelectedTitle;
    if (revPurpose) revPurpose.textContent = purposeVal;
    if (revUrgency) revUrgency.textContent = srvSelectedUrgency === 'urgent' ? 'Urgent (24–48 hours)' : 'Standard (3–5 business days)';
    if (revDelivery) revDelivery.textContent = deliveryVal;
    if (revFile) revFile.textContent = srvAttachedFile ? srvAttachedFile.name : 'None attached';
  }

  const body = document.getElementById('serviceWizardBody');
  if (body) body.scrollTop = 0;
}

function submitServiceWizard() {
  const check = document.getElementById('srvConfirmCheck');
  if (!check || !check.checked) {
    if (window.toast) window.toast('Please check the confirmation box before submitting.', 'warning');
    return;
  }

  if (window.toast) {
    window.toast('Service request submitted successfully! Registry reference: SR-' + Math.floor(1000 + Math.random() * 9000), 'success');
  } else {
    alert('Service request submitted successfully!');
  }

  closeNewRequestModal(true);
}'''

if old_block in text:
    new_text = text.replace(old_block, new_block)
    with open('pages/student/student-services.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Successfully updated student-services.html JavaScript with guided wizard controller!')
else:
    print('Could not find old_block in student-services.html')
