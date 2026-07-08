const API = 'http://127.0.0.1:5000';
let montoInsertado = 0.00;
let modoUSD = false;

const TIPO_CAMBIO = 3.70;
const DENOMINACIONES = [200, 100, 50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10];

const MONEDAS_SOLES = [0.10, 0.20, 0.50, 1.00, 2.00, 5.00];
const BILLETES_SOLES = [10, 20, 50, 100, 200];
const MONEDAS_USD = [0.25, 0.50, 1.00];
const BILLETES_USD = [1, 5, 10, 20, 50, 100];

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
    if (p.stock > 0) card.onclick = () => comprar(p.id, p.nombre, p.precio);
    grid.appendChild(card);
  });
}

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

function toggleMoneda() {
  modoUSD = !modoUSD;
  const toggle = document.getElementById('toggle-moneda');
  toggle.textContent = modoUSD ? '🇵🇪 S/ PEN' : '🇺🇸 $ USD';
  toggle.classList.toggle('activo', modoUSD);
  renderizarBotonesDinero();
}

function renderizarBotonesDinero() {
  const monedas = modoUSD ? MONEDAS_USD : MONEDAS_SOLES;
  const billetes = modoUSD ? BILLETES_USD : BILLETES_SOLES;
  const simbolo = modoUSD ? '$' : 'S/';

  const contenedorMonedas = document.getElementById('botones-monedas');
  const contenedorBilletes = document.getElementById('botones-billetes');

  contenedorMonedas.innerHTML = monedas.map(m =>
    `<button class="btn-dinero" onclick="insertarDinero(${m}, ${modoUSD})">${simbolo} ${m.toFixed(2)}</button>`
  ).join('');

  contenedorBilletes.innerHTML = billetes.map(b =>
    `<button class="btn-dinero billete" onclick="insertarDinero(${b}, ${modoUSD})">${simbolo} ${b}</button>`
  ).join('');
}

function calcularDesglose(vuelto) {
  let restante = Math.round(vuelto * 100);
  const desglose = [];
  for (const den of DENOMINACIONES) {
    const denCentavos = Math.round(den * 100);
    const cantidad = Math.floor(restante / denCentavos);
    if (cantidad > 0) {
      const tipo = den >= 10 ? 'billete' : 'moneda';
      const etiqueta = den >= 1 ? `S/ ${den.toFixed(0)}` : `S/ ${den.toFixed(2)}`;
      desglose.push(`${cantidad} ${tipo}${cantidad > 1 ? 's' : ''} de ${etiqueta}`);
      restante -= cantidad * denCentavos;
    }
  }
  return desglose;
}

async function insertarDinero(monto, esDolar = false) {
  const montoEnSoles = esDolar ? parseFloat((monto * TIPO_CAMBIO).toFixed(2)) : monto;
  const res = await fetch(`${API}/insertar-dinero`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ monto: montoEnSoles })
  });
  const data = await res.json();
  montoInsertado = data.dinero_insertado;
  const nota = esDolar ? ` ($ ${monto} × ${TIPO_CAMBIO})` : '';
  actualizarDisplay('LISTO', montoInsertado, `Seleccione un producto${nota}`);
}

async function comprar(id, nombre, precio) {
  if (montoInsertado === 0) {
    actualizarDisplay('⚠ ERROR', montoInsertado, 'Inserte dinero primero');
    return;
  }
  const res = await fetch(`${API}/comprar/${id}`, { method: 'POST' });
  const data = await res.json();
  if (res.ok) {
    montoInsertado = 0;
    const desglose = calcularDesglose(data.vuelto);
    actualizarDisplay('✓ COMPRA OK', 0.00, data.mensaje);
    document.getElementById('historial').innerHTML =
      `✓ ${nombre}<br>Vuelto: S/ ${data.vuelto.toFixed(2)}<br>${desglose.join('<br>')}`;
    cargarProductos();
  } else {
    actualizarDisplay('⚠ ERROR', montoInsertado, data.error);
  }
}

async function cancelar() {
  const res = await fetch(`${API}/cancelar`);
  const data = await res.json();
  montoInsertado = 0;
  const desglose = calcularDesglose(data.devuelto);
  actualizarDisplay('CANCELADO', 0.00, `Devuelto: S/ ${data.devuelto.toFixed(2)}`);
  document.getElementById('historial').innerHTML =
    `↩ Cancelado<br>Devuelto: S/ ${data.devuelto.toFixed(2)}<br>${desglose.join('<br>')}`;
}

function actualizarDisplay(estado, monto, mensaje) {
  document.getElementById('display-estado').textContent = estado;
  document.getElementById('display-monto').textContent = monto.toFixed(2);
  document.getElementById('display-mensaje').textContent = mensaje;
}

cargarProductos();
renderizarBotonesDinero();