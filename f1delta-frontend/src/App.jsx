import { useEffect, useState } from 'react';

function App() {
  const [driverInfo, setDriverInfo] = useState(null);
  const [error, setError] = useState(null);

  // Call the backend to get driver info
  useEffect(() => {
    const fetchDriverInfo = async () => {
      try {
        // Adjust the URL for your backend; this will call the driverInfo route
        const driver_number = 1; // Example driver number
        const session_key = '9158'; // Example session key
        const response = await fetch(`/driverInfo?driver_number=${driver_number}&session_key=${session_key}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch driver info');
        }

        const data = await response.json();
        setDriverInfo(data);  // Set the response data
      } catch (err) {
        setError(err.message);  // Handle any error
      }
    };

    fetchDriverInfo();
  }, []);

  return (
    <div>
      <h1>Driver Info</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {driverInfo ? (
        <pre>{JSON.stringify(driverInfo, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;
