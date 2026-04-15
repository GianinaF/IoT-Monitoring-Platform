fetch('/static/data.json')
  .then(response => response.json())
  .then(data => {
    const devices = data.devices;
    const alerts = data.alerts;

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

    if (chartCanvas) {
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