import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api/v1';

export const fetchPokemonsFromApi = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/pokemons`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
