document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('menuRegistrationForm');
    const menuListDiv = document.getElementById('menuList');

    function displayMenus() {
        const menus = JSON.parse(localStorage.getItem('menus')) || [];
        menuListDiv.innerHTML = ''; // 목록 초기화
        menus.forEach(menu => {
            const menuElement = document.createElement('div');
            menuElement.textContent = `${menu.name} - ${menu.description}`;
            menuListDiv.appendChild(menuElement);
        });
    }

    registrationForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const menuName = document.getElementById('menuName').value.trim();
        const menuDescription = document.getElementById('menuDescription').value.trim();

        if (!menuName || !menuDescription) {
            alert('메뉴 이름과 설명을 모두 입력해주세요.');
            return;
        }

        const menuData = JSON.parse(localStorage.getItem('menus')) || [];
        menuData.push({ name: menuName, description: menuDescription });
        localStorage.setItem('menus', JSON.stringify(menuData));

        document.getElementById('menuName').value = '';
        document.getElementById('menuDescription').value = '';

        displayMenus(); // 등록 후 목록을 바로 업데이트
    });

    displayMenus(); // 페이지 로드 시 저장된 메뉴 표시
});

document.addEventListener('DOMContentLoaded', function() {
    const reservationForm = document.getElementById('reservationForm');
    const reservationModifyForm = document.getElementById('reservationModifyForm');
    const reservationCancelForm = document.getElementById('reservationCancelForm');
    const reservationsDiv = document.getElementById('reservationList'); // 예약 목록을 표시할 요소의 ID

    // 예약 등록 처리
    reservationForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const customerName = document.getElementById('customerName').value.trim();
        const reservationDate = document.getElementById('reservationDate').value;
        const reservationTime = document.getElementById('reservationTime').value;
        const numberOfGuests = document.getElementById('numberOfGuests').value;

        if (!customerName || !reservationDate || !reservationTime || !numberOfGuests) {
            alert('모든 필드를 채워주세요!');
            return;
        }

        const newReservation = {
            id: Date.now(), // 간단한 ID 생성
            name: customerName,
            date: reservationDate,
            time: reservationTime,
            guests: numberOfGuests
        };

        const reservations = JSON.parse(localStorage.getItem('reservations')) || [];
        reservations.push(newReservation);
        localStorage.setItem('reservations', JSON.stringify(reservations));

        alert('예약이 등록되었습니다.');
        displayReservations();
    });

    // 예약 수정 처리
    reservationModifyForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const reservationId = parseInt(document.getElementById('modifyReservationId').value, 10);
        const newDate = document.getElementById('modifyReservationDate').value;
        const newTime = document.getElementById('modifyReservationTime').value;
        const newGuests = document.getElementById('modifyNumberOfGuests').value;

        let reservations = JSON.parse(localStorage.getItem('reservations')) || [];
        const index = reservations.findIndex(reservation => reservation.id === reservationId);
        if (index !== -1) {
            reservations[index] = { ...reservations[index], date: newDate, time: newTime, guests: newGuests };
            localStorage.setItem('reservations', JSON.stringify(reservations));
            alert('예약이 수정되었습니다.');
            displayReservations();
        } else {
            alert('예약 ID가 유효하지 않습니다.');
        }
    });

    // 예약 취소 처리
    reservationCancelForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const reservationId = parseInt(document.getElementById('cancelReservationId').value, 10);

        let reservations = JSON.parse(localStorage.getItem('reservations')) || [];
        reservations = reservations.filter(reservation => reservation.id !== reservationId);
        localStorage.setItem('reservations', JSON.stringify(reservations));

        alert('예약이 취소되었습니다.');
        displayReservations();
    });

    // 예약 목록 표시
    function displayReservations() {
        const reservations = JSON.parse(localStorage.getItem('reservations')) || [];
        reservationsDiv.innerHTML = ''; // 목록 초기화
        reservations.forEach(reservation => {
            const reservationElement = document.createElement('div');
            reservationElement.textContent = `ID: ${reservation.id}, 예약자: ${reservation.name}, 날짜: ${reservation.date}, 시간: ${reservation.time}, 인원: ${reservation.guests}`;
            reservationsDiv.appendChild(reservationElement);
        });
    }

    // 페이지 로드 시 저장된 예약 표시
    displayReservations();
});
