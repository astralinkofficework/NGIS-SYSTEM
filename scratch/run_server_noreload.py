"""Launch the NGIS Flask app with the stat-reloader DISABLED.

The debug reloader watches the whole project tree (including scratch/), so any
file written during e2e runs aborts in-flight HTTP requests. This launcher keeps
debug error pages but stops the file watcher.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

if __name__ == "__main__":
    server.app.run(host="0.0.0.0", port=3000, debug=False, use_reloader=False, threaded=True)
