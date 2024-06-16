import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchPokemons } from '../../redux/pokemonSlice';
import { useNavigate } from 'react-router-dom'; // Importa o hook useHistory
import './PokemonList.css';

const PokemonList = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate(); // Inicializa o hook useHistory
  const pokemons = useSelector((state) => state.pokemon.pokemons);
  const status = useSelector((state) => state.pokemon.status);

  React.useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchPokemons());
    }
  }, [dispatch, status]);

  const handlePokemonClick = (pokemon) => {
    // Navega para a rota /pokemon/id do Pokémon selecionado
    navigate(`/pokemon/${pokemon.id}`);
  };

  return (
    <div className="pokemon-grid">
      {pokemons?.map((pokemon) => (
        <div key={pokemon.id} className="pokemon-card" onClick={() => handlePokemonClick(pokemon)}>
          <img src={pokemon.front_picture} alt={pokemon.name} />
          <h2>{pokemon.name}</h2>
          <div className="types">
            {pokemon?.types?.map(type => (
              <span key={type.id} className="type">{type.name}</span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default PokemonList;
