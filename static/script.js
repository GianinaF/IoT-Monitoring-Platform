document.addEventListener('DOMContentLoaded', function () {
    // =========================
    // MOBILE NAVIGATION
    // =========================
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
    const mobileMenuClose = document.getElementById('mobileMenuClose');
    const mobileMenuLinks = document.querySelectorAll('.mobile-menu-link');
    const navLinks = document.querySelectorAll('.nav-link');

    function openMobileMenu() {
        if (!mobileToggle || !mobileMenu || !mobileMenuOverlay) return;

        mobileToggle.classList.add('active');
        mobileMenu.classList.add('active');
        mobileMenuOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMobileMenu() {
        if (!mobileToggle || !mobileMenu || !mobileMenuOverlay) return;

        mobileToggle.classList.remove('active');
        mobileMenu.classList.remove('active');
        mobileMenuOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (mobileToggle) {
        mobileToggle.addEventListener('click', function (e) {
            e.preventDefault();

            if (mobileMenu && mobileMenu.classList.contains('active')) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });
    }

    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', function (e) {
            e.preventDefault();
            closeMobileMenu();
        });
    }

    if (mobileMenuOverlay) {
        mobileMenuOverlay.addEventListener('click', closeMobileMenu);
    }

    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            navLinks.forEach(l => l.classList.remove('active'));

            if (!this.classList.contains('cta-button')) {
                this.classList.add('active');
            }
        });
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeMobileMenu();
        }
    });

    window.addEventListener('resize', function () {
        if (window.innerWidth > 992) {
            closeMobileMenu();
        }
    });

    // =========================
    // PENROSE ANIMATION
    // =========================
    if (typeof gsap !== 'undefined') {
        document.querySelectorAll('[data-origin]').forEach(function (el) {
            const origin = el.getAttribute('data-origin');

            if (origin) {
                gsap.set(el, {
                    transformOrigin: origin
                });
            }
        });

        gsap.to('g.circle-spinner', {
            rotation: 360,
            duration: 1.5,
            repeat: -1,
            ease: 'linear'
        });

        gsap.to('.penrose-bg', {
            opacity: 0.25,
            yoyo: true,
            duration: 3.5,
            repeat: -1
        });
    }

    // =========================
    // LOAD MOCK DATA
    // =========================
    fetch('/static/data.json')
        .then(response => response.json())
        .then(data => {
            const devices = data.devices || [];
            const alerts = data.alerts || [];

            const totalDevicesEl = document.getElementById('totalDevices');
            const onlineDevicesEl = document.getElementById('onlineDevices');
            const totalAlertsEl = document.getElementById('totalAlerts');
            const deviceTableBody = document.getElementById('deviceTableBody');
            const devicesPageTableBody = document.getElementById('devicesPageTableBody');
            const alertsTableBody = document.getElementById('alertsTableBody');

            if (totalDevicesEl) {
                totalDevicesEl.textContent = devices.length;
            }

            if (onlineDevicesEl) {
                const onlineDevices = devices.filter(device => device.status === 'online').length;
                onlineDevicesEl.textContent = onlineDevices;
            }

            if (totalAlertsEl) {
                totalAlertsEl.textContent = alerts.length;
            }

            if (deviceTableBody) {
                deviceTableBody.innerHTML = '';

                devices.forEach(device => {
                    const row = document.createElement('tr');

                    row.innerHTML = `
                        <td>${device.name}</td>
                        <td>${device.type}</td>
                        <td class="${device.status}">${device.status}</td>
                        <td>${device.value}</td>
                    `;

                    deviceTableBody.appendChild(row);
                });
            }

            if (devicesPageTableBody) {
                devicesPageTableBody.innerHTML = '';

                devices.forEach(device => {
                    const row = document.createElement('tr');

                    row.innerHTML = `
                        <td>${device.id}</td>
                        <td>${device.name}</td>
                        <td>${device.type}</td>
                        <td class="${device.status}">${device.status}</td>
                        <td>${device.value}</td>
                    `;

                    devicesPageTableBody.appendChild(row);
                });
            }

            if (alertsTableBody) {
                alertsTableBody.innerHTML = '';

                alerts.forEach(alert => {
                    const row = document.createElement('tr');

                    row.innerHTML = `
                        <td>${alert.id}</td>
                        <td>${alert.device}</td>
                        <td>${alert.message}</td>
                        <td>${alert.time}</td>
                    `;

                    alertsTableBody.appendChild(row);
                });
            }

            const chartCanvas = document.getElementById('deviceChart');

            if (chartCanvas && typeof Chart !== 'undefined') {
                const ctx = chartCanvas.getContext('2d');

                const labels = devices.map(device => device.name);
                const values = devices.map(device => device.value);

                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Device Values',
                            data: values,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }
        })
        .catch(error => console.error('Error loading data:', error));
});

function confirmDelete() {
    return confirm("Are you sure you want to delete this?");
}

function validateDeviceForm() {
    const name = document.querySelector('input[name="name"]');
    const type = document.querySelector('input[name="type"]');
    const location = document.querySelector('input[name="location"]');
    const user = document.querySelector('select[name="user_id"]');
    const status = document.querySelector('select[name="status"]');

    if (user && user.value === "") {
        alert("Please select a user.");
        return false;
    }

    if (name && name.value.trim().length < 2) {
        alert("Device name must be at least 2 characters.");
        return false;
    }

    if (type && type.value.trim().length < 2) {
        alert("Device type must be at least 2 characters.");
        return false;
    }

    if (location && location.value.trim().length < 2) {
        alert("Location must be at least 2 characters.");
        return false;
    }

    if (status && status.value === "") {
        alert("Please select a status.");
        return false;
    }

    return true;
}


function validateReadingForm() {
    const sensor = document.querySelector('select[name="sensor_id"]');
    const value = document.querySelector('input[name="value"]');

    if (sensor && sensor.value === "") {
        alert("Please select a sensor.");
        return false;
    }

    if (value && value.value.trim() === "") {
        alert("Please enter a reading value.");
        return false;
    }

    if (isNaN(value.value)) {
        alert("Reading value must be a number.");
        return false;
    }

    return true;
}

function validateUserDeviceForm() {
    const name = document.querySelector('input[name="name"]');
    const type = document.querySelector('input[name="type"]');
    const location = document.querySelector('input[name="location"]');

    if (name && name.value.trim().length < 2) {
        alert("Device name must be at least 2 characters.");
        return false;
    }

    if (type && type.value.trim().length < 2) {
        alert("Device type must be at least 2 characters.");
        return false;
    }

    if (location && location.value.trim().length < 2) {
        alert("Location must be at least 2 characters.");
        return false;
    }

    return true;
}