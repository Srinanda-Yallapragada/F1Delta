const api_url = 'https://api.openf1.org/v1';

export async function getDriverInfo(driver_number, session_key = 'latest') {
    const res = await fetch(`${api_url}/drivers?` + new URLSearchParams({
        driver_number: driver_number,
        session_key: session_key,
    }))
    

    return (await res.json())[0];

}
