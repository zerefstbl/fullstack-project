import { combineReducers } from '@reduxjs/toolkit';
import pokemonReducer from './pokemons/pokemonSlice';

const rootReducer = combineReducers({
  pokemon: pokemonReducer,
});

export default rootReducer;
