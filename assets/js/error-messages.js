/**
 * ============================================================
 * NGIS ERP — Centralized Error Messages & Copy (Single Source of Truth)
 * Rule 5 Standard: Users never see backend errors, stack traces, SQL,
 * or raw JSON. Every message is human, empathetic, reassuring,
 * and includes a clear next step.
 * ============================================================
 */

(function (window) {
  "use strict";

  const NGISErrors = {
    // Generates a short pseudo-unique request/trace ID for internal logging
    generateRequestId() {
      const now = Date.now().toString(36).toUpperCase();
      const rand = Math.random().toString(36).substring(2, 6).toUpperCase();
      return `REQ-${now}-${rand}`;
    },

    // Master dictionary of user-facing error copy
    messages: {
      // Network & Connection
      NETWORK_OFFLINE: {
        title: "No Internet Connection",
        description: "You appear to be offline. Your recent edits are safely stored in your local browser cache and will sync automatically when you reconnect.",
        actionText: "Check Connection",
        type: "offline"
      },
      REQUEST_TIMEOUT: {
        title: "Request Timed Out",
        description: "The server is taking longer than usual to respond. Your data has not been lost. Please try again or refresh the page.",
        actionText: "Try Again",
        type: "timeout"
      },
      SERVER_UNAVAILABLE: {
        title: "Service Temporarily Unavailable",
        description: "We couldn't connect to the academic server right now. Our engineering team has been notified. Your data is safe.",
        actionText: "Try Again",
        type: "server"
      },
      UNEXPECTED_ERROR: {
        title: "Something Went Wrong",
        description: "An unexpected issue occurred while processing your request. Your changes have been preserved. Please try again.",
        actionText: "Try Again",
        type: "error"
      },

      // Navigation & Resources
      RESOURCE_NOT_FOUND: {
        title: "Record Not Found",
        description: "The academic dossier, document, or campus record you requested could not be located. It may have been archived or moved.",
        actionText: "Return to Dashboard",
        type: "not_found"
      },
      PAGE_NOT_FOUND: {
        title: "Page Not Found",
        description: "The campus page or directory URL does not exist or may have been moved. Your data is completely safe.",
        actionText: "Go to Portal Home",
        type: "not_found"
      },

      // Security & Authentication
      UNAUTHORIZED: {
        title: "Authentication Required",
        description: "Your session has expired or requires verification. Any unsaved drafts have been safely preserved in your browser.",
        actionText: "Sign In Again",
        type: "auth"
      },
      FORBIDDEN: {
        title: "Access Restricted",
        description: "You do not have the required role permissions to view this academic section. Please contact your campus administrator if you need access.",
        actionText: "Return to Dashboard",
        type: "permission"
      },

      // Operations & Data Entry
      SUBMISSION_FAILED: {
        title: "Could Not Save Changes",
        description: "We encountered a temporary issue while saving your updates. None of your inputs were cleared. Please try again.",
        actionText: "Retry Save",
        type: "error"
      },
      FILE_TOO_LARGE: {
        title: "Attachment Exceeds Size Limit",
        description: "The file you selected exceeds the maximum allowed upload limit (15 MB). Please choose a smaller file and try again.",
        actionText: "Choose Another File",
        type: "validation"
      },
      INVALID_FILE_TYPE: {
        title: "Unsupported File Format",
        description: "Only standard academic document formats (PDF, DOCX, XLSX, PNG, JPG) are supported. Please convert your file and retry.",
        actionText: "Select New File",
        type: "validation"
      },
      DUPLICATE_ENTRY: {
        title: "Record Already Exists",
        description: "An entry with this institutional code or ID is already registered in the system. Please review the details.",
        actionText: "Review Record",
        type: "validation"
      },
      VALIDATION_ERROR: {
        title: "Please Check Required Fields",
        description: "Some required information is missing or formatted incorrectly. Please review the highlighted fields below.",
        actionText: "Review Fields",
        type: "validation"
      }
    },

    /**
     * Resolve a friendly message given an error code, status, or raw error object.
     * Logs the raw technical detail internally to the console with a request ID,
     * but NEVER exposes stack traces, SQL, or URLs to the user interface.
     */
    resolve(err, context = {}) {
      const reqId = context.requestId || this.generateRequestId();
      const screen = context.screen || (window.location ? window.location.pathname.split("/").pop() : "unknown");

      // Log internally for debugging purposes only
      console.error(`[NGIS Error Log] [${reqId}] [Screen: ${screen}]`, {
        error: err,
        context: context,
        timestamp: new Date().toISOString()
      });

      if (!navigator.onLine) {
        return { ...this.messages.NETWORK_OFFLINE, requestId: reqId };
      }

      let code = "UNEXPECTED_ERROR";

      if (typeof err === "string") {
        if (this.messages[err]) code = err;
        else if (err.toLowerCase().includes("timeout")) code = "REQUEST_TIMEOUT";
        else if (err.toLowerCase().includes("offline") || err.toLowerCase().includes("network")) code = "NETWORK_OFFLINE";
      } else if (err && typeof err === "object") {
        const status = err.status || (err.response && err.response.status);
        if (status === 404) code = "RESOURCE_NOT_FOUND";
        else if (status === 401) code = "UNAUTHORIZED";
        else if (status === 403) code = "FORBIDDEN";
        else if (status === 408 || status === 504) code = "REQUEST_TIMEOUT";
        else if (status >= 500) code = "SERVER_UNAVAILABLE";
        else if (status === 400 || status === 422) code = "VALIDATION_ERROR";
        else if (status === 409) code = "DUPLICATE_ENTRY";
        else if (err.code && this.messages[err.code]) code = err.code;
      }

      const template = this.messages[code] || this.messages.UNEXPECTED_ERROR;
      return {
        ...template,
        requestId: reqId
      };
    }
  };

  // Export globally
  window.NGISErrors = NGISErrors;
})(window);

