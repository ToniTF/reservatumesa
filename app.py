from flask import Flask,render_template,request,redirect,url_for,session
import db
import bcrypt  # Add this import for password hashing
from config import Config  # Import Config class
import json
from datetime import timedelta
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY  # Set the secret key from Config

# Configuración para la carga de archivos
UPLOAD_FOLDER = os.path.join('static', 'img', 'restaurants')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Asegurarse de que la carpeta existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')




# ------------- Parte de Usuario -------------

@app.route('/login_user')
def login_page():
    return render_template('user/login_user.html')

@app.route('/logged_user', methods=['POST'])
def login():
    # Obtener los datos del formulario: ahora usamos email en lugar de username
    email = request.form['email']
    password = request.form['password']
    
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            # Buscar el usuario por email
            query = "SELECT * FROM client WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            if user:
                stored_password = user['password'].encode('utf-8')
                # Verificar la contraseña con bcrypt
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    # Guardar datos en la sesión (incluyendo username)
                    session['email'] = email
                    session['client_id'] = user['client_id']
                    session['username'] = user['username']  # Se guarda el username
                    return redirect(url_for('userhome'))
                else:
                    return render_template("user/login_user.html", message="Email o contraseña incorrecta")
            else:
                return render_template("user/login_user.html", message="Email o contraseña incorrecta")
    except Exception as e:
        print("Ocurrió un error al conectar a la base de datos: ", e)
        return render_template("home.html", message="Error de conexión a la base de datos")
    finally:    
        connection.close()
        print("Conexión cerrada")
                
@app.route('/register_user')
def register_page():
    return render_template('user/register_user.html')

@app.route('/userhome')
def userhome():
    if 'username' in session:
        # coger la lista de restaurantes y sus data
        connection = db.get_connection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM restaurant ORDER BY restaurant_name ASC"
                cursor.execute(query)
                restaurants = cursor.fetchall()
                return render_template('user/home.html',restaurants=restaurants)
        except Exception as e:
            print("Ocurrió un error al conectar a la bbdd: ", e)
        finally:
            connection.close()
            print("Conexión cerrada")
    else:
        return redirect(url_for('home')) 
    
    
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_details(restaurant_id):
    if 'username' in session:
        connection = db.get_connection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM restaurant WHERE restaurant_id = %s"
                data = (restaurant_id,)  # Add comma to make this a tuple
                cursor.execute(query,data)
                restaurant = cursor.fetchone()
                return render_template('user/restaurant.html', restaurant=restaurant)
        except Exception as e:
            print("Ocurrió un error al conectar a la bbdd: ", e)
        finally:
            connection.close()
            print("Conexión cerrada")    
    else:
        return redirect(url_for('home'))
    

@app.route('/user/home')
def user_home():
    if 'username' not in session or session.get('user_type') != 'client':
        return redirect(url_for('login_page'))
    
    # Obtener los IDs de cocina seleccionados
    selected_cuisines = request.args.getlist('cuisine_ids')
    
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            # 1. Obtener todos los tipos de cocina para mostrar en el filtro
            cursor.execute("SELECT * FROM cuisine_type ORDER BY cuisine_name")
            cuisine_types = cursor.fetchall()
            
            # 2. Construir la consulta según los filtros
            if selected_cuisines:
                # Si hay filtros seleccionados, buscar restaurantes que tengan alguno de esos tipos
                placeholders = ", ".join(["%s"] * len(selected_cuisines))
                query = f"""
                SELECT DISTINCT r.* FROM restaurant r
                JOIN restaurant_cuisine rc ON r.restaurant_id = rc.restaurant_id
                WHERE rc.cuisine_id IN ({placeholders})
                ORDER BY r.restaurant_name
                """
                cursor.execute(query, selected_cuisines)
            else:
                # Si no hay filtros, mostrar todos
                cursor.execute("SELECT * FROM restaurant ORDER BY restaurant_name")
            
            restaurants = cursor.fetchall()
            
            # 3. Para cada restaurante, obtener sus tipos de cocina
            for restaurant in restaurants:
                cuisine_query = """
                SELECT ct.cuisine_name FROM cuisine_type ct
                JOIN restaurant_cuisine rc ON ct.cuisine_id = rc.cuisine_id
                WHERE rc.restaurant_id = %s
                """
                cursor.execute(cuisine_query, (restaurant['restaurant_id'],))
                cuisine_results = cursor.fetchall()
                restaurant['cuisine_types'] = [cuisine['cuisine_name'] for cuisine in cuisine_results]
            
            return render_template('user/home.html', 
                                  restaurants=restaurants,
                                  cuisine_types=cuisine_types,
                                  selected_cuisines=selected_cuisines)
    except Exception as e:
        print("Error al cargar restaurantes:", e)
        return render_template('user/home.html', message="Error al cargar restaurantes")
    finally:
        connection.close()

# ------------- Parte de Restaurante -------------

@app.route('/login_restaurant')
def login_pageRest():
    return render_template('restaurant/login_restaurant.html')
        
@app.route('/restaurant',methods=['POST'])
def loginRest():
    # obtener los datos del formulario: usamos email en lugar de username
    email = request.form['email']  
    password = request.form['password']
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM restaurant WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            if user:
                stored_password = user['password'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    # Guardar datos en la sesión
                    session['email'] = email
                    session['username'] = user['username']
                    session['user_type'] = 'restaurant'
                    session['restaurant_id'] = user['restaurant_id']
                    session['restaurant_name'] = user['restaurant_name']
                    return redirect(url_for('restaurant'))
                else:
                    return render_template("restaurant/login_restaurant.html", message="Email o contraseña incorrecta")
            else:
                return render_template("restaurant/login_restaurant.html", message="Email o contraseña incorrecta")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
        return render_template("home.html", message="Error de conexión a la base de datos")
    finally:    
        connection.close()

@app.route('/register_restaurant')
def register_pageRest():
    return render_template('restaurant/register_restaurant.html')

        
@app.route('/registered_restaurant', methods=['POST'])
def register_restaurant():
    # Obtener datos del formulario
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']  # Contraseña repetida
    email = request.form['email']          # Nuevo campo
    restaurant_name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    website = request.form['website']
    capacity = request.form['capacity']
    description = request.form['description']
    
    # Verificar que ambas contraseñas sean idénticas
    if password != password2:
        return render_template("restaurant/register_restaurant.html", mensaje="Las contraseñas no coinciden")
    
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            # Verificar si el email ya está registrado
            query = "SELECT * FROM restaurant WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            if user:
                return render_template("restaurant/register_restaurant.html", mensaje="El email ya está registrado")
            else:
                # Manejar la imagen si se proporciona
                image = request.files.get('restaurant_image')
                if image and image.filename and allowed_file(image.filename):
                    # Si se ha subido una imagen válida
                    from werkzeug.utils import secure_filename
                    import os, time
                    secure_filename_value = secure_filename(image.filename)
                    timestamp = int(time.time())
                    filename = f"{timestamp}_{secure_filename_value}"
                    # Crear directorio si no existe
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    image_path = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(image_path)
                    image_name = filename
                else:
                    # Si no se sube una imagen, asignar la imagen por defecto
                    image_name = "aquitulogo-27.webp"
                
                # Encriptar la contraseña
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                # Modificar la consulta para incluir el campo image
                query = """
                    INSERT INTO restaurant (username, password, restaurant_name, phone, address, website, capacity, description, email, image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                data = (username, hashed, restaurant_name, phone, address, website, capacity, description, email, image_name)
                cursor.execute(query, data)
                connection.commit()
                return render_template("home.html", mensaje="Restaurante registrado correctamente")
    except Exception as e:
        print("Ocurrió un error al registrar: ", e)
        return render_template("restaurant/register_restaurant.html", mensaje="Error al registrar el restaurante")
    finally:
        connection.close()

@app.route('/restaurant')
def restaurant():
    if 'username' in session and session.get('user_type') == 'restaurant':
        connection = db.get_connection()
        try:
            with connection.cursor() as cursor:
                # Obtener datos del restaurante
                query = "SELECT * FROM restaurant WHERE restaurant_id = %s"
                cursor.execute(query, (session['restaurant_id'],))
                restaurant = cursor.fetchone()
                
                if restaurant:
                    # Si se pasa una fecha en la URL, usar vista de calendario
                    selected_date = request.args.get('date')
                    
                    if selected_date:
                        # Vista de calendario para la fecha especificada
                        query = """
                            SELECT r.*, c.username as client_name 
                            FROM reservation r
                            JOIN client c ON r.client_id = c.client_id
                            WHERE r.restaurant_id = %s AND r.date = %s 
                              AND (r.status != 'cancelada' OR r.status IS NULL)
                            ORDER BY r.time
                        """
                        cursor.execute(query, (restaurant['restaurant_id'], selected_date))
                        all_reservations = cursor.fetchall()
                        
                        # Definir franjas (ejemplo para lunch y cena)
                        lunch_slots = ["13:00", "13:30", "14:00", "14:30", "15:00"]
                        dinner_slots = ["20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00"]
                        time_slots = lunch_slots + ["break"] + dinner_slots
                        
                        # Inicializar matriz: cada franja (excepto "break") tiene un diccionario de asientos ocupados
                        reservation_matrix = {slot: {} for slot in time_slots if slot != "break"}
                        
                        # Mapeo de franjas para reservas que ocupan varios intervalos
                        time_slot_mapping = {
                            "13:00": ["13:00", "13:30", "14:00", "14:30"],
                            "13:30": ["13:30", "14:00", "14:30", "15:00"],
                            "14:00": ["14:00", "14:30", "15:00"],
                            "14:30": ["14:30", "15:00"],
                            "15:00": ["15:00"],
                            "20:00": ["20:00", "20:30", "21:00", "21:30"],
                            "20:30": ["20:30", "21:00", "21:30", "22:00"],
                            "21:00": ["21:00", "21:30", "22:00", "22:30"],
                            "21:30": ["21:30", "22:00", "22:30", "23:00"],
                            "22:00": ["22:00", "22:30", "23:00"],
                            "22:30": ["22:30", "23:00"],
                            "23:00": ["23:00"]
                        }
                        
                        from operator import itemgetter
                        all_reservations = sorted(all_reservations, key=itemgetter('time'))
                        for reservation in all_reservations:
                            status = reservation.get('status', 'pendiente')
                            if status != 'cancelada':
                                if hasattr(reservation['time'], 'strftime'):
                                    res_time = reservation['time'].strftime('%H:%M')
                                else:
                                    time_str = str(reservation['time'])
                                    res_time = time_str[:5] if len(time_str) > 5 else time_str
                                
                                if res_time in reservation_matrix:
                                    found_spot = False
                                    affected_slots = time_slot_mapping.get(res_time, [res_time])
                                    start_seat = 0
                                    while start_seat < restaurant['capacity'] and not found_spot:
                                        all_slots_available = True
                                        max_occupied_seat = start_seat - 1
                                        for slot in affected_slots:
                                            if slot not in reservation_matrix:
                                                continue
                                            for i in range(reservation['diners']):
                                                seat_idx = start_seat + i
                                                if seat_idx >= restaurant['capacity'] or seat_idx in reservation_matrix[slot]:
                                                    all_slots_available = False
                                                    existing_res = reservation_matrix[slot].get(seat_idx)
                                                    existing_end = seat_idx
                                                    if existing_res:
                                                        for j in range(1, existing_res['diners']):
                                                            if (seat_idx + j in reservation_matrix[slot] and 
                                                                reservation_matrix[slot][seat_idx + j] == existing_res):
                                                                existing_end = seat_idx + j
                                                    max_occupied_seat = max(max_occupied_seat, existing_end)
                                                    break
                                            if not all_slots_available:
                                                break
                                        if all_slots_available:
                                            for slot in affected_slots:
                                                if slot in reservation_matrix:
                                                    for i in range(reservation['diners']):
                                                        reservation_matrix[slot][start_seat + i] = reservation
                                            found_spot = True
                                        else:
                                            start_seat = max_occupied_seat + 1
                                            
                        return render_template("restaurant/home.html", 
                                               restaurant=restaurant, 
                                               selected_date=selected_date, 
                                               time_slots=time_slots, 
                                               reservation_matrix=reservation_matrix)
                    else:
                        # Vista de lista: Se muestran todas las reservas (incluyendo canceladas) ordenadas por fecha y hora 
                        query = """
                            SELECT r.*, c.username as client_name 
                            FROM reservation r
                            JOIN client c ON r.client_id = c.client_id
                            WHERE r.restaurant_id = %s
                            ORDER BY r.date ASC, r.time ASC
                        """
                        cursor.execute(query, (restaurant['restaurant_id'],))
                        reservations = cursor.fetchall()
                        
                        return render_template("restaurant/reservations.html", 
                                               restaurant=restaurant, 
                                               reservations=reservations,
                                               selected_date="Todas")
                else:
                    session.pop('username', None)
                    session.pop('user_type', None)
                    return redirect(url_for('home'))
        except Exception as e:
            print("Ocurrió un error al cargar reservas:", e)
            return render_template("home.html", message="Error al cargar reservas")
        finally:
            connection.close()
            print("Conexión cerrada")
    else:
        return redirect(url_for('login_pageRest'))
    
@app.route('/registered_user', methods=['POST'])
def register():
    # Obtener datos del formulario
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    phone = request.form['phone']
    email = request.form['email']

    # Verificar que ambas contraseñas coincidan
    if password != password2:
        return render_template("user/register_user.html", message="Las contraseñas no coinciden")

    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            # Verificar si el email ya existe (en vez de username)
            query = "SELECT * FROM client WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            if user:
                return render_template("user/register_user.html", message="El email ya está registrado")
            else:
                # Encriptar la contraseña
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                # Insertar el nuevo usuario (username se puede repetir)
                query = "INSERT INTO client (username, password, phone, email) VALUES (%s, %s, %s, %s)"
                data = (username, hashed, phone, email)
                cursor.execute(query, data)
                connection.commit()
                return render_template("home.html", message="Usuario registrado correctamente")
    except Exception as e:
        print("Ocurrió un error al conectar a la base de datos: ", e)
        return render_template("user/register_user.html", message="Error al registrar el usuario")
    finally:
        connection.close()
        print("Conexión cerrada")

@app.route('/logout_restaurant')
def logout_restaurant():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('home'))

        
@app.route('/restaurant/reservations/<date>')
def restaurant_reservations(date):
    if 'username' in session and session.get('user_type') == 'restaurant':
        connection = db.get_connection()
        try:
            with connection.cursor() as cursor:
                # Get restaurant data - CORREGIR AQUÍ: usar restaurant_id en lugar de email
                query = "SELECT * FROM restaurant WHERE restaurant_id = %s"
                data = (session['restaurant_id'],)  # Cambiado de session['email'] a session['restaurant_id']
                cursor.execute(query, data)
                restaurant = cursor.fetchone()
                
                if restaurant:
                    # Get non-canceled reservations for this restaurant on selected date with client info
                    query = """
                        SELECT r.*, c.username as client_name 
                        FROM reservation r
                        JOIN client c ON r.client_id = c.client_id
                        WHERE r.restaurant_id = %s AND r.date = %s AND (r.status != 'cancelada' OR r.status IS NULL)
                        ORDER BY r.time
                    """
                    cursor.execute(query, (restaurant['restaurant_id'], date))
                    reservations = cursor.fetchall()
                    
                    # Convert timedelta to string for display
                    for reservation in reservations:
                        if isinstance(reservation['time'], timedelta):
                            reservation['time'] = str(reservation['time'])
                    
                    return render_template('restaurant/reservations.html', 
                                          restaurant=restaurant,
                                          reservations=reservations,
                                          selected_date=date)
                else:
                    # Something went wrong with the session data
                    session.pop('username', None)
                    session.pop('user_type', None)
                    return redirect(url_for('home'))
        except Exception as e:
            print("Ocurrió un error al conectar a la bbdd: ", e)
            return render_template("home.html", message="Error de conexión a la base de datos")
        finally:
            connection.close()
            print("Conexión cerrada")
    else:
        return redirect(url_for('login_pageRest'))

@app.route('/restaurant/update_reservation_status', methods=['POST'])
def update_reservation_status():
    if 'username' in session and session.get('user_type') == 'restaurant':
        reservation_id = request.form.get('reservation_id')
        new_status = request.form.get('nuevo_estado')  # Debe coincidir con el nombre del campo en el formulario
        date = request.form.get('date')
        
        print(f"Updating reservation {reservation_id} to status {new_status}")
        
        connection = db.get_connection()
        try:
            with connection.cursor() as cursor:
                verify_query = """
                    SELECT r.*, rest.username 
                    FROM reservation r
                    JOIN restaurant rest ON r.restaurant_id = rest.restaurant_id
                    WHERE r.reservation_id = %s
                """
                cursor.execute(verify_query, (reservation_id,))
                result = cursor.fetchone()
                
                print(f"Verification result: {result}")
                
                if result and result['username'] == session['username']:
                    update_query = "UPDATE reservation SET status = %s WHERE reservation_id = %s"
                    cursor.execute(update_query, (new_status, reservation_id))
                    rows_affected = cursor.rowcount
                    connection.commit()
                    
                    print(f"Status updated successfully to {new_status}. Rows affected: {rows_affected}")
                    
                    # Si se recibe la fecha (vista de calendario) se redirige a la misma, 
                    # de lo contrario se redirige a la vista de lista de reservas
                    if date:
                        if date == "Todas":
                            return redirect(url_for('restaurant'))
                        else:
                            return redirect(url_for('restaurant_reservations', date=date))
                    else:
                        return redirect(url_for('restaurant'))
                else:
                    return render_template("home.html", message="No tienes permiso para modificar esta reserva")
        except Exception as e:
            print(f"Ocurrió un error al actualizar la reserva: {e}")
            return render_template("home.html", message=f"Error al actualizar la reserva: {e}")
        finally:
            connection.close()
            print("Conexión cerrada")
    else:
        return redirect(url_for('login_pageRest'))
    
@app.route('/restaurant/delete_reservation/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    # Verificar que el usuario (restaurante) está logueado
    if 'username' not in session or session.get('user_type') != 'restaurant':
        return redirect(url_for('login_pageRest'))
    
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            # Validar que la reserva está en estado cancelada
            verify_query = "SELECT status FROM reservation WHERE reservation_id = %s"
            cursor.execute(verify_query, (reservation_id,))
            result = cursor.fetchone()
            if not result or result['status'] != 'cancelada':
                return redirect(url_for('restaurant'))
            
            # Eliminar la reserva
            delete_query = "DELETE FROM reservation WHERE reservation_id = %s"
            cursor.execute(delete_query, (reservation_id,))
            connection.commit()
        return redirect(url_for('restaurant'))
    except Exception as e:
        print("Error al eliminar reserva:", e)
        connection.rollback()
        return redirect(url_for('restaurant'))
    finally:
        connection.close()

# ------------- Parte de Booking -------------

@app.route('/booking/<int:restaurant_id>')
def booking(restaurant_id):
    
    connnection = db.get_connection()
    with connnection.cursor() as cursor:
        consulta = "SELECT * FROM reservation WHERE restaurant_id = %s"
        cursor.execute(consulta,(restaurant_id))
        bookings = cursor.fetchall()
        consulta = "SELECT * FROM restaurant WHERE restaurant_id = %s"
        cursor.execute(consulta,(restaurant_id))
        restaurant = cursor.fetchone()
    
    # Convertir timedelta a string
    for booking in bookings:
        if isinstance(booking['time'], timedelta):
            booking['time'] = str(booking['time'])
    
    connnection.close()
    return render_template('user/booking.html',bookings = bookings,restaurant = restaurant)

@app.route('/booking',methods=['POST'])
def add_booking():
    #obtener los datos del formulario
    restaurant_id = request.form['restaurant']
    client_id = request.form['user']
    date = request.form['date'] 
    time = request.form['time']
    diners = request.form['people']
    #creamos
    #TODO: Comprobar que el hueco de reserva sigue libre
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            # First check if status column exists
            try:
                #crear la consulta con status
                consulta = "INSERT INTO reservation (restaurant_id,client_id,date,time,diners,status) VALUES (%s,%s,%s,%s,%s,'pending')"
                datos = (restaurant_id,client_id,date,time,diners)
                cursor.execute(consulta,datos)
                conexion.commit()
            except Exception as column_error:
                print(f"Error with status column: {column_error}")
                # Status column might not exist, try to add it
                try:
                    alter_query = "ALTER TABLE reservation ADD COLUMN status VARCHAR(20) DEFAULT 'pending'"
                    cursor.execute(alter_query)
                    conexion.commit()
                    print("Added status column to reservation table")
                    
                    # Now try the insert again without status (it will use default)
                    consulta = "INSERT INTO reservation (restaurant_id,client_id,date,time,diners) VALUES (%s,%s,%s,%s,%s)"
                    datos = (restaurant_id,client_id,date,time,diners)
                    cursor.execute(consulta,datos)
                    conexion.commit()
                except Exception as alter_error:
                    print(f"Error adding status column: {alter_error}")
                    # Try without status column as last resort
                    consulta = "INSERT INTO reservation (restaurant_id,client_id,date,time,diners) VALUES (%s,%s,%s,%s,%s)"
                    datos = (restaurant_id,client_id,date,time,diners)
                    cursor.execute(consulta,datos)
                    conexion.commit()
            
            return redirect(url_for('booking', restaurant_id=restaurant_id))
    except Exception as e:
        print(f"Ocurrió un error al conectar a la bbdd: {e}")
        return render_template("home.html", message=f"Error al crear la reserva: {e}")
    finally:
        conexion.close()
        print("Conexión cerrada")
        return redirect(url_for('userhome'))



# ------------- Parte de Mis Reservas -------------

@app.route('/my_reservations')
def my_reservations():
    print("DEBUG: Entrando a my_reservations")  # Para debug
    # Verificar si el usuario está logueado
    if 'username' not in session or 'client_id' not in session:
        return redirect(url_for('login_page'))
    
    client_id = session['client_id']
    connection = db.get_connection()
    
    try:
        with connection.cursor() as cursor:
            # Obtener todas las reservas del usuario con detalles del restaurante
            query = """
            SELECT r.*, rest.restaurant_name, rest.address, rest.image 
            FROM reservation r 
            JOIN restaurant rest ON r.restaurant_id = rest.restaurant_id 
            WHERE r.client_id = %s
            ORDER BY r.date, r.time
            """
            cursor.execute(query, (client_id,))
            reservations = cursor.fetchall()
            
            # Asegúrate de que la siguiente línea de código esté presente:
            print("Finalizando my_reservations")
            return render_template('user/my_reservations.html', 
                                  reservations=reservations, 
                                  username=session['username'])
    except Exception as e:
        print("Error al obtener reservas:", e)
        return render_template('user/my_reservations.html', 
                              message="Error al cargar tus reservas", 
                              reservations=[])
    finally:
        connection.close()

@app.route('/update_reservation/<int:reservation_id>', methods=['POST'])
def update_reservation(reservation_id):
    # Verificar si el usuario está logueado
    if 'username' not in session or 'client_id' not in session:
        return redirect(url_for('login_page'))
    
    client_id = session['client_id']
    diners = request.form.get('diners')
    date = request.form.get('date')
    time = request.form.get('time')
    
    connection = db.get_connection()
    
    try:
        with connection.cursor() as cursor:
            # Verificar que la reserva pertenece al usuario
            check_query = "SELECT * FROM reservation WHERE reservation_id = %s AND client_id = %s"
            cursor.execute(check_query, (reservation_id, client_id))
            reservation = cursor.fetchone()
            
            if not reservation:
                return redirect(url_for('my_reservations'))
            
            # Verificar el estado actual de la reserva
            # Si está confirmada, cambiarla a pendiente al modificarla
            current_status = reservation.get('status')
            
            if current_status == 'confirmada':
                # Si la reserva estaba confirmada, cambiarla a pendiente
                update_query = """
                UPDATE reservation 
                SET diners = %s, date = %s, time = %s, status = 'pendiente'
                WHERE reservation_id = %s AND client_id = %s
                """
                cursor.execute(update_query, (diners, date, time, reservation_id, client_id))
                message = "Reserva modificada. Al cambiar detalles, ha vuelto a estado pendiente."
            else:
                # Si no estaba confirmada, mantener el estado actual
                update_query = """
                UPDATE reservation 
                SET diners = %s, date = %s, time = %s
                WHERE reservation_id = %s AND client_id = %s
                """
                cursor.execute(update_query, (diners, date, time, reservation_id, client_id))
                message = "Reserva actualizada correctamente."
                
            connection.commit()
            
            return redirect(url_for('my_reservations', message=message))
    except Exception as e:
        print("Error al actualizar reserva:", e)
        connection.rollback()
        return redirect(url_for('my_reservations', message="Error al actualizar la reserva"))
    finally:
        connection.close()

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    # Verificar si el usuario (cliente) está logueado
    if 'username' not in session or 'client_id' not in session:
        return redirect(url_for('login_page'))
    
    client_id = session['client_id']
    connection = db.get_connection()
    
    try:
        with connection.cursor() as cursor:
            # Verificar que la reserva pertenece al usuario
            check_query = "SELECT * FROM reservation WHERE reservation_id = %s AND client_id = %s"
            cursor.execute(check_query, (reservation_id, client_id))
            reservation = cursor.fetchone()
            
            if not reservation:
                # Si no existe, redirigir o mostrar error
                return redirect(url_for('my_reservations'))
            
            # En lugar de borrar la reserva, actualizar el estado a "cancelada"
            update_query = "UPDATE reservation SET status = %s WHERE reservation_id = %s AND client_id = %s"
            cursor.execute(update_query, ('cancelada', reservation_id, client_id))
            connection.commit()
            
            return redirect(url_for('my_reservations'))
    except Exception as e:
        print("Error al cancelar reserva:", e)
        connection.rollback()
        return redirect(url_for('my_reservations'))
    finally:
        connection.close()



# ------------- Parte de Perfil de Usuario -------------

@app.route('/user/edit_profile')
def edit_client_profile():
    # Verificar que el cliente está logueado
    if 'client_id' not in session:
        return redirect(url_for('login_page'))
    
    client_id = session['client_id']
    connection = db.get_connection()
    
    try:
        with connection.cursor() as cursor:
            # Obtener datos del cliente
            query = "SELECT * FROM client WHERE client_id = %s"
            cursor.execute(query, (client_id,))
            client = cursor.fetchone()
            
            if not client:
                return redirect(url_for('login_page'))
            
            return render_template('user/edit_profile.html', client=client)
    except Exception as e:
        print("Error al obtener datos del cliente:", e)
        return redirect(url_for('userhome'))
    finally:
        connection.close()

@app.route('/user/update_profile', methods=['POST'])
def update_client_profile():
    # Verificar que el cliente está logueado
    if 'client_id' not in session:
        return redirect(url_for('login_page'))
    
    client_id = session['client_id']
    connection = db.get_connection()
    
    # Obtener datos del formulario (sin el campo name)
    username = request.form.get('username')
    phone = request.form.get('phone')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    try:
        with connection.cursor() as cursor:
            # Se elimina la verificación de duplicidad para username
            # (Si quieres que se verifique la duplicidad, se debe comparar el email y no el username)
            
            # Obtener datos actuales del cliente
            query = "SELECT * FROM client WHERE client_id = %s"
            cursor.execute(query, (client_id,))
            client = cursor.fetchone()
            
            # Verificar contraseña actual
            stored_password = client['password']
            if not bcrypt.checkpw(current_password.encode('utf-8'), stored_password.encode('utf-8')):
                return render_template(
                    'user/edit_profile.html',
                    client=client,
                    message="La contraseña actual no es correcta",
                    message_type="danger"
                )
            
            # Verificar si se quiere cambiar la contraseña
            if new_password:
                if new_password != confirm_password:
                    return render_template(
                        'user/edit_profile.html',
                        client=client,
                        message="Las nuevas contraseñas no coinciden",
                        message_type="danger"
                    )
                
                # Encriptar nueva contraseña
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            else:
                # Mantener la contraseña actual
                hashed_password = stored_password
            
            # Actualizar datos del cliente sin verificar duplicidad en username
            update_query = """
            UPDATE client 
            SET username = %s, phone = %s, password = %s
            WHERE client_id = %s
            """
            cursor.execute(update_query, (username, phone, hashed_password, client_id))
            connection.commit()
            
            # Actualizar el nombre de usuario en la sesión (si se quiere mantener, aunque pueda duplicarse)
            session['username'] = username
            
            # Obtener los datos actualizados para mostrar en el formulario
            query = "SELECT * FROM client WHERE client_id = %s"
            cursor.execute(query, (client_id,))
            updated_client = cursor.fetchone()
            
            return render_template(
                'user/edit_profile.html',
                client=updated_client,
                message="Perfil actualizado correctamente",
                message_type="success"
            )
    except Exception as e:
        print("Error al actualizar perfil del cliente:", e)
        connection.rollback()
        return render_template(
            'user/edit_profile.html',
            client=client if 'client' in locals() else {'username': username, 'phone': phone},
            message=f"Error al actualizar el perfil: {str(e)}",
            message_type="danger"
        )
    finally:
        connection.close()



# ------------- Parte de Perfil de Restaurante -------------

@app.route('/restaurant/edit_profile')
def edit_restaurant_profile():
    # Verificar que el restaurante está logueado
    if 'restaurant_id' not in session:
        return redirect(url_for('login_pageRest'))
    
    restaurant_id = session['restaurant_id']
    connection = db.get_connection()
    
    try:
        with connection.cursor() as cursor:
            # Obtener datos del restaurante
            query = "SELECT * FROM restaurant WHERE restaurant_id = %s"
            cursor.execute(query, (restaurant_id,))
            restaurant = cursor.fetchone()
            
            # Obtener todos los tipos de cocina
            cursor.execute("SELECT * FROM cuisine_type ORDER BY cuisine_name")
            cuisine_types = cursor.fetchall()
            
            # Obtener los tipos de cocina del restaurante
            cursor.execute(
                "SELECT cuisine_id FROM restaurant_cuisine WHERE restaurant_id = %s", 
                (restaurant_id,)
            )
            restaurant_cuisines = [item['cuisine_id'] for item in cursor.fetchall()]
            
            return render_template(
                'restaurant/edit_profile.html',
                restaurant=restaurant,
                cuisine_types=cuisine_types,
                restaurant_cuisines=restaurant_cuisines
            )
    except Exception as e:
        print("Error al obtener datos del restaurante:", e)
        return redirect(url_for('restauranthome'))
    finally:
        connection.close()

@app.route('/restaurant/update_profile', methods=['POST'])
def update_restaurant_profile():
    if 'restaurant_id' not in session:
        return redirect(url_for('login_pageRest'))
    
    restaurant_id = session['restaurant_id']
    connection = db.get_connection()
    
    # Obtener datos del formulario
    restaurant_name = request.form.get('restaurant_name')
    address = request.form.get('address')
    phone = request.form.get('phone')
    website = request.form.get('website')
    description = request.form.get('description')
    email = request.form.get('email').strip()
    repeat_email = request.form.get('repeat_email').strip()
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Obtener los tipos de cocina seleccionados (pueden ser múltiples)
    cuisine_ids = request.form.getlist('cuisine_ids')
    
    try:
        with connection.cursor() as cursor:
            # Obtener datos actuales del restaurante
            query = "SELECT * FROM restaurant WHERE restaurant_id = %s"
            cursor.execute(query, (restaurant_id,))
            restaurant = cursor.fetchone()
            
            # Si el usuario dejó vacíos los campos de email, se conserva el email actual
            if not email and not repeat_email:
                email = restaurant['email']
                repeat_email = restaurant['email']
            
            # Validar que los correos electrónicos sean iguales si se ingresó algo
            if email != repeat_email:
                # Obtener todos los tipos de cocina para el selector
                cursor.execute("SELECT * FROM cuisine_type ORDER BY cuisine_name")
                cuisine_types = cursor.fetchall()
                
                # Obtener los tipos de cocina actuales del restaurante
                cursor.execute(
                    "SELECT cuisine_id FROM restaurant_cuisine WHERE restaurant_id = %s",
                    (restaurant_id,)
                )
                restaurant_cuisines = [item['cuisine_id'] for item in cursor.fetchall()]
                
                return render_template('restaurant/edit_profile.html',
                                       restaurant=restaurant,
                                       cuisine_types=cuisine_types,
                                       restaurant_cuisines=restaurant_cuisines,
                                       message="Los correos electrónicos no coinciden",
                                       message_type="danger")
            
            # Verificar la contraseña actual
            stored_password = restaurant['password']
            if not bcrypt.checkpw(current_password.encode('utf-8'), stored_password.encode('utf-8')):
                cursor.execute("SELECT * FROM cuisine_type ORDER BY cuisine_name")
                cuisine_types = cursor.fetchall()
                
                cursor.execute(
                    "SELECT cuisine_id FROM restaurant_cuisine WHERE restaurant_id = %s",
                    (restaurant_id,)
                )
                restaurant_cuisines = [item['cuisine_id'] for item in cursor.fetchall()]
                
                return render_template(
                    'restaurant/edit_profile.html',
                    restaurant=restaurant,
                    cuisine_types=cuisine_types,
                    restaurant_cuisines=restaurant_cuisines,
                    message="La contraseña actual no es correcta",
                    message_type="danger"
                )
            
            # Verificar si se quiere cambiar la contraseña
            if new_password:
                if new_password != confirm_password:
                    cursor.execute("SELECT * FROM cuisine_type ORDER BY cuisine_name")
                    cuisine_types = cursor.fetchall()
                    
                    cursor.execute(
                        "SELECT cuisine_id FROM restaurant_cuisine WHERE restaurant_id = %s",
                        (restaurant_id,)
                    )
                    restaurant_cuisines = [item['cuisine_id'] for item in cursor.fetchall()]
                    
                    return render_template(
                        'restaurant/edit_profile.html',
                        restaurant=restaurant,
                        cuisine_types=cuisine_types,
                        restaurant_cuisines=restaurant_cuisines,
                        message="Las nuevas contraseñas no coinciden",
                        message_type="danger"
                    )
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            else:
                hashed_password = stored_password
            
            # Manejar la imagen si se proporciona
            image = request.files.get('image')
            if image and image.filename:
                # Si se ha subido una imagen válida
                from werkzeug.utils import secure_filename
                import os, time
                secure_filename_value = secure_filename(image.filename)
                timestamp = int(time.time())
                filename = f"{timestamp}_{secure_filename_value}"
                # Crear directorio si no existe
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image.save(image_path)
                image_name = filename
            else:
                # Si no se sube una imagen, mantener la actual o usar default
                image_name = restaurant.get('image') or "aquitulogo-27.webp"
            
            # Actualizar datos del restaurante en la tabla restaurant
            update_query = """
            UPDATE restaurant 
            SET restaurant_name = %s, address = %s, phone = %s, website = %s, 
                description = %s, password = %s, image = %s, email = %s
            WHERE restaurant_id = %s
            """
            cursor.execute(update_query, (
                restaurant_name, address, phone, website, description,
                hashed_password, image_name, email, restaurant_id
             ))
            
            # Actualizar los tipos de cocina:
            # 1. Primero eliminar todos los tipos de cocina actuales del restaurante
            cursor.execute("DELETE FROM restaurant_cuisine WHERE restaurant_id = %s", (restaurant_id,))
            
            # 2. Luego insertar los nuevos tipos seleccionados
            if cuisine_ids:
                for cuisine_id in cuisine_ids:
                    cursor.execute(
                        "INSERT INTO restaurant_cuisine (restaurant_id, cuisine_id) VALUES (%s, %s)",
                        (restaurant_id, cuisine_id)
                    )
            
            # Confirmar los cambios en la base de datos
            connection.commit()
            
            # Actualizar la sesión con el nombre del restaurante y email
            session['restaurant_name'] = restaurant_name
            session['email'] = email
            
            # Obtener los datos actualizados para mostrar en el formulario
            cursor.execute("SELECT * FROM restaurant WHERE restaurant_id = %s", (restaurant_id,))
            updated_restaurant = cursor.fetchone()
            
            # Obtener los tipos de cocina para el selector
            cursor.execute("SELECT * FROM cuisine_type ORDER BY cuisine_name")
            cuisine_types = cursor.fetchall()
            
            # Obtener los tipos de cocina actuales del restaurante (después de la actualización)
            cursor.execute(
                "SELECT cuisine_id FROM restaurant_cuisine WHERE restaurant_id = %s",
                (restaurant_id,)
            )
            restaurant_cuisines = [item['cuisine_id'] for item in cursor.fetchall()]
            
            return render_template(
                'restaurant/edit_profile.html',
                restaurant=updated_restaurant,
                cuisine_types=cuisine_types,
                restaurant_cuisines=restaurant_cuisines,
                message="Perfil actualizado correctamente",
                message_type="success"
            )
    except Exception as e:
        print("Error al actualizar perfil del restaurante:", e)
        connection.rollback()
        
        # Si ocurre un error, volver a obtener los datos para mostrar el formulario
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM restaurant WHERE restaurant_id = %s", (restaurant_id,))
        restaurant = cursor.fetchone()
        
        # Obtener los tipos de cocina para el selector
        cursor.execute("SELECT * FROM cuisine_type ORDER BY cuisine_name")
        cuisine_types = cursor.fetchall()
        
        # Obtener los tipos de cocina actuales del restaurante
        cursor.execute(
            "SELECT cuisine_id FROM restaurant_cuisine WHERE restaurant_id = %s", 
            (restaurant_id,)
        )
        restaurant_cuisines = [item['cuisine_id'] for item in cursor.fetchall()]
        
        return render_template(
            'restaurant/edit_profile.html',
            restaurant=restaurant,
            cuisine_types=cuisine_types,
            restaurant_cuisines=restaurant_cuisines,
            message=f"Error al actualizar el perfil: {str(e)}",
            message_type="danger"
        )
    finally:
        connection.close()

@app.route('/restaurant/delete_account', methods=['POST'])
def delete_restaurant_account():
    # Verificar que el restaurante está logueado
    if 'restaurant_id' not in session:
        return redirect(url_for('login_pageRest'))
    
    restaurant_id = session['restaurant_id']
    password = request.form.get('password')
    
    connection = db.get_connection()
    
    try:
        with connection.cursor() as cursor:
            # Verificar la contraseña
            query = "SELECT * FROM restaurant WHERE restaurant_id = %s"
            cursor.execute(query, (restaurant_id,))
            restaurant = cursor.fetchone()
            
            if not restaurant:
                return redirect(url_for('login_pageRest'))
            
            # Verificar contraseña
            stored_password = restaurant['password']
            
            if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return render_template(
                    'restaurant/edit_profile.html',
                    restaurant=restaurant,
                    message="Contraseña incorrecta. No se pudo eliminar la cuenta.",
                    message_type="danger"
                )
            
            # Primero eliminar todas las reservas asociadas
            delete_reservations_query = "DELETE FROM reservation WHERE restaurant_id = %s"
            cursor.execute(delete_reservations_query, (restaurant_id,))
            
            # Luego eliminar la cuenta del restaurante
            delete_account_query = "DELETE FROM restaurant WHERE restaurant_id = %s"
            cursor.execute(delete_account_query, (restaurant_id,))
            
            connection.commit()
            
            # Cerrar la sesión
            session.pop('username', None)
            session.pop('user_type', None)
            session.pop('restaurant_id', None)
            session.pop('restaurant_name', None)
            
            # Mostrar mensaje de éxito en la página principal
            return redirect(url_for('home', message="Tu cuenta ha sido eliminada correctamente", message_type="success"))
    except Exception as e:
        print("Error al eliminar cuenta de restaurante:", e)
        connection.rollback()
        return render_template(
            'restaurant/edit_profile.html',
            restaurant=restaurant if 'restaurant' in locals() else None,
            message=f"Error al eliminar la cuenta: {str(e)}",
            message_type="danger"
        )
    finally:
        connection.close()

@app.route('/restaurant/update_cuisine', methods=['POST'])
def update_restaurant_cuisine():
    if 'restaurant_id' not in session:
        return redirect(url_for('login_pageRest'))
    
    restaurant_id = session['restaurant_id']
    # Obtener los tipos de cocina seleccionados
    cuisine_ids = request.form.getlist('cuisine_ids')
    
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            # Primero eliminar todas las relaciones actuales
            cursor.execute("DELETE FROM restaurant_cuisine WHERE restaurant_id = %s", (restaurant_id,))
            
            # Luego insertar las nuevas selecciones
            if cuisine_ids:
                for cuisine_id in cuisine_ids:
                    cursor.execute(
                        "INSERT INTO restaurant_cuisine (restaurant_id, cuisine_id) VALUES (%s, %s)", 
                        (restaurant_id, cuisine_id)
                    )
            
            connection.commit()
            return redirect(url_for('edit_restaurant_profile', message="Tipos de cocina actualizados correctamente"))
    except Exception as e:
        print("Error al actualizar tipos de cocina:", e)
        connection.rollback()
        return redirect(url_for('edit_restaurant_profile', message="Error al actualizar tipos de cocina"))
    finally:
        connection.close()

@app.route('/search_restaurants')
def search_restaurants():
    cuisine_id = request.args.get('cuisine_id')
    
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            # Obtener todos los tipos de cocina para el selector
            cursor.execute("SELECT * FROM cuisine_type ORDER BY cuisine_name")
            cuisine_types = cursor.fetchall()
            
            # Si se seleccionó un tipo de cocina, filtrar por ese tipo
            if cuisine_id:
                query = """
                SELECT DISTINCT r.* FROM restaurant r
                JOIN restaurant_cuisine rc ON r.restaurant_id = rc.restaurant_id
                WHERE rc.cuisine_id = %s
                ORDER BY r.restaurant_name
                """
                cursor.execute(query, (cuisine_id,))
            else:
                # Si no, mostrar todos los restaurantes
                cursor.execute("SELECT * FROM restaurant ORDER BY restaurant_name")
                
            restaurants = cursor.fetchall()
            
            return render_template('user/home.html', 
                                  restaurants=restaurants,
                                  cuisine_types=cuisine_types,
                                  selected_cuisine=cuisine_id)
    except Exception as e:
        print("Error al buscar restaurantes:", e)
        return render_template('user/home.html', message="Error en la búsqueda")
    finally:
        connection.close()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)