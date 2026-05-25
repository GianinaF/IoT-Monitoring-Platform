from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import pymysql
from werkzeug.security import check_password_hash
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE username = %s",
                    (username,)
                )
                user = cursor.fetchone()

            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                session['role'] = user['role']

                if user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('user_dashboard'))

            return render_template('login.html', error="Invalid credentials")

        finally:
            conn.close()

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total_devices FROM devices")
            total_devices = cursor.fetchone()['total_devices']

            cursor.execute("SELECT COUNT(*) AS online_devices FROM devices WHERE status = 'online'")
            online_devices = cursor.fetchone()['online_devices']

            cursor.execute("SELECT COUNT(*) AS total_alerts FROM alerts")
            total_alerts = cursor.fetchone()['total_alerts']

            cursor.execute("""
                SELECT 
                    d.device_id,
                    d.name,
                    d.type,
                    d.location,
                    d.status,
                    u.username
                FROM devices d
                JOIN users u ON d.user_id = u.user_id
                ORDER BY d.registered_at DESC
                LIMIT 10
            """)
            devices = cursor.fetchall()

        return render_template(
            'admin/dashboard.html',
            username=session.get('username'),
            total_devices=total_devices,
            online_devices=online_devices,
            total_alerts=total_alerts,
            devices=devices
        )

    finally:
        conn.close()

@app.route('/user/dashboard')
def user_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'user':
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS total_devices FROM devices WHERE user_id = %s",
                (session['user_id'],)
            )
            total_devices = cursor.fetchone()['total_devices']

            cursor.execute(
                "SELECT COUNT(*) AS online_devices FROM devices WHERE user_id = %s AND status = 'online'",
                (session['user_id'],)
            )
            online_devices = cursor.fetchone()['online_devices']

            cursor.execute("""
                SELECT COUNT(*) AS total_alerts
                FROM alerts a
                JOIN sensors s ON a.sensor_id = s.sensor_id
                JOIN devices d ON s.device_id = d.device_id
                WHERE d.user_id = %s
            """, (session['user_id'],))
            total_alerts = cursor.fetchone()['total_alerts']

            cursor.execute("""
                SELECT 
                    d.device_id,
                    d.name,
                    d.type,
                    d.location,
                    d.status
                FROM devices d
                WHERE d.user_id = %s
                ORDER BY d.registered_at DESC
                LIMIT 10
            """, (session['user_id'],))
            devices = cursor.fetchall()

        return render_template(
            'user/dashboard.html',
            username=session.get('username'),
            total_devices=total_devices,
            online_devices=online_devices,
            total_alerts=total_alerts,
            devices=devices
        )

    finally:
        conn.close()

@app.route('/admin/devices')
def admin_devices():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    d.device_id,
                    d.name,
                    d.type,
                    d.location,
                    d.status,
                    d.registered_at,
                    u.username
                FROM devices d
                JOIN users u ON d.user_id = u.user_id
                ORDER BY d.registered_at DESC
            """)
            devices = cursor.fetchall()

            cursor.execute("""
                SELECT user_id, username 
                FROM users 
                WHERE role = 'user'
                ORDER BY username
            """)
            users = cursor.fetchall()

        return render_template(
            'admin/devices.html',
            username=session.get('username'),
            devices=devices,
            users=users
        )

    finally:
        conn.close()

@app.route('/user/devices')
def user_devices():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'user':
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    device_id,
                    name,
                    type,
                    location,
                    status,
                    registered_at
                FROM devices
                WHERE user_id = %s
                ORDER BY registered_at DESC
            """, (session['user_id'],))

            devices = cursor.fetchall()

        return render_template(
            'user/devices.html',
            username=session.get('username'),
            devices=devices
        )

    finally:
        conn.close()

@app.route('/alerts')
def alerts():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            if session.get('role') == 'admin':
                cursor.execute("""
                    SELECT
                        a.alert_id,
                        a.message,
                        a.severity,
                        a.is_read,
                        a.triggered_at,
                        s.name AS sensor_name,
                        d.name AS device_name,
                        d.location
                    FROM alerts a
                    JOIN sensors s ON a.sensor_id = s.sensor_id
                    JOIN devices d ON s.device_id = d.device_id
                    ORDER BY a.triggered_at DESC
                """)
            else:
                cursor.execute("""
                    SELECT
                        a.alert_id,
                        a.message,
                        a.severity,
                        a.is_read,
                        a.triggered_at,
                        s.name AS sensor_name,
                        d.name AS device_name,
                        d.location
                    FROM alerts a
                    JOIN sensors s ON a.sensor_id = s.sensor_id
                    JOIN devices d ON s.device_id = d.device_id
                    WHERE d.user_id = %s
                    ORDER BY a.triggered_at DESC
                """, (session['user_id'],))

            alerts = cursor.fetchall()

        return render_template(
            'alerts.html',
            alerts=alerts
        )

    finally:
        conn.close()

@app.route('/admin/readings')
def admin_readings():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    r.reading_id,
                    r.value,
                    r.recorded_at,
                    s.name AS sensor_name,
                    s.unit,
                    d.name AS device_name,
                    d.location
                FROM sensor_readings r
                JOIN sensors s ON r.sensor_id = s.sensor_id
                JOIN devices d ON s.device_id = d.device_id
                ORDER BY r.recorded_at DESC
                LIMIT 30
            """)
            readings = cursor.fetchall()

            cursor.execute("""
                SELECT
                    s.sensor_id,
                    s.name AS sensor_name,
                    d.name AS device_name,
                    d.location
                FROM sensors s
                JOIN devices d ON s.device_id = d.device_id
                ORDER BY d.name, s.name
            """)
            sensors = cursor.fetchall()

        return render_template(
            'admin/readings.html',
            username=session.get('username'),
            readings=readings,
            sensors=sensors
        )

    finally:
        conn.close()


@app.route('/user/readings')
def user_readings():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'user':
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    r.reading_id,
                    r.value,
                    r.recorded_at,
                    s.name AS sensor_name,
                    s.unit,
                    d.name AS device_name,
                    d.location
                FROM sensor_readings r
                JOIN sensors s ON r.sensor_id = s.sensor_id
                JOIN devices d ON s.device_id = d.device_id
                WHERE d.user_id = %s
                ORDER BY r.recorded_at DESC
                LIMIT 30
            """, (session['user_id'],))

            readings = cursor.fetchall()

        return render_template(
            'user/readings.html',
            username=session.get('username'),
            readings=readings
        )

    finally:
        conn.close()


@app.route('/admin/devices/edit/<int:device_id>', methods=['GET', 'POST'])
def edit_device(device_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                user_id = request.form.get('user_id')
                name = request.form.get('name')
                device_type = request.form.get('type')
                location = request.form.get('location')
                status = request.form.get('status')

                if not user_id or not name or not device_type or not location or not status:
                    flash("All fields are required.", "error")
                    return redirect(url_for('edit_device', device_id=device_id))

                cursor.execute("""
                    UPDATE devices
                    SET user_id = %s,
                        name = %s,
                        type = %s,
                        location = %s,
                        status = %s
                    WHERE device_id = %s
                """, (user_id, name, device_type, location, status, device_id))

                conn.commit()
                flash("Device updated successfully.", "success")
                return redirect(url_for('admin_devices'))

            cursor.execute("""
                SELECT device_id, user_id, name, type, location, status
                FROM devices
                WHERE device_id = %s
            """, (device_id,))
            device = cursor.fetchone()

            cursor.execute("""
                SELECT user_id, username
                FROM users
                WHERE role = 'user'
                ORDER BY username
            """)
            users = cursor.fetchall()

        if not device:
            flash("Device not found.", "error")
            return redirect(url_for('admin_devices'))

        return render_template(
            'admin/edit_device.html',
            device=device,
            users=users
        )

    finally:
        conn.close()


@app.route('/admin/readings/edit/<int:reading_id>', methods=['GET', 'POST'])
def edit_reading(reading_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                sensor_id = request.form.get('sensor_id')
                value = request.form.get('value')

                if not sensor_id or not value:
                    flash("All fields are required.", "error")
                    return redirect(url_for('edit_reading', reading_id=reading_id))

                cursor.execute("""
                    UPDATE sensor_readings
                    SET sensor_id = %s,
                        value = %s
                    WHERE reading_id = %s
                """, (sensor_id, value, reading_id))

                conn.commit()
                flash("Reading updated successfully.", "success")
                return redirect(url_for('admin_readings'))

            cursor.execute("""
                SELECT reading_id, sensor_id, value, recorded_at
                FROM sensor_readings
                WHERE reading_id = %s
            """, (reading_id,))
            reading = cursor.fetchone()

            cursor.execute("""
                SELECT
                    s.sensor_id,
                    s.name AS sensor_name,
                    d.name AS device_name,
                    d.location
                FROM sensors s
                JOIN devices d ON s.device_id = d.device_id
                ORDER BY d.name, s.name
            """)
            sensors = cursor.fetchall()

        if not reading:
            flash("Reading not found.", "error")
            return redirect(url_for('admin_readings'))

        return render_template(
            'admin/edit_reading.html',
            reading=reading,
            sensors=sensors
        )

    finally:
        conn.close()

@app.route('/admin/devices/create', methods=['POST'])
def create_device():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    user_id = request.form.get('user_id')
    name = request.form.get('name')
    device_type = request.form.get('type')
    location = request.form.get('location')
    status = request.form.get('status')

    if not user_id or not name or not device_type or not location or not status:
        flash("All fields are required.", "error")
        return redirect(url_for('admin_devices'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO devices (user_id, name, type, location, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, name, device_type, location, status))

        conn.commit()
        flash("Device created successfully.", "success")
        return redirect(url_for('admin_devices'))

    finally:
        conn.close()

@app.route('/admin/devices/delete/<int:device_id>', methods=['POST'])
def delete_device(device_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM devices WHERE device_id = %s",
                (device_id,)
            )

        conn.commit()
        flash("Device deleted successfully.", "success")
        return redirect(url_for('admin_devices'))

    finally:
        conn.close()        

@app.route('/admin/readings/create', methods=['POST'])
def create_reading():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    sensor_id = request.form.get('sensor_id')
    value = request.form.get('value')

    if not sensor_id or not value:
        flash("All fields are required.", "error")
        return redirect(url_for('admin_readings'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO sensor_readings (sensor_id, value)
                VALUES (%s, %s)
            """, (sensor_id, value))

        conn.commit()
        flash("Reading created successfully.", "success")
        return redirect(url_for('admin_readings'))

    finally:
        conn.close()

@app.route('/admin/readings/delete/<int:reading_id>', methods=['POST'])
def delete_reading(reading_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sensor_readings WHERE reading_id = %s",
                (reading_id,)
            )

        conn.commit()
        flash("Reading deleted successfully.", "success")
        return redirect(url_for('admin_readings'))

    finally:
        conn.close()

@app.route('/user/devices/create', methods=['POST'])
def create_user_device():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'user':
        return redirect(url_for('login'))

    name = request.form.get('name')
    device_type = request.form.get('type')
    location = request.form.get('location')

    if not name or not device_type or not location:
        flash("All fields are required.", "error")
        return redirect(url_for('user_devices'))

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO devices (user_id, name, type, location, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (session['user_id'], name, device_type, location, 'offline'))

        conn.commit()
        flash("Device added successfully.", "success")
        return redirect(url_for('user_devices'))

    finally:
        conn.close()

@app.route('/api/devices', methods=['GET'])
def api_get_devices():
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    d.device_id,
                    d.name,
                    d.type,
                    d.location,
                    d.status,
                    d.registered_at,
                    u.username
                FROM devices d
                JOIN users u ON d.user_id = u.user_id
                ORDER BY d.device_id
            """)
            devices = cursor.fetchall()

        return jsonify(devices), 200

    finally:
        conn.close()


@app.route('/api/devices/<int:device_id>', methods=['GET'])
def api_get_single_device(device_id):
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    d.device_id,
                    d.name,
                    d.type,
                    d.location,
                    d.status,
                    d.registered_at,
                    u.username
                FROM devices d
                JOIN users u ON d.user_id = u.user_id
                WHERE d.device_id = %s
            """, (device_id,))
            device = cursor.fetchone()

        if not device:
            return jsonify({"error": "Device not found"}), 404

        return jsonify(device), 200

    finally:
        conn.close()


@app.route('/api/devices', methods=['POST'])
def api_create_device():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    user_id = data.get('user_id')
    name = data.get('name')
    device_type = data.get('type')
    location = data.get('location')
    status = data.get('status', 'offline')

    if not user_id or not name or not device_type or not location:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO devices (user_id, name, type, location, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, name, device_type, location, status))

            new_device_id = cursor.lastrowid

        conn.commit()

        return jsonify({
            "message": "Device created successfully",
            "device_id": new_device_id
        }), 201

    finally:
        conn.close()


@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def api_update_device(device_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    name = data.get('name')
    device_type = data.get('type')
    location = data.get('location')
    status = data.get('status')

    if not name or not device_type or not location or not status:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT device_id FROM devices WHERE device_id = %s",
                (device_id,)
            )
            device = cursor.fetchone()

            if not device:
                return jsonify({"error": "Device not found"}), 404

            cursor.execute("""
                UPDATE devices
                SET name = %s,
                    type = %s,
                    location = %s,
                    status = %s
                WHERE device_id = %s
            """, (name, device_type, location, status, device_id))

        conn.commit()

        return jsonify({
            "message": "Device updated successfully",
            "device_id": device_id
        }), 200

    finally:
        conn.close()


@app.route('/api/reports/summary', methods=['GET'])
def api_reports_summary():
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT status, COUNT(*) AS total
                FROM devices
                GROUP BY status
            """)
            devices_by_status = cursor.fetchall()

            cursor.execute("""
                SELECT severity, COUNT(*) AS total
                FROM alerts
                GROUP BY severity
            """)
            alerts_by_severity = cursor.fetchall()

            cursor.execute("""
                SELECT COUNT(*) AS total_readings
                FROM sensor_readings
            """)
            total_readings = cursor.fetchone()['total_readings']

        return jsonify({
            "devices_by_status": devices_by_status,
            "alerts_by_severity": alerts_by_severity,
            "total_readings": total_readings
        }), 200

    finally:
        conn.close()


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)