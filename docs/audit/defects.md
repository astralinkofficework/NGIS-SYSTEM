# NGIS-SYSTEM — Categorized Defect Backlog

## Shared Architectural Defects
1. **D-SH-01**: Unexpected centered layout on wide operational pages. (Fixed in S2/S3)
2. **D-SH-02**: Modal z-index occlusion by fixed navbar and mobile bottom nav. (Fixed: raised to 2100/2101)
3. **D-SH-03**: Broken sidebar icons showing text ligature fallbacks on shared deep links. (Fixed: root-relative asset path resolution)
4. **D-SH-04**: Duplicate "Log out" button rendered in sidebar nav links and sidebar footer. (Fixed: filtered in `layout.js`)
5. **D-SH-05**: Button text disappearing on hover due to white-on-white text collision. (Fixed: semantic variants)
6. **D-SH-06**: Frontend lag due to unthrottled resize/scroll event listeners. (Fixed: RAF debouncing)

## Page-Specific Defects
1. **D-ST-01**: Student dashboard hero previously displaying cyan gradient and test heading "Published Test Heading". (Fixed: restored to emerald green `#176B45` and "Student Academic Dashboard")
2. **D-ST-02**: Student dashboard clunky promo banner pushing academic content below the fold. (Fixed: hidden `.dash-banner-section`)
3. **D-PR-01**: Principal portal duplicating Admin Timetable Builder. (Fixed: converted to read-only Timetable Matrix with Adjustment Request)
