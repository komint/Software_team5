from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
@app.route('/reservations/<int:reservation_id>/delete', methods=['POST'])
def cancel_reservation(reservation_id):
    reservation = next((r for r in reservations if r['id'] == reservation_id), None)
    if reservation:
        reservations.remove(reservation)
    return redirect(url_for('manage_reservations'))

@app.route('/cancel_reservation')
def cancel_reserved_reservations():
    return render_template('cancel_reservation.html')

@app.route('/modify_reservation')
def modify_reservation():
    return render_template('modify_reservation.html')

@app.route('/reservation_lookup')
def reservation_lookup():
    return render_template('reservation_lookup.html')

@app.route('/reserve')
def reserve():
    return render_template('reserve.html')

@app.route('/inquiry', methods=['GET','POST'])
def inquiry():
    return render_template('customer_inquiry.html')

@app.route('/view_menu')
def view_menu():
    return render_template('view_menu.html', menus=menus)

if __name__ == '__main__':
    app.run(debug=True)