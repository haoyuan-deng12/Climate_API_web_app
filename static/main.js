// static/main.js

/**
 * Fetch climate data from the /climate_data API.
 */
async function fetchExternalData() {
    const display = document.getElementById('externalDataDisplay');
    display.style.display = 'block';
    display.innerHTML = 'Fetching climate data...';

    // fetch user query from input fields
    const latitude = document.getElementById('latitude').value.trim();
    const longitude = document.getElementById('longitude').value.trim();

    // basic input check
    if (!latitude || !longitude) {
        display.innerHTML = 'All fields are required.';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/climate_data?latitude=${latitude}&longitude=${longitude}`);
        if (!response.ok) throw new Error('Request failed');
        const dataResponse = await response.json();
        const data = dataResponse.data;

        // fetch useful info from response
        const elevation = data.elevation;
        const timezone = data.timezone;
        const daily = data.daily;
        const dailyUnits = data.daily_units;

        // use infos and creat a basic table element to show them in order
        let output = `<strong>Climate Forecast for (${data.latitude}, ${data.longitude})</strong><br>`;
        output += `<strong>Elevation:</strong> ${elevation} m<br>`;
        output += `<strong>Timezone:</strong> ${timezone}<br><br>`;

        output += `<strong>Daily Forecast (next 16 days):</strong>
                   <table class="table table-bordered table-striped">
                      <thead>
                        <tr>
                          <th>Date</th>
                          <th>Max Temp (${dailyUnits.temperature_2m_max})</th>
                          <th>Min Temp (${dailyUnits.temperature_2m_min})</th>
                        </tr>
                      </thead>
                      <tbody>`;

        for (let i = 0; i < daily.time.length; i++) {
            output += `
                <tr>
                    <td>${daily.time[i]}</td>
                    <td>${daily.temperature_2m_max[i]} ${dailyUnits.temperature_2m_max}</td>
                    <td>${daily.temperature_2m_min[i]} ${dailyUnits.temperature_2m_min}</td>
                </tr>`;
        }

        output += `</tbody></table>`;

        display.innerHTML = output;

    } catch (err) {
        display.innerHTML = 'Error fetching climate data.';
        console.error(err);
    }
}



/**
 * Fetch fire data from the /fire_data API.
 */
async function fetchFireData() {
    const display = document.getElementById('fireDataDisplay');
    display.style.display = 'block';
    display.innerHTML = 'Fetching fire data...';

    // set query parameter
    const country = document.getElementById('country').value.trim() || 'USA';
    const source = document.getElementById('source').value || 'VIIRS_SNPP_NRT';
    const dayRange = document.getElementById('dayRange').value || '10';
    const displayNumber = document.getElementById('displayNumber').value.trim();

    try {
        const response = await fetch(`http://127.0.0.1:5000/fire_data?country=${country}&source=${source}&day_range=${dayRange}&display_number=${displayNumber}`);
        if (!response.ok) throw new Error('Request failed');
        const dataResponse = await response.json();
        const fireData = dataResponse.data;

        let output = `<strong>Message:</strong> ${dataResponse.message || 'No message'}<br>`;
        output += `<strong>Fire Data:</strong>
                   <table class="table table-bordered table-striped">
                      <thead>
                        <tr>
                          <th>Latitude</th>
                          <th>Longitude</th>
                          <th>Brightness</th>
                          <th>Acquisition Date</th>
                          <th>FRP</th>
                        </tr>
                      </thead>
                      <tbody>`;

        fireData.forEach(fire => {
            output += `
                <tr>
                    <td>${fire.latitude}</td>
                    <td>${fire.longitude}</td>
                    <td>${fire.bright_ti4}</td>
                    <td>${fire.acq_date}</td>
                    <td>${fire.frp}</td>
                </tr>`;
        });

        output += `</tbody></table>`;
        display.innerHTML = output;

    } catch (err) {
        display.innerHTML = 'Error fetching fire data.';
        console.error(err);
    }
}

async function fetchSlickData() {
    const display = document.getElementById('slickDataDisplay');
    display.style.display = 'block';
    display.innerHTML = 'Fetching oil slick data...';

    // Get user input values
    const bbox = document.getElementById('bbox').value.trim()
    const start_date = document.getElementById('start_date').value
    const end_date = document.getElementById('end_date').value
    const min_confidence = document.getElementById('min_confidence').value.trim()
    const limit = document.getElementById("limit").value.trim()

    if (!bbox || !start_date || !end_date || !min_confidence||!limit) {

        let missingFields = [];

        if (!bbox) missingFields.push("Bounding Box");
        if (!start_date) missingFields.push("Start Date");
        if (!end_date) missingFields.push("End Date");
        if (!min_confidence) missingFields.push("Min Confidence");

        if (missingFields.length > 0) {
            display.innerHTML = `Please fill in the following fields: ${missingFields.join(", ")}.`;
            return;
        }

    }

    try {
        const params = new URLSearchParams({
            bbox: bbox,
            start_date: start_date,
            end_date: end_date,
            min_confidence: min_confidence,
            limit:limit
        }).toString();

        // Call the backend route (assuming backend runs on http://127.0.0.1:5000)
        const response = await fetch(`http://127.0.0.1:5000/spill_data_oil?${params}`);

        if (!response.ok) throw new Error('Request failed');
        const dataResponse = await response.json();
        const slickData = dataResponse.data
        console.log(slickData)

        let output = `<strong>Message:</strong> ${dataResponse.message || 'No message'}<br>`;
        output += `<strong>Results:</strong>
                           <table class="table table-bordered table-striped">
                              <thead>
                                <tr>
                                  <th>ID</th>
                                  <th>Area (sq.m)</th>
                                  <th>Machine Confidence</th>
                                  <th>Detection Timestamp</th>
                                  <th>Classification</th>
                                </tr>
                              </thead>
                              <tbody>`;
        slickData.forEach(slick => {
            output += `
                     <tr>
                         <td>${slick.id}</td>
                         <td>${slick.area.toFixed(0)}</td>
                         <td>${slick.machine_confidence.toFixed(3)}</td>
                         <td>${slick.slick_timestamp}</td>
                         <td>${slick.classification}</td>  <!-- Use the new property -->       
                     </tr>`;
        });
        output += `</tbody></table>`;

        display.innerHTML = output;
    } catch (err) {
        display.innerHTML = 'Error fetching oil slick data.';
        console.error(err);
    }
}









