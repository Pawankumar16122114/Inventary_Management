var App = {};

document.addEventListener('DOMContentLoaded', function () {
    App.initToasts();
    App.initSidebar();
    App.initModals();
    App.initSearch();
    App.initAnimations();
    App.initCharts();
});

App.initToasts = function () {
    document.querySelectorAll('.toast').forEach(function (t) {
        t.querySelector('.toast-close').addEventListener('click', function () { t.remove(); });
        setTimeout(function () {
            if (t.parentNode) t.style.animation = 'toastFadeOut 0.4s ease forwards';
            setTimeout(function () { if (t.parentNode) t.remove(); }, 500);
        }, 4000);
    });
};

App.showToast = function (message, type) {
    type = type || 'info';
    var icons = { success: 'check-circle', error: 'exclamation-circle', warning: 'triangle-exclamation', info: 'info-circle' };
    var container = document.querySelector('.toast-container');
    if (!container) { container = document.createElement('div'); container.className = 'toast-container'; document.body.appendChild(container); }
    var t = document.createElement('div');
    t.className = 'toast toast-' + type;
    t.innerHTML = '<div class="toast-icon"><i class="fas fa-' + (icons[type] || 'info-circle') + '"></i></div>'
        + '<span>' + message + '</span>'
        + '<button class="toast-close">&times;</button>';
    container.appendChild(t);
    t.querySelector('.toast-close').addEventListener('click', function () { t.remove(); });
    setTimeout(function () {
        t.style.animation = 'toastFadeOut 0.4s ease forwards';
        setTimeout(function () { if (t.parentNode) t.remove(); }, 500);
    }, 4000);
};

App.initSidebar = function () {
    var toggle = document.querySelector('.sidebar-toggle-btn');
    var sidebar = document.querySelector('.sidebar');
    var mainContent = document.querySelector('.main-content');
    var mobileBtn = document.querySelector('.mobile-menu-btn');
    var backdrop = document.querySelector('.sidebar-backdrop');

    if (localStorage.getItem('sidebarCollapsed') === 'true' && window.innerWidth > 768) {
        sidebar.classList.add('collapsed');
        if (mainContent) mainContent.classList.add('expanded');
    }

    if (toggle) {
        toggle.addEventListener('click', function () {
            var collapsed = sidebar.classList.toggle('collapsed');
            if (mainContent) mainContent.classList.toggle('expanded');
            if (window.innerWidth > 768) localStorage.setItem('sidebarCollapsed', collapsed);
        });
    }

    if (mobileBtn) {
        mobileBtn.addEventListener('click', function () {
            sidebar.classList.toggle('mobile-open');
            if (backdrop) backdrop.classList.toggle('active');
        });
    }

    if (backdrop) {
        backdrop.addEventListener('click', function () {
            sidebar.classList.remove('mobile-open');
            backdrop.classList.remove('active');
        });
    }
};

App.initModals = function () {
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            e.preventDefault();
            var msg = el.getAttribute('data-confirm') || 'Are you sure?';
            var action = el.getAttribute('data-action') || el.getAttribute('href');
            App.showConfirm(msg, function () {
                if (el.tagName === 'A') window.location.href = action;
                else if (el.tagName === 'FORM') el.submit();
                else if (el.tagName === 'BUTTON' && el.form) el.form.submit();
            });
        });
    });

    document.querySelectorAll('[data-delete-url]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            e.preventDefault();
            var name = el.getAttribute('data-name') || 'this item';
            var url = el.getAttribute('data-delete-url');
            var form = el.getAttribute('data-form-id');
            App.showConfirm('Are you sure you want to delete <strong>"' + name + '"</strong>? This action cannot be undone.', function () {
                if (form) document.getElementById(form).submit();
                else if (url) { var f = document.createElement('form'); f.method = 'POST'; f.action = url; var csrf = document.querySelector('[name=csrfmiddlewaretoken]'); if (csrf) { var inp = document.createElement('input'); inp.type = 'hidden'; inp.name = 'csrfmiddlewaretoken'; inp.value = csrf.value; f.appendChild(inp); } document.body.appendChild(f); f.submit(); }
            }, 'danger');
        });
    });
};

App.showConfirm = function (message, callback, type) {
    type = type || 'warning';
    var overlay = document.createElement('div');
    overlay.className = 'modal-overlay active';
    var icon = type === 'danger' ? 'triangle-exclamation' : 'circle-exclamation';
    overlay.innerHTML = '<div class="modal">'
        + '<div class="modal-icon ' + type + '"><i class="fas fa-' + icon + '"></i></div>'
        + '<h3>Confirm Action</h3>'
        + '<p>' + message + '</p>'
        + '<div class="modal-actions">'
        + '<button class="btn btn-secondary modal-cancel">Cancel</button>'
        + '<button class="btn btn-' + (type === 'danger' ? 'danger' : 'primary') + ' modal-confirm"><i class="fas fa-check"></i> Confirm</button>'
        + '</div></div>';
    document.body.appendChild(overlay);

    overlay.querySelector('.modal-cancel').addEventListener('click', function () { overlay.remove(); });
    overlay.querySelector('.modal-confirm').addEventListener('click', function () { overlay.remove(); if (callback) callback(); });
    overlay.addEventListener('click', function (e) { if (e.target === overlay) overlay.remove(); });
};

App.initSearch = function () {
    var searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(function (input) {
        var timer = null;
        input.addEventListener('input', function () {
            clearTimeout(timer);
            timer = setTimeout(function () {
                if (input.form) input.form.submit();
            }, 400);
        });
    });

    document.querySelectorAll('[data-filter-chips]').forEach(function (container) {
        container.querySelectorAll('.filter-chip .remove').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var chip = btn.closest('.filter-chip');
                var param = chip.getAttribute('data-param');
                var url = new URL(window.location);
                url.searchParams.delete(param);
                window.location = url.toString();
            });
        });
    });
};

App.initAnimations = function () {
    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.stat-card, .chart-card, .quick-action-card').forEach(function (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });

    var countEls = document.querySelectorAll('[data-count-to]');
    countEls.forEach(function (el) {
        var target = parseInt(el.getAttribute('data-count-to'));
        var duration = parseInt(el.getAttribute('data-count-duration')) || 800;
        var start = 0;
        var step = Math.max(1, Math.floor(target / (duration / 16)));
        var timer = setInterval(function () {
            start += step;
            if (start >= target) { start = target; clearInterval(timer); }
            el.textContent = start.toLocaleString();
        }, 16);
    });
};

App.initCharts = function () {
    if (typeof Chart === 'undefined') return;

    var origColor = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#94a3b8';
    var gridColor = 'rgba(255,255,255,0.04)';

    function initChart(id, config) {
        var canvas = document.getElementById(id);
        if (!canvas) return;
        var ctx = canvas.getContext('2d');
        config.options = config.options || {};
        config.options.responsive = true;
        config.options.maintainAspectRatio = false;
        config.options.plugins = config.options.plugins || {};
        config.options.plugins.legend = config.options.plugins.legend || {};
        config.options.plugins.legend.labels = config.options.plugins.legend.labels || {};
        config.options.plugins.legend.labels.color = origColor;
        config.options.plugins.tooltip = config.options.plugins.tooltip || {};
        config.options.plugins.tooltip.backgroundColor = 'rgba(17,24,39,0.95)';
        config.options.plugins.tooltip.titleColor = '#f1f5f9';
        config.options.plugins.tooltip.bodyColor = '#94a3b8';
        config.options.plugins.tooltip.borderColor = 'rgba(255,255,255,0.08)';
        config.options.plugins.tooltip.borderWidth = 1;
        config.options.plugins.tooltip.padding = 12;
        config.options.plugins.tooltip.cornerRadius = 8;
        if (config.options.scales) {
            Object.values(config.options.scales).forEach(function (scale) {
                scale.ticks = scale.ticks || {};
                scale.ticks.color = origColor;
                scale.grid = scale.grid || {};
                scale.grid.color = gridColor;
            });
        }
        new Chart(ctx, config);
    }

    function fetchAndRender(url, chartId, dataFn) {
        fetch(url).then(function (r) { return r.json(); }).then(function (data) {
            var cfg = dataFn(data);
            if (cfg && chartId) initChart(chartId, cfg);
        }).catch(function () {});
    }

    var chartDataUrl = document.querySelector('[data-chart-url]');
    if (chartDataUrl) {
        var url = chartDataUrl.getAttribute('data-chart-url');
        fetchAndRender(url, 'categoryChart', function (data) {
            if (!data.category_labels || !data.category_labels.length) return null;
            return {
                type: 'bar',
                data: {
                    labels: data.category_labels,
                    datasets: [{
                        label: 'Quantity',
                        data: data.category_quantity,
                        backgroundColor: [
                            'rgba(79,142,247,0.7)', 'rgba(139,92,246,0.7)',
                            'rgba(6,182,212,0.7)', 'rgba(34,197,94,0.7)',
                            'rgba(249,115,22,0.7)', 'rgba(236,72,153,0.7)',
                        ],
                        borderColor: ['#4f8ef7','#8b5cf6','#06b6d4','#22c55e','#f97316','#ec4899'],
                        borderWidth: 2,
                        borderRadius: 6,
                        borderSkipped: false,
                    }]
                },
                options: {
                    plugins: {
                        legend: { display: false },
                    },
                    scales: {
                        x: { grid: { display: false } },
                        y: { beginAtZero: true }
                    }
                }
            };
        });

        fetchAndRender(url, 'transactionChart', function (data) {
            if (!data.transaction_labels || !data.transaction_labels.length) return null;
            return {
                type: 'doughnut',
                data: {
                    labels: data.transaction_labels,
                    datasets: [{
                        data: data.transaction_counts,
                        backgroundColor: ['rgba(34,197,94,0.8)', 'rgba(239,68,68,0.8)', 'rgba(234,179,8,0.8)'],
                        borderWidth: 0,
                        hoverOffset: 8,
                    }]
                },
                options: {
                    plugins: {
                        legend: { position: 'bottom', labels: { padding: 16, usePointStyle: true, pointStyle: 'circle' } }
                    },
                    cutout: '65%',
                }
            };
        });
    }
};
