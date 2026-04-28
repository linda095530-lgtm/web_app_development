// ============================================
// 考古題收藏系統 — 全站 JavaScript
// ============================================

// Flash message 自動消失（5 秒後）
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
