new_services_modal_html = '''<!-- ════════ RESPONSIVE GUIDED 4-STEP NEW SERVICE REQUEST MODAL ════════ -->
<div id="mobileNewRequestModal" class="hidden fixed inset-0 z-[9999] flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/60 backdrop-blur-sm transition-opacity" style="z-index: 9999;">
  <div class="absolute inset-0 cursor-pointer" onclick="closeNewRequestModal(false)"></div>
  <div class="relative w-full max-w-xl bg-white dark:bg-slate-900 rounded-t-3xl sm:rounded-3xl shadow-xl border border-slate-200 dark:border-slate-800 flex flex-col z-10 max-h-[92vh] sm:max-h-[88vh] overflow-hidden">
    <!-- Header with Step Indicator -->
    <div class="sticky top-0 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md z-20 border-b border-surface-border px-4 sm:px-6 py-3.5 flex items-center justify-between">
      <div>
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-forest-50 text-forest-800 border border-forest-200 text-[11px] font-normal mb-0.5">
          <span class="w-1.5 h-1.5 rounded-full bg-forest-600"></span>
          <span id="serviceWizardStepBadge">Step 1 of 4: Select Service</span>
        </div>
        <h2 id="serviceWizardStepTitle" class="text-base sm:text-lg text-forest-800 dark:text-slate-100 font-normal font-display">
          Select Service Request
        </h2>
      </div>
      <!-- Working X Close button -->
      <button type="button" onclick="closeNewRequestModal(false)" class="w-8 h-8 rounded-full bg-surface-subtle hover:bg-surface-border flex items-center justify-center text-ink-muted hover:text-forest-800 transition cursor-pointer" title="Close Request (Esc)" aria-label="Close">
        <span class="material-symbols-outlined text-[18px]">close</span>
      </button>
    </div>

    <!-- Scrollable Form Body for 4 Steps -->
    <div class="flex-1 overflow-y-auto p-4 sm:p-6 flex flex-col gap-4 pb-24 sm:pb-22" id="serviceWizardBody">
      
      <!-- ═════════ STEP 1: SELECT SERVICE ═════════ -->
      <div id="serviceStep1" class="space-y-3">
        <p class="text-xs text-ink-muted font-normal">Choose the academic service or institutional document you wish to request:</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5" id="serviceOptionsGrid">
          <button type="button" onclick="selectServiceOption('enrollment_cert', 'Certificate of Enrollment')" class="service-opt-btn p-3.5 rounded-2xl border-2 border-forest-700 bg-forest-50/50 text-left transition flex items-start gap-3 cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-forest-100 text-forest-800 flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[20px]">badge</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-medium text-forest-800 leading-tight">Certificate of Enrollment</div>
              <div class="text-[11px] text-ink-soft mt-0.5">Official proof of active enrollment</div>
            </div>
          </button>

          <button type="button" onclick="selectServiceOption('transcript', 'Official Academic Transcript')" class="service-opt-btn p-3.5 rounded-2xl border border-surface-border hover:border-forest-400 bg-white text-left transition flex items-start gap-3 cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-surface-subtle text-ink-main flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[20px]">history_edu</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-medium text-ink-main leading-tight">Academic Transcript</div>
              <div class="text-[11px] text-ink-soft mt-0.5">Official grades and course records</div>
            </div>
          </button>

          <button type="button" onclick="selectServiceOption('id_card', 'Student ID Card Replacement')" class="service-opt-btn p-3.5 rounded-2xl border border-surface-border hover:border-forest-400 bg-white text-left transition flex items-start gap-3 cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-surface-subtle text-ink-main flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[20px]">credit_card</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-medium text-ink-main leading-tight">Student ID Card</div>
              <div class="text-[11px] text-ink-soft mt-0.5">Replacement for lost or damaged card</div>
            </div>
          </button>

          <button type="button" onclick="selectServiceOption('leave', 'Leave of Absence Request')" class="service-opt-btn p-3.5 rounded-2xl border border-surface-border hover:border-forest-400 bg-white text-left transition flex items-start gap-3 cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-surface-subtle text-ink-main flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[20px]">event_busy</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-medium text-ink-main leading-tight">Leave of Absence</div>
              <div class="text-[11px] text-ink-soft mt-0.5">Formal medical or planned leave</div>
            </div>
          </button>

          <button type="button" onclick="selectServiceOption('recommendation', 'Recommendation Letter')" class="service-opt-btn p-3.5 rounded-2xl border border-surface-border hover:border-forest-400 bg-white text-left transition flex items-start gap-3 cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-surface-subtle text-ink-main flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[20px]">recommend</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-medium text-ink-main leading-tight">Recommendation Letter</div>
              <div class="text-[11px] text-ink-soft mt-0.5">Faculty reference for applications</div>
            </div>
          </button>

          <button type="button" onclick="selectServiceOption('other', 'Other Administrative Request')" class="service-opt-btn p-3.5 rounded-2xl border border-surface-border hover:border-forest-400 bg-white text-left transition flex items-start gap-3 cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-surface-subtle text-ink-main flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[20px]">more_horiz</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-medium text-ink-main leading-tight">Other Request</div>
              <div class="text-[11px] text-ink-soft mt-0.5">Custom administrative inquiry</div>
            </div>
          </button>
        </div>
      </div>

      <!-- ═════════ STEP 2: REQUEST INFORMATION ═════════ -->
      <div id="serviceStep2" class="space-y-4 hidden">
        <div>
          <label class="block text-xs font-medium text-forest-800 mb-1" for="srvPurpose">
            Purpose of Request <span class="text-rose-500">*</span>
          </label>
          <select id="srvPurpose" class="w-full text-xs rounded-xl border border-surface-border p-2.5 bg-white text-slate-800 focus:border-forest-700">
            <option value="Visa & Embassy Application">Visa &amp; Embassy Application</option>
            <option value="University Application">University / College Application</option>
            <option value="Scholarship Program">Scholarship Application</option>
            <option value="Personal Records">Personal Records</option>
            <option value="Medical Documentation">Medical or Health Documentation</option>
            <option value="Other">Other Specific Purpose</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-medium text-forest-800 mb-1" for="srvDetails">
            Specific Details &amp; Additional Information
          </label>
          <textarea id="srvDetails" rows="3" placeholder="Provide any specific requirements, recipient institutions, or dates…" class="w-full text-xs rounded-xl border border-surface-border p-2.5 bg-white text-slate-800 focus:border-forest-700 leading-relaxed"></textarea>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-medium text-forest-800 mb-1">
              Processing Urgency
            </label>
            <div class="grid grid-cols-2 gap-2">
              <button type="button" id="srvUrgencyStandard" onclick="setServiceUrgency('standard')" class="p-2.5 rounded-xl border-2 border-forest-700 bg-forest-50/50 text-center text-xs font-normal text-forest-800 cursor-pointer">
                Standard (3–5 days)
              </button>
              <button type="button" id="srvUrgencyUrgent" onclick="setServiceUrgency('urgent')" class="p-2.5 rounded-xl border border-surface-border bg-white text-center text-xs font-normal text-ink-muted cursor-pointer hover:border-forest-400">
                Urgent (24–48h)
              </button>
            </div>
          </div>

          <div>
            <label class="block text-xs font-medium text-forest-800 mb-1" for="srvDelivery">
              Delivery Method
            </label>
            <select id="srvDelivery" class="w-full text-xs rounded-xl border border-surface-border p-2.5 bg-white text-slate-800 focus:border-forest-700">
              <option value="Digital PDF (Email)">Digital PDF (Delivered to Student Email)</option>
              <option value="Physical Pick-up (Registrar)">Physical Copy (Pick up at Registrar)</option>
              <option value="Sealed Official Envelope">Official Sealed Envelope (Campus Pick-up)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- ═════════ STEP 3: SUPPORTING DOCUMENTS ═════════ -->
      <div id="serviceStep3" class="space-y-4 hidden">
        <p class="text-xs text-ink-muted font-normal">Attach any required supporting documentation (e.g., previous transcripts, medical clearance, embassy forms):</p>
        
        <div id="srvDropzone" class="border-2 border-dashed border-surface-border hover:border-forest-400 rounded-2xl p-6 text-center bg-surface-subtle/40 transition cursor-pointer" onclick="document.getElementById('srvFileInput').click()">
          <input type="file" id="srvFileInput" class="hidden" accept=".pdf,.png,.jpg,.jpeg,.doc,.docx" onchange="handleServiceFile(this.files[0])" />
          <div class="w-10 h-10 rounded-full bg-forest-50 text-forest-700 flex items-center justify-center mx-auto mb-2">
            <span class="material-symbols-outlined text-[20px]">upload_file</span>
          </div>
          <div class="text-xs font-medium text-forest-800">Click or drag file to attach</div>
          <div class="text-[11px] text-ink-soft mt-1">Supports PDF, PNG, JPG, or DOCX (Max 20 MB)</div>
        </div>

        <div id="srvFilePreview" class="hidden bg-white border border-surface-border rounded-2xl p-3.5 flex items-center justify-between gap-3 shadow-xs">
          <div class="flex items-center gap-2.5 min-w-0">
            <span class="material-symbols-outlined text-forest-700 text-[20px]">description</span>
            <div class="min-w-0">
              <div id="srvFileName" class="text-xs font-medium text-forest-800 truncate">document.pdf</div>
              <div id="srvFileSize" class="text-[11px] text-ink-soft">1.2 MB</div>
            </div>
          </div>
          <button type="button" onclick="removeServiceFile()" class="p-1.5 rounded-lg text-rose-600 hover:bg-rose-50 transition cursor-pointer" title="Remove attachment">
            <span class="material-symbols-outlined text-[18px]">delete</span>
          </button>
        </div>
      </div>

      <!-- ═════════ STEP 4: REVIEW & SUBMIT ═════════ -->
      <div id="serviceStep4" class="space-y-4 hidden">
        <div class="bg-forest-50/60 border border-forest-200 rounded-2xl p-4 space-y-2.5 text-xs">
          <div class="flex items-center justify-between pb-2 border-b border-forest-200/60">
            <span class="text-ink-soft">Requested Service:</span>
            <span id="reviewService" class="font-medium text-forest-800">Certificate of Enrollment</span>
          </div>
          <div class="flex items-center justify-between pb-2 border-b border-forest-200/60">
            <span class="text-ink-soft">Purpose:</span>
            <span id="reviewPurpose" class="font-medium text-forest-800">Visa &amp; Embassy Application</span>
          </div>
          <div class="flex items-center justify-between pb-2 border-b border-forest-200/60">
            <span class="text-ink-soft">Urgency &amp; Turnaround:</span>
            <span id="reviewUrgency" class="font-medium text-forest-800">Standard (3–5 business days)</span>
          </div>
          <div class="flex items-center justify-between pb-2 border-b border-forest-200/60">
            <span class="text-ink-soft">Delivery:</span>
            <span id="reviewDelivery" class="font-medium text-forest-800">Digital PDF (Email)</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-ink-soft">Supporting Document:</span>
            <span id="reviewFile" class="font-medium text-forest-800">None attached</span>
          </div>
        </div>

        <div class="flex items-start gap-2.5 p-3 rounded-xl bg-surface-subtle border border-surface-borderLight text-xs">
          <input type="checkbox" id="srvConfirmCheck" class="rounded border-slate-300 text-forest-700 focus:ring-forest-600 mt-0.5 cursor-pointer" onchange="toggleServiceSubmitBtn()" />
          <label for="srvConfirmCheck" class="text-ink-muted cursor-pointer font-normal leading-relaxed">
            I confirm that the above request details are accurate and acknowledge that official documents are digitally logged in the NGIS Registrar Registry.
          </label>
        </div>
      </div>

    </div>

    <!-- Sticky Bottom Bar inside Modal -->
    <div class="sticky bottom-0 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md px-4 sm:px-6 py-3.5 border-t border-surface-border flex items-center justify-between gap-3 z-20 pb-safe">
      <button type="button" id="srvPrevBtn" onclick="serviceWizardNav(-1)" class="px-4 py-2.5 rounded-xl border border-surface-border bg-white hover:bg-surface-subtle text-slate-700 text-xs font-normal transition cursor-pointer hidden">
        Back
      </button>

      <div class="flex items-center gap-2 ml-auto">
        <button type="button" onclick="closeNewRequestModal(false)" class="px-4 py-2.5 rounded-xl text-ink-muted hover:text-slate-800 text-xs font-normal transition cursor-pointer">
          Cancel
        </button>
        <button type="button" id="srvNextBtn" onclick="serviceWizardNav(1)" class="px-5 py-2.5 rounded-xl bg-forest-800 hover:bg-forest-900 text-white text-xs font-normal transition shadow-xs flex items-center gap-1.5 cursor-pointer">
          <span>Continue</span>
          <span class="material-symbols-outlined text-[16px]">arrow_forward</span>
        </button>
        <button type="button" id="srvSubmitBtn" onclick="submitServiceWizard()" class="px-5 py-2.5 rounded-xl bg-forest-800 hover:bg-forest-900 text-white text-xs font-normal transition shadow-xs flex items-center gap-1.5 cursor-pointer hidden disabled:opacity-40 disabled:cursor-not-allowed" disabled>
          <span>Submit Request</span>
          <span class="material-symbols-outlined text-[16px]">check</span>
        </button>
      </div>
    </div>
  </div>
</div>
'''

with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find start and end of mobileNewRequestModal in text
idx1 = text.find('<!-- ════════ RESPONSIVE NEW SERVICE REQUEST MODAL ════════ -->')
idx2 = text.find('<!-- ════════ UNIFIED SERVICE HUB JAVASCRIPT ════════ -->')

if idx1 != -1 and idx2 != -1:
    new_text = text[:idx1] + new_services_modal_html + '\n\n' + text[idx2:]
    with open('pages/student/student-services.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Successfully replaced service request modal with 4-step wizard HTML!')
else:
    print('Could not find modal markers in student-services.html')
