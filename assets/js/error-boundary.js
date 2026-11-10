/**
 * ============================================================
 * NGIS ERP — Global Error Boundary & API Interceptor (Rule 5 Compliant)
 * Rule 5: Users never see backend errors, 404, 500, stack traces,
 * SQL messages, request URLs, or raw JSON errors.
 * 
 * - Catches uncaught runtime errors and unhandled promise rejections
 * - Intercepts API fetch errors, logs technical details internally with Request ID
 * - Presents empathetic, human-friendly messages with "Try again" recovery
 * ============================================================
 */

(function (window, document) {
  "use strict";

  const NGISErrorBoundary = {
    initialized: false,

    init() {
      if (this.initialized) return;
      this.initialized = true;

      // 1. Global uncaught exception listener
      window.addEventListener("error", (event) => {
        // Prevent default browser error reporting popup
        const reqId = window.NGISErrors ? window.NGISErrors.generateRequestId() : "REQ-" + Date.now().toString(36).toUpperCase();
        console.error(`[NGIS Error Boundary] [${reqId}] Uncaught Exception:`, {
          message: event.message,
          filename: event.filename,
          lineno: event.lineno,
          colno: event.colno,
          error: event.error,
          timestamp: new Date().toISOString()
        });

        // If a fatal crash happens on a main container, render friendly recovery UI
        const mainContent = document.querySelector("main, #mainContent, .main-content, .content-wrap");
        if (mainContent && !mainContent.dataset.hasErrorBoundary) {
          mainContent.dataset.hasErrorBoundary = "true";
          if (window.NGISErrorState) {
            window.NGISErrorState.render(mainContent, {
              title: "Temporary Display Issue",
              message: "We encountered an unexpected display issue on this section. Your account data remains secure.",
              retryText: "Reload Section",
              requestId: reqId,
              onRetry: () => window.location.reload()
            });
          }
        }
      });

      // 2. Unhandled promise rejections listener
      window.addEventListener("unhandledrejection", (event) => {
        const reqId = window.NGISErrors ? window.NGISErrors.generateRequestId() : "REQ-" + Date.now().toString(36).toUpperCase();
        console.error(`[NGIS Error Boundary] [${reqId}] Unhandled Promise Rejection:`, {
          reason: event.reason,
          timestamp: new Date().toISOString()
        });

        // Show friendly toast notice if available
        if (window.NGISUI && window.NGISUI.toast) {
          const resolved = window.NGISErrors ? window.NGISErrors.resolve(event.reason, { requestId: reqId }) : null;
          const title = resolved ? resolved.title : "Temporary Sync Issue";
          const desc = resolved ? resolved.description : "Could not complete update. Your saved work is safe.";
          window.NGISUI.toast.error(title, desc);
        }
      });

      // 3. Global API fetch interceptor
      this.interceptFetch();
    },

    interceptFetch() {
      const originalFetch = window.fetch;
      if (!originalFetch) return;

      window.fetch = async function (...args) {
        try {
          const response = await originalFetch.apply(this, args);
          
          // Check for HTTP error status codes (5xx, 404, etc.)
          if (!response.ok && response.status >= 500) {
            const reqId = window.NGISErrors ? window.NGISErrors.generateRequestId() : "REQ-" + Date.now().toString(36).toUpperCase();
            console.error(`[NGIS API Interceptor] [${reqId}] Server Error ${response.status}:`, {
              url: args[0],
              status: response.status,
              timestamp: new Date().toISOString()
            });
          }
          return response;
        } catch (netErr) {
          const reqId = window.NGISErrors ? window.NGISErrors.generateRequestId() : "REQ-" + Date.now().toString(36).toUpperCase();
          console.error(`[NGIS API Interceptor] [${reqId}] Network Connection Failure:`, {
            url: args[0],
            error: netErr.message,
            timestamp: new Date().toISOString()
          });
          throw netErr;
        }
      };
    },

    /**
     * Safely run an API call with automatic friendly error state rendering into a target container
     */
    async safeApiCall(apiFn, container, options = {}) {
      if (typeof container === "string") container = document.querySelector(container);
      try {
        return await apiFn();
      } catch (err) {
        if (container && window.NGISErrorState) {
          window.NGISErrorState.render(container, {
            error: err,
            context: options.context,
            onRetry: options.onRetry || (() => this.safeApiCall(apiFn, container, options))
          });
        }
        throw err;
      }
    }
  };

  // Initialize
  NGISErrorBoundary.init();

  window.NGISErrorBoundary = NGISErrorBoundary;
})(window, document);

