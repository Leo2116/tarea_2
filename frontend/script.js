// URL base del backend (ajusta si es necesario)
const API_URL = 'http://localhost:5000/alumnos';

const form = document.getElementById('alumno-form');
const alumnosTable = document.getElementById('alumnos-table').getElementsByTagName('tbody')[0];
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const alumnoIdInput = document.getElementById('alumno-id');
const nombreInput = document.getElementById('nombre');
const apellidoInput = document.getElementById('apellido');
const edadInput = document.getElementById('edad');

// Cargar alumnos al iniciar
window.onload = listarAlumnos;

function listarAlumnos() {
    fetch(API_URL)
        .then(res => res.json())
        .then(data => {
            alumnosTable.innerHTML = '';
            data.forEach(alumno => {
                const row = alumnosTable.insertRow();
                row.insertCell().textContent = alumno.id;
                row.insertCell().textContent = alumno.nombre;
                row.insertCell().textContent = alumno.apellido;
                row.insertCell().textContent = alumno.edad;
                const acciones = row.insertCell();
                // Botón Editar
                const editBtn = document.createElement('button');
                editBtn.textContent = 'Editar';
                editBtn.className = 'edit';
                editBtn.onclick = () => editarAlumno(alumno);
                acciones.appendChild(editBtn);
                // Botón Eliminar
                const deleteBtn = document.createElement('button');
                deleteBtn.textContent = 'Eliminar';
                deleteBtn.className = 'delete';
                deleteBtn.onclick = () => eliminarAlumno(alumno.id);
                acciones.appendChild(deleteBtn);
            });
        });
}

form.onsubmit = function(e) {
    e.preventDefault();
    const id = alumnoIdInput.value;
    const nombre = nombreInput.value.trim();
    const apellido = apellidoInput.value.trim();
    const edad = parseInt(edadInput.value);
    if (!nombre || !apellido || isNaN(edad)) return;
    const alumno = { nombre, apellido, edad };
    if (id) {
        // Modificar
        fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(alumno)
        })
        .then(res => res.json())
        .then(() => {
            resetForm();
            listarAlumnos();
        });
    } else {
        // Agregar
        fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(alumno)
        })
        .then(res => res.json())
        .then(() => {
            resetForm();
            listarAlumnos();
        });
    }
};

function editarAlumno(alumno) {
    alumnoIdInput.value = alumno.id;
    nombreInput.value = alumno.nombre;
    apellidoInput.value = alumno.apellido;
    edadInput.value = alumno.edad;
    submitBtn.textContent = 'Modificar';
    cancelBtn.style.display = 'inline-block';
}

cancelBtn.onclick = resetForm;

function resetForm() {
    alumnoIdInput.value = '';
    nombreInput.value = '';
    apellidoInput.value = '';
    edadInput.value = '';
    submitBtn.textContent = 'Agregar';
    cancelBtn.style.display = 'none';
}

function eliminarAlumno(id) {
    if (confirm('¿Seguro que deseas eliminar este alumno?')) {
        fetch(`${API_URL}/${id}`, { method: 'DELETE' })
            .then(res => res.json())
            .then(() => listarAlumnos());
    }
}
