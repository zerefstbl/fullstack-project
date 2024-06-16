import React from 'react';
import { useSelector } from 'react-redux';

const PokemonDetail = () => {
  const selectedPokemon = useSelector(state => state.selectedPokemon);

  return (
    <div>
      <h2>{selectedPokemon.name}</h2>
      {/* Adicione mais detalhes como imagem, tipo, etc */}
    </div>
  );
};

export default PokemonDetail;
