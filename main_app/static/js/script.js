// Script básico
document.addEventListener('DOMContentLoaded', () => {
    console.log('Página cargada correctamente.');
    getWeather();
});

// Weather functionality
async function getWeather() {
    console.log('Iniciando getWeather');
    
    const weatherContainers = document.querySelectorAll('.weather-widget');
    if (!weatherContainers.length) {
        console.error('No se encontraron contenedores del clima');
        return;
    }

    try {
        // Obtener la API key
        const apiKeyResponse = await fetch('/api/weather-key/');
        if (!apiKeyResponse.ok) {
            throw new Error('Error al obtener la API key');
        }
        const apiKeyData = await apiKeyResponse.json();
        const apiKey = apiKeyData.api_key;
        
        if (!apiKey) {
            throw new Error('API key no disponible');
        }
        
        console.log('API key obtenida correctamente');
        
        // Usar directamente las coordenadas de Santiago de Chile con el formato correcto
        const lat = "33.4489S";  // Formato: 33.4489S
        const lon = "70.6693W";  // Formato: 70.6693W
        
        // Obtener datos del clima usando coordenadas (idioma inglés)
        const weatherUrl = `https://www.meteosource.com/api/v1/free/point?lat=${lat}&lon=${lon}&sections=current&language=en&units=metric&key=${apiKey}`;
        console.log('Obteniendo datos del clima:', weatherUrl);
        
        const weatherResponse = await fetch(weatherUrl);
        if (!weatherResponse.ok) {
            const errorData = await weatherResponse.json();
            console.error('Error de la API:', errorData);
            throw new Error(`Error al obtener datos del clima: ${JSON.stringify(errorData)}`);
        }
        const weatherData = await weatherResponse.json();
        
        if (!weatherData || !weatherData.current) {
            throw new Error('Datos del clima no disponibles');
        }
        
        console.log('Datos del clima obtenidos:', weatherData);
        console.log('Datos actuales:', weatherData.current);
        console.log('Objeto current completo:', JSON.stringify(weatherData.current, null, 2));
        
        // Actualizar todos los widgets del clima
        weatherContainers.forEach(weatherContainer => {
            const tempElement = weatherContainer.querySelector('.weather-temp');
            const descElement = weatherContainer.querySelector('.weather-desc');
            const humidityElement = weatherContainer.querySelector('.weather-details span:first-child');
            const windElement = weatherContainer.querySelector('.weather-details span:last-child');
            const iconElement = weatherContainer.querySelector('.weather-icon i');
            
            const current = weatherData.current;
            
            // Traducir la descripción del clima al español
            let weatherDesc = current.summary || 'Despejado';
            const translations = {
                'Sunny': 'Soleado',
                'Partly sunny': 'Parcialmente soleado',
                'Mostly sunny': 'Mayormente soleado',
                'Cloudy': 'Nublado',
                'Mostly cloudy': 'Mayormente nublado',
                'Overcast': 'Cubierto',
                'Light rain': 'Lluvia ligera',
                'Rain': 'Lluvia',
                'Heavy rain': 'Lluvia intensa',
                'Thunderstorm': 'Tormenta',
                'Snow': 'Nieve',
                'Fog': 'Niebla',
                'Clear': 'Despejado',
                'Partly clear': 'Parcialmente despejado',
                'Mostly clear': 'Mayormente despejado'
            };
            
            // Aplicar traducción si existe
            if (translations[weatherDesc]) {
                weatherDesc = translations[weatherDesc];
            }
            
            if (tempElement) tempElement.textContent = `${Math.round(current.temperature)}°C`;
            if (descElement) descElement.textContent = weatherDesc;
            if (humidityElement) humidityElement.textContent = `Nubes: ${current.cloud_cover}%`;
            if (windElement) windElement.textContent = `Viento: ${Math.round(current.wind.speed * 3.6)} km/h`;
            
            // Actualizar el icono según el clima
            if (iconElement) {
                const weatherText = weatherDesc.toLowerCase();
                if (weatherText.includes('lluvia')) {
                    iconElement.className = 'fas fa-cloud-rain';
                } else if (weatherText.includes('nublado')) {
                    iconElement.className = 'fas fa-cloud';
                } else if (weatherText.includes('soleado') || weatherText.includes('despejado')) {
                    iconElement.className = 'fas fa-sun';
                } else if (weatherText.includes('nieve')) {
                    iconElement.className = 'fas fa-snowflake';
                } else if (weatherText.includes('tormenta')) {
                    iconElement.className = 'fas fa-bolt';
                } else if (weatherText.includes('niebla')) {
                    iconElement.className = 'fas fa-smog';
                } else {
                    iconElement.className = 'fas fa-cloud';
                }
            }
        });
        
        console.log('Widgets del clima actualizados con datos reales');
        
    } catch (error) {
        console.error('Error al obtener el clima:', error);
        
        // Mostrar mensaje de error en los widgets
        weatherContainers.forEach(weatherContainer => {
            const descElement = weatherContainer.querySelector('.weather-desc');
            if (descElement) descElement.textContent = `Error: ${error.message}`;
        });
    }
}