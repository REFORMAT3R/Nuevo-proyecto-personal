const content = document.querySelector(".players-grid");

jugadores.forEach(jugador => {

  // contenedor principal
  const card = document.createElement("div");
  card.classList.add("player-card");

  // icono
  const img = document.createElement("img");
  img.src = STATIC_PJ_URL + jugador.icono;
  img.alt = jugador.personaje;

  // top + nombre
  const top = document.createElement("h3");
  top.textContent = `#${jugador.top} ${jugador.nombre}`;

  // personaje
  const personaje = document.createElement("p");
  personaje.textContent = `Personaje: ${jugador.personaje}`;

  // nacionalidad
  const nacionalidad = document.createElement("p");
  nacionalidad.textContent = `País: ${jugador.nacionalidad}`;

  // armar card
  card.appendChild(img);
  card.appendChild(top);
  card.appendChild(personaje);
  card.appendChild(nacionalidad);

  // meter al content
  content.appendChild(card);
});