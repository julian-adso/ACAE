document.addEventListener('DOMContentLoaded', function() {
    // --- DATOS DE EJEMPLO ---
    const mockData = {
        employees: [
            {
                id: 1,
                name: "Ana García",
                schedule: { days: [1, 2, 3, 4, 5], start: "09:00", end: "17:00" }, // Lunes a Viernes
                attendance: [
                    { date: "2024-07-01", checkIn: "08:58" },
                    { date: "2024-07-02", checkIn: "09:05" }, // Tarde
                    { date: "2024-07-03", checkIn: "08:50" },
                    // 4 de julio ausente
                    { date: "2024-07-05", checkIn: "09:00" },
                    { date: "2024-07-08", checkIn: "09:15" }, // Tarde
                    { date: "2024-07-09", checkIn: "08:55" },
                    { date: "2024-07-10", checkIn: "08:59" },
                ]
            },
            {
                id: 2,
                name: "Carlos Rodriguez",
                schedule: { days: [1, 2, 3, 4, 5], start: "08:30", end: "16:30" }, // Lunes a Viernes
                attendance: [
                    { date: "2024-07-01", checkIn: "08:30" },
                    { date: "2024-07-02", checkIn: "08:25" },
                    { date: "2024-07-03", checkIn: "08:40" }, // Tarde
                    { date: "2024-07-04", checkIn: "08:28" },
                    { date: "2024-07-05", checkIn: "08:31" }, // Tarde
                    // 8-10 Julio vacaciones
                ]
            }
        ]
    };

    // --- ELEMENTOS DEL DOM ---
    const employeeSelect = document.getElementById('employee-select');
    const calendarEl = document.getElementById('calendar');
    const detailsContent = document.getElementById('details-content');

    // --- INICIALIZACIÓN DEL CALENDARIO ---
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek'
        },
        height: 'auto',
        events: [],
        eventClick: function(info) {
            updateDetailsPanel(info.event.extendedProps);
        }
    });
    calendar.render();

    // --- FUNCIONES ---

    function populateEmployeeSelector() {
        mockData.employees.forEach(emp => {
            const option = document.createElement('option');
            option.value = emp.id;
            option.textContent = emp.name;
            employeeSelect.appendChild(option);
        });
    }

    function getStatus(checkIn, scheduleStart) {
        if (!checkIn) return { text: 'Ausente', className: 'absent' };
        return checkIn > scheduleStart ? 
            { text: 'Tarde', className: 'late' } : 
            { text: 'A tiempo', className: 'on-time' };
    }

    function updateCalendarForEmployee(employeeId) {
        const employee = mockData.employees.find(e => e.id == employeeId);
        if (!employee) return;

        calendar.removeAllEvents();
        const events = [];
        const today = new Date();
        const currentMonth = today.getMonth();
        const currentYear = today.getFullYear();

        // Generar eventos para el mes actual
        const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(currentYear, currentMonth, day);
            const dateString = date.toISOString().split('T')[0];
            const dayOfWeek = date.getDay() === 0 ? 6 : date.getDay() -1; // Ajuste para que Lunes sea 0

            // Es un día laboral según el horario?
            if (employee.schedule.days.includes(date.getDay())) {
                const attendanceRecord = employee.attendance.find(a => a.date === dateString);
                const status = getStatus(attendanceRecord?.checkIn, employee.schedule.start);

                events.push({
                    title: attendanceRecord ? `Ingreso: ${attendanceRecord.checkIn}` : 'Ausente',
                    start: dateString,
                    className: status.className,
                    allDay: true,
                    extendedProps: {
                        date: dateString,
                        schedule: employee.schedule,
                        attendance: attendanceRecord,
                        status: status.text
                    }
                });
            }
        }

        calendar.addEventSource(events);
        resetDetailsPanel();
    }

    function updateDetailsPanel(props) {
        if (!props || !props.date) {
            resetDetailsPanel();
            return;
        }

        let content = `
            <div class="detail-item"><strong>Fecha:</strong> ${new Date(props.date).toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' })}</div>
            <div class="detail-item"><strong>Horario:</strong> ${props.schedule.start} - ${props.schedule.end}</div>
        `;

        if (props.attendance) {
            content += `
                <div class="detail-item"><strong>Ingreso:</strong> ${props.attendance.checkIn}</div>
                <div class="detail-item"><strong>Estado:</strong> <span class="status ${getStatus(props.attendance.checkIn, props.schedule.start).className}">${props.status}</span></div>
            `;
        } else {
             content += `<div class="detail-item"><strong>Estado:</strong> <span class="status absent">Ausente</span></div>`;
        }

        detailsContent.innerHTML = content;
    }

    function resetDetailsPanel() {
        detailsContent.innerHTML = '<p>Seleccione un día en el calendario para ver los detalles.</p>';
    }

    // --- EVENT LISTENERS ---
    employeeSelect.addEventListener('change', (e) => {
        updateCalendarForEmployee(e.target.value);
    });

    // --- EJECUCIÓN INICIAL ---
    populateEmployeeSelector();
    if (mockData.employees.length > 0) {
        employeeSelect.value = mockData.employees[0].id;
        updateCalendarForEmployee(mockData.employees[0].id);
    }
});

