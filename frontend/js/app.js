const API = 'http://127.0.0.1:5000';
let montoInsertado = 0.00;

// ── CARGAR PRODUCTOS ──
async function cargarProductos() {
  const res = await fetch(`${API}/productos`);
  const data = await res.json();
  const grid = document.getElementById('grid-productos');
  grid.innerHTML = '';

  const codigos = generarCodigos(data.productos.length);

  data.productos.forEach((p, i) => {
    const card = document.createElement('div');
    card.className = `producto-card ${p.stock === 0 ? 'sin-stock' : ''}`;
    card.innerHTML = `
      <div class="producto-codigo">${codigos[i]}</div>
      <div class="producto-nombre">${p.nombre}</div>
      <div class="producto-marca">${p.marca}</div>
      <div class="producto-precio">S/ ${p.precio.toFixed(2)}</div>
      <div class="producto-stock">Stock: ${p.stock}</div>
    `;
    if (p.stock > 0) {
      card.onclick = () => comprar(p.id, p.nombre, p.precio);
    }
    grid.appendChild(card);
  });
}

// ── GENERAR CÓDIGOS A1, A2... ──
function generarCodigos(total) {
  const letras = ['A', 'B', 'C', 'D', 'E'];
  const codigos = [];
  let letra = 0, numero = 1;
  for (let i = 0; i < total; i++) {
    codigos.push(`${letras[letra]}${numero}`);
    numero++;
    if (numero > 4) { numero = 1; letra++; }
  }
  return codigos;
}

// ── INSERTAR DINERO ──
async function insertarDinero(monto) {
  const res = await fetch(`${API}/insertar-dinero`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ monto })
  });
  const data = await res.json();
  montoInsertado = data.dinero_insertado;
  actualizarDisplay('LISTO', montoInsertado, 'Seleccione un producto');
}

// ── COMPRAR ──
async function comprar(id, nombre, precio) {
  if (montoInsertado === 0) {
    actualizarDisplay('⚠ ERROR', montoInsertado, 'Inserte dinero primero');
    return;
  }
  const res = await fetch(`${API}/comprar/${id}`, { method: 'POST' });
  const data = await res.json();

  if (res.ok) {
    montoInsertado = 0;
    actualizarDisplay('✓ COMPRA OK', 0.00, data.mensaje);
    document.getElementById('historial').innerHTML =
      `✓ ${nombre}<br>Vuelto: S/ ${data.vuelto.toFixed(2)}`;
    cargarProductos();
  } else {
    actualizarDisplay('⚠ ERROR', montoInsertado, data.error);
  }
}

// ── CANCELAR ──
async function cancelar() {
  const res = await fetch(`${API}/cancelar`);
  const data = await res.json();
  montoInsertado = 0;
  actualizarDisplay('CANCELADO', 0.00, `Devuelto: S/ ${data.devuelto.toFixed(2)}`);
}

// ── ACTUALIZAR DISPLAY ──
function actualizarDisplay(estado, monto, mensaje) {
  document.getElementById('display-estado').textContent = estado;
  document.getElementById('display-monto').textContent = monto.toFixed(2);
  document.getElementById('display-mensaje').textContent = mensaje;
}

// ── INICIO ──
cargarProductos();