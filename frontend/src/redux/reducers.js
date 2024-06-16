import { combineReducers } from '@reduxjs/toolkit';
import pokemonReducer from './pokemonSlice';

const rootReducer = combineReducers({
  pokemon: pokemonReducer,
});

export default rootReducer;
