import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchPokemons } from '../../redux/pokemonSlice';
import './PokemonList.css'; // Certifique-se de importar o arquivo CSS

const PokemonList = () => {
  const dispatch = useDispatch();
  const pokemons = useSelector((state) => state.pokemon.pokemons);
  const status = useSelector((state) => state.pokemon.status);

  React.useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchPokemons());
    }
  }, [dispatch, status]);

  return (
    <div className="pokemon-grid">
      {pokemons.map((pokemon) => (
        <div key={pokemon.id} className="pokemon-card">
          <img src={pokemon.front_picture} alt={pokemon.name} />
          <h2>{pokemon.name}</h2>
          {/* Adicione mais informações do Pokémon aqui se necessário */}
        </div>
      ))}
    </div>
  );
};

export default PokemonList;
