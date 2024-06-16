import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { fetchPokemonsFromApi, fetchPokemonByIdFromApi } from '../../services/pokemonApi';

export const fetchPokemons = createAsyncThunk(
  'pokemon/fetchPokemons',
  async () => {
    const response = await fetchPokemonsFromApi();
    return response.pokemons;
  }
);

export const fetchPokemonById = createAsyncThunk(
  'pokemon/fetchPokemonById',
  async (id) => {
    const response = await fetchPokemonByIdFromApi(id);
    return response;
  }
);

const pokemonSlice = createSlice({
  name: 'pokemon',
  initialState: {
    pokemons: [],
    selectedPokemon: null,
    status: 'idle',
    error: null,
  },
  reducers: {},
  extraReducers(builder) {
    builder
      .addCase(fetchPokemons.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchPokemons.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.pokemons = action.payload;
      })
      .addCase(fetchPokemons.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(fetchPokemonById.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchPokemonById.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.selectedPokemon = action.payload;
      })
      .addCase(fetchPokemonById.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  },
});

export default pokemonSlice.reducer;
