document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('searchInput').value;
    fetch('/weather', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({ location: query })
    })
    .then(response => response.json())
    .then(data => {
      updateWeatherCards(data);
    })
    .catch(error => {
      console.error('Error fetching weather data:', error);
    });
  });
  
  function updateWeatherCards(data) {
    const weatherCards = document.getElementById('weatherCards');
    weatherCards.innerHTML = ''; // Clear existing cards
    
    if (data.weather && data.weather.properties && data.weather.properties.periods) {
      // Create a header with city, state, and ZIP code
      const header = document.createElement('div');
      header.className = 'header-info';
      header.innerHTML = `
        <h2>${data.city}, ${data.state} ${data.zip_code}</h2>
      `;
      weatherCards.appendChild(header);
  
      // Add weather cards
      data.weather.properties.periods.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div class="card-body">
            <div class="weather-icon">
              <img src="${mapIcon(item.shortForecast)}" alt="${item.shortForecast}">
            </div>
            <div class="weather-details">
              <h5 class="card-title">${item.name}</h5>
              <p class="card-text">
                ${item.temperature}°F - ${item.shortForecast}
                <br>
                <small>Time: ${item.startTime}</small>
              </p>
            </div>
          </div>
        `;
        weatherCards.appendChild(card);
      });
    } else {
      weatherCards.innerHTML = '<p>No weather data available.</p>';
    }
  }
  
  function mapIcon(forecast) {
    // Map weather descriptions to image URLs
    const iconMap = {
      'sunny': 'static/images/sunny.jpg',
      'mostly sunny': 'static/images/sunny.jpg',
      'partly cloudy': 'static/images/cloudy.jpg',
      'cloudy': 'static/images/cloudy.jpg',
      'mostly cloudy': 'static/images/cloudy.jpg',
      'rainy': 'static/images/rainy.jpg',
      'showers': 'static/images/rainy.jpg',
      'rain': 'static/images/rainy.jpg'
    };
    
    // Check each condition and return corresponding image URL
    for (const [condition, imageUrl] of Object.entries(iconMap)) {
      if (forecast.toLowerCase().includes(condition)) {
        return imageUrl;
      }
    }
    
    // Default image if no match found
    return 'static/images/cloudy.jpg'; // Default to cloudy if no match
  }
  