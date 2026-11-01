with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    c = f.read()

upcoming_start = c.find('ov-upcoming')
if upcoming_start != -1:
    print('=== OV-UPCOMING ===')
    print(c[upcoming_start:upcoming_start+1500].encode('ascii', 'ignore').decode())

deadlines_start = c.find('ov-deadlines')
if deadlines_start != -1:
    print('=== OV-DEADLINES ===')
    print(c[deadlines_start:deadlines_start+1500].encode('ascii', 'ignore').decode())
