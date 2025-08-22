document.addEventListener('DOMContentLoaded', () => {

    // --- DATOS DE EJEMPLO ---
    // En una aplicación real, estos datos vendrían de una base de datos.
    const attendanceData = [
        { date: '2023-11-01', entryTime: '08:55' },
        { date: '2023-11-02', entryTime: '09:07' },
        { date: '2023-11-03', entryTime: '08:59' },
        { date: '2023-11-04', entryTime: null }, // Ausencia
        { date: '2023-11-05', entryTime: '09:01' },
        { date: '2023-11-06', entryTime: '09:15' },
        { date: '2023-11-07', entryTime: '08:50' },
        { date: '2023-11-08', entryTime: null }, // Ausencia
        { date: '2023-11-09', entryTime: '09:00' },
        { date: '2023-11-10', entryTime: '09:30' },
        { date: '2023-11-11', entryTime: '08:58' },
    ];

    const HORA_ENTRADA_OFICIAL = '09:00';

    // --- ELEMENTOS DEL DOM ---
    const asistenciasCountEl = document.getElementById('asistencias-count');
    const fallasCountEl = document.getElementById('fallas-count');
    const historyTableBodyEl = document.querySelector('#history-table tbody');

    // --- LÓGICA ---
    let asistencias = 0;
    let fallas = 0;

    // Procesar datos y llenar la tabla
    attendanceData.forEach(record => {
        const row = document.createElement('tr');

        const fechaCell = document.createElement('td');
        fechaCell.textContent = record.date;
        row.appendChild(fechaCell);

        const horaCell = document.createElement('td');
        const estadoCell = document.createElement('td');
        const statusSpan = document.createElement('span');
        statusSpan.classList.add('status');
        
        if (record.entryTime) {
            asistencias++;
            horaCell.textContent = record.entryTime;
            
            if (record.entryTime > HORA_ENTRADA_OFICIAL) {
                statusSpan.textContent = 'Tarde';
                statusSpan.classList.add('status-tarde');
            } else {
                statusSpan.textContent = 'Puntual';
                statusSpan.classList.add('status-puntual');
            }
        } else {
            fallas++;
            horaCell.textContent = '---';
            statusSpan.textContent = 'Ausente';
            statusSpan.classList.add('status-ausente');
        }
        
        estadoCell.appendChild(statusSpan);
        row.appendChild(horaCell);
        row.appendChild(estadoCell);

        historyTableBodyEl.appendChild(row);
    });

    // Actualizar los contadores en las tarjetas
    asistenciasCountEl.textContent = asistencias;
    fallasCountEl.textContent = fallas;

});

