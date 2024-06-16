import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { fetchPokemonById } from '../../redux/pokemonSlice';
import './PokemonDetail.css'; // Importe seu arquivo CSS aqui

const PokemonDetail = () => {
  const { pokemonId } = useParams();
  const dispatch = useDispatch();
  const pokemon = useSelector((state) => state.pokemon.selectedPokemon);

  React.useEffect(() => {
    dispatch(fetchPokemonById(pokemonId));
  }, [dispatch, pokemonId]);

  if (!pokemon) {
    return <div>Carregando...</div>;
  }

  const Stat = ({ label, value }) => (
    <li className={`${label}`}>
      <h3>{label}</h3>
      <div className="progress">
        <span>{value}</span>
        <progress value={value} max="100"></progress>
      </div>
    </li>
  );

  return (
    <main className="content" aria-label="Detalhes do Pokémon">
      <section id="loadPokemon" aria-label="Pokemon">
        <div className="pokemon-individual container">
          <div className="pokemon-infos">
            <div className="pokemon-img slideInLeft">
              <img src={pokemon.front_picture} width="150" height="150" alt={pokemon.name} />
            </div>
            <div className="pokemon-conteudo">
              <span className="number slideInDown" aria-label="número do Pokemon">#{pokemon.id}</span>
              <h1 className="name slideInRight">{pokemon.name}</h1>
            </div>
          </div>
        </div>
        <div className='element-type-bpx'>
              {pokemon?.types?.map(type => (
                <div className='element-type' key={type.id}>{type.name}</div>
              ))}
        </div>
        <div className="pokemon-detail fadeIn">
          <h2>Estatísticas</h2>
          <ul className="stats">
            <Stat label='hp' value={pokemon.hp} />
            <Stat label='speed' value={pokemon.speed} />
            <Stat label='attack' value={pokemon.attack} />
            <Stat label='defense' value={pokemon.defense} />
            <Stat label='special-attack' value={pokemon.special_attack} />
            <Stat label='special-defense' value={pokemon.special_defense} />
          </ul>
        </div>
      </section>
    </main>
  );
};

export default PokemonDetail;
