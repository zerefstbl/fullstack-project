import React from 'react';
import './Header.css'; // Certifique-se de importar o arquivo CSS do Header

function Header() {
  return (
    <>
      <header className="header-bg fadeIn" aria-label="Cabeçalho">
        <div className="header container">
          <a href="/" className="logo">
            <img src="https://raw.githubusercontent.com/gist/Galadirith/baaf38c7286b568973cc50a50ff57f4d/raw/34d60cae491bc505c212398b94f12705665c12fc/pokeball.svg" width="32" height="32" alt="Logo Pokeball" />
          </a>

          <nav aria-label="Primária">
            <ul className="header-menu">
              <li><a href="index.html">Início</a></li>
              <li><a href="details.html">Pokemons</a></li>
            </ul>
          </nav>
        </div>
      </header>
    </>
  );
}

export default Header;
