from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 메뉴 데이터 (임시)
menus = [
    {'id': 1, 'name': '불고기', 'description': '맛있는 불고기'},
    {'id': 2, 'name': '비빔밥', 'description': '신선한 채소와 함께'},
    {'id': 3, 'name': '잡채', 'description': '다양한 야채와 고기'}
]

# 예약 데이터 (임시)
reservations = []

# 루트 경로
@app.route('/')
def index():
    return render_template('index.html', menus=menus)

# 메뉴 관리 페이지
@app.route('/manage_menus', methods=['GET', 'POST'])
def manage_menus():
    if request.method == 'POST':
        # 메뉴 추가
        if 'add' in request.form:
            name = request.form['name']
            description = request.form['description']
            new_id = max([menu['id'] for menu in menus]) + 1 if menus else 1
            menus.append({'id': new_id, 'name': name, 'description': description})
        # 메뉴 수정
        elif 'edit' in request.form:
            menu_id = int(request.form['id'])
            menu = next((menu for menu in menus if menu['id'] == menu_id), None)
            if menu:
                menu['name'] = request.form['name']
                menu['description'] = request.form['description']
        # 메뉴 삭제
        elif 'delete' in request.form:
            menu_id = int(request.form['id'])
            menu = next((menu for menu in menus if menu['id'] == menu_id), None)
            if menu:
                menus.remove(menu)
    return render_template('manage_menus.html', menus=menus)

@app.route('/menus/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu(menu_id):
    menu = next((m for m in menus if m['id'] == menu_id), None)
    if request.method == 'POST':
        menu['name'] = request.form['name']
        menu['description'] = request.form['description']
        return redirect(url_for('manage_menus'))
    return render_template('manage_menus.html', menu=menu)

@app.route('/menus/<int:menu_id>/delete', methods=['POST'])
def delete_menu(menu_id):
    menu = next((m for m in menus if m['id'] == menu_id), None)
    if menu:
        menus.remove(menu)
    return redirect(url_for('manage_menus'))

# 예약 관리
@app.route('/reservations', methods=['POST'])
def make_reservation():
    customer_name = request.form['customerName']
    reservation_date = request.form['reservationDate']
    reservation_time = request.form['reservationTime']
    number_of_guests = request.form['numberOfGuests']
    new_id = max([res['id'] for res in reservations]) + 1 if reservations else 1
    new_reservation = {
        'id': new_id,
        'customer_name': customer_name,
        'reservation_date': reservation_date,
        'reservation_time': reservation_time,
        'number_of_guests': number_of_guests
    }
    reservations.append(new_reservation)
    flash(f"예약이 성공적으로 완료되었습니다! 예약 번호는 {new_id}입니다.")
    return redirect(url_for('index'))


@app.route('/cancel_reservation', methods=['GET'])
def cancel_reservation():
    return render_template('cancel_reservation.html')


@app.route('/cancel_reservation', methods=['POST'], endpoint='cancel_reservation_action')
def cancel_reservation_action():
    reservation_id = int(request.form['cancelReservationId'])

    reservation = next((r for r in reservations if r['id'] == reservation_id), None)

    if reservation:
        reservations.remove(reservation)
        return render_template('cancel_reservation.html', reservation_cancelled=True)
    else:
        return render_template('cancel_reservation.html', reservation_not_found=True)


@app.route('/modify_reservation', methods=['GET', 'POST'])
def modify_reservation():
    if request.method == 'POST':
        reservation_id = int(request.form['modifyReservationId'])
        reservation_date = request.form['modifyReservationDate']
        reservation_time = request.form['modifyReservationTime']
        number_of_guests = int(request.form['modifyNumberOfGuests'])

        reservation = next((r for r in reservations if r['id'] == reservation_id), None)

        if reservation:
            reservation['reservation_date'] = reservation_date
            reservation['reservation_time'] = reservation_time
            reservation['number_of_guests'] = number_of_guests
            return render_template('modify_reservation.html', reservation_modified=True)
        else:
            return render_template('modify_reservation.html', reservation_not_found=True)

    return render_template('modify_reservation.html')


@app.route('/reservation_lookup', methods=['GET', 'POST'])
def reservation_lookup():
    if request.method == 'POST':
        reservation_id = int(request.form['reservation_id'])
        reservation = next((r for r in reservations if r['id'] == reservation_id), None)
        if reservation:
            return render_template('reservation_lookup.html', reservation=reservation)
        else:
            return render_template('reservation_lookup.html', reservation_not_found=True)
    return render_template('reservation_lookup.html')

@app.route('/reserve')
def reserve():
    return render_template('reserve.html')

@app.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    return render_template('customer_inquiry.html')

@app.route('/view_menu')
def view_menu():
    return render_template('view_menu.html', menus=menus)

if __name__ == '__main__':
    app.run(debug=True)
