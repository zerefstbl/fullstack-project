import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api/v1';

export const fetchPokemonsFromApi = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/pokemons?limit=10`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const fetchPokemonByIdFromApi = async (id) => {
  try {
    const response = await axios.get(`${BASE_URL}/pokemons/${id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
