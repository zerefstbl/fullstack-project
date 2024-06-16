import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PokemonList from './Pokemons/PokemonList';
import PokemonDetail from './Pokemons/PokemonDetail';
import Header from './Header/Header';

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<PokemonList />} />
        <Route path="/pokemon/:pokemonId" element={<PokemonDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
