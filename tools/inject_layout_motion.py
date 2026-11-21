with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

motion_bridge = """
  /* Global Motion Design, Animation & GSAP Micro-Interaction System bridge */
  if (!window.NGIS_MOTION) {
    var motionScript = document.createElement('script');
    motionScript.src = (function() {
      var currentScript = document.currentScript;
      if (currentScript && currentScript.src) {
        return currentScript.src.replace(/layout\\.js.*$/, 'motion.js');
      }
      return '../../assets/js/motion.js';
    })();
    motionScript.defer = true;
    document.head.appendChild(motionScript);
  }
"""

target = "  /* Global Skeleton Loading System bridge */"
if "Global Motion Design, Animation & GSAP Micro-Interaction System bridge" not in text:
    if target in text:
        text = text.replace(target, motion_bridge.strip() + "\n\n  " + target, 1)
        with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Injected motion.js bridge into assets/js/layout.js!")
    else:
        print("Target not found in layout.js")
else:
    print("Motion bridge already in layout.js")
