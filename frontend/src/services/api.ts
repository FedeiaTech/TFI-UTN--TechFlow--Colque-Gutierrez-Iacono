const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) throw new Error('Error al conectar con el backend');
    return await response.json();
  } catch (error) {
    console.error('Backend offline:', error);
    return { status: 'offline' };
  }
}