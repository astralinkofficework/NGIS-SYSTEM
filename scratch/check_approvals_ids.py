import io

path = r'pages/principal/principal-approvals.html'
s = io.open(path, encoding='utf-8').read()
ids = [
    'statTotal', 'statPending', 'statRevision', 'urgentQueuesCount', 'mobUrgentCount',
    'authAllBtn', 'authAllBtnLabel', 'tabCountAll', 'tabCountPending', 'tabCountRevision',
    'tabCountApproved', 'totalCountFooter', 'showingCount', 'typeFilterSelect', 'searchInput',
    'approvalsTableBody', 'selectAllCheckbox', 'batchBar', 'batchCount', 'feedbackModal',
    'modalItemId', 'modalActionType', 'feedbackModalTitle', 'feedbackModalSubtitle',
    'modalNoteInput', 'toast',
]
missing = [i for i in ids if ('id="%s"' % i) not in s]
for i in ids:
    print(('OK  ' if i not in missing else 'MISS ') + i)
print('TOTAL_MISSING', len(missing))
